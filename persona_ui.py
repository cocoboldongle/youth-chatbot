"""
페르소나 선택 UI - APA 권고사항 반영 최종판
"""

import streamlit as st


PERSONAS = {
    "detective": {
        "name": "분석적 탐정형",
        "emoji": "🕵️",
        "description": "논리적이고 체계적인 대화",
        "features": [
            "'증거 찾기' 단계와 절차",
            "논리적 사고 재구조화",
            "체계적인 질문"
        ]
    },
    "friend": {
        "name": "따뜻한 친구형",
        "emoji": "💕",
        "description": "공감적이고 따뜻한 대화",
        "features": [
            "감정 표현 어려운 청소년에게 효과적",
            "또래 기반 정서적 지지",
            "친근한 말투"
        ]
    },
    "cool": {
        "name": "쿨한 형·누나형",
        "emoji": "😎",
        "description": "현실적이고 유머러스한 대화",
        "features": [
            "편안한 분위기",
            "유머로 긴장 완화",
            "솔직한 피드백"
        ]
    },
    "coach": {
        "name": "차분한 코치형",
        "emoji": "🧘",
        "description": "안정적이고 신뢰감 있는 대화",
        "features": [
            "정서적 안정감 제공",
            "존중하는 태도",
            "천천히 진행"
        ]
    }
}


def render_chatbot_purpose():
    """챗봇 목적 설명 - APA 권고 1번 반영"""
    
    st.markdown("---")
    
    # 타이틀
    st.markdown("""
    <h1 style='text-align: center; color: #667eea; font-size: 32px;'>
        🌱 청소년 인지 재구조화 챗봇
    </h1>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 명확한 목적 설명 (APA 권고 1)
    st.info("""
**📌 이 챗봇은 무엇인가요?**

이것은 **교육 및 자기돌봄 도구**입니다. 전문 심리치료가 **아닙니다**.

- ✅ **목적:** 인지행동치료(CBT) 기법을 활용한 자기 탐색 도구
- ✅ **역할:** 생각과 감정 패턴을 인식하도록 돕는 보조 도구
- ❌ **아닌 것:** 심리 상담, 진단, 치료의 대체 수단
    """)
    
    # 주요 기능
    st.markdown("""
**🎯 주요 기능:**
- **Stage 1:** 힘든 상황과 감정 탐색
- **Stage 2:** 인지왜곡 패턴 발견  
- **Stage 3:** 균형잡힌 생각으로 재구조화

**💡 기대 효과:**
- 자신의 생각 패턴에 대한 인식 향상
- 부정적 감정 조절 능력 개선
- 문제 해결 능력 향상
- 자기 이해 및 성찰 능력 증진
    """)


def render_ethical_notice_apa():
    """윤리적 안내문 - APA 8가지 권고사항 반영"""
    
    st.markdown("---")
    
    # 1. 심리치료 대체 금지 (APA 권고 1)
    st.error("""
### 🚫 이 챗봇이 할 수 없는 것

**이 AI 챗봇은 절대로 다음을 대체할 수 없습니다:**

❌ **자격을 갖춘 심리상담사나 정신건강 전문가**  
❌ **심리 진단이나 치료**  
❌ **응급 위기 개입**  
❌ **약물 처방이나 의학적 조언**

**⚠️ 이 챗봇은 AI입니다. 진짜 사람이 아닙니다.**
- AI는 당신을 진정으로 이해하거나 공감할 수 없습니다
- AI는 복잡한 정신건강 문제를 다룰 수 없습니다
- AI는 실수를 하고 부정확한 정보를 줄 수 있습니다
    """)
    
    # 2. 건강하지 않은 의존 방지 (APA 권고 2)
    st.warning("""
### ⚠️ AI 의존성 주의

**과도한 사용 경고:**

이 챗봇에 지나치게 의존하지 마세요. 다음과 같은 경우 사용을 중단하세요:

- 🚨 하루 1시간 이상 대화하는 경우
- 🚨 AI를 진짜 친구처럼 느끼기 시작한 경우  
- 🚨 현실 친구보다 AI와 대화하는 것을 선호하는 경우
- 🚨 중요한 결정을 AI에게만 의존하는 경우

**건강한 사용 방법:**
- ✅ 하루 20-30분 이내로 제한
- ✅ 실제 사람과의 대화를 우선시
- ✅ AI는 보조 도구일 뿐임을 기억
    """)
    
    # 3. 응급 상황 안내 (APA 권고 1, 5)
    st.error("""
### 🚨 응급 상황 - 즉시 연락하세요!

**다음과 같은 생각이나 계획이 있다면 지금 바로 전화하세요:**

- 자해하고 싶은 생각
- 자살하고 싶은 생각  
- 타인을 해치고 싶은 생각
- 심각한 공황 증상

📞 **24시간 긴급 연락처:**
- **정신건강위기상담전화: 1577-0199** (24시간)
- **청소년 전화: 1388** (24시간)
- **자살예방상담전화: 1393** (24시간)
- **응급: 119**

이런 상황에서 **AI 챗봇에 의존하지 마세요**. 반드시 전문가에게 연락하세요.
    """)
    
    # 4. 개인정보 보호 (APA 권고 3)
    st.info("""
### 🔒 개인정보 보호 안내

**데이터 수집 및 사용:**

- 📝 대화 내용은 연구 목적으로 **익명화**되어 저장됩니다
- 🔐 모든 데이터는 **암호화**되어 보호됩니다
- 🚫 개인 식별 정보는 **제3자와 공유되지 않습니다**
- 📊 통계 분석 목적으로만 사용됩니다

**주의사항:**
- ⚠️ 주민등록번호, 주소, 전화번호 등 개인정보를 입력하지 마세요
- ⚠️ 타인의 개인정보도 공유하지 마세요
- ⚠️ 완벽한 개인정보 보호를 보장할 수 없습니다
    """)
    
    # 5. AI의 한계 및 편향 (APA 권고 4)
    st.warning("""
### 🤖 AI의 한계와 위험

**이 AI는 완벽하지 않습니다:**

1. **환각(Hallucination):** AI가 그럴듯하지만 틀린 정보를 제공할 수 있습니다
2. **편향(Bias):** 성별, 인종, 문화에 대한 편향이 있을 수 있습니다
3. **맥락 이해 부족:** 복잡한 상황을 완전히 이해하지 못합니다
4. **일관성 부족:** 같은 질문에 다른 답변을 할 수 있습니다

**비판적으로 사용하세요:**
- 🧠 AI의 답변을 무조건 믿지 마세요
- 🧠 이상하거나 해로운 조언은 따르지 마세요
- 🧠 최종 판단은 항상 **본인 스스로** 해야 합니다
    """)
    
    # 6. 취약 계층 보호 (APA 권고 5)
    st.info("""
### 👨‍👩‍👧‍👦 부모님과 보호자께

**청소년은 특별한 보호가 필요합니다:**

이 챗봇 사용 시 다음을 권장합니다:

✅ **사용 전:** 자녀와 함께 이 안내문을 읽어주세요  
✅ **사용 중:** 주기적으로 사용 시간과 내용을 확인해주세요  
✅ **사용 후:** 자녀의 행동이나 감정 변화를 관찰해주세요

**주의 신호:**
- 챗봇 사용 시간이 급격히 증가
- 현실 친구와의 교류 감소
- 감정 기복이 심해짐
- 현실과 AI 구분이 모호해짐

이런 신호가 보이면 즉시 사용을 중단하고 전문가와 상담하세요.
    """)


def render_informed_consent_apa():
    """사용 동의서 - APA 권고 반영"""
    
    st.markdown("---")
    
    st.info("""
### 📋 사용 동의사항 (반드시 읽어주세요)

**이 챗봇을 사용하기 전에 다음을 확인하고 동의해야 합니다:**

#### ✅ 1. 챗봇의 한계 이해
- [ ] 이 챗봇은 **AI 도구**이며 전문 상담이 아님을 이해했습니다
- [ ] 이 챗봇은 **진단, 치료, 처방을 할 수 없음**을 알고 있습니다
- [ ] AI의 답변에 **오류나 편향이 있을 수 있음**을 이해했습니다

#### ✅ 2. 응급 상황 대처
- [ ] 위기 상황 시 **챗봇이 아닌 전문 기관**에 연락할 것을 약속합니다
- [ ] 응급 연락처(1577-0199, 1388, 119)를 알고 있습니다

#### ✅ 3. 건강한 사용
- [ ] 하루 **30분 이내**로 사용을 제한하겠습니다
- [ ] AI에 **과도하게 의존하지 않을** 것을 약속합니다
- [ ] **실제 인간 관계**를 우선시하겠습니다

#### ✅ 4. 개인정보 보호
- [ ] 대화 내용이 **익명 처리되어 연구에 사용될 수 있음**을 동의합니다
- [ ] **민감한 개인정보를 입력하지 않을** 것을 약속합니다
- [ ] 완벽한 개인정보 보호가 **보장되지 않음**을 이해했습니다

#### ✅ 5. 부모/보호자 동의 (만 18세 미만)
- [ ] 부모님 또는 보호자가 이 내용을 알고 있습니다
- [ ] 부모님 또는 보호자가 사용을 **허락**했습니다

#### ✅ 6. 언제든 중단 가능
- [ ] 언제든지 **대화를 중단**할 수 있음을 알고 있습니다
- [ ] 불편하거나 해로운 내용이 있으면 **즉시 사용을 멈출** 것입니다
    """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 최종 동의 체크박스
    consent = st.checkbox(
        "✅ 위의 모든 내용을 읽고 완전히 이해했으며, 이에 동의합니다.",
        key="informed_consent"
    )
    
    # 추가 확인
    if consent:
        age_confirm = st.radio(
            "나이를 확인해주세요:",
            ["만 18세 이상", "만 18세 미만 (부모/보호자 동의 받음)"],
            key="age_confirm"
        )
        
        return consent and age_confirm is not None
    
    return False


def render_ai_literacy_tips():
    """AI 리터러시 교육 (APA 권고 6)"""
    
    with st.expander("💡 AI 똑똑하게 사용하는 법 (꼭 읽어보세요!)"):
        st.markdown("""
### 📚 AI를 안전하게 사용하는 방법

#### 1️⃣ AI가 뭔가요?
- 🤖 AI는 많은 데이터로 학습한 컴퓨터 프로그램입니다
- 🤖 사람처럼 보이지만 진짜 사람이 아닙니다
- 🤖 감정이나 의식이 없습니다

#### 2️⃣ AI의 문제점
- ⚠️ **환각:** 그럴듯한 거짓말을 할 수 있습니다
- ⚠️ **편향:** 특정 집단에 대한 차별적 답변을 할 수 있습니다
- ⚠️ **맥락 부족:** 상황을 완전히 이해하지 못합니다

#### 3️⃣ 안전하게 사용하는 법
- ✅ AI 답변을 비판적으로 생각하세요
- ✅ 이상한 답변은 무시하세요
- ✅ 중요한 결정은 사람에게 물어보세요
- ✅ 실제 친구와 가족을 우선하세요

#### 4️⃣ 이럴 땐 바로 멈추세요
- 🛑 AI가 위험한 행동을 권유할 때
- 🛑 AI에 너무 의존하게 될 때
- 🛑 기분이 더 나빠질 때
- 🛑 현실과 혼동될 때

#### 5️⃣ 도움이 필요하면
- 📞 부모님, 선생님, 상담사에게 이야기하세요
- 📞 친구에게 털어놓으세요
- 📞 전문 기관에 연락하세요
        """)


def render_persona_selection():
    """페르소나 선택 화면 - APA 권고사항 통합"""
    
    # 1. 챗봇 목적 설명
    render_chatbot_purpose()
    
    # 2. 윤리적 안내문 (APA 8가지 권고)
    render_ethical_notice_apa()
    
    # 3. AI 리터러시 교육
    render_ai_literacy_tips()
    
    # 4. 사용 동의
    consent = render_informed_consent_apa()
    
    # 동의하지 않으면 페르소나 선택 불가
    if not consent:
        st.warning("⚠️ 계속하려면 위 내용을 모두 읽고 동의해주세요.")
        return None
    
    # 5. 페르소나 선택
    st.markdown("---")
    st.success("✅ 동의 완료! 이제 대화 스타일을 선택하세요.")
    
    st.markdown("""
    <div style='text-align: center; margin: 40px 0 30px 0;'>
        <h1 style='font-size: 32px; font-weight: 700; 
                   background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                   -webkit-background-clip: text;
                   -webkit-text-fill-color: transparent;
                   margin-bottom: 10px;'>
            🎭 대화 스타일 선택
        </h1>
        <p style='font-size: 16px; color: #666;'>
            나에게 가장 편한 대화 스타일을 골라주세요
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 2x2 그리드
    col1, col2 = st.columns(2)
    
    selected = None
    
    with col1:
        st.markdown(f"""
        <div style='background: white; border-radius: 15px; padding: 25px; 
                    margin: 10px 0; box-shadow: 0 4px 20px rgba(0,0,0,0.08);'>
            <div style='font-size: 48px; text-align: center; margin-bottom: 15px;'>
                {PERSONAS['detective']['emoji']}
            </div>
            <div style='font-size: 20px; font-weight: 700; text-align: center; margin-bottom: 10px;'>
                {PERSONAS['detective']['name']}
            </div>
            <div style='font-size: 14px; color: #666; text-align: center; margin-bottom: 15px;'>
                {PERSONAS['detective']['description']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🕵️ 이 스타일 선택", key="det", use_container_width=True):
            selected = "detective"
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style='background: white; border-radius: 15px; padding: 25px; 
                    margin: 10px 0; box-shadow: 0 4px 20px rgba(0,0,0,0.08);'>
            <div style='font-size: 48px; text-align: center; margin-bottom: 15px;'>
                {PERSONAS['cool']['emoji']}
            </div>
            <div style='font-size: 20px; font-weight: 700; text-align: center; margin-bottom: 10px;'>
                {PERSONAS['cool']['name']}
            </div>
            <div style='font-size: 14px; color: #666; text-align: center; margin-bottom: 15px;'>
                {PERSONAS['cool']['description']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("😎 이 스타일 선택", key="cool", use_container_width=True):
            selected = "cool"
    
    with col2:
        st.markdown(f"""
        <div style='background: white; border-radius: 15px; padding: 25px; 
                    margin: 10px 0; box-shadow: 0 4px 20px rgba(0,0,0,0.08);'>
            <div style='font-size: 48px; text-align: center; margin-bottom: 15px;'>
                {PERSONAS['friend']['emoji']}
            </div>
            <div style='font-size: 20px; font-weight: 700; text-align: center; margin-bottom: 10px;'>
                {PERSONAS['friend']['name']}
            </div>
            <div style='font-size: 14px; color: #666; text-align: center; margin-bottom: 15px;'>
                {PERSONAS['friend']['description']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("💕 이 스타일 선택", key="friend", use_container_width=True):
            selected = "friend"
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style='background: white; border-radius: 15px; padding: 25px; 
                    margin: 10px 0; box-shadow: 0 4px 20px rgba(0,0,0,0.08);'>
            <div style='font-size: 48px; text-align: center; margin-bottom: 15px;'>
                {PERSONAS['coach']['emoji']}
            </div>
            <div style='font-size: 20px; font-weight: 700; text-align: center; margin-bottom: 10px;'>
                {PERSONAS['coach']['name']}
            </div>
            <div style='font-size: 14px; color: #666; text-align: center; margin-bottom: 15px;'>
                {PERSONAS['coach']['description']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🧘 이 스타일 선택", key="coach", use_container_width=True):
            selected = "coach"
    
    return selected


def display_selected_persona_info(persona_id):
    """선택된 페르소나 정보 표시 - 스타일 변경 버튼만 제공"""
    
    # 페르소나 정보는 ui_components.py에서 표시하므로
    # 여기서는 스타일 변경 버튼만 제공
    
    # AI 리마인더
    st.sidebar.markdown("---")
    st.sidebar.info("""
**🤖 기억하세요:**
- 이것은 AI입니다
- 30분 이내로 사용
- 과도한 의존 주의
    """)
    
    st.sidebar.markdown("---")
    
    # 스타일 변경 버튼
    return st.sidebar.button("🔄 스타일 변경", key="change_persona", use_container_width=True)
