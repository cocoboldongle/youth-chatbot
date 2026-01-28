"""
청소년 인지 재구조화 챗봇 - 메인 애플리케이션
"""

import streamlit as st
from ui_components import (
    apply_custom_css,
    render_user_info_form,
    render_sidebar_profile,
    render_chat_header,
    render_chat_messages,
    get_user_input
)
from chatbot_logic import (
    initialize_session_state,
    save_user_info,
    reset_session,
    initialize_chat_messages,
    process_user_input,
    export_conversation_to_json
)
from persona_ui import (
    render_persona_selection,
    display_selected_persona_info
)


def show_persona_selection_page():
    """페르소나 선택 페이지"""
    selected_persona = render_persona_selection()
    
    if selected_persona:
        # 페르소나 저장
        st.session_state.selected_persona = selected_persona
        st.session_state.persona_selected = True
        # 화면 전환
        st.rerun()


def show_user_info_page():
    """사용자 정보 수집 페이지"""
    user_info = render_user_info_form()
    
    if user_info is not None:
        # 정보 저장
        save_user_info(user_info)
        # 화면 전환
        st.rerun()


def show_chat_page():
    """채팅 페이지"""
    user_info = st.session_state.user_info
    
    # 사이드바 렌더링 및 초기화 버튼 처리
    if render_sidebar_profile(user_info):
        reset_session()
        st.rerun()
    
    # 페르소나 정보 표시 및 변경 버튼
    if display_selected_persona_info(st.session_state.get('selected_persona', 'friend')):
        # 페르소나 변경 요청
        st.session_state.persona_selected = False
        st.session_state.user_info_collected = False
        reset_session()
        st.rerun()
    
    # 사이드바에 다운로드 버튼 추가
    with st.sidebar:
        st.markdown("---")
        st.subheader("📥 대화 내보내기")
        
        if len(st.session_state.get('messages', [])) > 0:
            # JSON 데이터 생성
            json_data = export_conversation_to_json()
            
            # 파일명 생성
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversation_{timestamp}.json"
            
            # 다운로드 버튼
            st.download_button(
                label="💾 대화 내용 다운로드",
                data=json_data,
                file_name=filename,
                mime="application/json",
                help="현재까지의 대화 내용과 분석 결과를 JSON 파일로 다운로드합니다.",
                use_container_width=True
            )
            
            # 통계 표시
            stats = st.session_state.get('messages', [])
            user_messages = [m for m in stats if m['role'] == 'user']
            
            st.caption(f"📊 총 {len(user_messages)}턴의 대화")
            
            current_stage = st.session_state.get('current_stage', 'collection')
            stage_names = {
                'collection': 'Stage 1: 정보 수집',
                'analysis': 'Stage 2: 인지왜곡 탐색',
                'restructuring': 'Stage 3: 재구조화'
            }
            st.caption(f"📍 현재: {stage_names.get(current_stage, current_stage)}")
        else:
            st.info("💬 대화를 시작하면 다운로드할 수 있습니다.")
    
    # 채팅 헤더 렌더링
    render_chat_header(user_info)
    
    # 초기 환영 메시지 설정
    initialize_chat_messages(user_info)
    
    # 채팅 메시지 렌더링
    render_chat_messages(st.session_state.messages)
    
    # 사용자 입력 처리
    if prompt := get_user_input():
        # 사용자 입력 처리 및 응답 생성
        with st.spinner("생각 중..."):
            process_user_input(prompt, user_info)
        
        # 화면 새로고침
        st.rerun()


def main():
    """메인 함수"""
    # 페이지 설정
    st.set_page_config(
        page_title="청소년 인지 재구조화 챗봇",
        page_icon="🌱",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # 커스텀 CSS 적용
    apply_custom_css()
    
    # 세션 상태 초기화
    initialize_session_state()
    
    # 페르소나 선택 상태 초기화
    if 'persona_selected' not in st.session_state:
        st.session_state.persona_selected = False
    if 'selected_persona' not in st.session_state:
        st.session_state.selected_persona = None
    
    # 화면 전환 로직
    # 1. 페르소나 선택
    if not st.session_state.persona_selected:
        show_persona_selection_page()
    # 2. 사용자 정보 수집
    elif not st.session_state.user_info_collected:
        show_user_info_page()
    # 3. 채팅
    else:
        show_chat_page()


if __name__ == "__main__":
    main()