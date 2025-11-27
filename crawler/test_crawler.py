"""
크롤러 테스트 스크립트
실제 크롤링 전에 환경 설정을 테스트합니다.
"""

import os
from dotenv import load_dotenv

def test_env_variables():
    """환경 변수 로드 테스트"""
    print("=" * 60)
    print("🧪 환경 변수 테스트")
    print("=" * 60)
    
    load_dotenv()
    
    required_vars = {
        'SUPABASE_URL': os.getenv('SUPABASE_URL'),
        'SUPABASE_KEY': os.getenv('SUPABASE_KEY'),
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
        'TARGET_URL': os.getenv('TARGET_URL')
    }
    
    all_set = True
    for var_name, var_value in required_vars.items():
        if var_value and var_value != f'your-{var_name.lower().replace("_", "-")}':
            print(f"✅ {var_name}: 설정됨")
        else:
            print(f"❌ {var_name}: 설정 필요")
            all_set = False
    
    return all_set

def test_supabase_connection():
    """Supabase 연결 테스트"""
    print("\n" + "=" * 60)
    print("🗄️  Supabase 연결 테스트")
    print("=" * 60)
    
    try:
        from supabase import create_client
        
        supabase = create_client(
            os.getenv('SUPABASE_URL'),
            os.getenv('SUPABASE_KEY')
        )
        
        # 테이블 조회 테스트
        result = supabase.table('scholarships').select('*', count='exact').limit(1).execute()
        print(f"✅ Supabase 연결 성공!")
        print(f"   현재 저장된 장학금: {result.count}개")
        return True
        
    except Exception as e:
        print(f"❌ Supabase 연결 실패: {e}")
        return False

def test_openai_connection():
    """OpenAI API 연결 테스트"""
    print("\n" + "=" * 60)
    print("🤖 OpenAI API 테스트")
    print("=" * 60)
    
    try:
        from openai import OpenAI
        
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # 간단한 API 호출 테스트
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": "Hello! Just testing."}
            ],
            max_tokens=10
        )
        
        print(f"✅ OpenAI API 연결 성공!")
        print(f"   응답: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"❌ OpenAI API 연결 실패: {e}")
        return False

def test_target_url():
    """크롤링 대상 URL 접근 테스트"""
    print("\n" + "=" * 60)
    print("🌐 크롤링 대상 URL 테스트")
    print("=" * 60)
    
    try:
        import requests
        
        target_url = os.getenv('TARGET_URL')
        
        if not target_url or 'your-target' in target_url:
            print("⚠️  TARGET_URL이 설정되지 않았습니다.")
            print("   .env 파일에서 실제 장학금 게시판 URL을 설정하세요.")
            return False
        
        response = requests.get(target_url, timeout=10)
        response.raise_for_status()
        
        print(f"✅ URL 접근 성공!")
        print(f"   URL: {target_url}")
        print(f"   상태 코드: {response.status_code}")
        print(f"   페이지 크기: {len(response.content)} bytes")
        return True
        
    except Exception as e:
        print(f"❌ URL 접근 실패: {e}")
        return False

def main():
    """전체 테스트 실행"""
    print("\n🚀 장학금 크롤러 환경 테스트 시작\n")
    
    results = {
        '환경 변수': test_env_variables(),
        'Supabase': test_supabase_connection(),
        'OpenAI API': test_openai_connection(),
        '크롤링 URL': test_target_url()
    }
    
    print("\n" + "=" * 60)
    print("📊 테스트 결과 요약")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = "✅ 통과" if result else "❌ 실패"
        print(f"{test_name}: {status}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n✅ 모든 테스트 통과! crawler.py를 실행할 준비가 되었습니다.")
        print("\n실행 명령어:")
        print("  python crawler.py")
    else:
        print("\n⚠️  일부 테스트가 실패했습니다.")
        print("   .env 파일 설정을 확인하고 다시 시도하세요.")
        print("\n설정 가이드:")
        print("  1. env_template.txt를 복사하여 .env 파일 생성")
        print("  2. .env 파일에 실제 API 키와 URL 입력")
        print("  3. python test_crawler.py 다시 실행")
    
    return all_passed

if __name__ == "__main__":
    main()

