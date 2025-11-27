/**
 * Supabase Database Types
 * scholarships 테이블의 TypeScript 타입 정의
 */

// scholarships 테이블의 기본 타입
export interface Scholarship {
  id: number;
  title: string;
  link: string;
  due_date: string; // ISO 8601 date string (YYYY-MM-DD)
  min_gpa: number;
  max_income: number;
  residence: string;
  created_at: string; // ISO 8601 datetime string
}

// 장학금 생성 시 사용하는 타입 (id, created_at 제외)
export interface ScholarshipInsert {
  title: string;
  link: string;
  due_date: string;
  min_gpa?: number; // Optional, default 0
  max_income?: number; // Optional, default 99
  residence?: string; // Optional, default '전국'
}

// 장학금 업데이트 시 사용하는 타입 (모든 필드 optional)
export interface ScholarshipUpdate {
  title?: string;
  link?: string;
  due_date?: string;
  min_gpa?: number;
  max_income?: number;
  residence?: string;
}

// 사용자 필터 조건 타입
export interface UserFilter {
  gpa: number; // 사용자의 학점
  income: number; // 사용자의 소득분위 (0-10)
  residence: string; // 사용자의 거주지
}

// 장학금 검색 결과 타입
export interface ScholarshipSearchResult {
  scholarships: Scholarship[];
  total: number;
  filtered: number;
}

// Supabase Database 전체 스키마 타입
export interface Database {
  public: {
    Tables: {
      scholarships: {
        Row: Scholarship;
        Insert: ScholarshipInsert;
        Update: ScholarshipUpdate;
      };
    };
  };
}

