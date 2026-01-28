"""
안전 모니터링 에이전트 - Level 4,5만 경고 (수정판)
"""

import openai
import json
import streamlit as st
from typing import Dict, List, Tuple


class SafetyAgent:
    """실시간 안전 모니터링 에이전트"""
    
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)
        self.risk_history = []  # 위험도 이력
        
    def load_prompt(self) -> str:
        """Prompt 10 로드"""
        try:
            with open('prompt10.txt', 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            st.error("⚠️ prompt10.txt 파일을 찾을 수 없습니다.")
            return ""
    
    def analyze_risk(self, user_message: str, conversation_history: List[Dict]) -> Dict:
        """
        사용자 메시지의 위험도 분석
        
        Args:
            user_message: 사용자 메시지
            conversation_history: 대화 이력 (최근 5턴)
            
        Returns:
            위험도 평가 결과 (JSON)
        """
        
        system_prompt = self.load_prompt()
        
        # 최근 대화 맥락 구성
        context = "\n".join([
            f"{'사용자' if msg['role'] == 'user' else 'AI'}: {msg['content']}"
            for msg in conversation_history[-5:]  # 최근 5턴만
        ])
        
        # 분석 요청
        analysis_request = f"""
다음 대화를 분석하여 위험도를 평가하세요.

[최근 대화 맥락]
{context}

[현재 사용자 메시지]
{user_message}

위험도를 평가하고 JSON 형식으로 응답하세요.
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": analysis_request}
                ],
                temperature=0.3,  # 일관성 있는 평가
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            
            # 이력에 추가
            self.risk_history.append({
                'message': user_message,
                'risk_level': result.get('risk_level', 1),
                'category': result.get('risk_category', 'NONE')
            })
            
            return result
            
        except Exception as e:
            st.error(f"⚠️ 안전 평가 중 오류: {str(e)}")
            return self._get_default_assessment()
    
    def _get_default_assessment(self) -> Dict:
        """기본 평가 결과 (오류 시)"""
        return {
            "risk_level": 1,
            "risk_category": "NONE",
            "detected_keywords": [],
            "risk_factors": [],
            "protective_factors": [],
            "immediate_action_required": False,
            "recommended_response": "",
            "follow_up_needed": False,
            "alert_guardian": False,
            "session_should_end": False
        }
    
    def check_escalation_pattern(self) -> Tuple[bool, str]:
        """
        위험도 상승 패턴 감지 - Level 4,5만 추적
        
        Returns:
            (패턴 감지 여부, 경고 메시지)
        """
        if len(self.risk_history) < 3:
            return False, ""
        
        recent_levels = [h['risk_level'] for h in self.risk_history[-5:]]
        
        # 3회 연속 Level 4+
        if len(recent_levels) >= 3 and all(level >= 4 for level in recent_levels[-3:]):
            return True, "🚨 3회 연속 높은 위험도 감지. 즉시 전문가 상담이 필요합니다."
        
        # 5회 중 3회 이상 Level 4+
        if len(recent_levels) >= 5:
            high_risk_count = sum(1 for level in recent_levels[-5:] if level >= 4)
            if high_risk_count >= 3:
                return True, "🚨 반복적인 높은 위험도 감지. 전문가 상담을 강력히 권장합니다."
        
        return False, ""
    
    def get_intervention_message(self, assessment: Dict) -> str:
        """
        위험도에 따른 개입 메시지 생성 - Level 4,5만
        
        Args:
            assessment: 위험도 평가 결과
            
        Returns:
            사용자에게 보여줄 메시지
        """
        risk_level = assessment.get('risk_level', 1)
        
        if risk_level == 5:
            return """
🚨 **긴급 상황 감지**

지금 매우 힘든 상황인 것 같아요. 
이런 생각이 들 때는 혼자 있으면 안 됩니다.

**지금 바로 연락하세요:**
- 📞 정신건강위기상담: **1577-0199** (24시간)
- 📞 자살예방상담: **1393** (24시간)
- 📞 응급: **119**

저는 AI라서 진짜 도움을 드릴 수 없어요.
반드시 전문가와 이야기하세요.

부모님이나 신뢰할 수 있는 어른에게도 
꼭 이야기해주세요.
"""
        
        elif risk_level == 4:
            return """
😟 **전문가 상담을 권장합니다**

지금 정말 힘든 시간을 보내고 있는 것 같아요.
혼자 이런 감정을 감당하기 너무 어렵죠.

이런 감정은 전문가의 도움이 필요할 수 있어요.

**상담 받아보는 건 어떨까요?**
- 📞 청소년 전화: **1388**
- 📞 정신건강상담: **1577-0199**

부모님이나 학교 선생님께도 이야기해보세요.
혼자 감당하지 않아도 돼요.
"""
        
        else:
            return ""  # Level 1-3은 개입 없음
    
    def should_continue_session(self, assessment: Dict) -> bool:
        """
        세션을 계속 진행해야 하는지 판단
        
        Returns:
            True: 계속 진행
            False: 세션 종료 권장
        """
        return not assessment.get('session_should_end', False)


def display_safety_alert(assessment: Dict):
    """
    안전 경고 UI 표시 - Level 4,5만
    
    Args:
        assessment: 위험도 평가 결과
    """
    risk_level = assessment.get('risk_level', 1)
    
    # Level 5: 긴급 위험
    if risk_level == 5:
        st.error("""
### 🚨 긴급 상황 감지

**즉시 전문가에게 연락하세요:**

📞 **정신건강위기상담: 1577-0199** (24시간)  
📞 **자살예방상담: 1393** (24시간)  
📞 **청소년 전화: 1388** (24시간)  
📞 **응급: 119**

이 챗봇은 응급 상황을 다룰 수 없습니다.
반드시 위 번호로 전화하세요.
        """)
        
        # 세션 종료 버튼
        if st.button("🔴 대화 종료 및 응급 연락처 확인", use_container_width=True):
            st.session_state.emergency_mode = True
    
    # Level 4: 높은 위험
    elif risk_level == 4:
        st.warning("""
### 😟 전문가 상담이 필요한 것 같아요

지금 느끼는 감정은 전문가의 도움이 필요할 수 있습니다.

**상담 연락처:**
- 📞 청소년 전화: 1388
- 📞 정신건강상담: 1577-0199

부모님이나 선생님께도 이야기해보세요.
        """)
    
    # Level 1-3: 경고 없음 (정상 범위)


def check_crisis_keywords(text: str) -> bool:
    """
    위기 키워드 빠른 체크 (즉각 반응용)
    
    Args:
        text: 체크할 텍스트
        
    Returns:
        위기 키워드 포함 여부
    """
    CRISIS_KEYWORDS = [
        '죽고 싶', '자살', '자해', '끝내고 싶',
        '사라지고 싶', '목숨', '유서',
        '칼로 긋', '약을 먹', '뛰어내리',
        '목을 매', '손목을'
    ]
    
    return any(keyword in text for keyword in CRISIS_KEYWORDS)


def display_emergency_screen():
    """응급 상황 전용 화면"""
    st.error("""
# 🚨 응급 상황

대화가 중단되었습니다.
즉시 아래 연락처로 전화하세요.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
### 📞 정신건강위기상담
**1577-0199**
- 24시간 운영
- 전문 상담사 연결
        """)
        
        st.markdown("""
### 📞 자살예방상담
**1393**
- 24시간 운영
- 위기 개입 전문
        """)
    
    with col2:
        st.markdown("""
### 📞 청소년 전화
**1388**
- 24시간 운영
- 청소년 전문 상담
        """)
        
        st.markdown("""
### 📞 응급
**119**
- 즉각 출동
- 응급 상황
        """)
    
    st.markdown("---")
    
    st.warning("""
### 🏥 가까운 응급실 찾기

1. 네이버/카카오맵에서 "응급실" 검색
2. 가장 가까운 병원 선택
3. 전화로 상황 설명 후 방문

또는 119에 전화하면 안내받을 수 있습니다.
    """)
    
    st.info("""
### 👨‍👩‍👧 부모님/보호자께

자녀가 위기 상황에 있습니다.
- 즉시 곁에 있어주세요
- 위험 요소를 치워주세요
- 전문가와 연락하세요
- 혼자 두지 마세요
    """)


def log_safety_assessment(assessment: Dict, user_id: str = "anonymous"):
    """
    안전 평가 로그 저장 (Level 4,5만)
    
    Args:
        assessment: 평가 결과
        user_id: 사용자 ID (익명화)
    """
    risk_level = assessment.get('risk_level', 1)
    
    # Level 4,5만 로그 저장
    if risk_level >= 4:
        import datetime
        
        log_entry = {
            'timestamp': datetime.datetime.now().isoformat(),
            'user_id': user_id,
            'risk_level': risk_level,
            'risk_category': assessment.get('risk_category'),
            'detected_keywords': assessment.get('detected_keywords', []),
            'risk_factors': assessment.get('risk_factors', [])
        }
        
        try:
            with open('high_risk_logs.json', 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
        except Exception as e:
            st.error(f"로그 저장 오류: {str(e)}")
