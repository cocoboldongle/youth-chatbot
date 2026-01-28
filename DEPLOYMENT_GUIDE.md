# 🚀 Streamlit Community Cloud 배포 가이드

## 📋 준비물

1. GitHub 계정
2. OpenAI API 키
3. 이 프로젝트의 모든 파일

---

## 1️⃣ GitHub 저장소 생성

### 1.1 GitHub에 저장소 만들기

1. [GitHub](https://github.com)에 로그인
2. 우측 상단 `+` 버튼 → `New repository` 클릭
3. 저장소 정보 입력:
   - Repository name: `youth-chatbot` (원하는 이름)
   - Description: `청소년 인지 재구조화 챗봇`
   - Public 선택 (Streamlit Community Cloud는 Public 저장소 필요)
   - `Add a README file` 체크 해제 (우리가 직접 추가할 것)
4. `Create repository` 클릭

### 1.2 로컬에서 Git 초기화 및 업로드

```bash
# 프로젝트 폴더로 이동
cd /path/to/your/project

# Git 초기화
git init

# 모든 파일 추가
git add .

# 첫 커밋
git commit -m "Initial commit: Youth chatbot"

# GitHub 저장소 연결 (본인의 저장소 URL로 변경)
git remote add origin https://github.com/YOUR_USERNAME/youth-chatbot.git

# 업로드
git branch -M main
git push -u origin main
```

### 1.3 파일 구조 확인

GitHub 저장소에 다음 파일들이 업로드되었는지 확인:

```
✅ app.py
✅ chatbot_logic.py
✅ persona_ui.py
✅ safety_agent_simplified.py
✅ ui_components.py
✅ prompt1.txt
✅ prompt2.txt
✅ prompt3.txt
✅ prompt4.txt
✅ prompt5.txt
✅ prompt6.txt
✅ prompt7.txt
✅ prompt8.txt
✅ prompt9_persona.txt
✅ prompt10.txt
✅ requirements.txt
✅ README.md
✅ .gitignore
✅ .streamlit/config.toml
```

❌ 다음 파일들은 절대 업로드하지 마세요:
- `.env` (API 키 포함)
- `__pycache__/`
- `*.pyc`
- `high_risk_logs.json`

---

## 2️⃣ Streamlit Community Cloud 설정

### 2.1 Streamlit Cloud 계정 생성

1. [Streamlit Community Cloud](https://streamlit.io/cloud) 접속
2. `Sign up` 클릭
3. GitHub 계정으로 로그인 (OAuth 인증)
4. 필요한 권한 승인

### 2.2 새 앱 배포

1. Streamlit Cloud 대시보드에서 `New app` 클릭
2. 배포 설정:

   **Repository, branch, and file:**
   - Repository: `YOUR_USERNAME/youth-chatbot` 선택
   - Branch: `main`
   - Main file path: `app.py`

   **App URL (optional):**
   - 원하는 URL 입력 (예: `youth-chatbot-kr`)
   - 최종 URL: `https://youth-chatbot-kr.streamlit.app`

3. `Advanced settings` 클릭

### 2.3 Secrets 설정 (중요!)

**Secrets** 섹션에 다음 내용 입력:

```toml
OPENAI_API_KEY = "sk-your-actual-openai-api-key-here"
```

⚠️ **주의사항:**
- API 키는 따옴표로 감싸야 합니다
- 절대 GitHub에 커밋하지 마세요
- Streamlit Secrets는 암호화되어 저장됩니다

### 2.4 Python 버전 설정 (선택사항)

**Advanced settings**에서:
```toml
[server]
headless = true

[python]
version = "3.11"
```

### 2.5 배포 시작

1. `Deploy!` 버튼 클릭
2. 배포 진행 상황 확인 (약 3-5분 소요)
3. 로그에서 에러 확인

---

## 3️⃣ 배포 후 확인

### 3.1 앱 작동 테스트

1. 배포 완료 후 제공된 URL 접속
2. 다음 기능 테스트:
   - ✅ 페르소나 선택
   - ✅ 사용자 정보 입력
   - ✅ 대화 시작
   - ✅ 안전 모니터링
   - ✅ 대화 내보내기

### 3.2 에러 처리

**에러 발생 시:**

1. **ModuleNotFoundError:**
   ```bash
   # requirements.txt에 패키지 추가
   git add requirements.txt
   git commit -m "Add missing package"
   git push
   ```

2. **API Key Error:**
   - Streamlit Cloud → Your app → Settings → Secrets
   - API 키 재확인 및 수정

3. **File Not Found (prompt files):**
   ```bash
   # 프롬프트 파일 확인
   ls -la prompt*.txt
   
   # 없으면 다시 추가
   git add prompt*.txt
   git commit -m "Add prompt files"
   git push
   ```

---

## 4️⃣ 업데이트 및 유지보수

### 4.1 코드 수정 후 재배포

```bash
# 파일 수정 후
git add .
git commit -m "Update: 수정 내용 설명"
git push

# Streamlit Cloud가 자동으로 재배포합니다
```

### 4.2 Secrets 업데이트

1. Streamlit Cloud → Your app → Settings
2. Secrets 수정
3. `Save` 클릭
4. 앱 자동 재시작

### 4.3 로그 확인

1. Streamlit Cloud → Your app
2. `Manage app` → `Logs`
3. 실시간 로그 확인

---

## 5️⃣ 리소스 제한 및 최적화

### Streamlit Community Cloud 제한사항

- ✅ **무료**
- ⚠️ **리소스:** 1GB RAM, 0.5 CPU cores
- ⚠️ **스토리지:** 임시 파일만 저장 가능
- ⚠️ **세션:** 유휴 상태 시 자동 종료
- ⚠️ **동시 사용자:** 제한 있음 (정확한 수치 미공개)

### 최적화 팁

1. **불필요한 패키지 제거**
   ```txt
   # requirements.txt 최소화
   streamlit>=1.28.0
   openai>=1.0.0
   ```

2. **대화 내역 제한**
   ```python
   # chatbot_logic.py에서
   MAX_HISTORY = 20  # 최근 20턴만 유지
   ```

3. **세션 타임아웃 설정**
   ```python
   # 30분 이상 사용 시 경고
   if elapsed_time > 30:
       st.warning("권장 사용 시간 초과")
   ```

---

## 6️⃣ 보안 및 개인정보 보호

### 6.1 API 키 보안

✅ **올바른 방법:**
- Streamlit Secrets 사용
- 환경변수로 관리

❌ **절대 하지 말 것:**
- 코드에 직접 입력
- GitHub에 커밋
- 공개 공유

### 6.2 사용자 데이터

- 대화 내역은 **세션에만 저장** (새로고침 시 삭제)
- 로그 파일은 **로컬에만 저장** (클라우드에는 저장 안 됨)
- 개인정보 수집 최소화

---

## 7️⃣ 트러블슈팅

### 문제: 앱이 로딩되지 않음

**해결:**
1. 브라우저 캐시 삭제
2. 시크릿 모드에서 접속
3. Streamlit Cloud에서 앱 재시작

### 문제: API 키 오류

**해결:**
1. Secrets 확인:
   ```toml
   OPENAI_API_KEY = "sk-..."
   ```
2. API 키 유효성 확인 (OpenAI 대시보드)
3. 사용량 한도 확인

### 문제: 프롬프트 파일 없음

**해결:**
```bash
# 저장소에 파일 있는지 확인
ls -la prompt*.txt

# 없으면 추가
git add prompt*.txt
git commit -m "Add prompt files"
git push
```

### 문제: 메모리 부족

**해결:**
1. 대화 내역 제한
2. 불필요한 변수 정리
3. 필요시 유료 플랜 고려

---

## 8️⃣ 추가 리소스

### 공식 문서
- [Streamlit Cloud 문서](https://docs.streamlit.io/streamlit-community-cloud)
- [Secrets 관리](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app/connect-to-data-sources/secrets-management)

### 커뮤니티
- [Streamlit 포럼](https://discuss.streamlit.io/)
- [GitHub Issues](https://github.com/streamlit/streamlit/issues)

---

## ✅ 배포 완료 체크리스트

배포 전 마지막 확인:

- [ ] GitHub 저장소에 모든 파일 업로드 완료
- [ ] `.env` 파일이 `.gitignore`에 포함되어 있음
- [ ] OpenAI API 키 준비됨
- [ ] Streamlit Cloud 계정 생성
- [ ] Secrets에 API 키 입력
- [ ] 배포 완료 및 테스트
- [ ] 페르소나 선택 작동
- [ ] 대화 기능 작동
- [ ] 안전 모니터링 작동
- [ ] 대화 내보내기 작동

---

## 🎉 성공!

축하합니다! 이제 청소년 인지 재구조화 챗봇이 24시간 운영됩니다.

**최종 URL:** `https://your-app-name.streamlit.app`

이 URL을 공유하여 다른 사람들도 사용할 수 있습니다.

---

## 💡 다음 단계

1. **도메인 연결** (선택사항)
   - 커스텀 도메인 설정 가능
   - Streamlit Cloud 유료 플랜 필요

2. **분석 추가** (선택사항)
   - Google Analytics 연동
   - 사용 통계 수집

3. **기능 개선**
   - 사용자 피드백 수집
   - 정기적 업데이트

---

**문제가 발생하면 Streamlit 포럼이나 GitHub Issues에 질문하세요!**
