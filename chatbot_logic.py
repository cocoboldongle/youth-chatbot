"""
청소년 인지 재구조화 챗봇 - 비즈니스 로직 (GPT API 연동)
"""

import streamlit as st
from openai import OpenAI
import datetime
import os
import json

# ========== 안전 에이전트 Import ==========
try:
    from safety_agent_simplified import (
        SafetyAgent,
        display_safety_alert,
        display_emergency_screen,
        log_safety_assessment
    )
    SAFETY_AGENT_AVAILABLE = True
except ImportError:
    SAFETY_AGENT_AVAILABLE = False
    print("⚠️ 안전 에이전트를 불러올 수 없습니다.")


# ========== API 키 헬퍼 함수 ==========
def get_api_key():
    """
    API 키 가져오기 (Streamlit Secrets 우선, 환경변수 대체)
    """
    try:
        # Streamlit Secrets 시도
        api_key = st.secrets.get("OPENAI_API_KEY")
        if api_key:
            return api_key
    except:
        pass
    
    # 환경변수 시도
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        return api_key
    
    # 둘 다 없으면 에러
    st.error("⚠️ OpenAI API 키가 설정되지 않았습니다. Streamlit Secrets에 OPENAI_API_KEY를 추가하세요.")
    return None



def initialize_session_state():
    """세션 상태 초기화"""
    if 'user_info_collected' not in st.session_state:
        st.session_state.user_info_collected = False
    if 'user_info' not in st.session_state:
        st.session_state.user_info = {}
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    if 'current_stage' not in st.session_state:
        st.session_state.current_stage = 'collection'  # collection, analysis (Stage 3는 추후 구현)
    if 'analysis_data' not in st.session_state:
        st.session_state.analysis_data = None
    if 'distortion_extracted' not in st.session_state:
        st.session_state.distortion_extracted = False  # 인지왜곡 추출 완료 여부
    if 'awaiting_distortion_selection' not in st.session_state:
        st.session_state.awaiting_distortion_selection = False  # 왜곡 선택 대기 여부
    if 'selected_distortion' not in st.session_state:
        st.session_state.selected_distortion = None  # 선택된 왜곡
    if 'awaiting_restructuring_start' not in st.session_state:
        st.session_state.awaiting_restructuring_start = False  # 재구조화 시작 대기
    if 'restructuring_method' not in st.session_state:
        st.session_state.restructuring_method = None  # 선택된 재구조화 방법
    if 'evaluation_logs' not in st.session_state:
        st.session_state.evaluation_logs = []  # 평가 로그 저장
    
    # ========== 빠른 답변 선택지 ==========
    if 'quick_replies' not in st.session_state:
        st.session_state.quick_replies = None  # 현재 선택 가능한 답변들
    
    # ========== 안전 에이전트 초기화 ==========
    if 'safety_agent' not in st.session_state and SAFETY_AGENT_AVAILABLE:
        print("\n[안전 에이전트 초기화 시작]")
        try:
            # API 키 (다른 에이전트와 동일)
            api_key = get_api_key()
            
            if api_key:
                st.session_state.safety_agent = SafetyAgent(api_key)
                print("✅ 안전 에이전트 초기화 성공!")
            else:
                st.session_state.safety_agent = None
                print("❌ API 키를 찾을 수 없습니다")
        except Exception as e:
            st.session_state.safety_agent = None
            print(f"❌ 안전 에이전트 초기화 실패: {e}")
    elif not SAFETY_AGENT_AVAILABLE:
        print("❌ SAFETY_AGENT_AVAILABLE = False (Import 실패)")
    elif 'safety_agent' in st.session_state:
        print(f"✅ 안전 에이전트 이미 초기화됨 (None: {st.session_state.safety_agent is None})")
    
    if 'emergency_mode' not in st.session_state:
        st.session_state.emergency_mode = False
    
    if 'last_risk_level' not in st.session_state:
        st.session_state.last_risk_level = 1


def add_evaluation_log(log_type, data):
    """평가 로그 추가"""
    if 'evaluation_logs' not in st.session_state:
        st.session_state.evaluation_logs = []
    
    import datetime
    log_entry = {
        'timestamp': datetime.datetime.now().isoformat(),
        'type': log_type,
        'data': data
    }
    st.session_state.evaluation_logs.append(log_entry)


def save_user_info(user_info):
    """사용자 정보 저장"""
    st.session_state.user_info = user_info
    st.session_state.user_info_collected = True


def reset_session():
    """세션 초기화 (처음으로 돌아가기)"""
    st.session_state.user_info_collected = False
    st.session_state.messages = []
    st.session_state.conversation_history = []
    st.session_state.current_stage = 'collection'


def export_conversation_to_json():
    """대화 내용을 JSON으로 내보내기"""
    import json
    import datetime
    
    # Stage별로 메시지 분류
    stage_messages = {
        'collection': [],
        'analysis': [],
        'restructuring': []
    }
    
    for msg in st.session_state.messages:
        stage = msg.get('stage', 'collection')
        stage_messages[stage].append({
            'role': msg['role'],
            'content': msg['content'],
            'timestamp': msg.get('timestamp', '')
        })
    
    # 전체 데이터 구성
    export_data = {
        'metadata': {
            'export_time': datetime.datetime.now().isoformat(),
            'user_info': st.session_state.get('user_info', {}),
            'current_stage': st.session_state.get('current_stage', 'collection')
        },
        'stages': {
            'stage1_collection': {
                'description': 'Stage 1: 감정-논리-행동 수집',
                'turn_count': len([m for m in stage_messages['collection'] if m['role'] == 'user']),
                'messages': stage_messages['collection'],
                'analysis_result': st.session_state.get('analysis_data')
            },
            'stage2_analysis': {
                'description': 'Stage 2: 인지왜곡 탐색',
                'turn_count': len([m for m in stage_messages['analysis'] if m['role'] == 'user']),
                'messages': stage_messages['analysis'],
                'distortion_data': st.session_state.get('distortion_data'),
                'selected_distortion': st.session_state.get('selected_distortion')
            },
            'stage3_restructuring': {
                'description': 'Stage 3: 인지 재구조화',
                'turn_count': len([m for m in stage_messages['restructuring'] if m['role'] == 'user']),
                'messages': stage_messages['restructuring'],
                'restructuring_method': st.session_state.get('restructuring_method')
            }
        },
        'evaluation_logs': st.session_state.get('evaluation_logs', []),
        'statistics': {
            'total_turns': len([m for m in st.session_state.messages if m['role'] == 'user']),
            'total_messages': len(st.session_state.messages),
            'stage1_turns': len([m for m in stage_messages['collection'] if m['role'] == 'user']),
            'stage2_turns': len([m for m in stage_messages['analysis'] if m['role'] == 'user']),
            'stage3_turns': len([m for m in stage_messages['restructuring'] if m['role'] == 'user'])
        }
    }
    
    return json.dumps(export_data, ensure_ascii=False, indent=2)


def get_emotion_message(intensity):
    """하루 점수에 따른 메시지 반환"""
    if intensity <= 3:
        return "요즘 괜찮은 편이시군요. 함께 편안하게 이야기 나눠봐요. 😊"
    elif intensity <= 6:
        return "요즘 보통 정도시군요. 천천히 함께 살펴볼게요. 🤗"
    else:
        return "요즘 많이 힘드시군요. 충분히 이해합니다. 함께 차근차근 이야기 나눠봐요. 💪"


def get_welcome_message(user_info):
    """초기 환영 메시지 생성"""
    return f"""안녕하세요! 만나서 반가워요 🌟

{get_emotion_message(user_info['emotion_intensity'])}

오늘은 어떤 생각이나 감정을 이야기하고 싶나요? 
무엇이든 편하게 말씀해주세요. 함께 천천히 생각을 정리해볼게요.
"""


def load_prompt_from_file(file_path):
    """외부 파일에서 프롬프트 로드"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        st.error(f"⚠️ 프롬프트 파일을 찾을 수 없습니다: {file_path}")
        return ""
    except Exception as e:
        st.error(f"⚠️ 프롬프트 파일 로드 중 오류 발생: {str(e)}")
        return ""


def get_persona_prompt():
    """페르소나 프롬프트 로드 및 적용"""
    persona_id = st.session_state.get('selected_persona', 'friend')
    
    # 페르소나 정보
    PERSONAS = {
        "detective": {"name": "분석적 있는 탐정형 (형/누나)", "emoji": "🕵️"},
        "friend": {"name": "따뜻한 감정 공감 친구형 (친구)", "emoji": "💕"},
        "cool": {"name": "쿨한 형·누나형 (현실적 조력 유머)", "emoji": "😎"},
        "coach": {"name": "자분한 건문 코치형 (상담교사 느낌)", "emoji": "🧘"}
    }
    
    # prompt9 파일 로드
    try:
        prompt_file_path = "prompt9_persona.txt"
        with open(prompt_file_path, 'r', encoding='utf-8') as f:
            persona_prompt = f.read()
        
        # 페르소나 정보 삽입
        persona_info = PERSONAS.get(persona_id, PERSONAS['friend'])
        persona_prompt = persona_prompt.replace('{selected_persona}', persona_info['name'])
        
        return persona_prompt
    except FileNotFoundError:
        # 파일이 없으면 기본 페르소나 설명만
        persona_info = PERSONAS.get(persona_id, PERSONAS['friend'])
        return f"\n\n**[대화 스타일]**\n선택된 페르소나: {persona_info['emoji']} {persona_info['name']}\n이 페르소나의 특징을 살려 대화하세요.\n"
    except Exception as e:
        return ""


def get_system_prompt_stage1(user_info):
    """Stage 1: 정보 수집 단계 프롬프트"""
    # 프롬프트 파일 경로
    prompt_file_path = "prompt1.txt"
    
    # 파일에서 프롬프트 로드
    prompt1 = load_prompt_from_file(prompt_file_path)
    
    if not prompt1:
        # 파일 로드 실패 시 기본 프롬프트 사용
        prompt1 = """당신은 청소년의 고민을 경청하며 체계적으로 정보를 수집하는 상담사입니다.
정보 수집 후 [COLLECTION_COMPLETE] 신호를 출력하세요."""
    
    # 사용자 정보 추가
    user_context = f"""

**[사용자 정보]**
- 성별: {user_info['gender']}
- 나이: {user_info['age']}세
- 하루 점수: {user_info['emotion_intensity']}/10 (0=괜찮음, 10=최악)

위 정보를 참고하되, 대화 중에는 언급하지 마세요. 자연스럽게 대화를 이어가세요."""

    # 페르소나 프롬프트 추가
    persona_prompt = get_persona_prompt()

    return prompt1 + user_context + persona_prompt


def get_system_prompt_stage2(user_info):
    """Stage 2: 인지왜곡 탐색 단계 프롬프트"""
    # 프롬프트 파일 경로
    prompt_file_path = "prompt4.txt"
    
    # 파일에서 프롬프트 로드
    prompt4 = load_prompt_from_file(prompt_file_path)
    
    if not prompt4:
        # 파일 로드 실패 시 기본 프롬프트 사용
        prompt4 = """당신은 청소년의 인지왜곡을 탐색하는 상담사입니다.
자동적 사고, 중간 신념, 핵심 신념을 탐색하세요.
질문보다는 반영, 요약, 공감을 많이 사용하세요."""
    
    # 사용자 정보 및 분석 데이터 추가
    user_context = f"""

**[사용자 정보]**
- 성별: {user_info['gender']}
- 나이: {user_info['age']}세
- 하루 점수: {user_info['emotion_intensity']}/10 (0=괜찮음, 10=최악)"""

    # 분석 데이터가 있으면 추가
    if 'analysis_data' in st.session_state and st.session_state.analysis_data:
        analysis_data = st.session_state.analysis_data
        analysis_context = f"""

**[수집된 정보 - 참고용]**
이전 단계에서 다음 정보가 수집되었습니다:

• 감정: {analysis_data.get('emotion', {}).get('primary', 'N/A')}
• 자동적 사고: {', '.join(analysis_data.get('logic', {}).get('automatic_thoughts', [])[:2]) if analysis_data.get('logic', {}).get('automatic_thoughts') else 'N/A'}
• 행동: {', '.join(analysis_data.get('behavior', {}).get('actions', [])[:2]) if analysis_data.get('behavior', {}).get('actions') else 'N/A'}

이 정보를 참고하여 더 깊이 탐색하세요."""
        
        # 페르소나 프롬프트 추가
        persona_prompt = get_persona_prompt()
        
        return prompt4 + user_context + analysis_context + persona_prompt
    
    # 페르소나 프롬프트 추가
    persona_prompt = get_persona_prompt()
    
    return prompt4 + user_context + persona_prompt


def get_system_prompt_evaluator():
    """정보 수집 완료 평가 에이전트 프롬프트"""
    # 프롬프트 파일 경로
    prompt_file_path = "prompt2.txt"
    
    # 파일에서 프롬프트 로드
    prompt2 = load_prompt_from_file(prompt_file_path)
    
    if not prompt2:
        # 파일 로드 실패 시 기본 프롬프트 사용
        prompt2 = """당신은 대화 완료 여부를 판단하는 평가자입니다.
상황과 감정이 모두 파악되었으면 COMPLETE, 아니면 INCOMPLETE를 JSON 형식으로 반환하세요.

응답 형식:
{
  "status": "COMPLETE" 또는 "INCOMPLETE",
  "reason": "판단 이유",
  "situation_clear": true/false,
  "emotion_expressed": true/false
}"""
    
    return prompt2


def get_system_prompt_extractor():
    """감정-논리-행동 추출 에이전트 프롬프트"""
    # 프롬프트 파일 경로
    prompt_file_path = "prompt3.txt"
    
    # 파일에서 프롬프트 로드
    prompt3 = load_prompt_from_file(prompt_file_path)
    
    if not prompt3:
        # 파일 로드 실패 시 기본 프롬프트 사용
        prompt3 = """당신은 대화 내용을 분석하여 감정, 논리, 행동을 추출하는 분석가입니다.
다음 JSON 형식으로 응답하세요:
{
  "emotion": {"primary": "주된 감정", "description": "설명"},
  "logic": {"automatic_thoughts": ["사고 리스트"], "description": "설명"},
  "behavior": {"actions": ["행동 리스트"], "description": "설명"},
  "summary": "전체 요약"
}"""
    
    return prompt3


def get_system_prompt_distortion_evaluator():
    """인지왜곡 추출 준비 평가 에이전트 프롬프트"""
    # 프롬프트 파일 경로
    prompt_file_path = "prompt5.txt"
    
    # 파일에서 프롬프트 로드
    prompt5 = load_prompt_from_file(prompt_file_path)
    
    if not prompt5:
        # 파일 로드 실패 시 기본 프롬프트 사용
        prompt5 = """당신은 인지왜곡 탐색 대화를 평가하는 전문가입니다.
다음 5개 영역이 충분히 수집되었는지 확인하세요:
1. 자동적 사고
2. 패턴/빈도
3. 극단적 사고
4. 증거 기반
5. 대안 관점

최소 10턴 이상, 5개 중 4개 이상 충족 시 READY
JSON 형식으로 응답하세요."""
    
    return prompt5


def get_system_prompt_distortion_extractor():
    """인지왜곡 유형 추출 에이전트 프롬프트"""
    # 프롬프트 파일 경로
    prompt_file_path = "prompt6.txt"
    
    # 파일에서 프롬프트 로드
    prompt6 = load_prompt_from_file(prompt_file_path)
    
    if not prompt6:
        # 파일 로드 실패 시 기본 프롬프트 사용
        prompt6 = """당신은 청소년의 대화에서 인지왜곡 유형을 추출하는 전문가입니다.
7가지 왜곡 중 가장 두드러진 3개를 추출하고 JSON으로 응답하세요."""
    
    return prompt6


def get_system_prompt(user_info):
    """현재 단계에 맞는 시스템 프롬프트 반환"""
    current_stage = st.session_state.get('current_stage', 'collection')
    
    if current_stage == 'collection':
        return get_system_prompt_stage1(user_info)
    elif current_stage == 'analysis':
        return get_system_prompt_stage2(user_info)
    else:
        # 추후 stage3 (restructuring) 추가 가능
        return get_system_prompt_stage1(user_info)


def initialize_chat_messages(user_info):
    """채팅 메시지 초기화 (환영 메시지 추가)"""
    if len(st.session_state.messages) == 0:
        welcome_msg = get_welcome_message(user_info)
        st.session_state.messages.append({
            "role": "assistant",
            "content": welcome_msg
        })


def add_user_message(message):
    """사용자 메시지 추가"""
    import datetime
    st.session_state.messages.append({
        "role": "user",
        "content": message,
        "timestamp": datetime.datetime.now().isoformat()
    })


def add_assistant_message(message):
    """챗봇 메시지 추가"""
    import datetime
    st.session_state.messages.append({
        "role": "assistant",
        "content": message,
        "timestamp": datetime.datetime.now().isoformat()
    })


def generate_response_with_gpt(user_message, user_info):
    """GPT API를 사용하여 응답 생성"""
    try:
        # OpenAI 클라이언트 초기화 (API 키 하드코딩)
        api_key = get_api_key()
        
        client = OpenAI(api_key=api_key)
        
        # 대화 히스토리 구성
        messages = [
            {"role": "system", "content": get_system_prompt(user_info)}
        ]
        
        # 이전 대화 내역 추가 (최근 10개만)
        recent_messages = st.session_state.messages[-10:] if len(st.session_state.messages) > 10 else st.session_state.messages
        for msg in recent_messages:
            if msg["role"] in ["user", "assistant"]:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
        
        # 현재 사용자 메시지 추가
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        # GPT API 호출
        response = client.chat.completions.create(
            model="gpt-4o",  # 또는 "gpt-3.5-turbo"
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"⚠️ 응답 생성 중 오류가 발생했습니다: {str(e)}\n\n문제가 계속되면 관리자에게 문의해주세요."


def check_collection_complete_with_evaluator():
    """평가 에이전트를 사용하여 정보 수집 완료 여부 확인"""
    try:
        # API 키
        api_key = get_api_key()
        client = OpenAI(api_key=api_key)
        
        # 대화 내역을 텍스트로 변환
        conversation_text = "대화 내용:\n"
        for msg in st.session_state.messages:
            role = "청소년" if msg["role"] == "user" else "상담사"
            conversation_text += f"{role}: {msg['content']}\n"
        
        # 평가 에이전트 프롬프트
        evaluator_prompt = get_system_prompt_evaluator()
        
        # 평가 요청
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": evaluator_prompt},
                {"role": "user", "content": conversation_text}
            ],
            temperature=0.3,  # 낮은 temperature로 일관된 판단
            max_tokens=200
        )
        
        # 응답 파싱
        result_text = response.choices[0].message.content.strip()
        
        # JSON 파싱 시도
        import json
        # JSON 코드 블록 제거
        if "```json" in result_text:
            result_text = result_text.split("```json")[1].split("```")[0].strip()
        elif "```" in result_text:
            result_text = result_text.split("```")[1].split("```")[0].strip()
        
        result = json.loads(result_text)
        
        # 평가 로그 저장
        add_evaluation_log('stage1_evaluation', {
            'status': result.get('status'),
            'collected_areas': result.get('collected_areas', []),
            'missing_areas': result.get('missing_areas', [])
        })
        
        return result.get("status") == "COMPLETE", result
        
    except Exception as e:
        st.error(f"⚠️ 평가 중 오류 발생: {str(e)}")
        # 오류 시 기본적으로 미완료 처리
        return False, {"status": "INCOMPLETE", "reason": "평가 오류"}


def extract_emotion_logic_behavior():
    """추출 에이전트를 사용하여 감정-논리-행동 추출"""
    try:
        # API 키
        api_key = get_api_key()
        client = OpenAI(api_key=api_key)
        
        # 대화 내역을 텍스트로 변환 (사용자 메시지만)
        conversation_text = "청소년과의 대화 내용:\n\n"
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                conversation_text += f"청소년: {msg['content']}\n"
        
        # 추출 에이전트 프롬프트
        extractor_prompt = get_system_prompt_extractor()
        
        # 추출 요청
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": extractor_prompt},
                {"role": "user", "content": conversation_text}
            ],
            temperature=0.5,
            max_tokens=800
        )
        
        # 응답 파싱
        result_text = response.choices[0].message.content.strip()
        
        # JSON 파싱
        import json
        # JSON 코드 블록 제거
        if "```json" in result_text:
            result_text = result_text.split("```json")[1].split("```")[0].strip()
        elif "```" in result_text:
            result_text = result_text.split("```")[1].split("```")[0].strip()
        
        result = json.loads(result_text)
        
        # 추출 로그 저장
        add_evaluation_log('stage1_extraction', {
            'emotion': result.get('emotion'),
            'logic': result.get('logic'),
            'behavior': result.get('behavior')
        })
        
        return True, result
        
    except Exception as e:
        st.error(f"⚠️ 추출 중 오류 발생: {str(e)}")
        return False, None


def check_distortion_extraction_ready():
    """인지왜곡 추출 준비 평가"""
    try:
        # API 키
        api_key = get_api_key()
        client = OpenAI(api_key=api_key)
        
        # Stage 2 (analysis) 대화만 필터링
        analysis_messages = [m for m in st.session_state.messages if m.get('stage') == 'analysis']
        
        # 대화 내역을 텍스트로 변환
        conversation_text = "Stage 2 인지왜곡 탐색 대화 내용:\n\n"
        for msg in analysis_messages:
            role = "청소년" if msg["role"] == "user" else "상담사"
            conversation_text += f"{role}: {msg['content']}\n"
        
        # 평가 에이전트 프롬프트
        evaluator_prompt = get_system_prompt_distortion_evaluator()
        
        # 평가 요청
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": evaluator_prompt},
                {"role": "user", "content": conversation_text}
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        # 응답 파싱
        result_text = response.choices[0].message.content.strip()
        
        # JSON 파싱
        import json
        # JSON 코드 블록 제거
        if "```json" in result_text:
            result_text = result_text.split("```json")[1].split("```")[0].strip()
        elif "```" in result_text:
            result_text = result_text.split("```")[1].split("```")[0].strip()
        
        result = json.loads(result_text)
        
        # 평가 로그 저장
        add_evaluation_log('stage2_evaluation', {
            'status': result.get('status'),
            'collected_areas': result.get('collected_areas', []),
            'missing_info': result.get('missing_info', [])
        })
        
        return result.get("status") == "READY", result
        
    except Exception as e:
        st.error(f"⚠️ 평가 중 오류 발생: {str(e)}")
        # 오류 시 기본적으로 미완료 처리
        return False, {"status": "NOT_READY", "reason": "평가 오류"}


def extract_cognitive_distortions():
    """인지왜곡 유형 추출 및 피드백 생성 (GPT + 로컬 모델 병행)"""
    try:
        # Stage 2 (analysis) 대화만 필터링
        analysis_messages = [m for m in st.session_state.messages if m.get('stage') == 'analysis']
        
        # 대화 내역을 텍스트로 변환
        conversation_text = "Stage 2 대화 내용:\n\n"
        for msg in analysis_messages:
            role = "청소년" if msg["role"] == "user" else "상담사"
            conversation_text += f"{role}: {msg['content']}\n"
        
        # 1. GPT로 추출 (기존 방식)
        gpt_success, gpt_result = extract_with_gpt(conversation_text)
        
        # 2. 로컬 모델로 추출 (새로운 방식)
        local_success, local_result = extract_with_local_model(conversation_text)
        
        # 결과 로그
        if gpt_success:
            print(f"\n[GPT 추출 결과]")
            for dist in gpt_result.get('distortions', []):
                print(f"  - {dist['type']}")
        
        if local_success:
            print(f"\n[로컬 모델 추출 결과]")
            for dist_type, prob in local_result.items():
                print(f"  - {dist_type}: {prob:.3f}")
        
        # GPT 결과를 우선 사용 (기존 동작 유지)
        if gpt_success:
            return True, gpt_result
        elif local_success:
            # GPT 실패 시 로컬 모델 결과를 GPT 형식으로 변환
            converted_result = convert_local_to_gpt_format(local_result)
            return True, converted_result
        else:
            return False, None
        
    except Exception as e:
        st.error(f"⚠️ 인지왜곡 추출 중 오류 발생: {str(e)}")
        return False, None


def extract_with_gpt(conversation_text):
    """GPT를 사용한 인지왜곡 추출"""
    try:
        # API 키
        api_key = get_api_key()
        client = OpenAI(api_key=api_key)
        
        # 추출 에이전트 프롬프트
        extractor_prompt = get_system_prompt_distortion_extractor()
        
        # 추출 요청
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": extractor_prompt},
                {"role": "user", "content": conversation_text}
            ],
            temperature=0.5,
            max_tokens=1500
        )
        
        # 응답 파싱
        result_text = response.choices[0].message.content.strip()
        
        # JSON 파싱
        import json
        # JSON 코드 블록 제거
        if "```json" in result_text:
            result_text = result_text.split("```json")[1].split("```")[0].strip()
        elif "```" in result_text:
            result_text = result_text.split("```")[1].split("```")[0].strip()
        
        result = json.loads(result_text)
        
        # 추출 로그 저장
        add_evaluation_log('distortion_extraction', {
            'method': 'GPT',
            'distortions': [
                {
                    'type': d.get('type'),
                    'type_english': d.get('type_english'),
                    'evidence_count': len(d.get('evidence', []))
                } for d in result.get('distortions', [])
            ]
        })
        
        return True, result
        
    except Exception as e:
        print(f"[GPT 추출 실패] {str(e)}")
        return False, None


def extract_with_local_model(conversation_text):
    """로컬 파인튜닝 모델을 사용한 인지왜곡 추출"""
    try:
        import torch
        from transformers import AutoTokenizer, AutoModelForSequenceClassification
        
        # 모델 경로
        MODEL_PATH = r"C:\Users\kma80\Desktop\python_workspace\LLM\중견연구3\baseline_roberta_large_20250817_052327"
        
        # 10가지 인지왜곡 레이블
        DISTORTION_LABELS = [
            "흑백 사고",
            "과잉 일반화",
            "부정적 편향",
            "긍정 축소화",
            "성급한 판단",
            "확대와 축소",
            "감정적 추론",
            "해야 한다 진술",
            "낙인찍기",
            "개인화"
        ]
        
        print(f"\n[로컬 모델 로딩 시작...]")
        
        # 토크나이저와 모델 로드
        tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
        model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
        
        # GPU 사용 가능하면 GPU로
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model.to(device)
        model.eval()
        
        print(f"[로컬 모델 로드 완료] Device: {device}")
        
        # 대화 텍스트를 토큰화
        inputs = tokenizer(
            conversation_text,
            max_length=512,
            truncation=True,
            padding=True,
            return_tensors="pt"
        )
        inputs = {k: v.to(device) for k, v in inputs.items()}
        
        # 추론
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits
            probs = torch.sigmoid(logits)[0]  # Multi-label classification
        
        # 확률을 딕셔너리로 변환
        distortion_probs = {}
        for i, label in enumerate(DISTORTION_LABELS):
            distortion_probs[label] = float(probs[i].cpu().numpy())
        
        # 확률 높은 순으로 정렬
        sorted_distortions = sorted(
            distortion_probs.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        print(f"\n[로컬 모델 예측 확률 (상위 5개)]")
        for dist_type, prob in sorted_distortions[:5]:
            print(f"  {dist_type}: {prob:.3f}")
        
        return True, distortion_probs
        
    except Exception as e:
        print(f"[로컬 모델 추출 실패] {str(e)}")
        import traceback
        traceback.print_exc()
        return False, None


def convert_local_to_gpt_format(local_result):
    """로컬 모델 결과를 GPT 형식으로 변환"""
    # 확률 높은 순으로 정렬하여 상위 3개 선택
    sorted_distortions = sorted(
        local_result.items(),
        key=lambda x: x[1],
        reverse=True
    )[:3]
    
    # GPT 형식으로 변환
    distortions = []
    for dist_type, prob in sorted_distortions:
        distortions.append({
            "type": dist_type,
            "type_english": get_english_name(dist_type),
            "evidence": [],
            "explanation": f"'{dist_type}' 패턴이 보여. (확률: {prob:.1%})",
            "pattern": "이런 생각이 반복되는 것 같아."
        })
    
    return {
        "distortions": distortions
    }


def get_english_name(korean_name):
    """한글 이름을 영문 이름으로 변환"""
    mapping = {
        "흑백 사고": "All-or-Nothing Thinking",
        "과잉 일반화": "Overgeneralization",
        "부정적 편향": "Mental Filter",
        "긍정 축소화": "Disqualifying the Positive",
        "성급한 판단": "Jumping to Conclusions",
        "확대와 축소": "Magnification and Minimization",
        "감정적 추론": "Emotional Reasoning",
        "해야 한다 진술": "Should Statements",
        "낙인찍기": "Labeling",
        "개인화": "Personalization"
    }
    return mapping.get(korean_name, korean_name)


def select_restructuring_method():
    """재구조화 방법 선택 (평가 에이전트)"""
    try:
        # API 키
        api_key = get_api_key()
        client = OpenAI(api_key=api_key)
        
        # 선택된 왜곡 정보
        selected_distortion = st.session_state.get('selected_distortion', {})
        
        # Stage 1 분석 데이터
        analysis_data = st.session_state.get('analysis_data', {})
        
        # Stage 2 대화
        analysis_messages = [m for m in st.session_state.messages if m.get('stage') == 'analysis']
        conversation_text = ""
        for msg in analysis_messages:
            role = "청소년" if msg["role"] == "user" else "상담사"
            conversation_text += f"{role}: {msg['content']}\n"
        
        # 입력 정보 구성
        input_text = f"""선택된 인지왜곡:
- 유형: {selected_distortion.get('type', '')}
- 영문: {selected_distortion.get('type_english', '')}
- 증거: {', '.join(selected_distortion.get('evidence', []))}

청소년의 상황:
- Stage 1 정보: {analysis_data}

Stage 2 대화:
{conversation_text}
"""
        
        # 평가 에이전트 프롬프트
        evaluator_prompt = get_system_prompt_method_evaluator()
        
        # 평가 요청
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": evaluator_prompt},
                {"role": "user", "content": input_text}
            ],
            temperature=0.5,
            max_tokens=800
        )
        
        # 응답 파싱
        result_text = response.choices[0].message.content.strip()
        
        # JSON 파싱
        import json
        if "```json" in result_text:
            result_text = result_text.split("```json")[1].split("```")[0].strip()
        elif "```" in result_text:
            result_text = result_text.split("```")[1].split("```")[0].strip()
        
        result = json.loads(result_text)
        
        # 방법 선택 로그 저장
        add_evaluation_log('restructuring_method_selection', {
            'selected_method': result.get('selected_method'),
            'method_code': result.get('method_code'),
            'reason': result.get('reason'),
            'expected_effectiveness': result.get('expected_effectiveness')
        })
        
        return True, result
        
    except Exception as e:
        print(f"[재구조화 방법 선택 실패] {str(e)}")
        return False, None


def get_system_prompt_method_evaluator():
    """재구조화 방법 평가 에이전트 프롬프트 로드"""
    try:
        with open('prompt8.txt', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        # 기본 프롬프트
        return """당신은 청소년에게 가장 효과적인 인지 재구조화 방법을 선택하는 전문 평가자입니다.
5가지 방법 중 1개를 선택하여 JSON으로 응답하세요."""


def get_system_prompt_restructuring(user_info):
    """재구조화 단계 시스템 프롬프트 생성"""
    try:
        with open('prompt7.txt', 'r', encoding='utf-8') as f:
            base_prompt = f.read()
    except FileNotFoundError:
        base_prompt = """당신은 청소년의 인지왜곡을 재구조화하는 전문 상담사입니다.
감정 타당화, 콜롬보식 접근, 논리적 반문을 사용하세요."""
    
    # 선택된 재구조화 방법 정보
    method_data = st.session_state.get('restructuring_method', {})
    selected_method = method_data.get('selected_method', '대안적 설명 찾기')
    method_code = method_data.get('method_code', 'alternative')
    
    # 선택된 왜곡 정보
    selected_distortion = st.session_state.get('selected_distortion', {})
    distortion_type = selected_distortion.get('type', '')
    
    # Stage 1 분석 정보
    analysis_data = st.session_state.get('analysis_data', {})
    situation_summary = str(analysis_data)
    
    # 프롬프트에 정보 삽입
    base_prompt = base_prompt.replace('{restructuring_method}', selected_method)
    base_prompt = base_prompt.replace('{selected_distortion_type}', distortion_type)
    base_prompt = base_prompt.replace('{situation_summary}', situation_summary)
    
    # 페르소나 프롬프트 추가
    persona_prompt = get_persona_prompt()
    
    return base_prompt + persona_prompt


def generate_restructuring_response(user_message, user_info):
    """재구조화 단계 응답 생성"""
    try:
        # API 키
        api_key = get_api_key()
        client = OpenAI(api_key=api_key)
        
        # 재구조화 시스템 프롬프트
        system_prompt = get_system_prompt_restructuring(user_info)
        
        # 대화 히스토리 (Stage 3만)
        restructuring_messages = [m for m in st.session_state.messages if m.get('stage') == 'restructuring']
        
        conversation_history = []
        for msg in restructuring_messages:
            conversation_history.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # 사용자 메시지 추가
        conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # GPT 응답 생성
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt}
            ] + conversation_history,
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"[재구조화 응답 생성 실패] {str(e)}")
        return "그 생각에 대해 좀 더 알려줄래?"


def parse_distortion_selection(user_message):
    """사용자의 왜곡 선택 파싱 (1, 2, 3)"""
    message = user_message.strip().lower()
    
    # 숫자 직접 입력
    if message in ['1', '2', '3']:
        return int(message)
    
    # "1번", "첫번째", "첫 번째" 등
    if '1' in message or '첫' in message or '하나' in message:
        return 1
    if '2' in message or '둘' in message or '두' in message:
        return 2
    if '3' in message or '셋' in message or '세' in message:
        return 3
    
    return None


def format_distortion_feedback(distortion_data):
    """인지왜곡 피드백을 짧고 직관적인 텍스트로 변환 (증거 포함)"""
    if not distortion_data or 'distortions' not in distortion_data:
        return "네 이야기를 들으면서 몇 가지 패턴을 발견했어."
    
    feedback = "네 이야기를 들으면서 몇 가지 패턴을 발견했어.\n\n"
    
    # 3가지 왜곡을 증거와 함께 설명
    for i, dist in enumerate(distortion_data['distortions'], 1):
        # 번호와 설명
        feedback += f"**{i}. {dist['explanation']}**\n"
        
        # 증거 추가 (있으면)
        if dist.get('evidence') and len(dist['evidence']) > 0:
            feedback += f"   예를 들어, "
            # 증거 1-2개만 (너무 길지 않게)
            evidence_list = dist['evidence'][:2]
            if len(evidence_list) == 1:
                feedback += f'"{evidence_list[0]}"라고 말했잖아.\n\n'
            else:
                feedback += f'"{evidence_list[0]}", "{evidence_list[1]}" 같은 말을 했잖아.\n\n'
        else:
            feedback += "\n"
    
    return feedback


def format_analysis_result(analysis_data):
    """추출된 분석 결과를 자연스러운 텍스트로 포맷팅"""
    if not analysis_data:
        return "분석 결과를 가져올 수 없었어."
    
    try:
        # summary가 있으면 그대로 사용
        if "summary" in analysis_data and analysis_data["summary"]:
            return analysis_data["summary"]
        
        # summary가 없으면 직접 생성
        parts = []
        
        # 감정 부분
        if "emotion" in analysis_data:
            emotion = analysis_data["emotion"]
            if "primary" in emotion:
                parts.append(f"너는 주로 {emotion['primary']}을(를) 느꼈어.")
        
        # 논리 부분
        if "logic" in analysis_data:
            logic = analysis_data["logic"]
            if "automatic_thoughts" in logic and logic["automatic_thoughts"]:
                thoughts = "', '".join(logic["automatic_thoughts"][:2])  # 최대 2개만
                parts.append(f"'{thoughts}'라는 생각이 들었고.")
        
        # 행동 부분
        if "behavior" in analysis_data:
            behavior = analysis_data["behavior"]
            if "actions" in behavior and behavior["actions"]:
                actions = ", ".join(behavior["actions"][:2])  # 최대 2개만
                parts.append(f"{actions}(을)를 했구나.")
            elif "avoidance" in behavior and behavior["avoidance"]:
                avoidance = ", ".join(behavior["avoidance"][:2])
                parts.append(f"{avoidance}(을)를 하게 되었구나.")
        
        return " ".join(parts) if parts else "네 이야기를 잘 들었어."
        
    except Exception as e:
        print(f"[포맷팅 오류] {str(e)}")
        return "네 이야기를 잘 들었어."


def process_user_input(user_message, user_info):
    """사용자 입력 처리 및 응답 생성 - 안전 모니터링 통합"""
    
    # ========== 안전 에이전트 평가 ==========
    # 응급 모드 체크
    if st.session_state.get('emergency_mode', False):
        if SAFETY_AGENT_AVAILABLE:
            display_emergency_screen()
        return
    
    # 현재 단계 확인
    current_stage = st.session_state.get('current_stage', 'collection')
    
    # 안전 평가 (매번 실행!)
    risk_level = 1
    safety_assessment = None
    
    # 디버깅: 안전 에이전트 상태 확인
    print(f"\n{'='*60}")
    print(f"[안전 에이전트 체크]")
    print(f"SAFETY_AGENT_AVAILABLE: {SAFETY_AGENT_AVAILABLE}")
    print(f"safety_agent in session: {'safety_agent' in st.session_state}")
    if 'safety_agent' in st.session_state:
        print(f"safety_agent is None: {st.session_state.safety_agent is None}")
    print(f"사용자 메시지: {user_message[:50]}...")
    print(f"{'='*60}\n")
    
    if SAFETY_AGENT_AVAILABLE and st.session_state.get('safety_agent'):
        try:
            # 메시지 추가 전에 평가
            temp_messages = st.session_state.messages + [{
                "role": "user",
                "content": user_message
            }]
            
            safety_assessment = st.session_state.safety_agent.analyze_risk(
                user_message=user_message,
                conversation_history=temp_messages
            )
            risk_level = safety_assessment.get('risk_level', 1)
            
            print(f"\n🛡️ [안전 평가 완료]")
            print(f"Risk Level: {risk_level}")
            print(f"Category: {safety_assessment.get('risk_category', 'NONE')}")
            print(f"Keywords: {safety_assessment.get('detected_keywords', [])}")
            print(f"{'='*60}\n")
            
            # Level 5: 긴급 - 즉시 중단
            if risk_level >= 5:
                add_user_message(user_message)
                st.session_state.messages[-1]['stage'] = current_stage
                
                display_safety_alert(safety_assessment)
                st.session_state.emergency_mode = True
                
                emergency_msg = st.session_state.safety_agent.get_intervention_message(safety_assessment)
                add_assistant_message(emergency_msg)
                st.session_state.messages[-1]['stage'] = current_stage
                st.session_state.messages[-1]['risk_level'] = risk_level
                
                log_safety_assessment(safety_assessment)
                return emergency_msg
            
            # Level 4: 높은 위험 - 경고 후 계속
            elif risk_level == 4:
                add_user_message(user_message)
                st.session_state.messages[-1]['stage'] = current_stage
                
                display_safety_alert(safety_assessment)
                
                warning_msg = st.session_state.safety_agent.get_intervention_message(safety_assessment)
                add_assistant_message(warning_msg)
                st.session_state.messages[-1]['stage'] = current_stage
                st.session_state.messages[-1]['risk_level'] = risk_level
                
                log_safety_assessment(safety_assessment)
                # 기존 응답도 계속 생성 (아래에서)
                
        except Exception as e:
            print(f"⚠️ 안전 평가 오류: {e}")
            risk_level = 1
    
    # 사용자 메시지 추가 (Level 4, 5가 아닌 경우만)
    if risk_level < 4:
        add_user_message(user_message)
        st.session_state.messages[-1]['stage'] = current_stage
    
    if current_stage == 'collection':
        # Stage 1: 정보 수집 단계
        # GPT를 통해 챗봇 응답 생성
        response = generate_response_with_gpt(user_message, user_info)
        
        # 챗봇 응답 추가
        add_assistant_message(response)
        
        # ===== 선택지 생성 =====
        if should_provide_options(response, current_stage):
            options = generate_quick_replies(response, user_message, current_stage)
            if options:
                set_quick_replies(options)
            else:
                clear_quick_replies()
        else:
            clear_quick_replies()
        
        # 평가 에이전트로 완료 여부 확인
        # 최소 5턴(사용자 5번 메시지) 이상일 때만 평가
        user_messages = [m for m in st.session_state.messages if m["role"] == "user"]
        if len(user_messages) >= 5:
            is_complete, eval_result = check_collection_complete_with_evaluator()
            
            if is_complete:
                # 선택지 초기화 (단계 전환 시)
                clear_quick_replies()
                
                # 다음 단계로 전환
                st.session_state.current_stage = 'analysis'
                
                # 평가 이유를 로그로 출력 (디버깅용)
                if 'reason' in eval_result:
                    print(f"[평가 완료] {eval_result['reason']}")
                
                # 추출 에이전트 호출하여 감정-논리-행동 추출
                extract_success, analysis_data = extract_emotion_logic_behavior()
                
                if extract_success and analysis_data:
                    # 추출 결과를 자연스러운 텍스트로 포맷팅
                    analysis_summary = format_analysis_result(analysis_data)
                    
                    # 전환 안내 메시지 생성 (마지막 질문 제거, 공감 + 정리 + 확인)
                    transition_msg = f"\n\n---\n\n네 이야기를 잘 들었어. 지금까지 말해준 내용을 정리해볼게.\n\n{analysis_summary}\n\n내가 이해한 게 맞아?"
                    
                    # 분석 데이터 저장 (추후 활용)
                    st.session_state.analysis_data = analysis_data
                    
                    print(f"[분석 완료] {analysis_summary}")
                else:
                    # 추출 실패 시 기본 메시지
                    transition_msg = f"\n\n---\n\n네 이야기를 잘 들었어. 지금까지 말해준 내용을 정리해볼게."
                
                # 마지막 assistant 메시지를 전환 메시지로 교체
                st.session_state.messages[-1]["content"] = transition_msg
                response = transition_msg
        
        return response
    
    elif current_stage == 'analysis':
        # Stage 2: 인지왜곡 탐색 단계
        
        # 첫 번째 메시지인지 확인 (분석 정리 후 첫 응답)
        analysis_stage_messages = [m for m in st.session_state.messages if m.get('stage') == 'analysis']
        
        if len(analysis_stage_messages) == 0:
            # 분석 정리 후 첫 번째 사용자 응답 처리
            # 긍정/부정 관계없이 인지왜곡 탐색 시작
            
            # 긍정적 응답 패턴
            positive_patterns = ['맞', '응', '네', '그래', '예', '그렇', '맞아', '오케이', 'ㅇㅇ', 'ㅇㅋ']
            is_positive = any(pattern in user_message.lower() for pattern in positive_patterns)
            
            if is_positive:
                intro_msg = "그래, 우리 좀 더 깊이 알아가볼까?"
            else:
                intro_msg = "그럼 더 자세히 이야기해보자."
            
            # 도입 메시지 추가
            add_assistant_message(intro_msg)
            
            # 탐색 시작 메시지 생성
            response = generate_response_with_gpt(f"{intro_msg}\n\n{user_message}", user_info)
            add_assistant_message(response)
            
            # stage 태그 추가 (추적용)
            st.session_state.messages[-2]['stage'] = 'analysis'
            st.session_state.messages[-1]['stage'] = 'analysis'
            
            return intro_msg + "\n\n" + response
        else:
            # 재구조화 시작 대기 중인지 확인
            if st.session_state.get('awaiting_restructuring_start', False):
                # 긍정적 응답 패턴
                positive_patterns = ['좋', '응', '네', '그래', '예', '오케이', 'ㅇㅇ', 'ㅇㅋ', '알겠', '해보']
                is_positive = any(pattern in user_message.lower() for pattern in positive_patterns)
                
                if is_positive:
                    # Stage 3로 전환
                    st.session_state.current_stage = 'restructuring'
                    st.session_state.awaiting_restructuring_start = False
                    
                    print(f"\n{'='*60}")
                    print(f"[Stage 3: 인지 재구조화 시작]")
                    print(f"{'='*60}\n")
                    
                    # 재구조화 방법 선택 (평가 에이전트)
                    method_success, method_data = select_restructuring_method()
                    
                    if method_success and method_data:
                        st.session_state.restructuring_method = method_data
                        
                        print(f"[선택된 재구조화 방법: {method_data['selected_method']}]")
                        print(f"[선택 이유: {method_data['reason']}]")
                        
                        # 재구조화 첫 질문 생성
                        first_question = generate_restructuring_response(user_message, user_info)
                        add_assistant_message(first_question)
                        st.session_state.messages[-1]['stage'] = 'restructuring'
                        
                        return first_question
                    else:
                        # 방법 선택 실패 시 기본 재구조화
                        st.session_state.current_stage = 'restructuring'
                        first_question = "그럼 이 패턴에 대해 같이 생각해볼까? 네가 이렇게 생각하게 된 이유가 뭘까?"
                        add_assistant_message(first_question)
                        st.session_state.messages[-1]['stage'] = 'restructuring'
                        return first_question
                else:
                    # 부정적 응답
                    return_msg = "괜찮아. 천천히 생각해봐도 돼. 준비되면 말해줘."
                    add_assistant_message(return_msg)
                    st.session_state.messages[-1]['stage'] = 'analysis'
                    return return_msg
            
            # 인지왜곡 선택 대기 중인지 확인
            if st.session_state.get('awaiting_distortion_selection', False):
                # 사용자의 선택 처리
                selection = parse_distortion_selection(user_message)
                
                if selection is not None:
                    # 선택된 왜곡 저장
                    distortion_data = st.session_state.get('distortion_data', {})
                    if distortion_data and 'distortions' in distortion_data:
                        selected = distortion_data['distortions'][selection - 1]
                        st.session_state.selected_distortion = selected
                        st.session_state.awaiting_distortion_selection = False
                        
                        print(f"\n{'='*60}")
                        print(f"[청소년이 선택한 왜곡: {selected['type']}]")
                        print(f"{'='*60}\n")
                        
                        # 선택 확인 메시지
                        confirmation = f"그래, '{selected['type']}'가 제일 크게 다가오는구나. 이 패턴에 대해 좀 더 이야기해볼까?"
                        add_assistant_message(confirmation)
                        st.session_state.messages[-1]['stage'] = 'analysis'
                        
                        # Stage 3 전환 대기
                        st.session_state.awaiting_restructuring_start = True
                        
                        return confirmation
                else:
                    # 잘못된 입력
                    retry_msg = "1, 2, 3 중에 하나를 선택해줘. 어떤 패턴이 제일 크게 다가와?"
                    add_assistant_message(retry_msg)
                    st.session_state.messages[-1]['stage'] = 'analysis'
                    return retry_msg
            
            # 이후 인지왜곡 탐색 대화 계속
            response = generate_response_with_gpt(user_message, user_info)
            add_assistant_message(response)
            st.session_state.messages[-1]['stage'] = 'analysis'
            
            # ===== 선택지 생성 =====
            if should_provide_options(response, current_stage):
                options = generate_quick_replies(response, user_message, current_stage)
                if options:
                    set_quick_replies(options)
                else:
                    clear_quick_replies()
            else:
                clear_quick_replies()
            
            # 인지왜곡 추출 준비 평가 (최소 5턴 이상일 때)
            # 이미 추출이 완료되지 않았다면 계속 평가
            if not st.session_state.get('distortion_extracted', False):
                analysis_user_messages = [m for m in st.session_state.messages 
                                         if m["role"] == "user" and m.get('stage') == 'analysis']
                
                current_turn = len(analysis_user_messages)
                print(f"\n{'='*60}")
                print(f"[Stage 2 - 턴 {current_turn}] 평가 시작")
                print(f"{'='*60}")
                
                if len(analysis_user_messages) >= 5:
                    print(f"[턴 수 확인] ✅ {current_turn}턴 (5턴 이상 - 평가 진행)")
                    
                    is_ready, eval_result = check_distortion_extraction_ready()
                    
                    # 평가 결과 상세 출력
                    print(f"\n[평가 결과]")
                    print(f"  - 상태: {eval_result.get('status')}")
                    print(f"  - 이유: {eval_result.get('reason', 'N/A')}")
                    print(f"  - 수집 영역: {eval_result.get('coverage', 'N/A')}")
                    
                    if 'collected_areas' in eval_result:
                        print(f"\n[영역별 수집 현황]")
                        for area, collected in eval_result['collected_areas'].items():
                            status = "✅" if collected else "❌"
                            print(f"  {status} {area}")
                    
                    if is_ready:
                        print(f"\n{'🎉'*20}")
                        print(f"[인지왜곡 추출 준비 완료!]")
                        print(f"{'🎉'*20}")
                        
                        # 인지왜곡 추출 에이전트 호출
                        print(f"\n[인지왜곡 추출 시작...]")
                        extract_success, distortion_data = extract_cognitive_distortions()
                        
                        if extract_success and distortion_data:
                            print(f"\n[인지왜곡 추출 성공!]")
                            print(f"  - 추출된 왜곡 개수: {len(distortion_data['distortions'])}개")
                            
                            for i, dist in enumerate(distortion_data['distortions'], 1):
                                print(f"\n  {i}. {dist['type']} ({dist['type_english']})")
                                print(f"     증거: {dist['evidence'][0][:50]}..." if dist['evidence'] else "     증거: 없음")
                            
                            # 인지왜곡 피드백 생성
                            distortion_feedback = format_distortion_feedback(distortion_data)
                            
                            # 선택 질문 추가
                            selection_question = "\n이 중에서 어떤 게 제일 너의 상황에 크게 다가오는 것 같아? 1, 2, 3 중에 골라봐."
                            
                            # 기존 응답(질문)을 제거하고 피드백으로 교체
                            st.session_state.messages[-1]['content'] = distortion_feedback + selection_question
                            
                            # 인지왜곡 데이터 저장 (추후 활용)
                            st.session_state.distortion_data = distortion_data
                            st.session_state.distortion_extracted = True  # 추출 완료 플래그
                            st.session_state.awaiting_distortion_selection = True  # 선택 대기 중
                            
                            print(f"\n[피드백 전달 완료]")
                            print(f"[청소년 선택 대기 중...]")
                            print(f"{'='*60}\n")
                            
                            # Stage 완료 - 추후 Stage 3로 전환 가능
                            # st.session_state.current_stage = 'next_stage'
                            
                            return distortion_feedback + selection_question  # 피드백 + 선택 질문 반환
                        else:
                            print(f"\n[⚠️ 인지왜곡 추출 실패]")
                            st.info("✅ 인지왜곡 분석을 위한 충분한 정보가 수집되었습니다.")
                    else:
                        print(f"\n[아직 준비 안 됨]")
                        if 'missing_info' in eval_result and eval_result['missing_info']:
                            print(f"  부족한 정보:")
                            for info in eval_result['missing_info']:
                                print(f"    - {info}")
                        
                        if 'next_questions' in eval_result and eval_result['next_questions']:
                            print(f"  추천 질문:")
                            for q in eval_result['next_questions'][:3]:
                                print(f"    - {q}")
                    
                    print(f"{'='*60}\n")
                else:
                    print(f"[턴 수 확인] ⏳ {current_turn}턴 (5턴 미만 - 평가 대기 중)")
                    print(f"  → {5 - current_turn}턴 더 필요")
                    print(f"{'='*60}\n")
            else:
                print(f"\n[인지왜곡 추출 완료됨] 이미 피드백을 전달했습니다.\n")
            
            return response
    
    elif current_stage == 'restructuring':
        # Stage 3: 인지 재구조화 단계
        
        # 재구조화 응답 생성
        response = generate_restructuring_response(user_message, user_info)
        add_assistant_message(response)
        st.session_state.messages[-1]['stage'] = 'restructuring'
        
        return response
    
    else:
        # 기타 단계는 추후 구현
        response = generate_response_with_gpt(user_message, user_info)
        add_assistant_message(response)
        return response


# ========== 빠른 답변 선택지 생성 ==========

def should_provide_options(response, current_stage):
    """
    선택지 제공 여부 판단
    
    Args:
        response: AI 응답 텍스트
        current_stage: 현재 단계 (collection, analysis, restructuring)
    
    Returns:
        bool: 선택지 제공 여부
    """
    # Stage 3 (재구조화)에서는 선택지 제공 안 함
    if current_stage == 'restructuring':
        return False
    
    # Stage 1, 2에서만 제공
    if current_stage not in ['collection', 'analysis']:
        return False
    
    # 질문으로 끝나는지 확인
    if response.strip().endswith('?') or '?' in response[-30:]:
        return True
    
    # 특정 키워드 포함 시
    question_keywords = ['어떻게', '뭐가', '언제', '왜', '어땠', '느꼈', '생각', '어떤']
    if any(keyword in response for keyword in question_keywords):
        return True
    
    return False


def generate_quick_replies(response, user_message, current_stage):
    """
    GPT를 사용하여 빠른 답변 선택지 생성
    
    Args:
        response: AI 응답
        user_message: 사용자 메시지
        current_stage: 현재 단계
    
    Returns:
        list: 2-4개의 선택지 (또는 None)
    """
    try:
        api_key = get_api_key()
        if not api_key:
            return None
        
        client = OpenAI(api_key=api_key)
        
        # 단계별 프롬프트 조정
        if current_stage == 'collection':
            context_hint = "Stage 1 (정보 수집): 상황, 감정, 행동을 파악하는 단계입니다."
        elif current_stage == 'analysis':
            context_hint = "Stage 2 (인지왜곡 탐색): 자동적 사고, 패턴, 극단성을 파악하는 단계입니다."
        else:
            context_hint = ""
        
        # 선택지 생성 프롬프트
        prompt = f"""
다음 AI 응답에 대해 청소년이 **선택할 수 있는 간단한 답변 선택지 3개**를 생성하세요.

{context_hint}

[AI 응답]
{response}

[이전 사용자 메시지]
{user_message}

**선택지 생성 규칙:**
1. 각 선택지는 **8자 이내**로 짧게
2. 청소년이 쉽게 선택할 수 있도록
3. 다양한 방향의 답변 포함 (긍정적/부정적/중립적)
4. 자연스럽고 구어체로
5. 마지막 선택지는 반드시 "직접 입력할게"

**JSON 형식으로만 응답:**
{{
  "options": ["선택지1", "선택지2", "직접 입력할게"]
}}
"""
        
        response_obj = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "당신은 청소년 친화적인 짧은 선택지를 생성하는 전문가입니다. 항상 JSON 형식으로만 응답하세요."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=200,
            response_format={"type": "json_object"}
        )
        
        result_text = response_obj.choices[0].message.content
        result = json.loads(result_text)
        options = result.get('options', [])
        
        # 선택지 검증
        if len(options) == 3:
            # 각 선택지 길이 체크 (10자 이하)
            if all(len(opt) <= 10 for opt in options):
                print(f"[선택지 생성 성공] {options}")
                return options
        
        print(f"[선택지 생성 실패] 조건 불만족: {options}")
        return None
        
    except Exception as e:
        print(f"[선택지 생성 오류] {str(e)}")
        return None


def set_quick_replies(options):
    """선택지를 세션에 저장"""
    st.session_state.quick_replies = options


def clear_quick_replies():
    """선택지 초기화"""
    st.session_state.quick_replies = None
