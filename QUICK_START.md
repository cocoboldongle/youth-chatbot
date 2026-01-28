# 🚀 빠른 시작 가이드

## 5분 안에 배포하기

### 1️⃣ GitHub 저장소 생성 (2분)

1. [GitHub](https://github.com/new) 접속
2. 저장소 이름 입력: `youth-chatbot`
3. Public 선택
4. Create repository 클릭

### 2️⃣ 파일 업로드 (2분)

**옵션 A: GitHub 웹에서 직접 업로드**

1. GitHub 저장소 페이지에서 `Add file` > `Upload files` 클릭
2. 다음 파일들을 드래그 앤 드롭:
   - `app.py`
   - `chatbot_logic.py`
   - `persona_ui.py`
   - `safety_agent_simplified.py`
   - `ui_components.py`
   - `requirements.txt`
   - `README.md`
   - `.gitignore`
   - `prompt1.txt` ~ `prompt10.txt` (모든 프롬프트 파일)
3. `.streamlit` 폴더도 업로드 (폴더 생성 후 `config.toml` 업로드)
4. `Commit changes` 클릭

**옵션 B: Git 명령어 사용**

```bash
cd /path/to/files
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/youth-chatbot.git
git branch -M main
git push -u origin main
```

### 3️⃣ Streamlit Cloud 배포 (1분)

1. [Streamlit Cloud](https://streamlit.io/cloud) 접속
2. GitHub 계정으로 로그인
3. `New app` 클릭
4. 설정:
   - Repository: `youth-chatbot`
   - Branch: `main`
   - Main file: `app.py`
5. `Advanced settings` > `Secrets` 클릭
6. 다음 내용 붙여넣기:
   ```toml
   OPENAI_API_KEY = "sk-your-api-key-here"
   ```
7. `Deploy!` 클릭

### ✅ 완료!

3-5분 후 앱이 배포됩니다.

URL: `https://your-app-name.streamlit.app`

---

## 문제 해결

### ❌ "ModuleNotFoundError: No module named 'openai'"

→ `requirements.txt` 파일이 업로드되었는지 확인

### ❌ "API key not found"

→ Streamlit Cloud Settings > Secrets에 API 키 추가 확인

### ❌ "File not found: prompt1.txt"

→ 모든 프롬프트 파일 (prompt1.txt ~ prompt10.txt) 업로드 확인

### ❌ 앱이 계속 로딩 중

→ Streamlit Cloud 로그 확인 (Manage app > Logs)

---

## 추가 도움말

상세한 가이드는 `DEPLOYMENT_GUIDE.md` 참고

문제가 지속되면:
1. GitHub 저장소의 파일 목록 확인
2. Streamlit Cloud 로그 확인
3. [Streamlit 포럼](https://discuss.streamlit.io/) 검색

---

**배포 완료 후 반드시 테스트하세요:**
- ✅ 페르소나 선택
- ✅ 사용자 정보 입력
- ✅ 대화 시작
- ✅ 안전 모니터링
- ✅ 대화 내보내기
