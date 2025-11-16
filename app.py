import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --- 1. 다중 종 생태계 모델 함수 정의 (4종) ---
# P: 잔디 (생산자)
# C1: 토끼 (1차 소비자)
# C2: 늑대 (2차 소비자)
# D: 곰팡이 (분해자)
def ecosystem_model(
    p0, c1_0, c2_0, d0, 
    alpha_P, beta_1, gamma_P, 
    alpha_1, beta_2, gamma_1, 
    alpha_2, gamma_2, 
    alpha_D, gamma_D, 
    time_steps, dt
):
    """
    4종 생태계 모델 시뮬레이션: 생산자(P), 1차 소비자(C1), 2차 소비자(C2), 분해자(D).
    """
    P = [p0]  # 잔디
    C1 = [c1_0]  # 토끼
    C2 = [c2_0]  # 늑대
    D = [d0]  # 곰팡이

    for i in range(1, time_steps):
        # 이전 시간 단계의 개체수
        prev_P = P[-1]
        prev_C1 = C1[-1]
        prev_C2 = C2[-1]
        prev_D = D[-1]
        
        # 1. 잔디 변화 (dP/dt): 성장 - 토끼 소비 - 자연 사멸
        dP_dt = (alpha_P * prev_P) - (beta_1 * prev_P * prev_C1) - (gamma_P * prev_P)
        
        # 2. 토끼 변화 (dC1/dt): 잔디 소비로 번식 - 늑대 소비 - 자연 사멸
        dC1_dt = (alpha_1 * prev_P * prev_C1) - (beta_2 * prev_C1 * prev_C2) - (gamma_1 * prev_C1)
        
        # 3. 늑대 변화 (dC2/dt): 토끼 소비로 번식 - 자연 사멸
        dC2_dt = (alpha_2 * prev_C1 * prev_C2) - (gamma_2 * prev_C2)
        
        # 4. 곰팡이 변화 (dD/dt): 모든 종의 사체(사멸항)를 분해하여 성장 - 자연 사멸
        # 분해되는 사체량: (잔디 사멸) + (토끼 자연 사멸) + (늑대 자연 사멸)
        death_matter = (gamma_P * prev_P) + (gamma_1 * prev_C1) + (gamma_2 * prev_C2)
        # 곰팡이는 사체량에 비례하여 성장하며, 곰팡이 자체의 개체수(prev_D)도 영향을 줌 (복잡도 단순화를 위해 단순화)
        dD_dt = (alpha_D * death_matter) - (gamma_D * prev_D)

        # 다음 시간 단계의 개체수 계산
        P.append(max(0, prev_P + dP_dt * dt))
        C1.append(max(0, prev_C1 + dC1_dt * dt))
        C2.append(max(0, prev_C2 + dC2_dt * dt))
        D.append(max(0, prev_D + dD_dt * dt))
        
    # 결과를 데이터프레임으로 변환
    time = np.arange(0, time_steps * dt, dt)
    df = pd.DataFrame({
        'Time': time[:len(P)], 
        '🌿 잔디 (생산자)': P, 
        '🐇 토끼 (1차 소비자)': C1, 
        '🐺 늑대 (2차 소비자)': C2,
        '🍄 곰팡이 (분해자)': D
    })
    return df

# --- 2. Streamlit UI 설정 ---
st.set_page_config(layout="wide")
st.title("🌳 4종 생태계 개체수 변화 시뮬레이션")
st.markdown("---")

st.sidebar.header("⚙️ 시뮬레이션 매개변수 설정")

# --- 3. 슬라이더를 이용한 초기값 설정 ---
st.sidebar.subheader("1. 초기 개체수 설정")
initial_p = st.sidebar.slider("🌿 잔디 (생산자) 초기 개체수", 100, 2000, 1000)
initial_c1 = st.sidebar.slider("🐇 토끼 (1차 소비자) 초기 개체수", 10, 500, 100)
initial_c2 = st.sidebar.slider("🐺 늑대 (2차 소비자) 초기 개체수", 10, 200, 30)
initial_d = st.sidebar.slider("🍄 곰팡이 (분해자) 초기 개체수", 10, 500, 50)

# --- 4. Lotka-Volterra 계수 설정 (상호작용 강도) ---
st.sidebar.subheader("2. 상호작용 계수 설정")

# 4-1. 잔디 (생산자) 계수
st.sidebar.markdown("##### 🌿 잔디 계수")
alpha_P = st.sidebar.slider("$\alpha_P$ (자연 성장률)", 0.0, 1.0, 0.4, 0.01)
gamma_P = st.sidebar.slider("$\gamma_P$ (자연 사멸률)", 0.0, 0.5, 0.05, 0.01)
beta_1 = st.sidebar.slider("$\beta_1$ (토끼에게 소비되는 비율)", 0.0, 0.1, 0.01, 0.001)

# 4-2. 토끼 (1차 소비자) 계수
st.sidebar.markdown("##### 🐇 토끼 계수")
alpha_1 = st.sidebar.slider("$\alpha_1$ (잔디 소비 효율)", 0.0, 0.1, 0.005, 0.001)
gamma_1 = st.sidebar.slider("$\gamma_1$ (자연 사멸률)", 0.0, 0.5, 0.2, 0.01)
beta_2 = st.sidebar.slider("$\beta_2$ (늑대에게 소비되는 비율)", 0.0, 0.1, 0.001, 0.0001)

# 4-3. 늑대 (2차 소비자) 계수
st.sidebar.markdown("##### 🐺 늑대 계수")
alpha_2 = st.sidebar.slider("$\alpha_2$ (토끼 소비 효율)", 0.0, 0.1, 0.0005, 0.0001)
gamma_2 = st.sidebar.slider("$\gamma_2$ (자연 사멸률)", 0.0, 0.5, 0.3, 0.01)

# 4-4. 곰팡이 (분해자) 계수
st.sidebar.markdown("##### 🍄 곰팡이 계수")
alpha_D = st.sidebar.slider("$\alpha_D$ (사체 분해 효율)", 0.0, 0.5, 0.01, 0.001)
gamma_D = st.sidebar.slider("$\gamma_D$ (자연 사멸률)", 0.0, 0.5, 0.1, 0.01)

# 시뮬레이션 시간 설정
total_time = st.sidebar.slider("3. 총 시뮬레이션 시간 (T)", 10, 300, 100)
dt = 0.1 # 시간 간격 (이 값을 작게 할수록 정확해짐)
time_steps = int(total_time / dt)

# --- 5. 모델 실행 및 결과 표시 ---
st.subheader("📊 시간에 따른 4종 개체수 변화 그래프")

# 모델 실행
population_df = ecosystem_model(
    initial_p, initial_c1, initial_c2, initial_d, 
    alpha_P, beta_1, gamma_P, 
    alpha_1, beta_2, gamma_1, 
    alpha_2, gamma_2, 
    alpha_D, gamma_D, 
    time_steps, dt
)

# Streamlit 차트 표시 (Pandas DataFrame을 바로 전달)
st.line_chart(population_df.set_index('Time'))

# 최종 개체수 요약 및 애니메이션 자리
st.subheader("💡 개체군 요약 및 생태계 애니메이션")

col1, col2, col3, col4 = st.columns(4)

# 잔디
final_p = int(population_df['🌿 잔디 (생산자)'].iloc[-1])
col1.metric(label="🌿 잔디 최종 개체수", value=f"{final_p:,} 단위")
col1.image("https://via.placeholder.com/150x150/4CAF50/FFFFFF?text=Grass", width=150)

# 토끼
final_c1 = int(population_df['🐇 토끼 (1차 소비자)'].iloc[-1])
col2.metric(label="🐇 토끼 최종 개체수", value=f"{final_c1:,} 마리")
col2.image("https://via.placeholder.com/150x150/FFD700/000000?text=Rabbit", width=150)

# 늑대
final_c2 = int(population_df['🐺 늑대 (2차 소비자)'].iloc[-1])
col3.metric(label="🐺 늑대 최종 개체수", value=f"{final_c2:,} 마리")
col3.image("https://via.placeholder.com/150x150/808080/FFFFFF?text=Wolf", width=150)

# 곰팡이
final_d = int(population_df['🍄 곰팡이 (분해자)'].iloc[-1])
col4.metric(label="🍄 곰팡이 최종 개체수", value=f"{final_d:,} 단위")
col4.image("https://via.placeholder.com/150x150/A0522D/FFFFFF?text=Fungi", width=150)

st.markdown("""
<style>
.stMetric {
    text-align: center;
    padding: 10px;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
.stImage > img {
    border-radius: 50%;
    margin-top: 10px;
    object-fit: cover;
    border: 3px solid #f0f0f0;
}
</style>
""", unsafe_allow_html=True)

st.markdown("---")
st.caption("참고: 애니메이션은 Placeholder 이미지로 대체되었으며, 실제 배포 시 'streamlit-lottie' 라이브러리와 적절한 .json 파일을 사용하여 동적 애니메이션을 구현할 수 있습니다.")
