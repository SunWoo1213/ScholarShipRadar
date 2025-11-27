# 🎓 장학금 레이더 (Scholarship Radar)

대학생을 위한 맞춤형 장학금 탐색 웹 플랫폼

사용자의 학점, 소득분위, 거주지에 맞는 장학금을 자동으로 필터링해서 보여주는 MVP 서비스입니다.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Next.js](https://img.shields.io/badge/Next.js-14-black)
![TypeScript](https://img.shields.io/badge/TypeScript-5-blue)
![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-green)
![Python](https://img.shields.io/badge/Python-3.8+-blue)

🔗 **데모:** [https://scholarship-radar.vercel.app](https://scholarship-radar.vercel.app) (배포 후 업데이트)

---

## 📸 스크린샷

```
┌─────────────────────────────────────────┐
│  🎓 장학금 레이더                        │
│  내 조건에 딱 맞는 장학금을 찾아보세요   │
└─────────────────────────────────────────┘
┌─────────────────────────────────────────┐
│  📋 나의 조건 입력                       │
│  ┌──────┬──────────┬────────┐          │
│  │ 학점 │ 소득분위 │ 거주지 │          │
│  └──────┴──────────┴────────┘          │
│  [    장학금 찾기    ]                   │
└─────────────────────────────────────────┘
┌─────────────────────────────────────────┐
│  🎯 검색 결과 12개                       │
│  ┌────────────┐  ┌────────────┐        │
│  │ D-15       │  │ D-7        │        │
│  │ 국가장학금  │  │ 서울시장학금│        │
│  │ [보기]     │  │ [보기]     │        │
│  └────────────┘  └────────────┘        │
└─────────────────────────────────────────┘
```

---

## ⚡ 빠른 시작 (5분 완성!)

### 1️⃣ Supabase 설정 (2분)

```bash
# 1. https://supabase.com 가입 및 프로젝트 생성
# 2. SQL Editor → supabase_schema.sql 복사 & 실행
# 3. Settings → API에서 키 확인 (잠시 후 사용)
```

### 2️⃣ 프론트엔드 실행 (3분)

```bash
# 의존성 설치
npm install

# 환경 변수 파일 생성
copy env_example.txt .env.local    # Windows
# cp env_example.txt .env.local    # Mac/Linux

# .env.local 편집 (메모장으로)
notepad .env.local

# 개발 서버 실행
npm run dev

# → http://localhost:3000 접속! 🎉
```

**`.env.local` 파일 내용:**
```env
NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

> 💡 **API 키 찾는 법:** Supabase Dashboard → Settings → API → `Project URL`과 `anon public` key 복사

### 3️⃣ 크롤러 실행 (선택사항, 5분)

```bash
cd crawler

# Python 패키지 설치
pip install -r requirements.txt

# 환경 변수 파일 생성
copy env_template.txt .env    # Windows
# cp env_template.txt .env    # Mac/Linux

# .env 편집
notepad .env

# 테스트 실행
python test_crawler.py

# 크롤링 시작!
python crawler_vision.py    # 이미지 기반 (권장)
# 또는
python crawler.py           # 텍스트 기반
```

**`crawler/.env` 파일 내용:**
```env
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGci... (⚠️ service_role key - anon 아님!)
OPENAI_API_KEY=sk-proj-xxxxx
TARGET_URL=https://web.kangnam.ac.kr/board/scholarship
```

---

## 🚀 기술 스택

### Frontend
- **Next.js 14** (App Router) - React 프레임워크
- **TypeScript** - 타입 안정성
- **Tailwind CSS** - 유틸리티 CSS 프레임워크
- **Supabase Client** - 실시간 데이터베이스 연동

### Backend & Database
- **Supabase** (PostgreSQL) - 백엔드 서비스
- **Row Level Security** - 데이터 보안

### Data Processing
- **Python 3.8+** - 크롤링 스크립트
- **BeautifulSoup4** - HTML 파싱
- **OpenAI GPT-4o** - Vision & 텍스트 분석
- **Requests** - HTTP 클라이언트

### Deployment
- **Vercel** - Frontend 배포
- **GitHub Actions** - 크롤러 자동화 (선택)

---

## 📋 주요 기능

### ✨ 사용자 기능

#### 🔍 맞춤형 검색
- 학점 기반 필터링 (0.0 ~ 4.5)
- 소득분위 필터링 (1~10분위)
- 거주지 필터링 (전국 17개 시도)
- 실시간 검색 결과

#### 📊 직관적인 UI
- 카드 형식 장학금 리스트
- D-day 자동 계산 및 표시
- 마감 임박 알림 (7일 이내)
- 조건별 태그 표시

#### 📱 완전 반응형
- 모바일 최적화
- 태블릿 지원
- 데스크톱 3열 레이아웃

### 🤖 자동화 기능

#### 🖼️ 이미지 기반 크롤링 (GPT-4o Vision)
- 학교 공지사항 이미지 자동 분석
- Base64 인코딩으로 외부 접근 제한 우회
- 고해상도 OCR 인식

#### 📝 Hybrid 전략
- 이미지 우선 분석
- 텍스트 폴백 지원
- 실패 없는 안정적인 크롤링

#### 💾 자동 데이터 수집
- 중복 방지 (link 기준)
- 자동 조건 추출
- Supabase 자동 저장

---

## 🛠️ 상세 설치 가이드

### 필수 요구사항

- **Node.js** 18.0 이상
- **Python** 3.8 이상 (크롤러 사용 시)
- **Supabase** 계정
- **OpenAI API** 키 (크롤러 사용 시)

### 전체 설치 과정

```
┌─────────────────────────────────────────┐
│  Step 1: Supabase 설정 (2분)            │
│  ├─ 프로젝트 생성                       │
│  ├─ SQL 스키마 실행                     │
│  └─ API 키 확인                         │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  Step 2: 프론트엔드 설정 (3분)          │
│  ├─ npm install                         │
│  ├─ .env.local 설정                     │
│  └─ npm run dev                         │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  Step 3: 크롤러 설정 (선택, 5분)        │
│  ├─ pip install -r requirements.txt     │
│  ├─ crawler/.env 설정                   │
│  └─ python crawler_vision.py            │
└─────────────────────────────────────────┘
```

---

## 🗄️ Step 1: Supabase 데이터베이스 설정

### 1.1 프로젝트 생성

1. https://supabase.com 접속
2. **Start your project** 클릭
3. GitHub으로 로그인
4. **New Project** 클릭
5. 프로젝트 정보 입력:
   - Name: `scholarship-radar`
   - Database Password: 강력한 비밀번호 입력 (저장!)
   - Region: `Northeast Asia (Seoul)` 선택
   - Pricing Plan: `Free` 선택
6. **Create new project** 클릭 (1~2분 소요)

### 1.2 데이터베이스 스키마 생성

1. 왼쪽 메뉴 **SQL Editor** 클릭
2. **New query** 클릭
3. `supabase_schema.sql` 파일 열기
4. 전체 내용 복사 (Ctrl+A → Ctrl+C)
5. SQL Editor에 붙여넣기
6. **Run** 버튼 클릭 ▶️
7. 성공 메시지 확인: `Success. No rows returned`

### 1.3 샘플 데이터 추가 (선택)

```sql
-- supabase_sample_data.sql 파일 내용을 SQL Editor에 실행
-- 10개의 테스트 장학금이 추가됩니다
```

### 1.4 API 키 확인

1. 왼쪽 메뉴 **Settings** ⚙️
2. **API** 클릭
3. 다음 정보 확인 (복사는 나중에):

```
Project URL: https://xxxxxxxxxxxxx.supabase.co
anon public: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
service_role: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9... (크롤러용)
```

---

## 💻 Step 2: 프론트엔드 설정

### 2.1 저장소 클론 및 의존성 설치

```bash
# 프로젝트 클론
git clone <repository-url>
cd scholarship-radar

# 의존성 설치
npm install
```

### 2.2 환경 변수 설정

#### 파일 생성

```bash
# Windows
copy env_example.txt .env.local

# Mac/Linux
cp env_example.txt .env.local
```

#### `.env.local` 파일 편집

메모장이나 VS Code로 열기:

```env
# Supabase 설정
NEXT_PUBLIC_SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh4eHh4eHh4eHh4eHgiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTcwMDAwMDAwMCwiZXhwIjoyMDE1NTc2MDAwfQ.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**중요:**
- `NEXT_PUBLIC_` 접두사 필수!
- Supabase Dashboard → Settings → API에서 복사:
  - `Project URL` → `NEXT_PUBLIC_SUPABASE_URL`
  - `anon public` key → `NEXT_PUBLIC_SUPABASE_ANON_KEY`

### 2.3 개발 서버 실행

```bash
npm run dev
```

성공 메시지:
```
  ▲ Next.js 14.2.15
  - Local:        http://localhost:3000
  - Environments: .env.local

 ✓ Ready in 2.3s
```

### 2.4 확인

브라우저에서 http://localhost:3000 접속

- ✅ 페이지가 열림
- ✅ 장학금 데이터 로드됨 (샘플 데이터 추가한 경우)
- ✅ 검색 기능 작동

---

## 🐍 Step 3: Python 크롤러 설정 (선택사항)

### 3.1 가상환경 생성 (권장)

```bash
cd crawler

# 가상환경 생성
python -m venv venv

# 활성화
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

### 3.2 의존성 설치

```bash
pip install -r requirements.txt
```

설치되는 패키지:
```
requests==2.31.0       # HTTP 클라이언트
beautifulsoup4==4.12.3 # HTML 파싱
lxml==5.1.0            # XML/HTML 파서
openai==1.51.0         # OpenAI API
supabase==2.7.4        # Supabase 클라이언트
python-dotenv==1.0.1   # 환경 변수
Pillow==10.4.0         # 이미지 처리
```

### 3.3 환경 변수 설정

#### 파일 생성

```bash
# Windows
copy env_template.txt .env

# Mac/Linux
cp env_template.txt .env
```

#### `crawler/.env` 파일 편집

```env
# Supabase 설정 (⚠️ service_role key 필요!)
SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh4eHh4eHh4eHh4eHgiLCJyb2xlIjoic2VydmljZV9yb2xlIiwiaWF0IjoxNzAwMDAwMDAwLCJleHAiOjIwMTU1NzYwMDB9.yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy

# OpenAI API 설정
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# 크롤링 대상 URL
TARGET_URL=https://web.kangnam.ac.kr/board/scholarship

# 선택사항
MAX_PAGES=10
DELAY_SECONDS=3
```

**API 키 가져오기:**

**🔹 Supabase (service_role key)**
1. Supabase Dashboard → Settings → API
2. **service_role** key 복사 (⚠️ 민감 정보!)

**🔹 OpenAI API Key**
1. https://platform.openai.com/api-keys 접속
2. **Create new secret key** 클릭
3. 생성된 키 복사 (한 번만 표시됨!)

### 3.4 환경 테스트

```bash
python test_crawler.py
```

출력 예시:
```
🧪 환경 변수 테스트
✅ SUPABASE_URL: 설정됨
✅ SUPABASE_KEY: 설정됨
✅ OPENAI_API_KEY: 설정됨
✅ TARGET_URL: 설정됨

🗄️  Supabase 연결 테스트
✅ Supabase 연결 성공!

🤖 OpenAI API 테스트
✅ OpenAI API 연결 성공!
```

### 3.5 크롤러 실행

#### 🖼️ 이미지 기반 크롤러 (권장)

```bash
python crawler_vision.py
```

**특징:**
- GPT-4o Vision으로 이미지 분석
- 학교 공지사항이 이미지인 경우 최적
- 텍스트 폴백 지원

**비용:** 공고 1개당 약 $0.002 (약 2원)

#### 📝 텍스트 기반 크롤러

```bash
python crawler.py
```

**특징:**
- GPT-4o-mini로 텍스트 분석
- 일반 텍스트 공고에 최적
- 저렴한 비용

**비용:** 공고 1개당 약 $0.0001 (약 0.1원)

---

## 📁 프로젝트 구조

```
scholarship-radar/
├── 📱 Frontend (Next.js)
│   ├── app/
│   │   ├── page.tsx              # 메인 페이지
│   │   ├── layout.tsx            # 레이아웃
│   │   └── globals.css           # 글로벌 스타일
│   ├── lib/
│   │   └── supabase.ts           # Supabase 클라이언트
│   ├── types/
│   │   └── database.types.ts     # TypeScript 타입
│   ├── package.json              # Node.js 의존성
│   ├── tailwind.config.ts        # Tailwind 설정
│   ├── tsconfig.json             # TypeScript 설정
│   └── .env.local               # 환경 변수 (생성 필요)
│
├── 🐍 Crawler (Python)
│   ├── crawler_vision.py         # 이미지 기반 크롤러 ⭐
│   ├── crawler.py                # 텍스트 기반 크롤러
│   ├── test_crawler.py           # 환경 테스트
│   ├── requirements.txt          # Python 의존성
│   ├── env_template.txt          # 환경 변수 템플릿
│   ├── README_VISION.md          # 크롤러 가이드
│   └── .env                     # 환경 변수 (생성 필요)
│
├── 🗄️ Database (Supabase)
│   ├── supabase_schema.sql       # DB 스키마 ⭐
│   ├── supabase_sample_data.sql  # 샘플 데이터
│   └── DATABASE_SETUP.md         # DB 설정 가이드
│
└── 📖 Documentation
    ├── README.md                 # 이 파일 ⭐
    ├── QUICKSTART.md             # 빠른 시작 가이드
    ├── ENV_SETUP_GUIDE.md        # 환경 변수 가이드
    ├── DEPLOYMENT.md             # Vercel 배포 가이드
    └── FRONTEND_SETUP.md         # 프론트엔드 가이드
```

---

## 🌐 Vercel 배포

### 배포 전 체크리스트

- [ ] Supabase 데이터베이스 설정 완료
- [ ] 로컬에서 정상 작동 확인
- [ ] GitHub 저장소 생성
- [ ] 환경 변수 준비

### 방법 1: Vercel Dashboard (가장 쉬움)

1. **Vercel 가입**
   - https://vercel.com 접속
   - GitHub 계정으로 로그인

2. **프로젝트 Import**
   - **New Project** 클릭
   - GitHub 저장소 선택
   - **Import** 클릭

3. **환경 변수 설정**
   - **Environment Variables** 섹션:
   
   ```
   Name: NEXT_PUBLIC_SUPABASE_URL
   Value: https://xxxxxxxxxxxxx.supabase.co
   
   Name: NEXT_PUBLIC_SUPABASE_ANON_KEY
   Value: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```
   
   - Environment: Production, Preview, Development 모두 체크

4. **Deploy**
   - **Deploy** 버튼 클릭
   - 1~2분 대기
   - 배포 완료! 🎉

### 방법 2: Vercel CLI

```bash
# CLI 설치
npm i -g vercel

# 로그인
vercel login

# 배포
vercel

# 환경 변수 설정
vercel env add NEXT_PUBLIC_SUPABASE_URL
vercel env add NEXT_PUBLIC_SUPABASE_ANON_KEY

# 프로덕션 배포
vercel --prod
```

### 배포 후 확인

1. 생성된 URL 접속 (예: `https://scholarship-radar.vercel.app`)
2. 장학금 데이터 로딩 확인
3. 검색 기능 테스트
4. 모바일 반응형 확인

📖 **상세 가이드:** [DEPLOYMENT.md](./DEPLOYMENT.md)

---

## 🔑 환경 변수 정리

### Frontend (.env.local)

| 변수명 | 설명 | 출처 |
|--------|------|------|
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase 프로젝트 URL | Dashboard → API → Project URL |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Supabase 공개 키 | Dashboard → API → anon public |

⚠️ `NEXT_PUBLIC_` 접두사 필수!

### Crawler (crawler/.env)

| 변수명 | 설명 | 출처 |
|--------|------|------|
| `SUPABASE_URL` | Supabase 프로젝트 URL | Dashboard → API → Project URL |
| `SUPABASE_KEY` | Supabase 서비스 키 | Dashboard → API → service_role ⚠️ |
| `OPENAI_API_KEY` | OpenAI API 키 | platform.openai.com/api-keys |
| `TARGET_URL` | 크롤링 대상 URL | 장학금 게시판 URL |

⚠️ **service_role** key 사용 (anon 아님!)

📖 **상세 가이드:** [ENV_SETUP_GUIDE.md](./ENV_SETUP_GUIDE.md)

---

## 💰 비용 안내

### Supabase (무료 플랜)

- ✅ 500MB 데이터베이스
- ✅ 2GB 데이터 전송/월
- ✅ 50,000 월간 활성 사용자

**장학금 1,000개 기준:** 무료 ✅

### OpenAI API

#### GPT-4o Vision (이미지 분석)
- Input: $2.50 / 1M tokens
- Output: $10.00 / 1M tokens
- **공고 1개:** ~$0.002 (약 2원)
- **100개:** ~$0.20 (약 260원)

#### GPT-4o-mini (텍스트 분석)
- Input: $0.15 / 1M tokens
- Output: $0.60 / 1M tokens
- **공고 1개:** ~$0.0001 (약 0.1원)
- **100개:** ~$0.01 (약 13원)

### Vercel (무료 플랜)

- ✅ 무제한 배포
- ✅ 자동 SSL
- ✅ 100GB 대역폭/월

**일반적인 사용:** 무료 ✅

---

## 🐛 문제 해결

### Frontend 오류

#### "supabaseUrl and supabaseAnonKey are required"

**원인:** 환경 변수 미설정

**해결:**
1. `.env.local` 파일이 프로젝트 루트에 있는지 확인
2. `NEXT_PUBLIC_` 접두사 확인
3. 개발 서버 재시작 (Ctrl+C 후 `npm run dev`)

#### 빌드 오류

```bash
# 캐시 삭제
rm -rf .next node_modules package-lock.json

# 재설치
npm install
npm run dev
```

### Crawler 오류

#### "ImportError: No module named 'xxx'"

```bash
pip install -r requirements.txt
```

#### "Invalid API key" (OpenAI)

1. API 키 재확인
2. 잔액 확인: https://platform.openai.com/usage
3. GPT-4o 접근 권한 확인

#### Supabase 연결 실패

1. `service_role` key 사용 여부 확인 (anon 아님!)
2. URL 정확성 확인
3. 네트워크 방화벽 확인

### Vercel 배포 오류

#### 환경 변수 오류

1. Vercel Dashboard → Settings → Environment Variables
2. 변수명 재확인
3. **Redeploy** 실행

---

## 📊 데이터베이스 스키마

### scholarships 테이블

| 컬럼 | 타입 | 설명 | 기본값 |
|------|------|------|--------|
| `id` | bigint | 고유 ID (자동 증가) | Auto |
| `title` | text | 장학금 제목 | - |
| `link` | text | 공고 원문 링크 (Unique) | - |
| `due_date` | date | 신청 마감일 | - |
| `min_gpa` | float | 최소 요구 학점 | 0.0 |
| `max_income` | integer | 소득분위 상한선 (0-10, 99=제한없음) | 99 |
| `residence` | text | 거주지 제한 | '전국' |
| `created_at` | timestamptz | 생성 시각 | NOW() |

### 필터링 로직

```sql
SELECT * FROM scholarships
WHERE due_date >= CURRENT_DATE                    -- 마감 전
  AND min_gpa <= 3.5                             -- 사용자 학점
  AND (max_income >= 4 OR max_income = 99)       -- 사용자 소득분위
  AND (residence = '서울' OR residence = '전국')  -- 사용자 거주지
ORDER BY due_date ASC;
```

---

## 🔧 커스터마이징

### 거주지 옵션 변경

`app/page.tsx` 파일:

```typescript
const RESIDENCE_OPTIONS = [
  { value: '제주', label: '제주' },
  // 추가...
];
```

### 크롤링 사이트 변경

`crawler/crawler_vision.py` 파일:

```python
# 26번째 줄
BASE_DOMAIN = "https://your-school.ac.kr"
TARGET_URL = "https://your-school.ac.kr/board/scholarship"

# 84번째 줄 (본문 클래스)
content_div = soup.find('div', class_='your-content-class')
```

### 색상 테마 변경

`tailwind.config.ts` 파일:

```typescript
colors: {
  primary: {
    500: '#0ea5e9',  // 메인 색상 변경
  }
}
```

---

## 📈 향후 개발 계획

- [ ] 사용자 인증 및 회원 기능
- [ ] 즐겨찾기 기능
- [ ] 마감 임박 알림 (이메일/푸시)
- [ ] 검색 히스토리
- [ ] 다크 모드
- [ ] 관리자 대시보드
- [ ] GitHub Actions 자동 크롤링
- [ ] 더 많은 장학금 사이트 지원
- [ ] 장학금 추천 알고리즘 (ML)

---

## 🤝 기여

이슈와 PR은 언제나 환영합니다!

### 기여 방법

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 라이선스

MIT License - 자유롭게 사용하세요!

---

## 🙏 감사

이 프로젝트는 다음 오픈소스 프로젝트들 덕분에 가능했습니다:

- [Next.js](https://nextjs.org/) - React 프레임워크
- [Supabase](https://supabase.com/) - 백엔드 서비스
- [Tailwind CSS](https://tailwindcss.com/) - CSS 프레임워크
- [OpenAI](https://openai.com/) - AI API
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - HTML 파싱
- [Vercel](https://vercel.com/) - 배포 플랫폼

---

## 📞 문의 및 지원

- 🐛 **버그 리포트:** [GitHub Issues](https://github.com/your-repo/issues)
- 💡 **기능 제안:** [GitHub Discussions](https://github.com/your-repo/discussions)
- 📧 **이메일:** your-email@example.com

---

## 🌟 스타 히스토리

도움이 되셨다면 ⭐ 를 눌러주세요!

[![Star History Chart](https://api.star-history.com/svg?repos=your-username/scholarship-radar&type=Date)](https://star-history.com/#your-username/scholarship-radar&Date)

---

**Made with ❤️ by [Your Name]**

🎓 대학생들의 장학금 탐색이 더 쉬워지기를!
