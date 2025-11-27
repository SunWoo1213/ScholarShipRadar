-- ============================================
-- 샘플 장학금 데이터 삽입
-- 테스트 및 개발용 더미 데이터
-- ============================================

-- 기존 샘플 데이터 삭제 (선택사항)
-- DELETE FROM scholarships WHERE link LIKE 'https://example.com/%';

-- 샘플 장학금 데이터 삽입
INSERT INTO scholarships (title, link, due_date, min_gpa, max_income, residence) VALUES
  ('청년 희망 장학금', 'https://example.com/scholarship/1', '2025-12-31', 3.0, 8, '전국'),
  ('서울시 대학생 장학금', 'https://example.com/scholarship/2', '2025-12-15', 2.5, 5, '서울'),
  ('경기도 인재 육성 장학금', 'https://example.com/scholarship/3', '2025-12-20', 3.5, 6, '경기'),
  ('저소득층 학업 장려금', 'https://example.com/scholarship/4', '2026-01-15', 0.0, 3, '전국'),
  ('우수학생 장학금', 'https://example.com/scholarship/5', '2025-12-25', 4.0, 99, '전국'),
  ('부산광역시 장학금', 'https://example.com/scholarship/6', '2025-11-30', 2.8, 7, '부산'),
  ('인천시 미래인재 장학금', 'https://example.com/scholarship/7', '2026-01-10', 3.2, 5, '인천'),
  ('대전시 과학기술 장학금', 'https://example.com/scholarship/8', '2025-12-28', 3.8, 8, '대전'),
  ('전국 저학년 장학금', 'https://example.com/scholarship/9', '2026-02-28', 2.0, 10, '전국'),
  ('강원도 지역인재 장학금', 'https://example.com/scholarship/10', '2025-12-10', 3.0, 6, '강원')
ON CONFLICT (link) DO NOTHING;

-- 삽입된 데이터 확인
SELECT 
  COUNT(*) as total_scholarships,
  COUNT(*) FILTER (WHERE due_date >= CURRENT_DATE) as active_scholarships,
  COUNT(*) FILTER (WHERE due_date < CURRENT_DATE) as expired_scholarships
FROM scholarships;

-- 거주지별 분포 확인
SELECT 
  residence,
  COUNT(*) as count
FROM scholarships
GROUP BY residence
ORDER BY count DESC;

