# 🤖 GitHub Actions 자동 크롤링 설정 가이드

GitHub Actions를 사용하여 매일 자동으로 장학금 정보를 크롤링하는 방법입니다.

---

## 📋 개요

### 워크플로우 구성

1. **daily_crawl.yml** - 매일 밤 12시 자동 실행
2. **manual_crawl.yml** - 수동 실행 (버튼 클릭)

### 실행 시간

- **자동 실행:** 매일 00:00 (한국 시간)
- **수동 실행:** 언제든지 GitHub에서 버튼 클릭

---

## 🔑 Step 1: GitHub Secrets 설정

### 1.1 저장소 Settings 이동

1. GitHub 저장소 접속: https://github.com/SunWoo1213/ScholarShipRadar
2. 상단 메뉴에서 **Settings** 클릭
3. 왼쪽 메뉴에서 **Secrets and variables** → **Actions** 클릭

### 1.2 Secrets 추가

**New repository secret** 버튼을 클릭하여 다음 secrets를 추가:

#### ✅ SUPABASE_URL

```
Name: SUPABASE_URL
Secret: https://xxxxxxxxxxxxx.supabase.co
```

**어디서 찾나요?**
- Supabase Dashboard → Settings → API → Project URL

#### ✅ SUPABASE_KEY

```
Name: SUPABASE_KEY
Secret: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh4eHh4eHh4eHh4eHgiLCJyb2xlIjoic2VydmljZV9yb2xlIiwiaWF0IjoxNzAwMDAwMDAwLCJleHAiOjIwMTU1NzYwMDB9.yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy
```

**⚠️ 중요:** `service_role` key를 사용하세요 (anon key 아님!)

**어디서 찾나요?**
- Supabase Dashboard → Settings → API → service_role key

#### ✅ OPENAI_API_KEY

```
Name: OPENAI_API_KEY
Secret: sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**어디서 찾나요?**
- https://platform.openai.com/api-keys
- Create new secret key

#### ✅ TARGET_URL

```
Name: TARGET_URL
Secret: https://web.kangnam.ac.kr/board/scholarship
```

**본인의 학교 장학금 게시판 URL로 변경하세요!**

#### ✅ BASE_DOMAIN (선택사항)

```
Name: BASE_DOMAIN
Secret: https://web.kangnam.ac.kr
```

### 1.3 Secrets 확인

모든 secrets가 추가되었는지 확인:

```
✅ SUPABASE_URL
✅ SUPABASE_KEY
✅ OPENAI_API_KEY
✅ TARGET_URL
✅ BASE_DOMAIN
```

---

## 🚀 Step 2: 워크플로우 파일 푸시

### 2.1 파일 생성 확인

다음 파일들이 생성되었는지 확인:

```
.github/
└── workflows/
    ├── daily_crawl.yml      # 자동 실행
    └── manual_crawl.yml     # 수동 실행
```

### 2.2 GitHub에 푸시

```bash
git add .github/
git commit -m "GitHub Actions 워크플로우 추가: 자동 크롤링"
git push
```

---

## ⏰ Step 3: 자동 실행 확인

### 3.1 워크플로우 활성화 확인

1. GitHub 저장소 → **Actions** 탭
2. 왼쪽에 다음 워크플로우가 보여야 함:
   - 🤖 Daily Scholarship Crawler
   - 🔧 Manual Crawler (On Demand)

### 3.2 실행 시간

**자동 실행:**
- 매일 00:00 (한국 시간)
- UTC 기준: 15:00 (전날)

**Cron 표현식:**
```yaml
cron: '0 15 * * *'  # UTC 15:00 = KST 00:00
```

---

## 🔧 Step 4: 수동 실행 (테스트)

### 방법 1: GitHub 웹사이트에서

1. GitHub 저장소 → **Actions** 탭
2. 왼쪽에서 **Manual Crawler (On Demand)** 클릭
3. 오른쪽 **Run workflow** 버튼 클릭
4. 옵션 설정:
   - 크롤링할 최대 공고 수: `50` (기본값)
   - 요청 간 딜레이: `3` (초)
5. **Run workflow** 클릭

### 방법 2: GitHub CLI

```bash
gh workflow run manual_crawl.yml
```

---

## 📊 Step 5: 실행 결과 확인

### 5.1 실행 로그 보기

1. GitHub 저장소 → **Actions** 탭
2. 실행 중이거나 완료된 워크플로우 클릭
3. 각 단계별 로그 확인:
   - 📥 Checkout repository
   - 🐍 Set up Python
   - 📦 Install dependencies
   - 🕷️ Run crawler

### 5.2 성공/실패 확인

**성공 시:**
```
✅ 크롤링 성공!
2025-11-27 15:00:00 - Daily crawling completed
```

**실패 시:**
```
❌ 크롤링 실패!
2025-11-27 15:00:00 - Daily crawling failed
```

---

## 🔍 문제 해결

### "Error: Process completed with exit code 1"

**원인:** Python 스크립트 실행 중 에러

**해결 방법:**
1. Actions 탭에서 실패한 워크플로우 클릭
2. "Run crawler" 단계의 로그 확인
3. 에러 메시지 확인:
   - API 키 오류
   - Supabase 연결 오류
   - OpenAI API 오류
   - 크롤링 대상 사이트 변경

### "Invalid API key"

**원인:** GitHub Secrets가 올바르지 않음

**해결 방법:**
1. Settings → Secrets → Actions
2. 각 Secret 값 재확인
3. 특히 `SUPABASE_KEY`는 `service_role` key인지 확인

### "Module not found"

**원인:** requirements.txt 설치 실패

**해결 방법:**
1. `crawler/requirements.txt` 파일 확인
2. 파일 경로가 올바른지 확인
3. 워크플로우 재실행

### Cron이 실행되지 않음

**원인:** GitHub Actions의 제한

**참고:**
- GitHub Free plan: Public 저장소만 무료
- Private 저장소: 월 2,000분 제한
- 정확한 시간이 아닐 수 있음 (±15분)

---

## ⚙️ 커스터마이징

### 실행 시간 변경

`daily_crawl.yml` 파일의 cron 수정:

```yaml
schedule:
  - cron: '0 9 * * *'  # UTC 09:00 = KST 18:00 (저녁 6시)
```

**Cron 표현식:**
```
분 시 일 월 요일
*  *  *  *  *

예시:
'0 15 * * *'  # 매일 15시 (UTC)
'0 9 * * 1'   # 매주 월요일 9시
'0 9 1 * *'   # 매월 1일 9시
```

**한국 시간으로 변환:**
- KST = UTC + 9시간
- KST 00:00 = UTC 15:00 (전날)
- KST 09:00 = UTC 00:00
- KST 18:00 = UTC 09:00

### 크롤링 옵션 변경

`daily_crawl.yml` 파일의 env 섹션 수정:

```yaml
env:
  MAX_ITEMS: 100        # 크롤링할 공고 수 증가
  DELAY_SECONDS: 5      # 딜레이 증가
```

### 주말에만 실행

```yaml
schedule:
  - cron: '0 15 * * 0,6'  # 일요일, 토요일만
```

### 알림 추가 (Slack, Discord 등)

워크플로우 마지막에 추가:

```yaml
- name: 📧 Send notification
  if: always()
  run: |
    curl -X POST https://hooks.slack.com/services/YOUR/WEBHOOK/URL \
    -H 'Content-Type: application/json' \
    -d '{"text":"크롤링 완료!"}'
```

---

## 💰 비용 안내

### GitHub Actions

**무료 플랜 (Public 저장소):**
- ✅ 무제한 실행 시간
- ✅ 무료!

**Private 저장소:**
- 월 2,000분 무료
- 매일 실행 시 약 5분 소요
- 월 150회 실행 가능 (충분함)

### OpenAI API

**GPT-4o Vision 사용 시:**
- 공고 1개당: ~$0.002
- 매일 50개: ~$0.10/일
- 월간 비용: ~$3/월

**절약 팁:**
- `MAX_ITEMS`를 줄이기 (예: 20개)
- 텍스트 공고는 GPT-4o-mini 사용 (저렴)

---

## 📝 모니터링

### 실행 히스토리 확인

1. Actions 탭 → 워크플로우 선택
2. 최근 실행 내역 확인
3. 성공/실패율 모니터링

### 이메일 알림 설정

GitHub Settings → Notifications:
- ✅ Actions → Email notifications

---

## 🎯 권장 사항

### 1. 초기 설정

1. **수동 실행으로 테스트**
   - Manual Crawler로 먼저 테스트
   - 에러 없는지 확인
   - Supabase에 데이터 저장되는지 확인

2. **자동 실행 활성화**
   - 테스트 성공 후 자동 실행 대기
   - 다음 날 Actions 탭에서 확인

### 2. 정기 점검

- **주 1회:** Actions 탭에서 실행 결과 확인
- **월 1회:** OpenAI API 사용량 확인
- **월 1회:** Supabase 데이터베이스 용량 확인

### 3. 에러 처리

- 연속 3일 실패 시 원인 파악
- API 키 만료 확인
- 크롤링 대상 사이트 구조 변경 확인

---

## 🔄 업데이트 방법

크롤러 코드 수정 후:

```bash
git add crawler/main.py
git commit -m "크롤러 로직 개선"
git push
```

다음 실행부터 자동으로 새 코드 사용됩니다!

---

## 📞 지원

문제가 발생하면:
1. Actions 탭에서 로그 확인
2. GitHub Issues에 질문 등록
3. Secrets 재확인

---

**Happy Automating! 🤖✨**

