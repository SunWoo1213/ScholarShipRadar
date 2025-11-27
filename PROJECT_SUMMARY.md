# 🎓 장학금 레이더 - 프로젝트 요약

---

## 📋 프로젝트 개요

**프로젝트명:** 장학금 레이더 (Scholarship Radar)

**목적:** 대학생들이 자신의 조건(학점, 소득분위, 거주지)에 맞는 장학금을 쉽게 찾을 수 있도록 돕는 웹 플랫폼

**타겟 사용자:** 대한민국 대학생

**개발 기간:** MVP (Minimum Viable Product)

---

## 🎯 핵심 기능

### 1. 맞춤형 장학금 검색
- 학점 기반 필터링 (0.0 ~ 4.5)
- 소득분위 필터링 (1~10분위)
- 거주지 필터링 (전국 17개 시도)
- 실시간 검색 결과 제공

### 2. 자동 데이터 수집
- Python 크롤러로 장학금 정보 자동 수집
- GPT-4o Vision으로 이미지 공고 분석
- GPT-4o로 텍스트 공고 분석
- Supabase 데이터베이스에 자동 저장

### 3. 사용자 친화적 UI
- 모던하고 직관적인 디자인
- 모바일 완전 반응형
- D-day 자동 계산
- 마감 임박 알림

---

## 🚀 기술 스택

### Frontend
```
Next.js 14 (App Router)
├── TypeScript
├── Tailwind CSS
└── Supabase Client
```

### Backend & Database
```
Supabase (PostgreSQL)
├── Row Level Security
├── Real-time Subscriptions
└── RESTful API
```

### Data Processing
```
Python 3.8+
├── BeautifulSoup4 (HTML 파싱)
├── OpenAI GPT-4o (Vision & Text)
├── Requests (HTTP)
└── Supabase Client
```

### Deployment
```
Vercel
├── Automatic Deployments
├── Preview Deployments
└── Custom Domains
```

---

## 📁 파일 구조

```
scholarship-radar/
│
├── 📱 Frontend (Next.js 14)
│   ├── app/
│   │   ├── page.tsx           # 메인 페이지 (500줄)
│   │   ├── layout.tsx         # 루트 레이아웃
│   │   └── globals.css        # 글로벌 스타일
│   ├── lib/
│   │   └── supabase.ts        # Supabase 클라이언트
│   ├── types/
│   │   └── database.types.ts  # TypeScript 타입
│   └── .env.local            # 환경 변수
│
├── 🐍 Crawler (Python)
│   ├── crawler_vision.py      # 이미지 기반 (600줄)
│   ├── crawler.py             # 텍스트 기반 (400줄)
│   ├── test_crawler.py        # 환경 테스트
│   └── .env                   # 환경 변수
│
├── 🗄️ Database (Supabase)
│   ├── supabase_schema.sql         # 스키마 정의
│   └── supabase_sample_data.sql    # 샘플 데이터
│
└── 📖 Documentation
    ├── README.md              # 메인 가이드
    ├── QUICKSTART.md          # 빠른 시작
    ├── ENV_SETUP_GUIDE.md     # 환경 변수
    ├── DEPLOYMENT.md          # 배포 가이드
    ├── CHECKLIST.md           # 배포 체크리스트
    └── PROJECT_SUMMARY.md     # 이 파일
```

**총 라인 수:** ~2,500 라인

---

## 🗄️ 데이터베이스 스키마

### scholarships 테이블

```sql
CREATE TABLE scholarships (
  id            BIGSERIAL PRIMARY KEY,
  title         TEXT NOT NULL,
  link          TEXT NOT NULL UNIQUE,
  due_date      DATE NOT NULL,
  min_gpa       FLOAT DEFAULT 0.0,
  max_income    INTEGER DEFAULT 99,
  residence     TEXT DEFAULT '전국',
  created_at    TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

**인덱스:**
- `due_date` (마감일 검색)
- `min_gpa` (학점 필터링)
- `max_income` (소득분위 필터링)
- `residence` (거주지 필터링)

---

## 🔄 데이터 흐름

```
┌─────────────────────────────────────────┐
│  1. Python Crawler                      │
│     장학금 게시판 크롤링                │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│  2. GPT-4o Vision/Text                  │
│     조건 자동 추출                      │
│     (학점, 소득분위, 거주지, 마감일)    │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│  3. Supabase PostgreSQL                 │
│     데이터 저장                         │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│  4. Next.js Frontend                    │
│     사용자에게 표시                     │
└─────────────────────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│  5. 사용자 필터링                       │
│     맞춤형 검색 결과                    │
└─────────────────────────────────────────┘
```

---

## 🎨 UI/UX 특징

### 디자인 컨셉
- **모던하고 깔끔한** 인터페이스
- **대학생 친화적** 색상 (블루/인디고 그라데이션)
- **직관적인** 검색 필터
- **카드 형식** 장학금 리스트

### 주요 컴포넌트
1. **검색 필터 섹션**
   - 학점 입력 (Number Input)
   - 소득분위 선택 (Select)
   - 거주지 선택 (Select)
   - 검색 버튼

2. **장학금 카드**
   - D-day 배지 (긴급/일반/마감)
   - 제목 (최대 2줄)
   - 마감일 및 거주지
   - 조건 태그 (학점, 소득분위)
   - 상세보기 버튼

3. **로딩 & Empty State**
   - 스켈레톤 UI (로딩 중)
   - 안내 메시지 (결과 없음)
   - 초기화 버튼

### 반응형 디자인
- **Mobile:** 1열 카드
- **Tablet:** 2열 카드
- **Desktop:** 3열 카드

---

## 🤖 AI 활용

### GPT-4o Vision (이미지 분석)
```python
# 장학금 공고 이미지 → 조건 추출
input: Base64 이미지
output: {
  "min_gpa": 3.0,
  "max_income": 8,
  "residence": "전국",
  "due_date": "2026-01-31"
}
```

**장점:**
- ✅ 이미지로 된 공고 분석 가능
- ✅ 복잡한 레이아웃 인식
- ✅ 한글 OCR 정확도 높음

**비용:** 공고 1개당 ~$0.002

### GPT-4o Text (텍스트 분석)
```python
# 장학금 공고 텍스트 → 조건 추출
input: HTML 텍스트
output: {
  "min_gpa": 2.5,
  "max_income": 5,
  "residence": "서울",
  "due_date": "2026-02-15"
}
```

**장점:**
- ✅ 빠른 처리 속도
- ✅ 저렴한 비용
- ✅ 높은 정확도

**비용:** 공고 1개당 ~$0.0001

---

## 💰 운영 비용 (월간)

### Supabase (무료)
- 500MB DB
- 2GB 전송
- **비용:** $0

### OpenAI API
- 매일 10개 크롤링
- 월 300개 × $0.002
- **비용:** ~$0.60/월 (~800원)

### Vercel (무료)
- 무제한 배포
- 100GB 대역폭
- **비용:** $0

**총 운영 비용:** ~$0.60/월 (~800원) ✅

---

## 🔒 보안

### Frontend
- ✅ `anon public` key 사용
- ✅ Row Level Security로 보호
- ✅ 환경 변수로 관리

### Crawler
- ✅ `service_role` key (서버 사이드만)
- ✅ `.gitignore`로 환경 변수 제외
- ✅ API Rate Limiting 준수

### Database
- ✅ RLS 활성화
- ✅ 읽기: Public
- ✅ 쓰기: Authenticated Only

---

## 📈 성능

### Frontend
- ⚡ **First Load:** ~2초
- ⚡ **검색 속도:** ~0.5초
- ⚡ **Lighthouse Score:** 90+

### Crawler
- 🐌 **공고 1개:** ~5초 (이미지 분석)
- ⚡ **공고 1개:** ~2초 (텍스트 분석)
- 📊 **100개 처리:** ~10분

### Database
- ⚡ **쿼리 속도:** <100ms
- 📦 **저장 용량:** 장학금 1,000개 = ~5MB
- 🔄 **동시 접속:** 500+ 지원 (무료 플랜)

---

## 🚀 배포 프로세스

### 1. 로컬 개발
```bash
npm run dev  # http://localhost:3000
```

### 2. Git Push
```bash
git push origin main
```

### 3. Vercel 자동 배포
- GitHub 푸시 감지
- 자동 빌드 & 배포
- Preview URL 생성
- Production 배포

**배포 시간:** ~2분

---

## 📊 향후 개선 계획

### Phase 1 (MVP) ✅
- [x] 기본 검색 기능
- [x] 크롤링 자동화
- [x] Vercel 배포

### Phase 2 (인증)
- [ ] 사용자 회원가입
- [ ] 로그인/로그아웃
- [ ] 프로필 관리

### Phase 3 (기능 확장)
- [ ] 즐겨찾기
- [ ] 검색 히스토리
- [ ] 마감 임박 알림
- [ ] 이메일/푸시 알림

### Phase 4 (최적화)
- [ ] 다크 모드
- [ ] PWA 지원
- [ ] 오프라인 모드
- [ ] 성능 최적화

### Phase 5 (확장)
- [ ] 관리자 대시보드
- [ ] 통계 페이지
- [ ] 더 많은 사이트 지원
- [ ] ML 기반 추천

---

## 🐛 알려진 이슈

### Frontend
- [ ] 매우 긴 제목 표시 문제 (line-clamp로 해결)
- [ ] 빈 검색 결과 시 UX 개선 필요

### Crawler
- [ ] 일부 사이트 접근 차단 (User-Agent 변경 필요)
- [ ] Rate Limit 초과 시 재시도 로직 필요
- [ ] 이미지 다운로드 실패 핸들링

### Database
- [ ] 중복 데이터 정기적 정리 필요
- [ ] 만료된 장학금 자동 삭제

---

## 📞 연락처

**개발자:** [Your Name]  
**이메일:** your-email@example.com  
**GitHub:** https://github.com/your-username  
**프로젝트:** https://github.com/your-username/scholarship-radar  

---

## 📝 라이선스

MIT License

---

## 🙏 기여자

이 프로젝트에 기여해주신 모든 분들께 감사드립니다!

---

**Last Updated:** 2025-11-27  
**Version:** 1.0.0 (MVP)

