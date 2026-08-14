import streamlit as st
import time

# ---------------------------------------------------------
# 1. 페이지 기본 설정 및 CSS 디자인 적용
# ---------------------------------------------------------
st.set_page_config(page_title="⏱️ 나만의 반응형 타이머", page_icon="⏱️", layout="centered")

# 화면 크기에 따라 글씨가 자연스럽게 변하는 반응형 CSS (clamp 사용)
st.markdown("""
<style>
    /* 중앙 타이머 카드 디자인 */
    .timer-card {
        background-color: #ffffff;
        border-radius: 20px;
        padding: 40px 20px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 20px;
        border: 2px solid #f0f2f6;
    }
    /* 타이머 숫자 디자인 (화면 크기에 따라 3rem ~ 8rem 사이로 자동 조절) */
    .timer-text {
        font-size: clamp(3rem, 15vw, 8rem);
        font-weight: 900;
        color: #1f77b4;
        font-family: 'Courier New', Courier, monospace;
        line-height: 1.2;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# 2. 상태 저장소 (Session State) 초기화
# ---------------------------------------------------------
# 앱이 새로고침되어도 유지되어야 하는 데이터들을 저장합니다.
if 'state' not in st.session_state:
    st.session_state.state = 'stopped'  # 상태: stopped, running, paused, finished
if 'total_seconds' not in st.session_state:
    st.session_state.total_seconds = 0
if 'remaining_seconds' not in st.session_state:
    st.session_state.remaining_seconds = 0
if 'target_time' not in st.session_state:
    st.session_state.target_time = 0.0
if 'show_balloons' not in st.session_state:
    st.session_state.show_balloons = False

# 숫자 입력창(number_input)과 동기화하기 위한 초기값
if 'in_min' not in st.session_state:
    st.session_state.in_min = 0
if 'in_sec' not in st.session_state:
    st.session_state.in_sec = 0


# ---------------------------------------------------------
# 3. 타이머 제어 함수 (시작, 일시정지, 계속, 초기화, 빠른설정)
# ---------------------------------------------------------
def set_time(minutes, seconds):
    """빠른 설정 버튼을 누르면 입력창의 분/초를 변경합니다."""
    st.session_state.in_min = minutes
    st.session_state.in_sec = seconds
    st.session_state.state = 'stopped'

def start_timer():
    """타이머를 시작합니다."""
    total = (st.session_state.in_min * 60) + st.session_state.in_sec
    if total > 0:
        st.session_state.total_seconds = total
        st.session_state.remaining_seconds = total
        # time.monotonic()은 컴퓨터의 절대 시간을 가져와 정확한 계산을 보장합니다.
        st.session_state.target_time = time.monotonic() + total
        st.session_state.state = 'running'
    else:
        st.warning("시간을 1초 이상 설정해 주세요!")

def pause_timer():
    """타이머를 일시정지 합니다."""
    st.session_state.state = 'paused'
    # 멈추는 순간의 남은 시간을 정확히 계산해서 저장합니다.
    st.session_state.remaining_seconds = st.session_state.target_time - time.monotonic()

def resume_timer():
    """일시정지된 타이머를 다시 이어서 실행합니다."""
    st.session_state.state = 'running'
    # 저장된 남은 시간을 바탕으로 목표 시간을 새로 설정합니다.
    st.session_state.target_time = time.monotonic() + st.session_state.remaining_seconds

def reset_timer():
    """타이머를 초기화합니다."""
    st.session_state.state = 'stopped'
    st.session_state.remaining_seconds = 0


# ---------------------------------------------------------
# 4. 완료 시 풍선 효과 처리 (Fragment 외부에서 실행)
# ---------------------------------------------------------
if st.session_state.show_balloons:
    st.balloons()
    st.session_state.show_balloons = False


# ---------------------------------------------------------
# 5. 화면 레이아웃 구성
# ---------------------------------------------------------
st.title("⏱️ 나만의 반응형 타이머")

# 현재 타이머가 실행 중이거나 일시정지 상태인지 확인합니다. (입력창 비활성화용)
is_active = st.session_state.state in ['running', 'paused']

# [시간 설정 영역]
st.markdown("##### ⚡ 빠른 설정")
# 모바일에서도 잘 보이도록 4열로 나누어 버튼을 배치합니다.
q1, q2, q3, q4 = st.columns(4)
with q1:
    if st.button("1분", use_container_width=True, disabled=is_active): set_time(1, 0)
with q2:
    if st.button("3분", use_container_width=True, disabled=is_active): set_time(3, 0)
with q3:
    if st.button("5분", use_container_width=True, disabled=is_active): set_time(5, 0)
with q4:
    if st.button("10분", use_container_width=True, disabled=is_active): set_time(10, 0)

# 직접 입력 영역
c1, c2 = st.columns(2)
with c1:
    st.number_input("분 (Minutes)", min_value=0, max_value=99, key="in_min", disabled=is_active)
with c2:
    st.number_input("초 (Seconds)", min_value=0, max_value=59, key="in_sec", disabled=is_active)


# ---------------------------------------------------------
# 6. 실시간 타이머 화면 (Fragment 기능 사용)
# ---------------------------------------------------------
# @st.fragment(run_every=0.1) : 이 부분만 0.1초마다 새로고침하여 깜빡임을 방지합니다.
@st.fragment(run_every=0.1)
def display_timer():
    # 실행 중일 때 남은 시간 계산
    if st.session_state.state == 'running':
        now = time.monotonic()
        rem = st.session_state.target_time - now
        
        # 타이머 종료 처리
        if rem <= 0:
            st.session_state.remaining_seconds = 0
            st.session_state.state = 'finished'
            st.session_state.show_balloons = True
            st.rerun() # 상태가 변경되었으므로 전체 화면을 한 번 새로고침합니다.
        else:
            st.session_state.remaining_seconds = rem

    # 남은 시간을 MM:SS 형태로 변환
    rem_s = int(st.session_state.remaining_seconds)
    mins = rem_s // 60
    secs = rem_s % 60
    time_str = f"{mins:02d}:{secs:02d}"

    # 카드 형태와 반응형 글씨로 화면에 출력 (HTML/CSS 활용)
    st.markdown(f"<div class='timer-card'><div class='timer-text'>{time_str}</div></div>", unsafe_allow_html=True)

    # 진행률 막대(Progress bar) 계산 및 출력
    progress = 0.0
    if st.session_state.total_seconds > 0:
        progress = st.session_state.remaining_seconds / st.session_state.total_seconds
    
    st.progress(max(0.0, min(1.0, progress)))

    # 완료 시 성공 메시지
    if st.session_state.state == 'finished':
        st.success("🎉 타이머가 종료되었습니다! 수고하셨습니다.")

# Fragment 함수 실행
display_timer()


# ---------------------------------------------------------
# 7. 조작 버튼 영역 (시작, 일시정지, 계속, 초기화)
# ---------------------------------------------------------
st.write("") # 약간의 여백
b1, b2 = st.columns(2)

with b1:
    if st.session_state.state == 'stopped' or st.session_state.state == 'finished':
        if st.button("▶️ 시작 (Start)", use_container_width=True, type="primary"):
            start_timer()
            st.rerun()
    elif st.session_state.state == 'running':
        if st.button("⏸️ 일시정지 (Pause)", use_container_width=True):
            pause_timer()
            st.rerun()
    elif st.session_state.state == 'paused':
        if st.button("▶️ 계속 (Resume)", use_container_width=True, type="primary"):
            resume_timer()
            st.rerun()

with b2:
    # 실행 중이거나 일시정지, 완료 상태일 때 초기화 버튼 표시
    if st.session_state.state != 'stopped':
        if st.button("🔄 초기화 (Reset)", use_container_width=True):
            reset_timer()
            st.rerun()
