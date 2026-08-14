시간 설정 기능이 조금 아쉽게 느껴지셨군요! 직접 숫자를 입력하거나 정해진 시간(1분, 3분 등)으로만 덮어쓰는 방식 대신, 원하는 시간을 쉽게 더하고 뺄 수 있는 '미세 조절' 기능과 더 직관적인 버튼 배치를 추가하여 시간 설정 기능을 대폭 업그레이드했습니다.

기존 코드에서 app.py 파일만 아래 코드로 덮어쓰기 하시면 됩니다.

📝 수정된 app.py (시간 설정 기능 강화)
Python
import streamlit as st
import time

# ---------------------------------------------------------
# 1. 페이지 기본 설정 및 CSS 디자인 적용
# ---------------------------------------------------------
st.set_page_config(page_title="⏱️ 나만의 반응형 타이머", page_icon="⏱️", layout="centered")

st.markdown("""
<style>
    .timer-card {
        background-color: #ffffff;
        border-radius: 20px;
        padding: 40px 20px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 20px;
        border: 2px solid #f0f2f6;
    }
    .timer-text {
        font-size: clamp(3rem, 15vw, 8rem);
        font-weight: 900;
        color: #1f77b4;
        font-family: 'Courier New', Courier, monospace;
        line-height: 1.2;
        margin: 10px 0;
    }
    /* 버튼 텍스트 크기 미세조정 */
    .stButton>button {
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# 2. 상태 저장소 (Session State) 초기화
# ---------------------------------------------------------
if 'state' not in st.session_state:
    st.session_state.state = 'stopped'  # stopped, running, paused, finished
if 'total_seconds' not in st.session_state:
    st.session_state.total_seconds = 0
if 'remaining_seconds' not in st.session_state:
    st.session_state.remaining_seconds = 0
if 'target_time' not in st.session_state:
    st.session_state.target_time = 0.0
if 'show_balloons' not in st.session_state:
    st.session_state.show_balloons = False

if 'in_min' not in st.session_state:
    st.session_state.in_min = 0
if 'in_sec' not in st.session_state:
    st.session_state.in_sec = 0


# ---------------------------------------------------------
# 3. 타이머 제어 함수
# ---------------------------------------------------------
def set_time(minutes, seconds):
    """지정된 시간으로 덮어씁니다."""
    st.session_state.in_min = minutes
    st.session_state.in_sec = seconds
    st.session_state.state = 'stopped'

def add_time(minutes, seconds):
    """현재 설정된 시간에 분/초를 더하거나 뺍니다."""
    # 현재 설정된 총 시간을 초로 계산
    total = (st.session_state.in_min * 60) + st.session_state.in_sec
    # 추가할 시간을 초 단위로 더함
    total += (minutes * 60) + seconds
    
    # 0초보다 작아지지 않게 방지
    if total < 0:
        total = 0
    # 99분 59초를 넘지 않게 방지 (에러 방지)
    if total > 5999:
        total = 5999
        
    st.session_state.in_min = total // 60
    st.session_state.in_sec = total % 60
    st.session_state.state = 'stopped'

def start_timer():
    total = (st.session_state.in_min * 60) + st.session_state.in_sec
    if total > 0:
        st.session_state.total_seconds = total
        st.session_state.remaining_seconds = total
        st.session_state.target_time = time.monotonic() + total
        st.session_state.state = 'running'
    else:
        st.warning("시간을 1초 이상 설정해 주세요!")

def pause_timer():
    st.session_state.state = 'paused'
    st.session_state.remaining_seconds = st.session_state.target_time - time.monotonic()

def resume_timer():
    st.session_state.state = 'running'
    st.session_state.target_time = time.monotonic() + st.session_state.remaining_seconds

def reset_timer():
    st.session_state.state = 'stopped'
    st.session_state.remaining_seconds = 0
    # 초기화 버튼을 누르면 입력창도 0으로 되돌립니다.
    st.session_state.in_min = 0
    st.session_state.in_sec = 0


# ---------------------------------------------------------
# 4. 완료 시 효과
# ---------------------------------------------------------
if st.session_state.show_balloons:
    st.balloons()
    st.session_state.show_balloons = False


# ---------------------------------------------------------
# 5. 화면 레이아웃 구성
# ---------------------------------------------------------
st.title("⏱️ 나만의 반응형 타이머")

is_active = st.session_state.state in ['running', 'paused']

# --- [시간 설정 기능 강화 영역] ---
st.markdown("##### ⚙️ 시간 설정")

# 1. 덮어쓰기 (간편 타이머)
st.caption("고정 시간 선택")
q1, q2, q3, q4 = st.columns(4)
with q1:
    if st.button("1분", use_container_width=True, disabled=is_active): set_time(1, 0)
with q2:
    if st.button("3분", use_container_width=True, disabled=is_active): set_time(3, 0)
with q3:
    if st.button("5분", use_container_width=True, disabled=is_active): set_time(5, 0)
with q4:
    if st.button("10분", use_container_width=True, disabled=is_active): set_time(10, 0)

# 2. 미세 조절 (더하기/빼기)
st.caption("시간 더하기 / 빼기")
a1, a2, a3, a4 = st.columns(4)
with a1:
    if st.button("+ 1분", use_container_width=True, disabled=is_active): add_time(1, 0)
with a2:
    if st.button("- 1분", use_container_width=True, disabled=is_active): add_time(-1, 0)
with a3:
    if st.button("+ 10초", use_container_width=True, disabled=is_active): add_time(0, 10)
with a4:
    if st.button("- 10초", use_container_width=True, disabled=is_active): add_time(0, -10)

# 3. 직접 입력
st.caption("직접 입력")
c1, c2 = st.columns(2)
with c1:
    st.number_input("분 (Minutes)", min_value=0, max_value=99, key="in_min", disabled=is_active)
with c2:
    st.number_input("초 (Seconds)", min_value=0, max_value=59, key="in_sec", disabled=is_active)

st.divider() # 구분선 추가


# ---------------------------------------------------------
# 6. 실시간 타이머 화면
# ---------------------------------------------------------
@st.fragment(run_every=0.1)
def display_timer():
    if st.session_state.state == 'running':
        now = time.monotonic()
        rem = st.session_state.target_time - now
        
        if rem <= 0:
            st.session_state.remaining_seconds = 0
            st.session_state.state = 'finished'
            st.session_state.show_balloons = True
            st.rerun()
        else:
            st.session_state.remaining_seconds = rem

    rem_s = int(st.session_state.remaining_seconds)
    mins = rem_s // 60
    secs = rem_s % 60
    time_str = f"{mins:02d}:{secs:02d}"

    st.markdown(f"<div class='timer-card'><div class='timer-text'>{time_str}</div></div>", unsafe_allow_html=True)

    progress = 0.0
    if st.session_state.total_seconds > 0:
        progress = st.session_state.remaining_seconds / st.session_state.total_seconds
    
    st.progress(max(0.0, min(1.0, progress)))

    if st.session_state.state == 'finished':
        st.success("🎉 타이머가 종료되었습니다! 수고하셨습니다.")

display_timer()


# ---------------------------------------------------------
# 7. 조작 버튼 영역
# ---------------------------------------------------------
st.write("")
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
    if st.button("🔄 초기화 (Reset)", use_container_width=True):
        reset_timer()
        st.rerun()
