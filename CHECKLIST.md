# ✅ 배포 체크리스트

프로젝트를 배포하기 전에 확인해야 할 사항들입니다.

---

## 🗄️ Database (Supabase)

### 초기 설정
- [ ] Supabase 계정 생성
- [ ] 새 프로젝트 생성
- [ ] Database password 저장
- [ ] Region 선택 (Northeast Asia - Seoul)

### 스키마 생성
- [ ] SQL Editor 열기
- [ ] `supabase_schema.sql` 복사
- [ ] SQL 실행 (Run)
- [ ] 성공 메시지 확인
- [ ] Table Editor에서 `scholarships` 테이블 확인

### API 키 확인
- [ ] Settings → API 접속
- [ ] Project URL 확인 (https://xxxxx.supabase.co)
- [ ] anon public key 확인 (Frontend용)
- [ ] service_role key 확인 (Crawler용)

### 샘플 데이터 (선택)
- [ ] `supabase_sample_data.sql` 실행
- [ ] Table Editor에서 데이터 확인

---

## 💻 Frontend (Next.js)

### 의존성 설치
- [ ] Node.js 18+ 설치 확인 (`node --version`)
- [ ] `npm install` 실행
- [ ] 설치 완료 확인 (node_modules 폴더 생성)

### 환경 변수 설정
- [ ] `env_example.txt` → `.env.local` 복사
- [ ] `NEXT_PUBLIC_SUPABASE_URL` 입력
- [ ] `NEXT_PUBLIC_SUPABASE_ANON_KEY` 입력
- [ ] `NEXT_PUBLIC_` 접두사 확인

### 로컬 테스트
- [ ] `npm run dev` 실행
- [ ] http://localhost:3000 접속
- [ ] 페이지 정상 로딩 확인
- [ ] F12 → Console에서 에러 확인
- [ ] 장학금 데이터 로딩 확인
- [ ] 검색 기능 테스트
- [ ] 모바일 반응형 확인 (F12 → 모바일 모드)

### 빌드 테스트
- [ ] `npm run build` 실행
- [ ] 빌드 성공 확인 (에러 없음)
- [ ] `npm start` 실행
- [ ] http://localhost:3000 접속 확인

---

## 🐍 Crawler (Python) - 선택사항

### Python 환경
- [ ] Python 3.8+ 설치 확인 (`python --version`)
- [ ] 가상환경 생성 (`python -m venv venv`)
- [ ] 가상환경 활성화
- [ ] `pip install -r requirements.txt` 실행

### 환경 변수 설정
- [ ] `crawler/env_template.txt` → `crawler/.env` 복사
- [ ] `SUPABASE_URL` 입력 (Project URL)
- [ ] `SUPABASE_KEY` 입력 (⚠️ service_role key)
- [ ] `OPENAI_API_KEY` 입력 (sk-proj-로 시작)
- [ ] `TARGET_URL` 입력 (크롤링할 사이트)

### OpenAI API 설정
- [ ] https://platform.openai.com 가입
- [ ] API key 생성
- [ ] GPT-4o 접근 권한 확인
- [ ] 잔액 확인 ($5 이상 권장)

### 환경 테스트
- [ ] `python test_crawler.py` 실행
- [ ] 환경 변수 테스트 통과
- [ ] Supabase 연결 테스트 통과
- [ ] OpenAI API 테스트 통과
- [ ] 크롤링 URL 접근 테스트 통과

### 크롤러 실행
- [ ] `python crawler_vision.py` 또는 `python crawler.py` 실행
- [ ] 크롤링 진행 확인
- [ ] 에러 없이 완료
- [ ] Supabase Table Editor에서 데이터 확인

---

## 🌐 Vercel 배포

### GitHub 설정
- [ ] GitHub 계정 생성/로그인
- [ ] 새 저장소 생성
- [ ] `.gitignore` 확인 (.env 파일 제외되는지)
- [ ] 프로젝트 푸시
  ```bash
  git init
  git add .
  git commit -m "Initial commit"
  git branch -M main
  git remote add origin <your-repo-url>
  git push -u origin main
  ```

### Vercel 계정
- [ ] https://vercel.com 접속
- [ ] GitHub 계정으로 로그인
- [ ] Vercel과 GitHub 연동

### 프로젝트 Import
- [ ] **New Project** 클릭
- [ ] GitHub 저장소 선택
- [ ] **Import** 클릭

### 환경 변수 설정
- [ ] **Environment Variables** 섹션 찾기
- [ ] `NEXT_PUBLIC_SUPABASE_URL` 추가
  - Value: Supabase Project URL
  - Environment: Production, Preview, Development 모두 체크
- [ ] `NEXT_PUBLIC_SUPABASE_ANON_KEY` 추가
  - Value: Supabase anon public key
  - Environment: Production, Preview, Development 모두 체크

### 배포
- [ ] **Deploy** 버튼 클릭
- [ ] 배포 진행 상태 확인 (1~2분)
- [ ] 배포 완료 확인 ✅

### 배포 후 확인
- [ ] 생성된 URL 접속 (https://your-project.vercel.app)
- [ ] 페이지 정상 로딩 확인
- [ ] 장학금 데이터 로딩 확인
- [ ] 검색 기능 테스트
- [ ] 모바일에서 접속 테스트
- [ ] 다른 브라우저에서 테스트 (Chrome, Safari, Firefox)

### 도메인 설정 (선택)
- [ ] 커스텀 도메인 구입
- [ ] Vercel Dashboard → Settings → Domains
- [ ] 도메인 추가
- [ ] DNS 설정
- [ ] SSL 인증서 확인

---

## 🔒 보안 체크

### 환경 변수
- [ ] `.env.local` 파일이 `.gitignore`에 포함되었는지 확인
- [ ] `crawler/.env` 파일이 `.gitignore`에 포함되었는지 확인
- [ ] GitHub에 환경 변수 파일이 올라가지 않았는지 확인

### Supabase RLS
- [ ] Row Level Security 활성화 확인
- [ ] 읽기 정책 확인 (public)
- [ ] 쓰기 정책 확인 (authenticated)

### API 키
- [ ] service_role key가 코드에 하드코딩되지 않았는지 확인
- [ ] 프론트엔드에는 anon key만 사용하는지 확인
- [ ] OpenAI API key가 노출되지 않았는지 확인

---

## 📱 사용자 테스트

### 기능 테스트
- [ ] 학점 입력 (0.0 ~ 4.5)
- [ ] 소득분위 선택 (1~10분위)
- [ ] 거주지 선택
- [ ] 검색 버튼 클릭
- [ ] 결과 표시 확인
- [ ] D-day 계산 정확성
- [ ] 카드 클릭 → 외부 링크 이동
- [ ] 초기화 버튼
- [ ] 빈 검색 결과 처리

### 반응형 테스트
- [ ] 모바일 (375px)
- [ ] 태블릿 (768px)
- [ ] 데스크톱 (1920px)
- [ ] 가로/세로 모드

### 브라우저 호환성
- [ ] Chrome
- [ ] Safari
- [ ] Firefox
- [ ] Edge
- [ ] Mobile Safari (iOS)
- [ ] Chrome Mobile (Android)

---

## 📊 모니터링 설정 (선택)

### Vercel Analytics
- [ ] Vercel Dashboard → Analytics 활성화
- [ ] 방문자 수 확인
- [ ] 페이지 로딩 속도 확인

### Supabase Metrics
- [ ] Dashboard → Database → Usage 확인
- [ ] API 요청 수 확인
- [ ] 스토리지 사용량 확인

---

## 🤖 자동화 설정 (선택)

### GitHub Actions
- [ ] `.github/workflows/crawler.yml` 생성
- [ ] Secrets 설정 (API 키들)
- [ ] 스케줄 설정 (매일 실행)
- [ ] 테스트 실행

### Windows Task Scheduler
- [ ] 작업 스케줄러 열기
- [ ] 기본 작업 만들기
- [ ] 트리거 설정 (매일 오전 9시)
- [ ] 동작 설정 (python crawler_vision.py)
- [ ] 테스트 실행

### Linux/Mac Cron
- [ ] `crontab -e` 열기
- [ ] cron job 추가
- [ ] 로그 경로 설정
- [ ] 테스트 실행

---

## 📝 문서화

### README 업데이트
- [ ] 프로젝트 설명
- [ ] 데모 URL 추가
- [ ] 스크린샷 추가
- [ ] 설치 가이드 확인
- [ ] 기여 가이드
- [ ] 라이선스

### 코드 정리
- [ ] 불필요한 console.log 제거
- [ ] 주석 추가
- [ ] TODO 처리
- [ ] 린트 에러 수정 (`npm run lint`)

---

## 🎉 완료!

모든 체크리스트를 완료하셨나요?

**축하합니다! 🎊**

이제 장학금 레이더가 성공적으로 배포되었습니다!

### 다음 단계:
1. 친구들에게 공유하기
2. 학교 커뮤니티에 홍보
3. 사용자 피드백 수집
4. 기능 개선 및 업데이트

---

**배포 URL:** https://your-project.vercel.app

**Last Updated:** 2025-11-27

