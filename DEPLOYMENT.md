# 🚀 Vercel 배포 가이드

---

## 📋 배포 전 체크리스트

- [ ] Supabase 데이터베이스 설정 완료
- [ ] 로컬에서 정상 작동 확인 (`npm run dev`)
- [ ] 환경 변수 준비
- [ ] GitHub 저장소 생성 (선택사항)

---

## 🔑 환경 변수 설정

### 1. `.env.local` 파일 (로컬 개발용)

프로젝트 루트 디렉토리에 `.env.local` 파일 생성:

```env
# Supabase 설정
NEXT_PUBLIC_SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 2. Supabase API 키 찾는 방법

#### Step 1: Supabase Dashboard 접속
1. https://app.supabase.com 접속
2. 프로젝트 선택

#### Step 2: API 설정 확인
1. 왼쪽 메뉴에서 **Settings** (⚙️) 클릭
2. **API** 메뉴 클릭

#### Step 3: 값 복사
```
┌─────────────────────────────────────────────┐
│ Project URL                                  │
│ https://xxxxxxxxxxxxx.supabase.co           │
│ ↓ 이 값을 복사                               │
│ NEXT_PUBLIC_SUPABASE_URL                    │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ API Keys                                     │
│ anon public                                  │
│ eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...     │
│ ↓ 이 값을 복사 (NOT service_role)           │
│ NEXT_PUBLIC_SUPABASE_ANON_KEY               │
└─────────────────────────────────────────────┘
```

⚠️ **중요:**
- Frontend는 **anon public** key 사용
- Python 크롤러는 **service_role** key 사용
- 두 개는 다릅니다!

---

## 🌐 Vercel 배포 방법

### 방법 1: Vercel Dashboard (추천)

#### Step 1: Vercel 계정 생성
1. https://vercel.com 접속
2. **Sign Up** (GitHub 계정 연동 추천)

#### Step 2: GitHub 저장소 연결
1. GitHub에 프로젝트 푸시:
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/your-username/scholarship-radar.git
git push -u origin main
```

2. Vercel Dashboard에서 **New Project** 클릭
3. GitHub 저장소 선택 (`scholarship-radar`)
4. **Import** 클릭

#### Step 3: 환경 변수 설정
1. **Environment Variables** 섹션에서 추가:

```
Name: NEXT_PUBLIC_SUPABASE_URL
Value: https://xxxxxxxxxxxxx.supabase.co
```

```
Name: NEXT_PUBLIC_SUPABASE_ANON_KEY
Value: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

2. **Environment** 선택:
   - ✅ Production
   - ✅ Preview
   - ✅ Development

#### Step 4: 배포
1. **Deploy** 버튼 클릭
2. 배포 진행 (약 1~2분)
3. 완료 후 생성된 URL 확인 (`https://your-project.vercel.app`)

---

### 방법 2: Vercel CLI

#### Step 1: Vercel CLI 설치

```bash
npm install -g vercel
```

#### Step 2: 로그인

```bash
vercel login
```

#### Step 3: 배포

```bash
# 프로젝트 루트에서 실행
vercel

# 프롬프트 응답:
# Set up and deploy? Yes
# Which scope? (본인 계정 선택)
# Link to existing project? No
# Project name? scholarship-radar
# In which directory? ./
# Auto-detected settings? Yes
```

#### Step 4: 환경 변수 설정

```bash
# Supabase URL 추가
vercel env add NEXT_PUBLIC_SUPABASE_URL

# 프롬프트에서 값 입력: https://xxxxxxxxxxxxx.supabase.co
# 환경 선택: Production, Preview, Development 모두 체크

# Supabase Key 추가
vercel env add NEXT_PUBLIC_SUPABASE_ANON_KEY

# 프롬프트에서 값 입력: eyJhbGciOiJIUzI1NiI...
# 환경 선택: Production, Preview, Development 모두 체크
```

#### Step 5: 프로덕션 배포

```bash
vercel --prod
```

---

## 🔄 재배포 (코드 업데이트 후)

### GitHub 연동 시 (자동 배포)
```bash
git add .
git commit -m "Update feature"
git push
# → Vercel이 자동으로 감지하여 배포
```

### CLI 사용 시
```bash
vercel --prod
```

---

## ✅ 배포 후 확인사항

### 1. 사이트 접속 확인
- 배포된 URL 접속 (예: https://scholarship-radar.vercel.app)
- 페이지가 정상적으로 로드되는지 확인

### 2. Supabase 연결 확인
- 브라우저 개발자 도구 (F12) 열기
- Console 탭에서 에러 확인
- 장학금 데이터가 로드되는지 확인

### 3. 검색 기능 테스트
- 학점, 소득분위, 거주지 입력
- 검색 버튼 클릭
- 결과가 정상적으로 표시되는지 확인

---

## 🐛 배포 문제 해결

### 1. "Module not found" 오류

**원인:** 의존성 설치 실패

**해결:**
```bash
# package-lock.json 확인
# package.json의 dependencies 확인
npm install
git add package-lock.json
git commit -m "Fix dependencies"
git push
```

### 2. 환경 변수 오류

**증상:**
```
Error: supabaseUrl and supabaseAnonKey are required
```

**해결:**
1. Vercel Dashboard → 프로젝트 선택
2. Settings → Environment Variables
3. 환경 변수 확인 및 재설정
4. **Redeploy** 클릭 (Deployments 탭에서)

### 3. Supabase CORS 오류

**증상:**
```
Access to fetch at 'https://xxx.supabase.co' has been blocked by CORS policy
```

**해결:**
1. Supabase Dashboard → Authentication → URL Configuration
2. **Site URL** 추가: `https://your-project.vercel.app`
3. **Redirect URLs** 추가: `https://your-project.vercel.app/**`

### 4. 빌드 실패

**증상:**
```
Error: Build failed
```

**해결:**
```bash
# 로컬에서 빌드 테스트
npm run build

# 에러 확인 및 수정 후
git push
```

---

## 🔒 보안 설정

### 1. Environment Variables 보호
- ✅ `.env.local` 파일은 절대 GitHub에 푸시하지 않기
- ✅ `.gitignore`에 `.env*` 포함되어 있는지 확인
- ✅ `NEXT_PUBLIC_` 접두사는 클라이언트에 노출됨 (괜찮음)

### 2. Supabase Row Level Security (RLS)
- ✅ `scholarships` 테이블에 RLS 활성화됨
- ✅ 읽기는 public, 쓰기는 인증된 사용자만

### 3. API Rate Limiting
- Supabase 무료 플랜: 500MB 데이터베이스, 2GB 전송
- 필요시 유료 플랜 고려

---

## 📊 성능 모니터링

### Vercel Analytics (무료)
1. Vercel Dashboard → 프로젝트 선택
2. **Analytics** 탭
3. 페이지 로딩 속도, 방문자 수 확인

### Vercel Speed Insights
1. Vercel Dashboard → Settings → Speed Insights
2. Enable
3. 실시간 성능 모니터링

---

## 🌍 커스텀 도메인 연결 (선택사항)

### 도메인이 있는 경우

1. Vercel Dashboard → 프로젝트 선택
2. **Settings** → **Domains**
3. **Add** 클릭
4. 도메인 입력 (예: `scholarshipradar.com`)
5. DNS 설정 안내에 따라 도메인 제공업체에서 설정:

```
Type: A
Name: @
Value: 76.76.21.21

Type: CNAME
Name: www
Value: cname.vercel-dns.com
```

6. DNS 전파 대기 (최대 48시간, 보통 몇 분)

---

## 📈 배포 후 할 일

### 1. 크롤러 자동화
- GitHub Actions로 매일 자동 크롤링
- 또는 로컬 서버에서 cron job 설정

### 2. 모니터링 설정
- Vercel Analytics 활성화
- Supabase 사용량 모니터링

### 3. SEO 최적화
- `app/layout.tsx`의 metadata 수정
- sitemap.xml 생성
- robots.txt 추가

### 4. 사용자 피드백 수집
- Google Analytics 연동
- 피드백 폼 추가

---

## 🎉 배포 완료!

축하합니다! 장학금 레이더가 성공적으로 배포되었습니다!

**배포 URL 공유하기:**
- 친구들에게 공유
- 학교 커뮤니티에 소개
- SNS에 홍보

**지속적인 개선:**
- 사용자 피드백 수집
- 새로운 기능 추가
- 성능 최적화

---

## 📞 추가 지원

- **Vercel 문서:** https://vercel.com/docs
- **Supabase 문서:** https://supabase.com/docs
- **Next.js 문서:** https://nextjs.org/docs

문제가 발생하면 GitHub Issues에 등록해주세요!

