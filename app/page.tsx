'use client';

import { useState, useEffect } from 'react';
import { supabase } from '@/lib/supabase';
import { Scholarship } from '@/types/database.types';

// 거주지 옵션
const RESIDENCE_OPTIONS = [
  { value: '', label: '선택 안 함' },
  { value: '전국', label: '전국' },
  { value: '서울', label: '서울' },
  { value: '경기', label: '경기' },
  { value: '인천', label: '인천' },
  { value: '부산', label: '부산' },
  { value: '대구', label: '대구' },
  { value: '대전', label: '대전' },
  { value: '광주', label: '광주' },
  { value: '울산', label: '울산' },
  { value: '세종', label: '세종' },
  { value: '강원', label: '강원' },
  { value: '충북', label: '충북' },
  { value: '충남', label: '충남' },
  { value: '전북', label: '전북' },
  { value: '전남', label: '전남' },
  { value: '경북', label: '경북' },
  { value: '경남', label: '경남' },
  { value: '제주', label: '제주' },
];

// 소득분위 옵션
const INCOME_OPTIONS = [
  { value: '', label: '선택 안 함' },
  { value: '1', label: '1분위' },
  { value: '2', label: '2분위' },
  { value: '3', label: '3분위' },
  { value: '4', label: '4분위' },
  { value: '5', label: '5분위' },
  { value: '6', label: '6분위' },
  { value: '7', label: '7분위' },
  { value: '8', label: '8분위' },
  { value: '9', label: '9분위' },
  { value: '10', label: '10분위' },
];

// D-day 계산 함수
function calculateDday(dueDate: string): string {
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  
  const due = new Date(dueDate);
  due.setHours(0, 0, 0, 0);
  
  const diffTime = due.getTime() - today.getTime();
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  
  if (diffDays < 0) return '마감';
  if (diffDays === 0) return 'D-day';
  return `D-${diffDays}`;
}

// 카드 컴포넌트
function ScholarshipCard({ scholarship }: { scholarship: Scholarship }) {
  const dday = calculateDday(scholarship.due_date);
  const isUrgent = dday !== '마감' && dday !== 'D-day' && parseInt(dday.replace('D-', '')) <= 7;
  const isExpired = dday === '마감';
  
  return (
    <div className="bg-white rounded-xl shadow-md p-6 card-hover border border-gray-100">
      {/* 상단: D-day 배지 */}
      <div className="flex justify-between items-start mb-3">
        <span
          className={`px-3 py-1 rounded-full text-sm font-semibold ${
            isExpired
              ? 'bg-gray-100 text-gray-500'
              : isUrgent
              ? 'bg-red-100 text-red-600'
              : 'bg-blue-100 text-blue-600'
          }`}
        >
          {dday}
        </span>
        
        {/* 조건 태그들 */}
        <div className="flex gap-2 flex-wrap justify-end">
          {scholarship.min_gpa > 0 && (
            <span className="px-2 py-1 bg-purple-50 text-purple-600 text-xs rounded-md">
              학점 {scholarship.min_gpa}+
            </span>
          )}
          {scholarship.max_income < 99 && (
            <span className="px-2 py-1 bg-green-50 text-green-600 text-xs rounded-md">
              {scholarship.max_income}분위 이하
            </span>
          )}
        </div>
      </div>

      {/* 제목 */}
      <h3 className="text-lg font-bold text-gray-800 mb-2 line-clamp-2 hover:text-blue-600 transition-colors">
        {scholarship.title}
      </h3>

      {/* 정보 */}
      <div className="space-y-2 mb-4 text-sm text-gray-600">
        <div className="flex items-center gap-2">
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          <span>마감일: {scholarship.due_date}</span>
        </div>
        
        <div className="flex items-center gap-2">
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
          <span>거주지: {scholarship.residence}</span>
        </div>
      </div>

      {/* 버튼 */}
      <a
        href={scholarship.link}
        target="_blank"
        rel="noopener noreferrer"
        className="block w-full text-center bg-gradient-to-r from-blue-600 to-indigo-600 text-white py-3 rounded-lg font-semibold hover:from-blue-700 hover:to-indigo-700 transition-all duration-300 shadow-md hover:shadow-lg"
      >
        공고 자세히 보기 →
      </a>
    </div>
  );
}

// 로딩 스켈레톤
function LoadingSkeleton() {
  return (
    <div className="space-y-4">
      {[1, 2, 3].map((i) => (
        <div key={i} className="bg-white rounded-xl shadow-md p-6 animate-pulse">
          <div className="flex justify-between mb-4">
            <div className="h-6 bg-gray-200 rounded-full w-16"></div>
            <div className="h-6 bg-gray-200 rounded-md w-24"></div>
          </div>
          <div className="h-6 bg-gray-200 rounded w-3/4 mb-2"></div>
          <div className="h-4 bg-gray-200 rounded w-1/2 mb-4"></div>
          <div className="h-10 bg-gray-200 rounded-lg w-full"></div>
        </div>
      ))}
    </div>
  );
}

// 메인 컴포넌트
export default function Home() {
  // 상태 관리
  const [gpa, setGpa] = useState<string>('');
  const [income, setIncome] = useState<string>('');
  const [residence, setResidence] = useState<string>('');
  const [scholarships, setScholarships] = useState<Scholarship[]>([]);
  const [filteredScholarships, setFilteredScholarships] = useState<Scholarship[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [searched, setSearched] = useState<boolean>(false);

  // 전체 장학금 로드 (초기)
  useEffect(() => {
    loadAllScholarships();
  }, []);

  const loadAllScholarships = async () => {
    setLoading(true);
    try {
      const { data, error } = await supabase
        .from('scholarships')
        .select('*')
        .gte('due_date', new Date().toISOString().split('T')[0])
        .order('due_date', { ascending: true });

      if (error) throw error;
      setScholarships(data || []);
    } catch (error) {
      console.error('장학금 로딩 오류:', error);
      alert('장학금 정보를 불러오는데 실패했습니다.');
    } finally {
      setLoading(false);
    }
  };

  // 장학금 검색
  const handleSearch = async () => {
    if (!gpa && !income && !residence) {
      alert('검색 조건을 하나 이상 입력해주세요.');
      return;
    }

    setLoading(true);
    setSearched(true);

    try {
      let query = supabase
        .from('scholarships')
        .select('*')
        .gte('due_date', new Date().toISOString().split('T')[0]);

      // 학점 필터
      if (gpa) {
        const gpaNum = parseFloat(gpa);
        query = query.lte('min_gpa', gpaNum);
      }

      // 소득분위 필터
      if (income) {
        const incomeNum = parseInt(income);
        query = query.or(`max_income.gte.${incomeNum},max_income.eq.99`);
      }

      // 거주지 필터
      if (residence) {
        query = query.or(`residence.eq.${residence},residence.eq.전국`);
      }

      query = query.order('due_date', { ascending: true });

      const { data, error } = await query;

      if (error) throw error;

      setFilteredScholarships(data || []);
    } catch (error) {
      console.error('검색 오류:', error);
      alert('검색 중 오류가 발생했습니다.');
    } finally {
      setLoading(false);
    }
  };

  // Enter 키로 검색
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  const displayScholarships = searched ? filteredScholarships : scholarships;

  return (
    <main className="min-h-screen py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-6xl mx-auto">
        {/* 헤더 */}
        <header className="text-center mb-12 animate-fade-in">
          <h1 className="text-5xl font-extrabold mb-4">
            <span className="gradient-text">장학금 레이더</span>
          </h1>
          <p className="text-gray-600 text-lg">
            내 조건에 딱 맞는 장학금을 찾아보세요 🎓
          </p>
        </header>

        {/* 검색 필터 섹션 */}
        <div className="bg-white rounded-2xl shadow-xl p-8 mb-8 animate-slide-up border border-gray-100">
          <h2 className="text-2xl font-bold text-gray-800 mb-6 flex items-center gap-2">
            <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            나의 조건 입력
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
            {/* 학점 입력 */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                내 학점
              </label>
              <input
                type="number"
                step="0.01"
                min="0"
                max="4.5"
                value={gpa}
                onChange={(e) => setGpa(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="예: 3.5"
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all outline-none"
              />
              <p className="text-xs text-gray-500 mt-1">
                0.0 ~ 4.5 사이 값을 입력하세요
              </p>
            </div>

            {/* 소득분위 선택 */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                내 소득분위
              </label>
              <select
                value={income}
                onChange={(e) => setIncome(e.target.value)}
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all outline-none bg-white"
              >
                {INCOME_OPTIONS.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
              <p className="text-xs text-gray-500 mt-1">
                소득분위를 선택하세요
              </p>
            </div>

            {/* 거주지 선택 */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                내 거주지
              </label>
              <select
                value={residence}
                onChange={(e) => setResidence(e.target.value)}
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all outline-none bg-white"
              >
                {RESIDENCE_OPTIONS.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
              <p className="text-xs text-gray-500 mt-1">
                거주지를 선택하세요
              </p>
            </div>
          </div>

          {/* 검색 버튼 */}
          <button
            onClick={handleSearch}
            disabled={loading}
            className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 text-white py-4 rounded-xl font-bold text-lg hover:from-blue-700 hover:to-indigo-700 transition-all duration-300 shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            {loading ? (
              <>
                <svg className="animate-spin h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                검색 중...
              </>
            ) : (
              <>
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                장학금 찾기
              </>
            )}
          </button>

          {/* 현재 필터 표시 */}
          {(gpa || income || residence) && (
            <div className="mt-4 flex flex-wrap gap-2">
              <span className="text-sm text-gray-600">현재 필터:</span>
              {gpa && (
                <span className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm font-medium">
                  학점 {gpa}+
                </span>
              )}
              {income && (
                <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm font-medium">
                  소득 {income}분위 이하
                </span>
              )}
              {residence && (
                <span className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm font-medium">
                  {residence}
                </span>
              )}
            </div>
          )}
        </div>

        {/* 결과 섹션 */}
        <div>
          {/* 결과 헤더 */}
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-gray-800">
              {searched ? '검색 결과' : '최신 장학금'}
              <span className="ml-3 text-blue-600">
                {displayScholarships.length}개
              </span>
            </h2>

            {searched && (
              <button
                onClick={() => {
                  setSearched(false);
                  setGpa('');
                  setIncome('');
                  setResidence('');
                }}
                className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors text-sm font-medium"
              >
                초기화
              </button>
            )}
          </div>

          {/* 로딩 상태 */}
          {loading && <LoadingSkeleton />}

          {/* 결과 없음 */}
          {!loading && displayScholarships.length === 0 && (
            <div className="bg-white rounded-xl shadow-md p-12 text-center">
              <div className="text-6xl mb-4">😢</div>
              <h3 className="text-xl font-bold text-gray-800 mb-2">
                {searched ? '조건에 맞는 장학금이 없습니다' : '등록된 장학금이 없습니다'}
              </h3>
              <p className="text-gray-600 mb-6">
                {searched
                  ? '다른 조건으로 다시 검색해보세요'
                  : '곧 새로운 장학금 정보가 업데이트 될 예정입니다'}
              </p>
              {searched && (
                <button
                  onClick={() => {
                    setSearched(false);
                    setGpa('');
                    setIncome('');
                    setResidence('');
                  }}
                  className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
                >
                  전체 장학금 보기
                </button>
              )}
            </div>
          )}

          {/* 장학금 카드 리스트 */}
          {!loading && displayScholarships.length > 0 && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {displayScholarships.map((scholarship) => (
                <ScholarshipCard key={scholarship.id} scholarship={scholarship} />
              ))}
            </div>
          )}
        </div>

        {/* 푸터 */}
        <footer className="mt-16 text-center text-gray-500 text-sm">
          <p>💡 새로운 장학금 정보는 매일 업데이트됩니다</p>
          <p className="mt-2">
            문의사항이 있으시면 언제든지 연락주세요
          </p>
        </footer>
      </div>
    </main>
  );
}

