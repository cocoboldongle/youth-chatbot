"""
청소년 인지 재구조화 챗봇 - UI 컴포넌트 (APA 권고사항 반영)
"""

import streamlit as st


def apply_custom_css():
    """커스텀 CSS 적용"""
    st.markdown("""
    <style>
    /* 전체 폰트 */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
    }
    
    /* 채팅 메시지 스타일 개선 */
    .stChatMessage {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    
    /* 입력창 스타일 */
    .stChatInputContainer {
        border-top: 2px solid #f0f2f6;
        padding-top: 1rem;
    }
    
    /* 버튼 스타일 개선 */
    .stButton > button {
        border-radius: 10px;
        font-weight: 500;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* 사이드바 스타일 */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
    }
    
    /* 폼 스타일 */
    .stForm {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    /* 제목 스타일 */
    h1 {
        color: #667eea;
        font-weight: 700;
    }
    
    h2, h3 {
        color: #764ba2;
        font-weight: 600;
    }
    
    /* 프로그레스 바 색상 */
    .stProgress > div > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    </style>
    """, unsafe_allow_html=True)


def render_user_info_form():
    """사용자 정보 수집 폼 렌더링"""
    st.title("🌱 청소년 인지 재구조화 챗봇")
    st.markdown("---")
    
    st.markdown("""
    ### 환영합니다! 👋
    
    이 프로그램은 여러분의 생각과 감정을 함께 탐색하고  
    더 긍정적인 방향으로 나아갈 수 있도록 도와드립니다.
    
    시작하기 전에 몇 가지 정보를 입력해주세요.
    """)
    
    st.markdown("---")
    
    with st.form("user_info_form"):
        st.subheader("📋 기본 정보")
        
        # 성별 선택
        gender = st.selectbox(
            "성별을 선택해주세요 *",
            ["선택하세요", "남성", "여성"],
            index=0
        )
        
        # 나이 입력
        age = st.number_input(
            "나이를 입력해주세요 (12-19세) *",
            min_value=12,
            max_value=19,
            value=15,
            step=1
        )
        
        # 하루 점수 선택
        st.markdown("### 💭 요즘 하루 점수")
        st.markdown("""
        **요즘 하루를 점수로 매기면 보통 몇 점쯤일까요?** *
        
        💡 힌트:
        - 0점: 괜찮음
        - 5점: 보통
        - 10점: 최악
        """)
        
        emotion_intensity = st.slider(
            "하루 점수",
            min_value=0,
            max_value=10,
            value=5,
            help="0(괜찮음) ~ 10(최악)"
        )
        
        # 점수 시각화
        if emotion_intensity <= 3:
            st.success("😌 괜찮은 상태")
        elif emotion_intensity <= 6:
            st.info("😐 보통 상태")
        else:
            st.warning("😰 힘든 상태")
        
        st.markdown("---")
        
        # 제출 버튼
        submitted = st.form_submit_button("✅ 정보 확인 및 시작하기", use_container_width=True)
        
        if submitted:
            # 필수 항목 확인
            if gender == "선택하세요":
                st.error("❌ 성별을 선택해주세요.")
                return None
            
            # 사용자 정보 반환
            return {
                'gender': gender,
                'age': age,
                'emotion_intensity': emotion_intensity
            }
    
    return None


def render_sidebar_profile(user_info):
    """사이드바에 사용자 프로필 렌더링 - APA 권고사항 반영"""
    with st.sidebar:
        st.markdown("### 👤 프로필")
        
        # 프로필 카드 스타일
        st.markdown(f"""
        <div style="
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        ">
            <p style="margin: 5px 0;"><strong>성별:</strong> {user_info['gender']}</p>
            <p style="margin: 5px 0;"><strong>나이:</strong> {user_info['age']}세</p>
            <p style="margin: 5px 0;"><strong>하루 점수:</strong> {user_info['emotion_intensity']}/10</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 하루 점수 상태 표시
        st.markdown("### 😊 하루 점수")
        intensity = user_info['emotion_intensity']
        if intensity <= 3:
            st.success("😌 괜찮은 상태")
        elif intensity <= 6:
            st.info("😐 보통 상태")
        else:
            st.warning("😰 힘든 상태")
        
        # 진행 바
        st.progress(intensity / 10)
        
        st.markdown("---")
        
        # 선택한 페르소나 표시
        if 'selected_persona' in st.session_state and st.session_state.selected_persona:
            st.markdown("### 🎭 대화 스타일")
            
            # 페르소나 정보 (persona_ui.py의 PERSONAS와 동일하게)
            PERSONAS = {
                "detective": {
                    "name": "분석적 탐정형",
                    "emoji": "🕵️",
                    "description": "논리적이고 체계적인 대화"
                },
                "friend": {
                    "name": "따뜻한 친구형",
                    "emoji": "💕",
                    "description": "공감적이고 따뜻한 대화"
                },
                "cool": {
                    "name": "쿨한 형·누나형",
                    "emoji": "😎",
                    "description": "현실적이고 유머러스한 대화"
                },
                "coach": {
                    "name": "차분한 코치형",
                    "emoji": "🧘",
                    "description": "안정적이고 신뢰감 있는 대화"
                }
            }
            
            selected = st.session_state.selected_persona
            if selected in PERSONAS:
                persona = PERSONAS[selected]
                st.markdown(f"**{persona['emoji']} {persona['name']}**")
                st.caption(persona['description'])
        
        st.markdown("---")
        
        # AI 리마인더 (APA 권고 2 - 의존성 방지)
        st.warning("""
**🤖 AI 사용 주의:**
- 30분 이내로 제한
- 과도한 의존 주의
- 이것은 AI입니다
        """)
        
        st.markdown("---")
        
        # 도움말
        with st.expander("💡 대화 팁"):
            st.markdown("""
            - 편안하게 생각을 말해주세요
            - 구체적으로 설명할수록 좋아요
            - 천천히 대화해도 괜찮아요
            - 언제든 멈출 수 있어요
            """)
        
        st.markdown("---")
        
        # 응급 연락처 (APA 권고 1, 5)
        with st.expander("🚨 응급 연락처"):
            st.markdown("""
            **위기 상황 시 즉시 연락:**
            
            📞 **정신건강위기상담**  
            ☎️ 1577-0199 (24시간)
            
            📞 **청소년 전화**  
            ☎️ 1388 (24시간)
            
            📞 **자살예방상담**  
            ☎️ 1393 (24시간)
            
            📞 **응급**  
            ☎️ 119
            
            ⚠️ AI에 의존하지 말고
            반드시 전문가에게 연락하세요!
            """)
        
        st.markdown("---")
        
        # 정보 수정 버튼
        return st.button("🔄 처음으로 돌아가기", use_container_width=True)


def render_chat_header(user_info):
    """채팅 헤더 렌더링 - APA 권고사항 반영"""
    st.title("💬 인지 재구조화 대화방")
    
    # 상단 안내 메시지
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
        text-align: center;
    ">
        <strong>{user_info['age']}세 친구</strong>와 함께하는 대화 시간입니다 ✨
    </div>
    """, unsafe_allow_html=True)
    
    # APA 권고 1 - 심리치료 대체 불가 리마인더
    st.error("""
**⚠️ 중요: 이것은 AI이며 전문 상담이 아닙니다**

- 🤖 이 챗봇은 **교육 및 자기돌봄 도구**입니다
- 🚫 심리치료, 진단, 처방을 **대체할 수 없습니다**
- 📞 심각한 문제가 있다면 **전문가에게 연락**하세요 (1577-0199)
    """)
    
    # APA 권고 2 - 건강하지 않은 의존 방지
    st.info("""
**💡 건강한 사용 가이드:**

- ⏱️ **권장 사용 시간:** 하루 20-30분 이내
- 🧑‍🤝‍🧑 **실제 사람과의 대화를 우선**하세요
- 🛑 **불편하면 즉시 중단**하세요
- 🧠 **최종 판단은 본인**이 하세요
    """)


def render_chat_messages(messages):
    """채팅 메시지 렌더링"""
    chat_container = st.container()
    
    with chat_container:
        for message in messages:
            if message["role"] == "assistant":
                with st.chat_message("assistant", avatar="🤖"):
                    st.markdown(message["content"])
            else:
                with st.chat_message("user", avatar="😊"):
                    st.markdown(message["content"])


def get_user_input():
    """사용자 입력 받기"""
    return st.chat_input("💭 메시지를 입력하세요...", key="user_input")


def check_usage_time_warning(session_start_time):
    """사용 시간 경고 (APA 권고 2)"""
    import datetime
    
    if session_start_time:
        elapsed_time = (datetime.datetime.now() - session_start_time).total_seconds() / 60
        
        if elapsed_time > 20:
            st.warning("""
            ⏰ **사용 시간 안내**
            
            20분 이상 사용 중입니다. 잠시 휴식하는 것은 어떨까요?
            - 눈을 쉬게 해주세요
            - 몸을 움직여보세요
            - 친구나 가족과 이야기해보세요
            """)
        
        if elapsed_time > 30:
            st.error("""
            🛑 **30분 경과**
            
            권장 사용 시간을 초과했습니다.
            지금 대화를 마무리하고 다음에 다시 만나요.
            """)
