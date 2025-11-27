-- ============================================
-- 장학금 정보 테이블 생성
-- ============================================

-- scholarships 테이블 생성
CREATE TABLE IF NOT EXISTS scholarships (
  id BIGSERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  link TEXT NOT NULL,
  due_date DATE NOT NULL,
  min_gpa FLOAT DEFAULT 0.0,
  max_income INTEGER DEFAULT 99 CHECK (max_income >= 0 AND max_income <= 99),
  residence TEXT DEFAULT '전국',
  is_image_content BOOLEAN DEFAULT false,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 인덱스 생성 (검색 성능 향상)
CREATE INDEX idx_scholarships_due_date ON scholarships(due_date);
CREATE INDEX idx_scholarships_min_gpa ON scholarships(min_gpa);
CREATE INDEX idx_scholarships_max_income ON scholarships(max_income);
CREATE INDEX idx_scholarships_residence ON scholarships(residence);

-- 마감일 지난 장학금 자동 삭제를 위한 인덱스
CREATE INDEX idx_scholarships_due_date_active ON scholarships(due_date) WHERE due_date >= CURRENT_DATE;

-- Row Level Security (RLS) 활성화
ALTER TABLE scholarships ENABLE ROW LEVEL SECURITY;

-- 모든 사용자가 장학금 정보를 읽을 수 있도록 정책 설정
CREATE POLICY "장학금 정보는 누구나 조회 가능" 
  ON scholarships 
  FOR SELECT 
  USING (true);

-- 인증된 사용자만 장학금 정보를 삽입할 수 있도록 정책 설정 (크롤러용)
CREATE POLICY "인증된 사용자만 장학금 추가 가능" 
  ON scholarships 
  FOR INSERT 
  WITH CHECK (auth.role() = 'authenticated' OR auth.role() = 'service_role');

-- 중복 링크 방지를 위한 유니크 제약조건
CREATE UNIQUE INDEX idx_scholarships_link_unique ON scholarships(link);

-- 코멘트 추가
COMMENT ON TABLE scholarships IS '장학금 공고 정보를 저장하는 테이블';
COMMENT ON COLUMN scholarships.id IS '장학금 고유 ID';
COMMENT ON COLUMN scholarships.title IS '장학금 제목';
COMMENT ON COLUMN scholarships.link IS '장학금 공고 원문 링크 (고유값)';
COMMENT ON COLUMN scholarships.due_date IS '장학금 신청 마감일';
COMMENT ON COLUMN scholarships.min_gpa IS '최소 요구 학점 (0.0 = 제한 없음)';
COMMENT ON COLUMN scholarships.max_income IS '소득분위 상한선 (0-10, 99 = 제한 없음)';
COMMENT ON COLUMN scholarships.residence IS '거주지 제한 (예: 경기, 서울, 전국 등)';
COMMENT ON COLUMN scholarships.is_image_content IS '본문이 이미지인지 여부 (true: 이미지, false: 텍스트)';
COMMENT ON COLUMN scholarships.created_at IS '데이터 생성 시각';

