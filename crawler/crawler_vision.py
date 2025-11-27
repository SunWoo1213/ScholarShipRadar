"""
장학금 정보 크롤링 및 분석 스크립트 (이미지 기반 - GPT-4o Vision)
학교 공지사항이 이미지로 되어 있는 경우를 위한 버전
"""

import os
import json
import time
import base64
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from urllib.parse import urljoin, urlparse
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

# 설정값
TARGET_URL = os.getenv("TARGET_URL", "https://web.kangnam.ac.kr")
BASE_DOMAIN = "https://web.kangnam.ac.kr"
MAX_PAGES = int(os.getenv("MAX_PAGES", "10"))
DELAY_SECONDS = int(os.getenv("DELAY_SECONDS", "2"))


class ScholarshipCrawler:
    """장학금 크롤러 클래스 (이미지 기반)"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        })
        self.processed_links = set()
    
    def crawl_scholarship_list(self, url: str) -> List[Dict]:
        """
        장학금 게시판 페이지를 크롤링하여 공고 목록을 가져옵니다.
        
        Args:
            url: 크롤링할 게시판 URL
            
        Returns:
            장학금 공고 리스트 [{'title': str, 'link': str, 'date': str}, ...]
        """
        try:
            print(f"📡 크롤링 시작: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'lxml')
            scholarships = []
            
            # class="detailLink"를 가진 모든 링크 찾기
            detail_links = soup.find_all('a', class_='detailLink')
            
            print(f"✅ {len(detail_links)}개의 공고를 발견했습니다.")
            
            for link in detail_links:
                title = link.get_text(strip=True)
                
                # href 속성에서 링크 추출
                href = link.get('href', '')
                
                # data-params에서 추가 정보 추출
                data_params = link.get('data-params', '')
                
                # 상세 페이지 URL 구성
                if href and href != '#':
                    detail_url = self._build_full_url(BASE_DOMAIN, href)
                elif data_params:
                    # data-params에서 URL 파라미터 추출
                    detail_url = self._extract_detail_url_from_params(data_params)
                else:
                    continue
                
                if detail_url and detail_url not in self.processed_links:
                    scholarships.append({
                        'title': title,
                        'link': detail_url,
                    })
                    self.processed_links.add(detail_url)
            
            return scholarships
            
        except Exception as e:
            print(f"❌ 크롤링 오류: {e}")
            return []
    
    def crawl_scholarship_detail(self, url: str) -> Tuple[Optional[str], Optional[str]]:
        """
        장학금 상세 페이지에서 이미지 URL과 텍스트 내용을 가져옵니다.
        
        Args:
            url: 상세 페이지 URL
            
        Returns:
            (image_url, text_content) 튜플
        """
        try:
            print(f"  📄 상세 페이지 크롤링: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'lxml')
            
            # 본문 영역 찾기 (.tbl_view 클래스)
            content_div = soup.find('div', class_='tbl_view')
            
            if not content_div:
                # 대체 클래스명 시도
                content_div = soup.find('div', class_=re.compile(r'content|view|detail|article', re.I))
            
            if not content_div:
                print(f"  ⚠️  본문 영역을 찾을 수 없습니다.")
                return None, None
            
            # 1. 이미지 찾기 (우선순위)
            image_url = None
            img_tag = content_div.find('img')
            
            if img_tag:
                img_src = img_tag.get('src', '')
                if img_src:
                    # 상대 경로를 절대 경로로 변환
                    image_url = self._build_full_url(BASE_DOMAIN, img_src)
                    print(f"  🖼️  이미지 발견: {image_url}")
            
            # 2. 텍스트 추출 (백업용)
            text_content = content_div.get_text(strip=True, separator='\n')
            
            return image_url, text_content
            
        except Exception as e:
            print(f"  ❌ 상세 페이지 크롤링 실패: {e}")
            return None, None
    
    def download_image_as_base64(self, image_url: str) -> Optional[str]:
        """
        이미지를 다운로드하여 Base64 문자열로 인코딩합니다.
        
        Args:
            image_url: 이미지 URL
            
        Returns:
            Base64 인코딩된 이미지 문자열
        """
        try:
            print(f"  📥 이미지 다운로드 중: {image_url}")
            
            # 이미지 다운로드
            response = self.session.get(image_url, timeout=15)
            response.raise_for_status()
            
            # Base64 인코딩
            image_data = base64.b64encode(response.content).decode('utf-8')
            
            # 이미지 타입 추출
            content_type = response.headers.get('Content-Type', 'image/jpeg')
            
            print(f"  ✅ 이미지 다운로드 완료 ({len(image_data)} bytes)")
            
            return f"data:{content_type};base64,{image_data}"
            
        except Exception as e:
            print(f"  ❌ 이미지 다운로드 실패: {e}")
            return None
    
    def _build_full_url(self, base_url: str, path: str) -> str:
        """상대 경로를 절대 경로로 변환"""
        if path.startswith('http'):
            return path
        return urljoin(base_url, path)
    
    def _extract_detail_url_from_params(self, data_params: str) -> Optional[str]:
        """data-params에서 상세 페이지 URL 추출"""
        try:
            # data-params가 JSON 형태인 경우
            params = json.loads(data_params.replace('&quot;', '"'))
            
            # 강남대 게시판 구조에 맞게 URL 구성
            if 'encMenuBoardSeq' in params:
                board_seq = params['encMenuBoardSeq']
                # 실제 게시판 상세 URL 패턴에 맞게 수정 필요
                return f"{BASE_DOMAIN}/board/view?seq={board_seq}"
            
            return None
        except Exception as e:
            print(f"  ⚠️  data-params 파싱 실패: {e}")
            return None


class GPTVisionAnalyzer:
    """GPT-4o Vision을 사용한 장학금 정보 분석"""
    
    @staticmethod
    def analyze_with_image(title: str, image_base64: str) -> Optional[Dict]:
        """
        GPT-4o Vision으로 이미지를 분석합니다.
        
        Args:
            title: 장학금 제목
            image_base64: Base64 인코딩된 이미지
            
        Returns:
            분석 결과 딕셔너리
        """
        try:
            print(f"  🤖 GPT-4o Vision 분석 중...")
            
            # GPT-4o Vision API 호출
            response = openai_client.chat.completions.create(
                model="gpt-4o",  # Vision 지원 모델
                messages=[
                    {
                        "role": "system",
                        "content": """당신은 장학금 공고 이미지를 분석하는 전문가입니다.
이미지에서 다음 정보를 추출하여 JSON 형태로 반환하세요.

추출할 정보:
1. min_gpa: 최소 학점 요구사항 (없으면 0.0)
2. max_income: 소득분위 상한선 (0~10, 제한 없으면 99)
3. residence: 거주지 제한 (예: '서울', '경기', '전국' 등, 제한 없으면 '전국')
4. due_date: 신청 마감일 (YYYY-MM-DD 형식, 찾을 수 없으면 null)

응답 형식 (JSON):
{
    "min_gpa": 3.0,
    "max_income": 8,
    "residence": "서울",
    "due_date": "2026-01-31"
}

주의사항:
- 학점이 명시되지 않았으면 0.0
- 소득분위가 명시되지 않았으면 99
- 거주지가 명시되지 않았으면 "전국"
- 마감일을 찾을 수 없으면 null
- 반드시 유효한 JSON만 반환할 것
- 이미지의 텍스트를 정확하게 읽어서 추출할 것"""
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"""제목: {title}

위 장학금 공고 이미지를 분석하여 min_gpa, max_income, residence, due_date를 추출해주세요.
이미지 내의 모든 텍스트를 주의 깊게 읽어주세요."""
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": image_base64,
                                    "detail": "high"  # 고해상도 분석
                                }
                            }
                        ]
                    }
                ],
                response_format={"type": "json_object"},
                temperature=0.1,
                max_tokens=500
            )
            
            # 응답 파싱
            result = json.loads(response.choices[0].message.content)
            
            # 데이터 검증 및 정제
            analyzed_data = {
                'min_gpa': float(result.get('min_gpa', 0.0)),
                'max_income': int(result.get('max_income', 99)),
                'residence': result.get('residence', '전국'),
                'due_date': result.get('due_date')
            }
            
            # due_date 유효성 검사
            if analyzed_data['due_date']:
                try:
                    datetime.strptime(analyzed_data['due_date'], '%Y-%m-%d')
                except ValueError:
                    analyzed_data['due_date'] = None
            
            print(f"  ✅ 분석 완료: {analyzed_data}")
            return analyzed_data
            
        except Exception as e:
            print(f"  ❌ GPT Vision 분석 실패: {e}")
            return None
    
    @staticmethod
    def analyze_with_text(title: str, content: str) -> Optional[Dict]:
        """
        텍스트 기반 분석 (이미지가 없을 때 폴백)
        
        Args:
            title: 장학금 제목
            content: 본문 텍스트
            
        Returns:
            분석 결과 딕셔너리
        """
        try:
            print(f"  🤖 GPT-4o 텍스트 분석 중...")
            
            system_prompt = """당신은 장학금 공고문을 분석하는 전문가입니다.
주어진 장학금 공고에서 다음 정보를 추출하여 JSON 형태로 반환하세요.

추출할 정보:
1. min_gpa: 최소 학점 요구사항 (없으면 0.0)
2. max_income: 소득분위 상한선 (0~10, 제한 없으면 99)
3. residence: 거주지 제한 (예: '서울', '경기', '전국' 등, 제한 없으면 '전국')
4. due_date: 신청 마감일 (YYYY-MM-DD 형식, 찾을 수 없으면 null)

응답 형식 (JSON):
{
    "min_gpa": 3.0,
    "max_income": 8,
    "residence": "서울",
    "due_date": "2026-01-31"
}

주의사항:
- 학점이 명시되지 않았으면 0.0
- 소득분위가 명시되지 않았으면 99
- 거주지가 명시되지 않았으면 "전국"
- 마감일을 찾을 수 없으면 null
- 반드시 유효한 JSON만 반환할 것"""

            user_prompt = f"""제목: {title}

내용:
{content[:4000]}  # 토큰 제한

위 장학금 공고를 분석하여 min_gpa, max_income, residence, due_date를 추출해주세요."""

            # GPT-4o API 호출
            response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.1,
                max_tokens=500
            )
            
            # 응답 파싱
            result = json.loads(response.choices[0].message.content)
            
            # 데이터 검증 및 정제
            analyzed_data = {
                'min_gpa': float(result.get('min_gpa', 0.0)),
                'max_income': int(result.get('max_income', 99)),
                'residence': result.get('residence', '전국'),
                'due_date': result.get('due_date')
            }
            
            # due_date 유효성 검사
            if analyzed_data['due_date']:
                try:
                    datetime.strptime(analyzed_data['due_date'], '%Y-%m-%d')
                except ValueError:
                    analyzed_data['due_date'] = None
            
            print(f"  ✅ 분석 완료: {analyzed_data}")
            return analyzed_data
            
        except Exception as e:
            print(f"  ❌ GPT 텍스트 분석 실패: {e}")
            return None


class SupabaseManager:
    """Supabase 데이터베이스 관리"""
    
    @staticmethod
    def insert_scholarship(scholarship_data: Dict) -> bool:
        """
        장학금 데이터를 Supabase에 삽입합니다.
        
        Args:
            scholarship_data: 삽입할 장학금 데이터
            
        Returns:
            성공 여부
        """
        try:
            print(f"  💾 DB 저장 중: {scholarship_data['title'][:30]}...")
            
            # 중복 체크 (link 기준)
            existing = supabase.table('scholarships') \
                .select('id') \
                .eq('link', scholarship_data['link']) \
                .execute()
            
            if existing.data:
                print(f"  ⚠️  이미 존재하는 공고입니다. 건너뜁니다.")
                return False
            
            # 데이터 삽입
            result = supabase.table('scholarships').insert(scholarship_data).execute()
            
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
        """데이터베이스 통계 조회"""
        try:
            result = supabase.table('scholarships').select('*', count='exact').execute()
            total = result.count
            
            # 활성 장학금 (마감일 지나지 않은 것)
            active_result = supabase.table('scholarships') \
                .select('*', count='exact') \
                .gte('due_date', datetime.now().strftime('%Y-%m-%d')) \
                .execute()
            active = active_result.count
            
            return {
                'total': total,
                'active': active,
                'expired': total - active
            }
        except Exception as e:
            print(f"❌ 통계 조회 실패: {e}")
            return {'total': 0, 'active': 0, 'expired': 0}


def main():
    """메인 실행 함수"""
    print("=" * 70)
    print("🎓 장학금 크롤러 시작 (이미지 기반 - GPT-4o Vision)")
    print("=" * 70)
    
    # 초기 통계
    print("\n📊 현재 DB 상태:")
    stats = SupabaseManager.get_statistics()
    print(f"  - 전체 장학금: {stats['total']}개")
    print(f"  - 활성 장학금: {stats['active']}개")
    print(f"  - 만료 장학금: {stats['expired']}개\n")
    
    # 크롤러 초기화
    crawler = ScholarshipCrawler()
    
    # 장학금 목록 크롤링
    scholarships = crawler.crawl_scholarship_list(TARGET_URL)
    
    if not scholarships:
        print("❌ 크롤링할 장학금이 없습니다.")
        return
    
    print(f"\n🔄 총 {len(scholarships)}개의 장학금을 처리합니다.\n")
    
    # 각 장학금 처리
    success_count = 0
    fail_count = 0
    image_count = 0
    text_count = 0
    
    for idx, scholarship in enumerate(scholarships, 1):
        print(f"\n[{idx}/{len(scholarships)}] {scholarship['title']}")
        print("-" * 70)
        
        # 상세 페이지 크롤링 (이미지 + 텍스트)
        image_url, text_content = crawler.crawl_scholarship_detail(scholarship['link'])
        
        if not image_url and not text_content:
            print("  ⚠️  본문을 가져올 수 없습니다. 건너뜁니다.")
            fail_count += 1
            time.sleep(DELAY_SECONDS)
            continue
        
        analyzed = None
        
        # 전략 1: 이미지가 있으면 Vision으로 분석 (우선순위)
        if image_url:
            # 이미지 다운로드 및 Base64 인코딩
            image_base64 = crawler.download_image_as_base64(image_url)
            
            if image_base64:
                # GPT-4o Vision 분석
                analyzed = GPTVisionAnalyzer.analyze_with_image(
                    scholarship['title'],
                    image_base64
                )
                
                if analyzed:
                    image_count += 1
                    print(f"  📸 이미지 기반 분석 성공")
        
        # 전략 2: 이미지 분석 실패 or 이미지 없음 → 텍스트 분석 (폴백)
        if not analyzed and text_content:
            print(f"  📝 텍스트 기반 분석으로 전환...")
            analyzed = GPTVisionAnalyzer.analyze_with_text(
                scholarship['title'],
                text_content
            )
            
            if analyzed:
                text_count += 1
                print(f"  📝 텍스트 기반 분석 성공")
        
        # 분석 실패
        if not analyzed:
            print("  ⚠️  분석에 실패했습니다. 건너뜁니다.")
            fail_count += 1
            time.sleep(DELAY_SECONDS)
            continue
        
        # due_date가 없으면 기본값 설정
        if not analyzed['due_date']:
            from datetime import timedelta
            default_due = datetime.now() + timedelta(days=90)
            analyzed['due_date'] = default_due.strftime('%Y-%m-%d')
            print(f"  ⚠️  마감일을 찾을 수 없어 기본값 설정: {analyzed['due_date']}")
        
        # DB에 저장할 데이터 구성
        scholarship_data = {
            'title': scholarship['title'],
            'link': scholarship['link'],
            'due_date': analyzed['due_date'],
            'min_gpa': analyzed['min_gpa'],
            'max_income': analyzed['max_income'],
            'residence': analyzed['residence']
        }
        
        # Supabase에 저장
        if SupabaseManager.insert_scholarship(scholarship_data):
            success_count += 1
        else:
            fail_count += 1
        
        # 요청 간 딜레이 (서버 부하 방지 + API Rate Limit)
        time.sleep(DELAY_SECONDS)
    
    # 최종 통계
    print("\n" + "=" * 70)
    print("✅ 크롤링 완료!")
    print("=" * 70)
    print(f"  - 성공: {success_count}개")
    print(f"  - 실패: {fail_count}개")
    print(f"  - 전체: {len(scholarships)}개")
    print(f"\n  📊 분석 방법:")
    print(f"  - 이미지 기반 (Vision): {image_count}개")
    print(f"  - 텍스트 기반: {text_count}개\n")
    
    # 최신 DB 상태
    print("📊 최종 DB 상태:")
    stats = SupabaseManager.get_statistics()
    print(f"  - 전체 장학금: {stats['total']}개")
    print(f"  - 활성 장학금: {stats['active']}개")
    print(f"  - 만료 장학금: {stats['expired']}개\n")


if __name__ == "__main__":
    main()

