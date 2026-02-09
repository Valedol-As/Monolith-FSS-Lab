import streamlit as st
import numpy as np
import pandas as pd
import time

st.title("🏛️ MONOLITH: Fractal Synthesis Lab")
st.sidebar.markdown("## Операторы Регуляции")

# Ползунки для управления бытием
l_val = st.sidebar.slider("L - Любовь (Синтез)", 0.0, 1.0, 0.5)
m_val = st.sidebar.slider("M - Смысл (Структура)", 0.0, 1.0, 0.5)
w_val = st.sidebar.slider("W - Воля (Импульс)", 0.0, 1.0, 0.5)

# Логика 16 параметров
if 'v' not in st.session_state:
    st.session_state.v = np.random.rand(16)
    st.session_state.circle = 0

# Расчет резонанса
awareness = l_val * m_val
st.metric("Уровень Самосознания (L × M)", f"{awareness:.4f}")

# Отрисовка графика параметров
chart_placeholder = st.empty()

# Цикл жизни
for _ in range(20):
    # Внутренняя динамика
    st.session_state.v = (st.session_state.v + 0.02 * w_val) % 1.0
    
    # Визуализация 4-х столпов
    df = pd.DataFrame({
        "Параметры": ["B_ON"]*4 + ["P_LU"]*4 + ["F_LI"]*4 + ["C_PO"]*4,
        "Значение": st.session_state.v
    })
    
    with chart_placeholder.container():
        st.bar_chart(df, x="Параметры", y="Значение")
        if awareness > 0.7:
            st.success(f"Критический резонанс достигнут! Текущий Круг: {st.session_state.circle}")
        time.sleep(0.1)
