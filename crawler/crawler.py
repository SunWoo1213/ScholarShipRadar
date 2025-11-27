"""
장학금 정보 크롤링 및 분석 스크립트
Supabase DB에 자동으로 장학금 데이터를 수집하고 저장합니다.
"""

import os
import json
import time
import re
from datetime import datetime
from typing import Dict, List, Optional
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
TARGET_URL = os.getenv("TARGET_URL")
MAX_PAGES = int(os.getenv("MAX_PAGES", "10"))
DELAY_SECONDS = int(os.getenv("DELAY_SECONDS", "2"))


class ScholarshipCrawler:
    """장학금 크롤러 클래스"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.processed_links = set()
    
    def crawl_scholarship_list(self, url: str) -> List[Dict]:
        """
        장학금 게시판 페이지를 크롤링하여 공고 목록을 가져옵니다.
        
        Args:
            url: 크롤링할 게시판 URL
            
        Returns:
            장학금 공고 리스트 [{'title': str, 'link': str, 'raw_html': str}, ...]
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
                
                # 링크 URL 추출 (실제 사이트에 맞게 수정 필요)
                # data-params에서 실제 링크를 구성하거나, href 속성 사용
                data_params = link.get('data-params', '')
                href = link.get('href', '#')
                
                # 실제 상세 페이지 URL 구성
                if href and href != '#':
                    detail_url = self._build_full_url(url, href)
                else:
                    # data-params에서 URL 구성 (사이트별로 다름)
                    detail_url = self._extract_detail_url(url, data_params)
                
                if detail_url and detail_url not in self.processed_links:
                    scholarships.append({
                        'title': title,
                        'link': detail_url,
                        'data_params': data_params
                    })
                    self.processed_links.add(detail_url)
            
            return scholarships
            
        except Exception as e:
            print(f"❌ 크롤링 오류: {e}")
            return []
    
    def crawl_scholarship_detail(self, url: str) -> Optional[str]:
        """
        장학금 상세 페이지의 본문 내용을 크롤링합니다.
        
        Args:
            url: 상세 페이지 URL
            
        Returns:
            본문 텍스트 (없으면 None)
        """
        try:
            print(f"  📄 상세 페이지 크롤링: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'lxml')
            
            # 본문 내용 추출 (사이트 구조에 맞게 수정 필요)
            # 일반적인 게시판 구조 시도
            content = None
            
            # 방법 1: class나 id로 본문 찾기
            content_div = soup.find('div', class_=re.compile(r'content|article|post|body', re.I))
            if content_div:
                content = content_div.get_text(strip=True, separator='\n')
            
            # 방법 2: 특정 태그 찾기
            if not content:
                article = soup.find('article')
                if article:
                    content = article.get_text(strip=True, separator='\n')
            
            # 방법 3: 전체 body에서 추출
            if not content:
                body = soup.find('body')
                if body:
                    # 불필요한 요소 제거
                    for tag in body(['script', 'style', 'nav', 'header', 'footer']):
                        tag.decompose()
                    content = body.get_text(strip=True, separator='\n')
            
            return content if content else None
            
        except Exception as e:
            print(f"  ❌ 상세 페이지 크롤링 실패: {e}")
            return None
    
    def _build_full_url(self, base_url: str, href: str) -> str:
        """상대 경로를 절대 경로로 변환"""
        from urllib.parse import urljoin
        return urljoin(base_url, href)
    
    def _extract_detail_url(self, base_url: str, data_params: str) -> Optional[str]:
        """data-params에서 상세 페이지 URL 추출 (사이트별 커스터마이징 필요)"""
        try:
            # data_params가 JSON 형태인 경우
            params = json.loads(data_params.replace('&quot;', '"'))
            
            # 예시: 파라미터로 URL 구성
            # 실제 사이트 구조에 맞게 수정 필요
            if 'encMenuSeq' in params and 'encMenuBoardSeq' in params:
                detail_url = f"{base_url}?seq={params['encMenuBoardSeq']}"
                return detail_url
            
            return None
        except:
            return None


class GPTAnalyzer:
    """GPT-4o-mini를 사용한 장학금 정보 분석"""
    
    @staticmethod
    def analyze_scholarship(title: str, content: str) -> Optional[Dict]:
        """
        GPT-4o-mini를 사용하여 장학금 정보를 분석합니다.
        
        Args:
            title: 장학금 제목
            content: 장학금 본문 내용
            
        Returns:
            분석 결과 딕셔너리 또는 None
        """
        try:
            print(f"  🤖 GPT 분석 중...")
            
            # GPT에게 전달할 프롬프트
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
{content[:3000]}  # 토큰 제한을 위해 3000자로 제한

위 장학금 공고를 분석하여 min_gpa, max_income, residence, due_date를 추출해주세요."""

            # GPT-4o-mini API 호출
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
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
            print(f"  ❌ GPT 분석 실패: {e}")
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
    print("=" * 60)
    print("🎓 장학금 크롤러 시작")
    print("=" * 60)
    
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
    
    for idx, scholarship in enumerate(scholarships, 1):
        print(f"\n[{idx}/{len(scholarships)}] {scholarship['title']}")
        print("-" * 60)
        
        # 상세 페이지 크롤링
        detail_content = crawler.crawl_scholarship_detail(scholarship['link'])
        
        if not detail_content:
            print("  ⚠️  본문을 가져올 수 없습니다. 건너뜁니다.")
            fail_count += 1
            time.sleep(DELAY_SECONDS)
            continue
        
        # GPT로 분석
        analyzed = GPTAnalyzer.analyze_scholarship(
            scholarship['title'],
            detail_content
        )
        
        if not analyzed:
            print("  ⚠️  분석에 실패했습니다. 건너뜁니다.")
            fail_count += 1
            time.sleep(DELAY_SECONDS)
            continue
        
        # due_date가 없으면 기본값 설정 (예: 3개월 후)
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
        
        # 요청 간 딜레이 (서버 부하 방지)
        time.sleep(DELAY_SECONDS)
    
    # 최종 통계
    print("\n" + "=" * 60)
    print("✅ 크롤링 완료!")
    print("=" * 60)
    print(f"  - 성공: {success_count}개")
    print(f"  - 실패: {fail_count}개")
    print(f"  - 전체: {len(scholarships)}개\n")
    
    # 최신 DB 상태
    print("📊 최종 DB 상태:")
    stats = SupabaseManager.get_statistics()
    print(f"  - 전체 장학금: {stats['total']}개")
    print(f"  - 활성 장학금: {stats['active']}개")
    print(f"  - 만료 장학금: {stats['expired']}개\n")


if __name__ == "__main__":
    main()

