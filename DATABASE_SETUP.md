# Supabase 데이터베이스 설정 가이드

## 📋 설정 단계

### 1. Supabase 프로젝트 생성
1. [Supabase](https://supabase.com) 접속
2. 새 프로젝트 생성
3. Database Password 설정 및 저장

### 2. SQL 스키마 실행
1. Supabase Dashboard → SQL Editor 이동
2. `supabase_schema.sql` 파일의 내용을 복사
3. SQL Editor에 붙여넣기
4. **Run** 버튼 클릭하여 실행

### 3. 테이블 확인
- Table Editor → `scholarships` 테이블이 생성되었는지 확인
- 컬럼 구조가 올바른지 검증

---

## 🗃️ 테이블 구조

### scholarships 테이블

| 컬럼명 | 타입 | 설명 | 기본값 | 제약조건 |
|--------|------|------|--------|----------|
| `id` | bigint | 장학금 고유 ID | Auto | PRIMARY KEY |
| `title` | text | 장학금 제목 | - | NOT NULL |
| `link` | text | 공고 원문 링크 | - | NOT NULL, UNIQUE |
| `due_date` | date | 신청 마감일 | - | NOT NULL |
| `min_gpa` | float | 최소 요구 학점 | 0.0 | - |
| `max_income` | integer | 소득분위 상한선 | 99 | 0-99 |
| `residence` | text | 거주지 제한 | '전국' | - |
| `created_at` | timestamptz | 생성 시각 | NOW() | - |

### 인덱스
- `idx_scholarships_due_date`: 마감일 검색 최적화
- `idx_scholarships_min_gpa`: 학점 필터링 최적화
- `idx_scholarships_max_income`: 소득분위 필터링 최적화
- `idx_scholarships_residence`: 거주지 필터링 최적화
- `idx_scholarships_link_unique`: 중복 링크 방지

---

## 🔐 보안 정책 (Row Level Security)

### 조회 정책
- 모든 사용자가 장학금 정보를 조회할 수 있습니다.

### 삽입 정책
- 인증된 사용자(크롤러)만 장학금 정보를 추가할 수 있습니다.

---

## 📝 TypeScript 타입 사용법

### 기본 사용 예제

```typescript
import { Scholarship, ScholarshipInsert, UserFilter } from '@/types/database.types';

// 장학금 조회
const scholarship: Scholarship = {
  id: 1,
  title: "청년 희망 장학금",
  link: "https://example.com/scholarship/1",
  due_date: "2025-12-31",
  min_gpa: 3.0,
  max_income: 8,
  residence: "전국",
  created_at: "2025-11-27T00:00:00Z"
};

// 장학금 추가
const newScholarship: ScholarshipInsert = {
  title: "대학생 장학금",
  link: "https://example.com/scholarship/2",
  due_date: "2025-12-31",
  min_gpa: 2.5,
  max_income: 5,
  residence: "서울"
};

// 사용자 필터
const userFilter: UserFilter = {
  gpa: 3.5,
  income: 4,
  residence: "서울"
};
```

---

## 🧪 테스트 데이터 삽입

```sql
-- 샘플 장학금 데이터 삽입
INSERT INTO scholarships (title, link, due_date, min_gpa, max_income, residence) VALUES
  ('청년 희망 장학금', 'https://example.com/1', '2025-12-31', 3.0, 8, '전국'),
  ('서울시 대학생 장학금', 'https://example.com/2', '2025-11-30', 2.5, 5, '서울'),
  ('경기도 인재 육성 장학금', 'https://example.com/3', '2025-12-15', 3.5, 6, '경기'),
  ('저소득층 학업 장려금', 'https://example.com/4', '2026-01-15', 0.0, 3, '전국'),
  ('우수학생 장학금', 'https://example.com/5', '2025-12-20', 4.0, 99, '전국');
```

---

## 🔍 유용한 쿼리 예제

### 1. 조건에 맞는 장학금 필터링
```sql
SELECT * FROM scholarships
WHERE due_date >= CURRENT_DATE
  AND min_gpa <= 3.5  -- 사용자 학점
  AND max_income >= 4  -- 사용자 소득분위
  AND (residence = '서울' OR residence = '전국')  -- 사용자 거주지
ORDER BY due_date ASC;
```

### 2. 마감 임박 장학금 조회
```sql
SELECT * FROM scholarships
WHERE due_date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '7 days'
ORDER BY due_date ASC;
```

### 3. 통계 조회
```sql
SELECT 
  COUNT(*) as total,
  COUNT(*) FILTER (WHERE due_date >= CURRENT_DATE) as active,
  COUNT(*) FILTER (WHERE due_date < CURRENT_DATE) as expired
FROM scholarships;
```

---

## 🚀 다음 단계

1. ✅ Supabase 스키마 생성 완료
2. ⏭️ Next.js 프로젝트 초기화
3. ⏭️ Supabase Client 설정
4. ⏭️ Python 크롤링 스크립트 작성
5. ⏭️ 프론트엔드 UI 구현

