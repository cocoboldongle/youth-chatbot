#!/bin/bash

# 청소년 챗봇 - Streamlit Cloud 배포 준비 스크립트

echo "🚀 Streamlit Cloud 배포 준비 시작..."

# 1. 필수 파일 확인
echo "📋 1단계: 필수 파일 확인 중..."
required_files=(
    "app.py"
    "chatbot_logic.py"
    "persona_ui.py"
    "safety_agent_simplified.py"
    "ui_components.py"
    "requirements.txt"
    "README.md"
    ".gitignore"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file (누락!)"
        exit 1
    fi
done

# 2. 프롬프트 파일 확인
echo "📝 2단계: 프롬프트 파일 확인 중..."
for i in {1..10}; do
    if [ "$i" -eq 9 ]; then
        file="prompt9_persona.txt"
    else
        file="prompt${i}.txt"
    fi
    
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file (누락!)"
        exit 1
    fi
done

# 3. API 키 하드코딩 확인
echo "🔒 3단계: API 키 하드코딩 확인 중..."
if grep -r "sk-proj-" *.py > /dev/null 2>&1; then
    echo "  ❌ 경고: 하드코딩된 API 키 발견!"
    echo "     파일을 수정하고 다시 실행하세요."
    exit 1
else
    echo "  ✅ API 키 하드코딩 없음"
fi

# 4. .streamlit 폴더 확인
echo "⚙️  4단계: Streamlit 설정 확인 중..."
if [ -f ".streamlit/config.toml" ]; then
    echo "  ✅ .streamlit/config.toml"
else
    echo "  ❌ .streamlit/config.toml (누락!)"
    exit 1
fi

# 5. Git 저장소 확인
echo "📦 5단계: Git 저장소 확인 중..."
if [ -d ".git" ]; then
    echo "  ✅ Git 저장소 초기화됨"
else
    echo "  ℹ️  Git 저장소가 없습니다. 다음 명령어로 초기화하세요:"
    echo "     git init"
    echo "     git add ."
    echo "     git commit -m 'Initial commit'"
fi

echo ""
echo "✅ 모든 준비 완료!"
echo ""
echo "📋 다음 단계:"
echo "1. GitHub에 저장소 생성"
echo "2. 로컬 저장소를 GitHub에 푸시:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/youth-chatbot.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. Streamlit Cloud (https://streamlit.io/cloud)에서 배포:"
echo "   - New app 클릭"
echo "   - GitHub 저장소 선택"
echo "   - Secrets에 OPENAI_API_KEY 추가"
echo "   - Deploy 클릭"
echo ""
echo "상세 가이드: DEPLOYMENT_GUIDE.md 참고"
