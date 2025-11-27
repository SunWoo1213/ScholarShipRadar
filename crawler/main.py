"""
장학금 메인 크롤러 (GPT-4o Vision 전용)
통이미지 공고를 분석하여 Supabase에 저장합니다.
"""

import os
import json
import base64
import time
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from urllib.parse import urljoin
from dotenv import load_dotenv

import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from supabase import create_client, Client

# 환경 변수 로드
load_dotenv()

# API 클라이언트 초기화
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

# 설정
TARGET_URL = os.getenv("TARGET_URL", "https://web.kangnam.ac.kr/board/scholarship")
BASE_DOMAIN = os.getenv("BASE_DOMAIN", "https://web.kangnam.ac.kr")
MAX_ITEMS = int(os.getenv("MAX_ITEMS", "50"))
DELAY_SECONDS = int(os.getenv("DELAY_SECONDS", "3"))


class ScholarshipCrawler:
    """장학금 크롤러"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        })
        
    def crawl_list(self, url: str) -> List[Dict]:
        """
        게시판 목록에서 제목, 링크 추출
        """
        try:
            print(f"📡 게시판 크롤링: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'html.parser')
            items = []
            
            # 링크 찾기 (사이트 구조에 맞게 수정)
            links = soup.find_all('a', class_='detailLink')
            
            if not links:
                # 대체 방법: href 속성이 있는 모든 a 태그
                links = soup.select('div.board-list a, table.board-list a, ul.board-list a')
            
            print(f"✅ {len(links)}개 공고 발견")
            
            for link in links[:MAX_ITEMS]:
                title = link.get_text(strip=True)
                href = link.get('href', '')
                
                if not href or href == '#':
                    # data-params에서 URL 추출 시도
                    data_params = link.get('data-params', '')
                    if data_params:
                        detail_url = self._extract_url_from_params(data_params)
                    else:
                        continue
                else:
                    detail_url = self._build_full_url(href)
                
                if detail_url and title:
                    items.append({
                        'title': title,
                        'link': detail_url
                    })
            
            return items
            
        except Exception as e:
            print(f"❌ 목록 크롤링 실패: {e}")
            return []
    
    def crawl_detail(self, url: str) -> Tuple[Optional[str], Optional[str], bool]:
        """
        상세 페이지에서 이미지 URL 또는 텍스트 추출
        
        Returns:
            (image_url, text_content, is_image)
        """
        try:
            print(f"  📄 상세 페이지: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 본문 영역 찾기
            content_div = soup.find('div', class_='tbl_view')
            
            if not content_div:
                # 대체 클래스명들 시도
                for class_name in ['view-content', 'board-content', 'content', 'article-body']:
                    content_div = soup.find('div', class_=class_name)
                    if content_div:
                        break
            
            if not content_div:
                print(f"  ⚠️  본문 영역을 찾을 수 없습니다")
                return None, None, False
            
            # 1. 이미지 찾기 (우선)
            img_tag = content_div.find('img')
            
            if img_tag:
                img_src = img_tag.get('src', '')
                if img_src:
                    image_url = self._build_full_url(img_src)
                    print(f"  🖼️  이미지 발견")
                    return image_url, None, True
            
            # 2. 텍스트 추출 (폴백)
            text_content = content_div.get_text(strip=True, separator='\n')
            if text_content:
                print(f"  📝 텍스트 추출 ({len(text_content)}자)")
                return None, text_content, False
            
            return None, None, False
            
        except Exception as e:
            print(f"  ❌ 상세 페이지 크롤링 실패: {e}")
            return None, None, False
    
    def download_image_as_base64(self, image_url: str) -> Optional[str]:
        """
        이미지를 Base64로 인코딩
        """
        try:
            print(f"  📥 이미지 다운로드 중...")
            response = self.session.get(image_url, timeout=15)
            response.raise_for_status()
            
            image_data = base64.b64encode(response.content).decode('utf-8')
            content_type = response.headers.get('Content-Type', 'image/jpeg')
            
            print(f"  ✅ 다운로드 완료 ({len(image_data)//1024}KB)")
            
            return f"data:{content_type};base64,{image_data}"
            
        except Exception as e:
            print(f"  ❌ 이미지 다운로드 실패: {e}")
            return None
    
    def _build_full_url(self, path: str) -> str:
        """상대 경로를 절대 경로로 변환"""
        if path.startswith('http'):
            return path
        return urljoin(BASE_DOMAIN, path)
    
    def _extract_url_from_params(self, data_params: str) -> Optional[str]:
        """data-params에서 URL 추출"""
        try:
            params = json.loads(data_params.replace('&quot;', '"'))
            if 'encMenuBoardSeq' in params:
                return f"{BASE_DOMAIN}/board/view?seq={params['encMenuBoardSeq']}"
            return None
        except:
            return None


class GPTAnalyzer:
    """GPT-4o Vision/Text 분석기"""
    
    @staticmethod
    def analyze_image(title: str, image_base64: str) -> Optional[Dict]:
        """
        GPT-4o Vision으로 이미지 분석
        """
        try:
            print(f"  🤖 GPT-4o Vision 분석 중...")
            
            response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": """당신은 장학금 공고 이미지를 분석하는 AI입니다.
이미지에서 다음 정보를 추출하여 JSON으로 반환하세요:

1. min_gpa: 최소 학점 요구사항 (예: 3.0, 없으면 0.0)
2. max_income: 소득분위 상한선 (0~10, 제한 없으면 99)
3. residence: 거주지 제한 (예: "서울", "경기도", 없으면 "전국")
4. due_date: 마감일 (YYYY-MM-DD, 없으면 null)

응답 형식:
{
    "min_gpa": 3.0,
    "max_income": 8,
    "residence": "전국",
    "due_date": "2026-01-31"
}

주의: 반드시 유효한 JSON만 반환하세요."""
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"제목: {title}\n\n위 장학금 공고 이미지를 분석해주세요."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": image_base64,
                                    "detail": "high"
                                }
                            }
                        ]
                    }
                ],
                response_format={"type": "json_object"},
                temperature=0.1,
                max_tokens=500
            )
            
            result = json.loads(response.choices[0].message.content)
            
            # 데이터 검증
            analyzed = {
                'min_gpa': float(result.get('min_gpa', 0.0)),
                'max_income': int(result.get('max_income', 99)),
                'residence': result.get('residence', '전국'),
                'due_date': result.get('due_date')
            }
            
            # 날짜 유효성 검사
            if analyzed['due_date']:
                try:
                    datetime.strptime(analyzed['due_date'], '%Y-%m-%d')
                except ValueError:
                    analyzed['due_date'] = None
            
            print(f"  ✅ 분석 완료: {analyzed}")
            return analyzed
            
        except Exception as e:
            print(f"  ❌ Vision 분석 실패: {e}")
            return None
    
    @staticmethod
    def analyze_text(title: str, content: str) -> Optional[Dict]:
        """
        GPT-4o로 텍스트 분석 (폴백)
        """
        try:
            print(f"  🤖 GPT-4o 텍스트 분석 중...")
            
            response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": """당신은 장학금 공고문을 분석하는 AI입니다.
텍스트에서 다음 정보를 추출하여 JSON으로 반환하세요:

1. min_gpa: 최소 학점 (없으면 0.0)
2. max_income: 소득분위 상한선 (0~10, 없으면 99)
3. residence: 거주지 (없으면 "전국")
4. due_date: 마감일 (YYYY-MM-DD, 없으면 null)

응답 형식:
{
    "min_gpa": 2.5,
    "max_income": 5,
    "residence": "서울",
    "due_date": "2026-02-15"
}"""
                    },
                    {
                        "role": "user",
                        "content": f"제목: {title}\n\n내용:\n{content[:3000]}\n\n위 공고를 분석해주세요."
                    }
                ],
                response_format={"type": "json_object"},
                temperature=0.1,
                max_tokens=500
            )
            
            result = json.loads(response.choices[0].message.content)
            
            analyzed = {
                'min_gpa': float(result.get('min_gpa', 0.0)),
                'max_income': int(result.get('max_income', 99)),
                'residence': result.get('residence', '전국'),
                'due_date': result.get('due_date')
            }
            
            if analyzed['due_date']:
                try:
                    datetime.strptime(analyzed['due_date'], '%Y-%m-%d')
                except ValueError:
                    analyzed['due_date'] = None
            
            print(f"  ✅ 분석 완료: {analyzed}")
            return analyzed
            
        except Exception as e:
            print(f"  ❌ 텍스트 분석 실패: {e}")
            return None


class DatabaseManager:
    """Supabase 데이터베이스 관리"""
    
    @staticmethod
    def upsert_scholarship(data: Dict) -> bool:
        """
        장학금 정보를 Upsert (링크 기준으로 중복 시 업데이트)
        """
        try:
            print(f"  💾 DB 저장 중...")
            
            # Upsert: link가 같으면 업데이트
            result = supabase.table('scholarships').upsert(
                data,
                on_conflict='link'
            ).execute()
            
            if result.data:
                print(f"  ✅ 저장 완료! ID: {result.data[0]['id']}")
                return True
            else:
                print(f"  ❌ 저장 실패")
                return False
                
        except Exception as e:
            print(f"  ❌ DB 오류: {e}")
            return False
    
    @staticmethod
    def get_statistics() -> Dict:
        """통계 조회"""
        try:
            total = supabase.table('scholarships').select('*', count='exact').execute().count
            
            today = datetime.now().strftime('%Y-%m-%d')
            active = supabase.table('scholarships').select('*', count='exact').gte('due_date', today).execute().count
            
            return {
                'total': total,
                'active': active,
                'expired': total - active
            }
        except:
            return {'total': 0, 'active': 0, 'expired': 0}


def main():
    """메인 실행 함수"""
    print("=" * 80)
    print("🎓 장학금 메인 크롤러 (GPT-4o Vision)")
    print("=" * 80)
    
    # 초기 통계
    print("\n📊 현재 DB 상태:")
    stats = DatabaseManager.get_statistics()
    print(f"  전체: {stats['total']}개 | 활성: {stats['active']}개 | 만료: {stats['expired']}개\n")
    
    # 크롤러 시작
    crawler = ScholarshipCrawler()
    
    # 1. 목록 크롤링
    items = crawler.crawl_list(TARGET_URL)
    
    if not items:
        print("❌ 크롤링할 공고가 없습니다.")
        return
    
    print(f"\n🔄 총 {len(items)}개 공고를 처리합니다.\n")
    
    # 통계
    success_count = 0
    fail_count = 0
    image_count = 0
    text_count = 0
    
    # 2. 각 공고 처리
    for idx, item in enumerate(items, 1):
        print(f"\n[{idx}/{len(items)}] {item['title'][:50]}...")
        print("-" * 80)
        
        # 상세 페이지 크롤링
        image_url, text_content, is_image = crawler.crawl_detail(item['link'])
        
        if not image_url and not text_content:
            print("  ⚠️  본문을 가져올 수 없습니다.")
            fail_count += 1
            time.sleep(DELAY_SECONDS)
            continue
        
        analyzed = None
        
        # Vision 분석 (이미지가 있을 때)
        if is_image and image_url:
            image_base64 = crawler.download_image_as_base64(image_url)
            
            if image_base64:
                analyzed = GPTAnalyzer.analyze_image(item['title'], image_base64)
                
                if analyzed:
                    image_count += 1
        
        # 텍스트 분석 (폴백)
        if not analyzed and text_content:
            analyzed = GPTAnalyzer.analyze_text(item['title'], text_content)
            
            if analyzed:
                text_count += 1
                is_image = False
        
        # 분석 실패
        if not analyzed:
            print("  ⚠️  분석 실패")
            fail_count += 1
            time.sleep(DELAY_SECONDS)
            continue
        
        # 마감일 없으면 기본값 (3개월 후)
        if not analyzed['due_date']:
            default_due = datetime.now() + timedelta(days=90)
            analyzed['due_date'] = default_due.strftime('%Y-%m-%d')
            print(f"  ⚠️  마감일 없음, 기본값: {analyzed['due_date']}")
        
        # DB 저장
        scholarship_data = {
            'title': item['title'],
            'link': item['link'],
            'due_date': analyzed['due_date'],
            'min_gpa': analyzed['min_gpa'],
            'max_income': analyzed['max_income'],
            'residence': analyzed['residence'],
            'is_image_content': is_image
        }
        
        if DatabaseManager.upsert_scholarship(scholarship_data):
            success_count += 1
        else:
            fail_count += 1
        
        # 딜레이
        time.sleep(DELAY_SECONDS)
    
    # 최종 결과
    print("\n" + "=" * 80)
    print("✅ 크롤링 완료!")
    print("=" * 80)
    print(f"  성공: {success_count}개 | 실패: {fail_count}개 | 전체: {len(items)}개")
    print(f"\n  📊 분석 방법:")
    print(f"    - 이미지 (Vision): {image_count}개")
    print(f"    - 텍스트: {text_count}개\n")
    
    # 최신 통계
    print("📊 최종 DB 상태:")
    stats = DatabaseManager.get_statistics()
    print(f"  전체: {stats['total']}개 | 활성: {stats['active']}개 | 만료: {stats['expired']}개\n")


if __name__ == "__main__":
    main()

