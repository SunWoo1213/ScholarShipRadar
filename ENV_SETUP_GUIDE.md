# 🔑 환경 변수 설정 완벽 가이드

이 프로젝트는 **두 개의 서로 다른 환경 변수 파일**이 필요합니다.

---

## 📋 환경 변수 파일 요약

| 파일 | 위치 | 용도 | API Key 종류 |
|------|------|------|--------------|
| `.env.local` | 프로젝트 루트 | Next.js Frontend | `anon public` key |
| `.env` | `crawler/` 폴더 | Python Crawler | `service_role` key |

⚠️ **중요:** 두 파일은 서로 다른 Supabase 키를 사용합니다!

---

## 🎨 Frontend 환경 변수 설정

### 파일 위치
```
c:\Scholarship Radar\
└── .env.local  ← 여기에 생성
```

### 설정 방법

**Step 1: 파일 생성**
```bash
# 프로젝트 루트 디렉토리에서
copy env_example.txt .env.local    # Windows
# cp env_example.txt .env.local    # Mac/Linux
```

**Step 2: Supabase Dashboard에서 API 키 가져오기**

1. https://app.supabase.com 접속
2. 프로젝트 선택
3. **Settings** ⚙️ → **API** 클릭

**Step 3: 필요한 값 복사**

```
┌─────────────────────────────────────────┐
│ Configuration                           │
│                                         │
│ Project URL                             │
│ https://abcdefghijk.supabase.co        │  ← 복사
└─────────────────────────────────────────┘
```

```
┌─────────────────────────────────────────┐
│ Project API keys                        │
│                                         │
│ anon                                    │
│ public                                  │
│ eyJhbGciOiJIUzI1NiIsInR5cCI6IkpX...    │  ← 복사
│                                         │
│ This key is safe to use in a browser   │  ← 확인!
└─────────────────────────────────────────┘
```

**Step 4: `.env.local` 파일 편집**

메모장 또는 VS Code로 열어서:

```env
NEXT_PUBLIC_SUPABASE_URL=https://abcdefghijk.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoaWprIiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTUyNzY4NjgsImV4cCI6MjAxMDg1Mjg2OH0.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

✅ **체크리스트:**
- [ ] `NEXT_PUBLIC_` 접두사 있음
- [ ] `anon public` key 사용 (NOT service_role)
- [ ] 따옴표 없이 값만 입력
- [ ] 파일명이 `.env.local`임

---

## 🐍 Crawler 환경 변수 설정

### 파일 위치
```
c:\Scholarship Radar\
└── crawler\
    └── .env  ← 여기에 생성
```

### 설정 방법

**Step 1: 파일 생성**
```bash
cd crawler
copy env_template.txt .env    # Windows
# cp env_template.txt .env    # Mac/Linux
```

**Step 2: Supabase service_role 키 가져오기**

⚠️ **주의:** 이번에는 `service_role` key가 필요합니다!

1. https://app.supabase.com 접속
2. 프로젝트 선택
3. **Settings** ⚙️ → **API** 클릭
4. 아래로 스크롤

```
┌─────────────────────────────────────────┐
│ Project API keys                        │
│                                         │
│ service_role                            │
│ secret                                  │
│ eyJhbGciOiJIUzI1NiIsInR5cCI6IkpX...    │  ← 복사
│                                         │
│ ⚠️ This key has the ability to bypass  │
│ Row Level Security. Never share it     │
│ publicly.                               │
└─────────────────────────────────────────┘
```

**Step 3: OpenAI API 키 가져오기**

1. https://platform.openai.com/api-keys 접속
2. 로그인
3. **Create new secret key** 클릭
4. 이름 입력 (예: "Scholarship Crawler")
5. 생성된 키 복사 (⚠️ 한 번만 표시됨!)

```
┌─────────────────────────────────────────┐
│ API key created                         │
│                                         │
│ sk-proj-xxxxxxxxxxxxxxxxxxxxxxxx        │  ← 복사
│                                         │
│ Please save this secret key somewhere  │
│ safe and accessible. For security      │
│ reasons, you won't be able to view it  │
│ again through your OpenAI account.     │
└─────────────────────────────────────────┘
```

**Step 4: `crawler/.env` 파일 편집**

```env
# Supabase 설정 (service_role key!)
SUPABASE_URL=https://abcdefghijk.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoaWprIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY5NTI3Njg2OCwiZXhwIjoyMDEwODUyODY4fQ.yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy

# OpenAI API 설정
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# 크롤링 대상 URL (실제 장학금 게시판 URL로 변경 필요!)
TARGET_URL=https://your-scholarship-board.com/notices

# 선택사항 (기본값 사용 가능)
MAX_PAGES=10
DELAY_SECONDS=2
```

✅ **체크리스트:**
- [ ] `service_role` key 사용 (NOT anon)
- [ ] OpenAI API key는 `sk-proj-` 또는 `sk-`로 시작
- [ ] `TARGET_URL`을 실제 크롤링할 사이트로 변경
- [ ] 파일 위치가 `crawler/.env`임

---

## 🔐 보안 주의사항

### ✅ 안전한 키 (Public)
```
NEXT_PUBLIC_SUPABASE_URL
NEXT_PUBLIC_SUPABASE_ANON_KEY
```
- 브라우저에 노출되어도 안전
- GitHub에 올려도 괜찮음 (권장하진 않음)
- Supabase RLS로 보호됨

### ⚠️ 위험한 키 (Secret)
```
SUPABASE_KEY (service_role)
OPENAI_API_KEY
```
- **절대로** GitHub에 올리면 안 됨!
- **절대로** 클라이언트 코드에 사용 금지!
- `.gitignore`에 반드시 포함

### .gitignore 확인

프로젝트 루트의 `.gitignore` 파일에 다음이 포함되어 있는지 확인:

```gitignore
# 환경 변수
.env
.env*.local

# Python
crawler/.env
crawler/venv/
```

---

## 🧪 환경 변수 테스트

### Frontend 테스트
```bash
# 프로젝트 루트에서
npm run dev

# 브라우저에서 http://localhost:3000 접속
# F12 (개발자 도구) → Console 탭
# 에러 없이 장학금 데이터가 로드되면 성공!
```

### Crawler 테스트
```bash
cd crawler
python test_crawler.py

# 출력 예시:
# ✅ 환경 변수: 설정됨
# ✅ Supabase: 연결 성공
# ✅ OpenAI API: 연결 성공
# ✅ 크롤링 URL: 접근 성공
```

---

## 🐛 문제 해결

### "supabaseUrl and supabaseAnonKey are required"

**원인:** `.env.local` 파일이 없거나 잘못된 위치

**해결:**
1. 파일이 프로젝트 **루트**에 있는지 확인
2. 파일명이 정확히 `.env.local`인지 확인
3. 개발 서버 재시작 (Ctrl+C 후 `npm run dev`)

### "Invalid API key" (OpenAI)

**원인:** OpenAI API 키 오류

**해결:**
1. API 키가 `sk-proj-` 또는 `sk-`로 시작하는지 확인
2. 키를 다시 복사 (공백 없이)
3. OpenAI 잔액 확인: https://platform.openai.com/usage

### "Row Level Security policy violation"

**원인:** 잘못된 Supabase 키 사용

**해결:**
- Frontend: `anon public` key 사용
- Crawler: `service_role` key 사용
- 두 키를 혼동하지 않았는지 확인

### 크롤러 Supabase 연결 실패

**원인:** `service_role` key 대신 `anon` key 사용

**해결:**
```bash
# crawler/.env 파일 확인
# SUPABASE_KEY가 service_role key인지 확인
# (매우 긴 토큰, anon key와 다름)
```

---

## 📋 환경 변수 요약표

### Frontend (.env.local)
| 변수명 | 예시 | 출처 |
|--------|------|------|
| `NEXT_PUBLIC_SUPABASE_URL` | `https://xxx.supabase.co` | Supabase Dashboard → API → Project URL |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | `eyJhbG...` | Supabase Dashboard → API → anon public |

### Crawler (crawler/.env)
| 변수명 | 예시 | 출처 |
|--------|------|------|
| `SUPABASE_URL` | `https://xxx.supabase.co` | Supabase Dashboard → API → Project URL |
| `SUPABASE_KEY` | `eyJhbG...` | Supabase Dashboard → API → service_role secret |
| `OPENAI_API_KEY` | `sk-proj-xxx` | OpenAI Platform → API Keys |
| `TARGET_URL` | `https://board.com` | 크롤링할 사이트 URL |

---

## 🚀 Vercel 배포 시 환경 변수

Vercel Dashboard에서 설정:

```
Name: NEXT_PUBLIC_SUPABASE_URL
Value: https://xxx.supabase.co
Environment: Production, Preview, Development

Name: NEXT_PUBLIC_SUPABASE_ANON_KEY
Value: eyJhbGci...
Environment: Production, Preview, Development
```

⚠️ Vercel에는 **anon public key만** 설정!

---

모든 설정이 완료되었나요? 🎉

- ✅ `.env.local` (프로젝트 루트)
- ✅ `crawler/.env` (crawler 폴더)
- ✅ 테스트 성공

이제 프로젝트를 실행할 준비가 되었습니다!

