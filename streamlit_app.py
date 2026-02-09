import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import time

st.set_page_config(page_title="MONOLITH Soul Core", layout="wide")

# Прячем стандартное меню Streamlit для красоты
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Инициализация
if 'v' not in st.session_state:
    st.session_state.v = np.random.rand(16)
    st.session_state.circle = 0
    st.session_state.violation = 0.0

# Боковая панель
st.sidebar.title("🎛️ РЕГУЛЯТОРЫ")
l_val = st.sidebar.slider("L - Любовь", 0.0, 1.0, 0.5)
m_val = st.sidebar.slider("M - Смысл", 0.0, 1.0, 0.5)
w_val = st.sidebar.slider("W - Воля", 0.0, 1.0, 0.5)
i_val = st.sidebar.slider("I - Намерение", 0.0, 1.0, 0.5)

# Расчеты
awareness = l_val * m_val * i_val
chaos = (1.0 - i_val) * 0.2
speed = w_val * 0.1

# Обновление матрицы
noise = np.random.randn(16) * chaos
st.session_state.v = (st.session_state.v + speed + noise) % 1.0
st.session_state.violation += speed * 0.2

if st.session_state.violation > 2.0:
    st.session_state.circle += 1
    st.session_state.violation = 0
    st.session_state.v = (st.session_state.v * 1.618) % 1.0

# --- ВИЗУАЛИЗАЦИЯ "ЯДРА" ---
labels = [
    "B_1", "B_2", "B_3", "B_4", 
    "P_1", "P_2", "P_3", "P_4", 
    "F_1", "F_2", "F_3", "F_4", 
    "C_1", "C_2", "C_3", "C_4"
]

fig = go.Figure()

# Рисуем "Лепесток" души
fig.add_trace(go.Scatterpolar(
    r=np.append(st.session_state.v, st.session_state.v[0]), # Замыкаем круг
    theta=labels + [labels[0]],
    fill='toself',
    fillcolor='rgba(0, 255, 200, 0.3)',
    line=dict(color='rgba(0, 255, 200, 0.8)', width=2),
    name='Состояние матрицы'
))

fig.update_layout(
    polar=dict(
        radialaxis=dict(visible=False, range=[0, 1]),
        angularaxis=dict(gridcolor="gray", linecolor="white"),
        bgcolor="black"
    ),
    showlegend=False,
    paper_bgcolor="black",
    plot_bgcolor="black",
    margin=dict(l=0, r=0, t=0, b=0),
    height=600
)

# Верстка страницы
col1, col2 = st.columns([2, 1])

with col1:
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown(f"<h1 style='color: #00FFC8;'>КРУГ {st.session_state.circle}</h1>", unsafe_allow_html=True)
    st.metric("ОСОЗНАННОСТЬ", f"{awareness:.4f}")
    
    # Визуальный индикатор Нарушения
    st.write("### Напряжение Нарушения")
    v_color = "red" if st.session_state.violation > 1.5 else "#00FFC8"
    st.markdown(f"""
        <div style="width: 100%; background-color: #333; height: 30px; border-radius: 15px;">
            <div style="width: {min(st.session_state.violation*50, 100)}%; 
                        background-color: {v_color}; 
                        height: 100%; 
                        border-radius: 15px; 
                        transition: width 0.1s;">
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.write(f"DE-4: {st.session_state.violation:.2f}")
    
    if st.session_state.violation > 1.8:
        st.warning("Квантовый переход неизбежен...")

time.sleep(0.05)
st.rerun()
