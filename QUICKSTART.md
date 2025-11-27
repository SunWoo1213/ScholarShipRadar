# ⚡ 5분 만에 시작하기

완전 초보자를 위한 단계별 가이드입니다. 차근차근 따라하세요!

---

## ✅ 준비물

- [ ] 컴퓨터 (Windows, Mac, Linux)
- [ ] 인터넷 연결
- [ ] 이메일 계정 (Supabase 가입용)

---

## 📋 단계 요약

```
1. Supabase 가입 및 DB 설정 (2분)
2. 프로젝트 설정 (3분)
3. 실행! 🚀
```

---

## 🗄️ Step 1: Supabase 데이터베이스 설정 (2분)

### 1.1 Supabase 가입

1. https://supabase.com 접속
2. **Start your project** 클릭
3. **Sign up** (GitHub 계정으로 가입 권장)
4. 이메일 인증

### 1.2 프로젝트 생성

1. **New Project** 클릭
2. 정보 입력:
   ```
   Name: scholarship-radar
   Database Password: (강력한 비밀번호 입력)
   Region: Northeast Asia (Seoul) 선택
   Pricing Plan: Free (무료)
   ```
3. **Create new project** 클릭
4. 프로젝트 생성 대기 (약 1~2분) ⏳

### 1.3 데이터베이스 스키마 생성

1. 왼쪽 메뉴에서 **SQL Editor** 클릭 (아이콘: `</>`)
2. **New query** 클릭
3. 프로젝트의 `supabase_schema.sql` 파일 열기
4. 전체 내용 복사 (Ctrl+A → Ctrl+C)
5. SQL Editor에 붙여넣기 (Ctrl+V)
6. 오른쪽 아래 **Run** 버튼 클릭 ▶️
7. 성공 메시지 확인: `Success. No rows returned`

### 1.4 (선택) 테스트 데이터 추가

1. SQL Editor에서 **New query**
2. `supabase_sample_data.sql` 파일 내용 복사 & 붙여넣기
3. **Run** 클릭
4. 이제 10개의 샘플 장학금이 추가되었습니다!

### 1.5 API 키 확인

1. 왼쪽 메뉴 **Settings** ⚙️ 클릭
2. **API** 클릭
3. 다음 화면을 유지 (나중에 사용)

```
┌────────────────────────────────────────┐
│ Project URL                            │
│ https://xxxxx.supabase.co             │  ← 잠시 후 복사
└────────────────────────────────────────┘

┌────────────────────────────────────────┐
│ anon public key                        │
│ eyJhbGci...                            │  ← 잠시 후 복사
└────────────────────────────────────────┘
```

---

## 💻 Step 2: 프로젝트 설정 (3분)

### 2.1 Node.js 설치 확인

터미널(명령 프롬프트) 열기:
- **Windows:** `Win + R` → `cmd` 입력 → Enter
- **Mac:** `Cmd + Space` → `terminal` 입력

```bash
node --version
npm --version
```

✅ 버전 번호가 나오면 OK!  
❌ 명령어를 찾을 수 없다면 → [Node.js 설치](https://nodejs.org/) (LTS 버전)

### 2.2 프로젝트 폴더로 이동

```bash
# Windows 예시
cd "c:\Scholarship Radar"

# Mac/Linux 예시
cd ~/scholarship-radar
```

### 2.3 의존성 설치

```bash
npm install
```

⏳ 잠시 대기 (약 1~2분)

### 2.4 환경 변수 설정

**Windows:**
```cmd
copy env_example.txt .env.local
notepad .env.local
```

**Mac/Linux:**
```bash
cp env_example.txt .env.local
nano .env.local
# 또는
open .env.local
```

`.env.local` 파일에 다음 내용 입력:

```env
NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGci...
```

**어디서 복사하나요?**
1. Supabase 브라우저 창으로 돌아가기
2. Settings → API 페이지
3. **Project URL** 복사 → `NEXT_PUBLIC_SUPABASE_URL=` 뒤에 붙여넣기
4. **anon public** 키 복사 → `NEXT_PUBLIC_SUPABASE_ANON_KEY=` 뒤에 붙여넣기
5. 파일 저장 (Ctrl+S)

---

## 🚀 Step 3: 실행!

### 3.1 개발 서버 시작

```bash
npm run dev
```

다음과 같은 메시지가 나오면 성공! 🎉

```
  ▲ Next.js 14.2.15
  - Local:        http://localhost:3000
  - Environments: .env.local

 ✓ Ready in 2.3s
```

### 3.2 브라우저에서 확인

1. 브라우저 열기
2. 주소창에 `http://localhost:3000` 입력
3. Enter!

### 3.3 테스트해보기

1. **검색 필터** 입력:
   - 학점: `3.5`
   - 소득분위: `8분위`
   - 거주지: `서울`

2. **장학금 찾기** 버튼 클릭

3. 결과 확인! ✨

---

## 🎉 완료!

축하합니다! 장학금 레이더가 실행되고 있습니다!

### 다음 단계:

#### 실제 장학금 데이터 수집하기
[Python 크롤러 설정](./crawler/README.md)

#### 배포하기
[Vercel 배포 가이드](./DEPLOYMENT.md)

#### 문제가 생겼나요?
[문제 해결 가이드](#-문제-해결)

---

## 🐛 문제 해결

### "npm: command not found"

**문제:** Node.js가 설치되지 않았습니다.

**해결:**
1. https://nodejs.org 접속
2. LTS 버전 다운로드 및 설치
3. 터미널 재시작
4. `node --version` 확인

### "Port 3000 is already in use"

**문제:** 3000 포트가 이미 사용 중입니다.

**해결:**
```bash
# 다른 포트로 실행
PORT=3001 npm run dev
```

### 장학금 데이터가 안 보여요

**문제:** Supabase 연결 오류

**해결 체크리스트:**
1. `.env.local` 파일이 프로젝트 루트에 있나요?
2. 파일명이 정확히 `.env.local`인가요?
3. `NEXT_PUBLIC_` 접두사가 있나요?
4. Supabase Project URL이 정확한가요?
5. `anon public` key를 사용했나요? (service_role 아님!)

**확인 방법:**
1. 브라우저에서 F12 눌러 개발자 도구 열기
2. **Console** 탭 확인
3. 빨간색 에러 메시지 확인

### 샘플 데이터가 없어요

**문제:** 데이터베이스가 비어있습니다.

**해결:**
1. Supabase Dashboard → SQL Editor
2. `supabase_sample_data.sql` 실행
3. 또는 Python 크롤러로 실제 데이터 수집

### 페이지가 안 열려요

**문제:** 여러 원인 가능

**해결:**
```bash
# 캐시 삭제
rm -rf .next node_modules  # Mac/Linux
# rmdir /s .next node_modules  # Windows

# 재설치
npm install

# 재실행
npm run dev
```

---

## 💡 유용한 명령어

```bash
# 개발 서버 실행
npm run dev

# 개발 서버 중지
Ctrl + C

# 프로덕션 빌드
npm run build

# 프로덕션 실행
npm start

# 린트 체크
npm run lint
```

---

## 📚 더 알아보기

- [환경 변수 완벽 가이드](./ENV_SETUP_GUIDE.md)
- [프론트엔드 설정 가이드](./FRONTEND_SETUP.md)
- [데이터베이스 설정 가이드](./DATABASE_SETUP.md)
- [크롤러 사용법](./crawler/README.md)
- [Vercel 배포 가이드](./DEPLOYMENT.md)

---

## 🆘 도움이 필요하신가요?

- 💬 GitHub Issues에 질문 올리기
- 📧 이메일 문의
- 💡 [자주 묻는 질문](./README.md#-문제-해결)

---

즐거운 개발 되세요! 🎓✨

