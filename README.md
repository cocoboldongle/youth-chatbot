# 청소년 인지 재구조화 챗봇

청소년의 인지왜곡을 탐색하고 재구조화하는 AI 기반 상담 챗봇입니다.

## 🌟 주요 기능

- **4가지 페르소나**: 탐정형, 친구형, 쿨한 형, 코치형
- **3단계 인지 재구조화**:
  - Stage 1: 정보 수집
  - Stage 2: 인지왜곡 탐색
  - Stage 3: 재구조화
- **실시간 안전 모니터링**: 위기 상황 감지 및 개입
- **대화 내보내기**: JSON 형식으로 저장

## 🚀 배포 방법

### 1. Streamlit Community Cloud 배포

1. 이 저장소를 Fork하거나 Clone
2. [Streamlit Community Cloud](https://streamlit.io/cloud)에 로그인
3. "New app" 클릭
4. GitHub 저장소 연결
5. Secrets 설정:
   ```
   OPENAI_API_KEY = "your-api-key-here"
   ```
6. Deploy 클릭

### 2. 로컬 실행

```bash
# 저장소 클론
git clone <repository-url>
cd <repository-name>

# 가상환경 생성 (선택사항)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt

# 환경변수 설정
echo "OPENAI_API_KEY=your-api-key" > .env

# 실행
streamlit run app.py
```

## 📁 파일 구조

```
.
├── app.py                          # 메인 앱
├── chatbot_logic.py                # 챗봇 로직
├── persona_ui.py                   # 페르소나 UI
├── safety_agent_simplified.py      # 안전 모니터링
├── ui_components.py                # UI 컴포넌트
├── prompt1.txt ~ prompt10.txt      # 프롬프트 파일
├── requirements.txt                # 패키지 의존성
└── .streamlit/
    └── config.toml                 # Streamlit 설정
```

## ⚙️ 환경 변수

- `OPENAI_API_KEY`: OpenAI API 키 (필수)

## 🔒 개인정보 보호

- 사용자 데이터는 로컬에만 저장됨
- API 키는 절대 커밋하지 마세요
- `.env` 파일은 `.gitignore`에 포함되어 있습니다

## 📞 응급 연락처

- 정신건강위기상담: 1577-0199 (24시간)
- 자살예방상담: 1393 (24시간)
- 청소년 전화: 1388 (24시간)
- 응급: 119

## ⚠️ 면책 사항

이 챗봇은 교육 및 자기돌봄 도구입니다. 
심리치료, 진단, 처방을 대체할 수 없습니다.
심각한 문제가 있다면 전문가에게 연락하세요.

## 📄 라이선스

이 프로젝트는 교육 목적으로 제공됩니다.

## 🙏 기여

버그 리포트나 기능 제안은 Issues에 남겨주세요.
