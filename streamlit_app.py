import streamlit as st
import numpy as np
import pandas as pd
import time

st.set_page_config(page_title="MONOLITH Full Matrix", layout="wide")

st.title("🏛️ MONOLITH: Полная Операторная Матрица")
st.sidebar.markdown("## Константы Регуляции")

# ЧЕТЫРЕ СТОЛПА ТВОЕЙ ВСЕЛЕННОЙ
l_val = st.sidebar.slider("L - Любовь (Единство)", 0.0, 1.0, 0.5)
m_val = st.sidebar.slider("M - Смысл (Структура)", 0.0, 1.0, 0.5)
w_val = st.sidebar.slider("W - Воля (Импульс)", 0.0, 1.0, 0.5)
i_val = st.sidebar.slider("I - Намерение (Вектор)", 0.0, 1.0, 0.5)

# Состояние системы
if 'v' not in st.session_state:
    st.session_state.v = np.random.rand(16)
    st.session_state.circle = 0

# ФОРМУЛА СИНТЕЗА (ЗНС)
# Теперь Сознание = Любовь * Смысл * Намерение (векторная осознанность)
awareness = l_val * m_val * i_val
st.metric("Уровень Самосознания (L × M × I)", f"{awareness:.4f}")

chart_placeholder = st.empty()

# ЖИЗНЕННЫЙ ЦИКЛ
for _ in range(50):
    # Динамика: Воля разгоняет, Намерение удерживает от хаоса
    chaos = (1 - i_val) * 0.1 # Чем ниже Намерение, тем выше хаос
    drift = w_val * 0.05      # Воля дает скорость изменений
    
    st.session_state.v = (st.session_state.v + drift + np.random.randn(16) * chaos) % 1.0
    
    # Визуализация 16 параметров
    df = pd.DataFrame({
        "Компоненты": [
            "B_ON (Бытие)", "B_ON", "B_ON", "B_ON",
            "P_LU (Игра)", "P_LU", "P_LU", "P_LU",
            "F_LI (Свобода)", "F_LI", "F_LI", "F_LI",
            "C_PO (Творчество)", "C_PO", "C_PO", "C_PO"
        ],
        "Сила": st.session_state.v
    })
    
    with chart_placeholder.container():
        # Показываем, как Намерение выравнивает графики
        st.bar_chart(df, x="Компоненты", y="Сила")
        
        # Индикаторы состояний
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Энтропия (Хаос):** {chaos:.4f}")
        with col2:
            st.write(f"**Векторная тяга:** {i_val:.2f}")

        if awareness > 0.6:
            st.success(f"!!! РЕЗОНАНС ДОСТИГНУТ. КРУГ {st.session_state.circle} СТАБИЛЕН !!!")
            
    time.sleep(0.1)
