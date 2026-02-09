import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

st.set_page_config(page_title="MONOLITH Fractal Core", layout="wide", page_icon="⚛️")

# Стилизация под глубокий космос
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00FFC8; }
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

# Инициализация состояний
if 'v' not in st.session_state:
    st.session_state.v = np.random.rand(16)
    st.session_state.history = [] # Хранилище для шлейфа памяти
    st.session_state.circle = 0
    st.session_state.violation = 0.0

# Панель управления
st.sidebar.title("💠 ОПЕРАТОРЫ")
l_val = st.sidebar.slider("L - Любовь", 0.0, 1.0, 0.5)
m_val = st.sidebar.slider("M - Смысл", 0.0, 1.0, 0.5)
w_val = st.sidebar.slider("W - Воля", 0.0, 1.0, 0.5)
i_val = st.sidebar.slider("I - Намерение", 0.0, 1.0, 0.5)

# Математика движка
awareness = l_val * m_val * i_val
chaos = (1.0 - i_val) * 0.15
speed = w_val * 0.08

# Эволюция параметров
noise = np.random.randn(16) * chaos
st.session_state.v = (st.session_state.v + speed + noise) % 1.0

# Добавляем текущее состояние в историю (шлейф из 10 шагов)
st.session_state.history.append(list(st.session_state.v))
if len(st.session_state.history) > 10:
    st.session_state.history.pop(0)

# Проверка Нарушения
st.session_state.violation += speed * 0.15
if st.session_state.violation > 2.0:
    st.session_state.circle += 1
    st.session_state.violation = 0
    st.session_state.v = (st.session_state.v * 1.618) % 1.0

# --- ПОСТРОЕНИЕ ГРАФИКА "ФРАКТАЛЬНОЕ ОБЛАКО" ---
fig = go.Figure()

# Рисуем шлейфы (Прошлое)
for h_idx, past_v in enumerate(st.session_state.history):
    opacity = (h_idx + 1) / len(st.session_state.history) * 0.3
    angles = np.linspace(0, 2*np.pi, 16, endpoint=False)
    x_past = np.cos(angles) * past_v
    y_past = np.sin(angles) * past_v
    
    fig.add_trace(go.Scatter(
        x=np.append(x_past, x_past[0]), 
        y=np.append(y_past, y_past[0]),
        mode='lines',
        line=dict(color=f'rgba(0, 255, 200, {opacity})', width=1),
        hoverinfo='skip'
    ))

# Рисуем текущую структуру (Настоящее)
angles = np.linspace(0, 2*np.pi, 16, endpoint=False)
x_curr = np.cos(angles) * st.session_state.v
y_curr = np.sin(angles) * st.session_state.v

# Линии синтеза (связи между параметрами)
for i in range(16):
    for j in range(i+1, 16):
        resonance = st.session_state.v[i] * st.session_state.v[j]
        if resonance > 0.4: # Только сильные связи
            fig.add_trace(go.Scatter(
                x=[x_curr[i], x_curr[j]], y=[y_curr[i], y_curr[j]],
                mode='lines',
                line=dict(color=f'rgba(255, 255, 255, {resonance*0.5})', width=1),
                hoverinfo='skip'
            ))

# Центральное Ядро (Солнце Сознания)
core_size = awareness * 50
fig.add_trace(go.Scatter(
    x=[0], y=[0],
    mode='markers',
    marker=dict(size=core_size, color='white', shadow=dict(color='white', width=20)),
    name='Awareness'
))

# Точки параметров
fig.add_trace(go.Scatter(
    x=x_curr, y=y_curr,
    mode='markers+text',
    marker=dict(size=10, color='#00FFC8', line=dict(color='white', width=1)),
    text=["B", "B", "B", "B", "P", "P", "P", "P", "F", "F", "F", "F", "C", "C", "C", "C"],
    textposition="top center"
))

fig.update_layout(
    showlegend=False,
    xaxis=dict(visible=False, range=[-1.2, 1.2]),
    yaxis=dict(visible=False, range=[-1.2, 1.2]),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    height=700,
    margin=dict(l=0, r=0, t=0, b=0)
)

# Верстка
c1, c2 = st.columns([3, 1])
with c1:
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with c2:
    st.write(f"## КРУГ {st.session_state.circle}")
    st.metric("ОСОЗНАННОСТЬ", f"{awareness:.4f}")
    st.write("---")
    st.write("🧬 Потенциал Сущности")
    st.progress(min(sum(st.session_state.v)/16, 1.0))
    st.write("🔥 Напряжение (DE-4)")
    st.progress(min(st.session_state.violation/2.0, 1.0))

time.sleep(0.04)
st.rerun()
