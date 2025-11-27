# 🖼️ 이미지 기반 장학금 크롤러 (GPT-4o Vision)

학교 공지사항이 이미지로 되어 있는 경우를 위한 크롤러입니다.

---

## 🎯 주요 특징

### ✨ Hybrid 분석 전략

```
┌─────────────────────────────────────┐
│   1. 게시판 목록 크롤링              │
│      제목 + 링크 수집               │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│   2. 상세 페이지 접근                │
│      .tbl_view 영역에서             │
│      ✓ 이미지 찾기 (우선)           │
│      ✓ 텍스트 추출 (백업)           │
└──────────────┬──────────────────────┘
               ↓
       ┌──────┴──────┐
       │             │
    이미지 있음?   이미지 없음
       │             │
       ↓             ↓
┌─────────────┐  ┌──────────────┐
│ GPT-4o      │  │ GPT-4o       │
│ Vision 분석 │  │ 텍스트 분석  │
│ (이미지)    │  │ (폴백)       │
└──────┬──────┘  └──────┬───────┘
       │                │
       └────────┬────────┘
                ↓
      ┌──────────────────┐
      │  조건 추출:       │
      │  - 학점          │
      │  - 소득분위      │
      │  - 거주지        │
      │  - 마감일        │
      └────────┬─────────┘
               ↓
      ┌──────────────────┐
      │  Supabase 저장   │
      └──────────────────┘
```

---

## 📋 기능

### 1️⃣ 이미지 크롤링
- ✅ `.tbl_view` 클래스 내 `<img>` 태그 자동 탐지
- ✅ 상대 경로 → 절대 경로 자동 변환
- ✅ Base64 인코딩 (외부 접근 차단 대응)

### 2️⃣ GPT-4o Vision 분석
- ✅ 고해상도 이미지 분석 (`detail: "high"`)
- ✅ 한글 OCR 정확도 높음
- ✅ 복잡한 레이아웃도 인식 가능

### 3️⃣ Hybrid 폴백
- ✅ 이미지 없으면 자동으로 텍스트 분석
- ✅ 실패 없는 안정적인 크롤링

---

## 🚀 설치 및 실행

### 1. 의존성 설치

```bash
cd crawler
pip install -r requirements.txt
```

### 2. 환경 변수 설정

`.env` 파일 생성:

```bash
# Windows
copy env_template.txt .env

# Mac/Linux
cp env_template.txt .env
```

`.env` 파일 편집:

```env
# Supabase 설정
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGci... (service_role key)

# OpenAI API 설정 (⚠️ GPT-4o 사용 - 비용 주의!)
OPENAI_API_KEY=sk-proj-xxxxx

# 크롤링 대상 URL (강남대 장학금 게시판)
TARGET_URL=https://web.kangnam.ac.kr/board/scholarship

# 선택사항
MAX_PAGES=10
DELAY_SECONDS=3  # 이미지 분석은 시간이 걸리므로 3초 권장
```

### 3. 실행

```bash
python crawler_vision.py
```

---

## 💰 비용 안내

### GPT-4o Vision 가격

| 항목 | 가격 |
|------|------|
| Input (텍스트) | $2.50 / 1M tokens |
| Input (이미지) | $5.00 / 1M tokens |
| Output | $10.00 / 1M tokens |

### 예상 비용 (공고 1개당)

```
이미지 크기: 1024x768 (약 170 tokens)
텍스트 프롬프트: 약 200 tokens
응답: 약 50 tokens

비용 = (170 * $5 + 200 * $2.5 + 50 * $10) / 1,000,000
     ≈ $0.002 (약 2원)

100개 크롤링 시: 약 $0.20 (약 200원)
```

⚠️ **주의:** gpt-4o-mini는 Vision 지원 안 함!

---

## 🔧 커스터마이징

### 1. 게시판 HTML 구조 변경

`crawler_vision.py` 파일의 `crawl_scholarship_list()` 수정:

```python
# 48번째 줄 근처
detail_links = soup.find_all('a', class_='detailLink')

# 실제 사이트 구조에 맞게 수정:
detail_links = soup.select('div.board-list > a')
```

### 2. 본문 영역 클래스 변경

`crawl_scholarship_detail()` 메서드 수정:

```python
# 84번째 줄 근처
content_div = soup.find('div', class_='tbl_view')

# 실제 사이트의 본문 클래스로 변경:
content_div = soup.find('div', class_='your-content-class')
```

### 3. Base Domain 변경

```python
# 26번째 줄
BASE_DOMAIN = "https://web.kangnam.ac.kr"

# 다른 학교 사이트로 변경:
BASE_DOMAIN = "https://your-school.ac.kr"
```

---

## 📊 실행 예시

```
======================================================================
🎓 장학금 크롤러 시작 (이미지 기반 - GPT-4o Vision)
======================================================================

📊 현재 DB 상태:
  - 전체 장학금: 5개
  - 활성 장학금: 5개
  - 만료 장학금: 0개

📡 크롤링 시작: https://web.kangnam.ac.kr/board/scholarship
✅ 8개의 공고를 발견했습니다.

🔄 총 8개의 장학금을 처리합니다.

[1/8] [국가장학금] 2026-1학기 국가장학금 I유형 신청 안내
----------------------------------------------------------------------
  📄 상세 페이지 크롤링: https://web.kangnam.ac.kr/board/view?seq=123
  🖼️  이미지 발견: https://web.kangnam.ac.kr/uploads/scholarship/2024/notice.jpg
  📥 이미지 다운로드 중: https://web.kangnam.ac.kr/uploads/scholarship/2024/notice.jpg
  ✅ 이미지 다운로드 완료 (245678 bytes)
  🤖 GPT-4o Vision 분석 중...
  ✅ 분석 완료: {'min_gpa': 0.0, 'max_income': 8, 'residence': '전국', 'due_date': '2026-01-31'}
  📸 이미지 기반 분석 성공
  💾 DB 저장 중: [국가장학금] 2026-1학기 국가장학금...
  ✅ 저장 완료! ID: 6

[2/8] 서울시 대학생 장학금
----------------------------------------------------------------------
  📄 상세 페이지 크롤링: https://web.kangnam.ac.kr/board/view?seq=124
  ⚠️  이미지를 찾을 수 없습니다.
  📝 텍스트 기반 분석으로 전환...
  🤖 GPT-4o 텍스트 분석 중...
  ✅ 분석 완료: {'min_gpa': 2.5, 'max_income': 5, 'residence': '서울', 'due_date': '2026-02-15'}
  📝 텍스트 기반 분석 성공
  💾 DB 저장 중: 서울시 대학생 장학금...
  ✅ 저장 완료! ID: 7

...

======================================================================
✅ 크롤링 완료!
======================================================================
  - 성공: 7개
  - 실패: 1개
  - 전체: 8개

  📊 분석 방법:
  - 이미지 기반 (Vision): 5개
  - 텍스트 기반: 2개

📊 최종 DB 상태:
  - 전체 장학금: 12개
  - 활성 장학금: 12개
  - 만료 장학금: 0개
```

---

## 🐛 문제 해결

### "Image download failed"

**원인:** 학교 서버가 외부 접근 차단

**해결:**
- Headers에 Referer 추가
- Session의 cookies 유지
- User-Agent 변경

```python
self.session.headers.update({
    'Referer': 'https://web.kangnam.ac.kr',
    'User-Agent': 'Mozilla/5.0...'
})
```

### "Invalid API key" (OpenAI)

**원인:** API 키 오류 또는 GPT-4o 권한 없음

**해결:**
1. API 키 재확인
2. OpenAI 계정에 GPT-4o 접근 권한 확인
3. 잔액 확인: https://platform.openai.com/usage

### "Rate limit exceeded"

**원인:** OpenAI API 요청 한도 초과

**해결:**
```python
# DELAY_SECONDS 증가
DELAY_SECONDS=5

# 또는 배치 크기 줄이기
MAX_PAGES=5
```

### 이미지는 찾았는데 분석 실패

**원인:** 이미지가 너무 크거나 형식 문제

**해결:**
```python
# Pillow로 이미지 리사이즈
from PIL import Image
import io

# 이미지 크기 제한 (예: 2048x2048)
img = Image.open(io.BytesIO(response.content))
img.thumbnail((2048, 2048))
```

---

## 📈 성능 비교

| 방식 | 정확도 | 속도 | 비용 |
|------|--------|------|------|
| **GPT-4o Vision** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | $$$ |
| GPT-4o Text | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | $$ |
| GPT-4o-mini Text | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | $ |

**추천:**
- 이미지 공고 → `crawler_vision.py` (GPT-4o Vision)
- 텍스트 공고 → `crawler.py` (GPT-4o-mini)

---

## 🔄 자동화

### Windows Task Scheduler

```
작업 이름: 장학금 크롤러
트리거: 매일 오전 9시
작업: python C:\path\to\crawler\crawler_vision.py
```

### Linux/Mac Cron

```bash
crontab -e

# 매일 오전 9시 실행
0 9 * * * cd /path/to/crawler && python crawler_vision.py >> crawler_vision.log 2>&1
```

---

## ⚠️ 주의사항

### 1. API 비용
- GPT-4o Vision은 GPT-4o-mini보다 **약 10배** 비쌈
- 크롤링 전 예상 비용 계산 필수

### 2. 크롤링 윤리
- 학교 서버 부하 고려
- `DELAY_SECONDS` 최소 3초 이상
- robots.txt 준수

### 3. 개인정보 보호
- 크롤링한 데이터 보안 주의
- 민감 정보 필터링

---

## 📞 지원

문제가 발생하면:
1. `test_crawler.py`로 환경 테스트
2. 에러 로그 확인
3. GitHub Issues 등록

---

**Happy Crawling! 🎓✨**

