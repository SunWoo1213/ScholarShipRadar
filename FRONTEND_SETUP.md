# 🎨 Next.js 프론트엔드 설정 가이드

---

## 📦 설치 단계

### 1. Node.js 버전 확인

```bash
node --version  # v18.0.0 이상 권장
npm --version
```

Node.js가 없다면:
- [Node.js 공식 사이트](https://nodejs.org/)에서 LTS 버전 설치

### 2. 의존성 설치

```bash
# 프로젝트 루트 디렉토리에서
npm install

# 또는 yarn 사용
yarn install
```

설치되는 주요 패키지:
- `next@14.2.15` - Next.js 프레임워크
- `react@18.3.1` - React 라이브러리
- `@supabase/supabase-js@2.45.4` - Supabase 클라이언트
- `tailwindcss@3.4.14` - CSS 프레임워크
- `typescript@5` - TypeScript

### 3. 환경 변수 설정

#### 3.1 `.env.local` 파일 생성

```bash
# Windows
copy env_example.txt .env.local

# Mac/Linux
cp env_example.txt .env.local
```

#### 3.2 Supabase API 키 설정

`.env.local` 파일을 열어 실제 값으로 수정:

```env
NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxxxx
```

**API 키 가져오기:**

1. [Supabase Dashboard](https://app.supabase.com/) 접속
2. 프로젝트 선택
3. **Settings** → **API** 메뉴
4. 다음 값 복사:
   - **Project URL** → `NEXT_PUBLIC_SUPABASE_URL`
   - **anon public key** → `NEXT_PUBLIC_SUPABASE_ANON_KEY`

⚠️ **주의:**
- Frontend는 `anon` (public) key 사용
- Backend/Crawler는 `service_role` key 사용
- `NEXT_PUBLIC_` 접두사 필수!

### 4. 개발 서버 실행

```bash
npm run dev

# 또는
yarn dev
```

브라우저에서 자동으로 열리거나 수동으로 접속:
- [http://localhost:3000](http://localhost:3000)

---

## 🎨 UI 컴포넌트 구조

### 메인 페이지 (`app/page.tsx`)

```
┌─────────────────────────────────────┐
│          Header (헤더)               │
│     "장학금 레이더" 🎓              │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│      검색 필터 섹션                  │
│  ┌───────────┬───────────┬────────┐│
│  │  학점     │ 소득분위   │ 거주지 ││
│  │  Input    │  Select   │ Select ││
│  └───────────┴───────────┴────────┘│
│         [장학금 찾기 버튼]          │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│      장학금 카드 리스트              │
│  ┌────────────┐  ┌────────────┐   │
│  │ 장학금 1   │  │ 장학금 2   │   │
│  │ D-day      │  │ D-day      │   │
│  │ [보기]     │  │ [보기]     │   │
│  └────────────┘  └────────────┘   │
└─────────────────────────────────────┘
```

### 주요 컴포넌트

#### 1. **검색 필터 섹션**
- 학점 입력 (0.0 ~ 4.5)
- 소득분위 선택 (1~10분위)
- 거주지 선택 (서울, 경기, 인천 등)
- 검색 버튼

#### 2. **장학금 카드 (`ScholarshipCard`)**
- D-day 배지 (긴급/일반/마감)
- 장학금 제목
- 마감일
- 거주지 정보
- 조건 태그 (학점, 소득분위)
- 상세보기 버튼

#### 3. **로딩 스켈레톤 (`LoadingSkeleton`)**
- 데이터 로딩 중 표시
- 부드러운 애니메이션

#### 4. **Empty State**
- 검색 결과 없을 때
- 안내 메시지 및 초기화 버튼

---

## 🎯 주요 기능 설명

### 1. 필터링 로직

#### 학점 필터
```typescript
// 사용자 학점이 최소 요구 학점 이상인 장학금만
query.lte('min_gpa', gpaNum)
```

#### 소득분위 필터
```typescript
// 사용자 소득분위 이하 OR 제한 없음(99)
query.or(`max_income.gte.${incomeNum},max_income.eq.99`)
```

#### 거주지 필터
```typescript
// 사용자 거주지 일치 OR 전국
query.or(`residence.eq.${residence},residence.eq.전국`)
```

### 2. D-day 계산

```typescript
function calculateDday(dueDate: string): string {
  const today = new Date();
  const due = new Date(dueDate);
  const diffDays = Math.ceil((due - today) / (1000 * 60 * 60 * 24));
  
  if (diffDays < 0) return '마감';
  if (diffDays === 0) return 'D-day';
  return `D-${diffDays}`;
}
```

### 3. 실시간 검색

- Enter 키 지원
- 로딩 상태 표시
- 에러 핸들링

---

## 🎨 스타일 커스터마이징

### Tailwind CSS 색상 변경

`tailwind.config.ts` 파일 수정:

```typescript
theme: {
  extend: {
    colors: {
      primary: {
        500: '#0ea5e9',  // 메인 블루 색상
        600: '#0284c7',  // 어두운 블루
        // ... 원하는 색상으로 변경
      }
    }
  }
}
```

### 전역 스타일 변경

`app/globals.css` 파일 수정:

```css
body {
  @apply bg-gradient-to-br from-blue-50 via-white to-indigo-50;
  /* 배경 그라데이션 변경 */
}
```

### 애니메이션 추가

```typescript
// tailwind.config.ts
animation: {
  'bounce-slow': 'bounce 3s infinite',
  'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
}
```

---

## 📱 반응형 디자인

### Breakpoints (Tailwind 기본)

- **sm:** 640px 이상 (모바일 가로)
- **md:** 768px 이상 (태블릿)
- **lg:** 1024px 이상 (데스크톱)
- **xl:** 1280px 이상 (큰 화면)

### 사용 예시

```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  {/* 모바일: 1열, 태블릿: 2열, 데스크톱: 3열 */}
</div>
```

---

## 🔧 개발 팁

### 1. Hot Reload

파일 저장 시 자동 새로고침됩니다.
- 코드 수정 → 저장 → 자동 반영

### 2. TypeScript 타입 체크

```bash
# 타입 에러 확인
npm run build
```

### 3. Linting

```bash
# ESLint 실행
npm run lint
```

### 4. 개발자 도구

- **React DevTools** 설치 권장
- **Redux DevTools** (상태 관리 시)

---

## 🚀 빌드 및 배포

### 1. 프로덕션 빌드

```bash
npm run build
```

생성되는 파일:
- `.next/` 폴더에 최적화된 빌드 파일

### 2. 로컬에서 프로덕션 실행

```bash
npm run start
```

### 3. Vercel 배포

#### 방법 1: Vercel CLI

```bash
# Vercel CLI 설치
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

#### 방법 2: Vercel Dashboard

1. [Vercel](https://vercel.com/) 접속 및 로그인
2. **New Project** 클릭
3. GitHub 저장소 연결
4. **Environment Variables** 설정:
   - `NEXT_PUBLIC_SUPABASE_URL`
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
5. **Deploy** 클릭

자동으로 배포되며 URL이 생성됩니다.

---

## 🐛 문제 해결

### 1. "Module not found" 오류

```bash
# node_modules 삭제 후 재설치
rm -rf node_modules package-lock.json
npm install
```

### 2. Supabase 연결 오류

**증상:**
```
Error: supabaseUrl and supabaseAnonKey are required
```

**해결:**
1. `.env.local` 파일이 프로젝트 루트에 있는지 확인
2. `NEXT_PUBLIC_` 접두사 확인
3. 개발 서버 재시작

```bash
# Ctrl+C로 중단 후
npm run dev
```

### 3. 포트 충돌

**증상:**
```
Port 3000 is already in use
```

**해결:**
```bash
# 다른 포트로 실행
PORT=3001 npm run dev

# 또는 기존 프로세스 종료
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:3000 | xargs kill -9
```

### 4. 빌드 오류

**증상:**
```
Type error: ...
```

**해결:**
```bash
# TypeScript 캐시 삭제
rm -rf .next
npm run dev
```

### 5. 스타일이 적용 안 됨

**해결:**
1. Tailwind CSS 설정 확인:
   ```typescript
   // tailwind.config.ts
   content: [
     "./app/**/*.{js,ts,jsx,tsx}",
   ]
   ```

2. `globals.css`에 Tailwind directives 확인:
   ```css
   @tailwind base;
   @tailwind components;
   @tailwind utilities;
   ```

---

## 📊 성능 최적화

### 1. 이미지 최적화

Next.js `Image` 컴포넌트 사용:

```tsx
import Image from 'next/image';

<Image 
  src="/logo.png" 
  alt="Logo" 
  width={100} 
  height={100}
/>
```

### 2. 동적 Import

필요한 컴포넌트만 로드:

```tsx
import dynamic from 'next/dynamic';

const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <LoadingSkeleton />,
});
```

### 3. 메모이제이션

```tsx
import { useMemo, useCallback } from 'react';

const filteredData = useMemo(() => {
  return scholarships.filter(/* ... */);
}, [scholarships, filters]);
```

---

## 📚 추가 리소스

- [Next.js 공식 문서](https://nextjs.org/docs)
- [Tailwind CSS 문서](https://tailwindcss.com/docs)
- [Supabase JavaScript 가이드](https://supabase.com/docs/reference/javascript)
- [TypeScript 핸드북](https://www.typescriptlang.org/docs/)

---

## 🎓 학습 자료

### Next.js App Router
- [App Router 마이그레이션 가이드](https://nextjs.org/docs/app/building-your-application/upgrading/app-router-migration)

### Tailwind CSS
- [Tailwind UI Components](https://tailwindui.com/)
- [Headless UI](https://headlessui.com/)

### Supabase
- [Supabase Auth](https://supabase.com/docs/guides/auth)
- [Supabase Realtime](https://supabase.com/docs/guides/realtime)

---

축하합니다! 🎉 이제 프론트엔드가 완전히 설정되었습니다.

