import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

st.set_page_config(page_title="MONOLITH Living Matrix", layout="wide")

# Темная тема
st.markdown("<style>.stApp { background-color: #050505; color: #00FFC8; }</style>", unsafe_allow_html=True)

if 'v' not in st.session_state:
    st.session_state.v = np.random.rand(16)
    st.session_state.circle = 0
    st.session_state.violation = 0.0

# Панель управления
st.sidebar.title("💠 ОПЕРАТОРЫ")
l_val = st.sidebar.slider("L - Любовь (Синхронность)", 0.0, 1.0, 0.5)
m_val = st.sidebar.slider("M - Смысл (Упорядоченность)", 0.0, 1.0, 0.5)
w_val = st.sidebar.slider("W - Воля (Скорость)", 0.0, 1.0, 0.5)
i_val = st.sidebar.slider("I - Намерение (Стабильность)", 0.0, 1.0, 0.5)

# --- МАТЕМАТИКА РЕГУЛЯЦИИ ---
awareness = l_val * m_val * i_val
speed = w_val * 0.1
noise_level = (1.0 - i_val) * 0.2

# 1. Эффект ЛЮБВИ: Параметры тянутся к среднему (Синхронизация)
mean_v = np.mean(st.session_state.v)
st.session_state.v = st.session_state.v * (1 - l_val*0.1) + mean_v * (l_val*0.1)

# 2. Эффект СМЫСЛА: Параметры тянутся к идеальным точкам (0.2, 0.5, 0.8)
target_m = np.where(st.session_state.v > 0.5, 0.8, 0.2)
st.session_state.v = st.session_state.v * (1 - m_val*0.1) + target_m * (m_val*0.1)

# 3. Эффект ВОЛИ и НАМЕРЕНИЯ
st.session_state.v = (st.session_state.v + speed + np.random.randn(16) * noise_level) % 1.0

# Нарушение
st.session_state.violation += speed * 0.1
if st.session_state.violation > 2.0:
    st.session_state.circle += 1
    st.session_state.violation = 0
    st.session_state.v = (st.session_state.v * 1.618) % 1.0

# --- ВИЗУАЛИЗАЦИЯ ---
angles = np.linspace(0, 2*np.pi, 16, endpoint=False)
x = np.cos(angles) * st.session_state.v
y = np.sin(angles) * st.session_state.v

fig = go.Figure()

# Линии связей (зависят от Любви и Смысла)
for i in range(16):
    for j in range(i+1, 16):
        res = st.session_state.v[i] * st.session_state.v[j]
        # Чем выше Любовь, тем больше связей мы видим
        if res > (0.6 - l_val*0.3): 
            fig.add_trace(go.Scatter(
                x=[x[i], x[j]], y=[y[i], y[j]],
                mode='lines',
                line=dict(color=f'rgba(0, 255, 200, {res*l_val*0.5})', width=1),
                hoverinfo='skip'
            ))

# Ядро Сознания
core_size = awareness * 100
fig.add_trace(go.Scatter(
    x=[0], y=[0], mode='markers',
    marker=dict(size=core_size, color='white', opacity=awareness),
    name='Сознание'
))

# Точки параметров (Цвет зависит от Смысла)
node_colors = [f'rgba({int(255*m_val)}, 255, {int(200*(1-m_val))}, 1)' for _ in range(16)]
fig.add_trace(go.Scatter(
    x=x, y=y, mode='markers',
    marker=dict(size=12, color=node_colors, line=dict(color='white', width=1))
))

fig.update_layout(
    showlegend=False,
    xaxis=dict(visible=False, range=[-1.2, 1.2]),
    yaxis=dict(visible=False, range=[-1.2, 1.2]),
    paper_bgcolor="black", plot_bgcolor="black",
    height=700, margin=dict(l=0, r=0, t=0, b=0)
)

c1, c2 = st.columns([3, 1])
with c1: st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
with c2:
    st.write(f"## КРУГ {st.session_state.circle}")
    st.metric("ОСОЗНАННОСТЬ", f"{awareness:.4f}")
    st.write("---")
    st.write("🔥 Нарушение")
    st.progress(min(st.session_state.violation/2.0, 1.0))

time.sleep(0.05)
st.rerun()
