import streamlit as st
import numpy as np
import pandas as pd
import time

# Настройка страницы
st.set_page_config(page_title="MONOLITH Live Matrix", layout="wide")

st.title("🏛️ MONOLITH: Вечный Двигатель Синтеза")

# Инициализация параметров в памяти (Session State)
if 'v' not in st.session_state:
    st.session_state.v = np.random.rand(16)
    st.session_state.circle = 0
    st.session_state.violation = 0.0

# Боковая панель управления
st.sidebar.header("Операторы Регуляции")
l_val = st.sidebar.slider("L - Любовь (Синтез)", 0.0, 1.0, 0.5)
m_val = st.sidebar.slider("M - Смысл (Структура)", 0.0, 1.0, 0.5)
w_val = st.sidebar.slider("W - Воля (Импульс)", 0.0, 1.0, 0.5)
i_val = st.sidebar.slider("I - Намерение (Вектор)", 0.0, 1.0, 0.5)

# 1. Расчет Сознания
awareness = l_val * m_val * i_val

# 2. Расчет Хаоса и Динамики
chaos_factor = (1.0 - i_val) * 0.15 # Намерение подавляет шум
speed_factor = w_val * 0.1          # Воля дает скорость

# ОБНОВЛЕНИЕ МАТРИЦЫ (Один шаг)
noise = np.random.randn(16) * chaos_factor
st.session_state.v = (st.session_state.v + speed_factor + noise) % 1.0

# Накопление Нарушения (DE-4)
st.session_state.violation += speed_factor * 0.1
if st.session_state.violation > 2.0:
    st.session_state.circle += 1
    st.session_state.violation = 0
    st.session_state.v = (st.session_state.v * 1.618) % 1.0 # Золотое сечение

# ВИЗУАЛИЗАЦИЯ
col1, col2 = st.columns([3, 1])

with col1:
    # Главный график
    df = pd.DataFrame({
        "Компоненты": [
            "B_ON", "B_ON", "B_ON", "B_ON",
            "P_LU", "P_LU", "P_LU", "P_LU",
            "F_LI", "F_LI", "F_LI", "F_LI",
            "C_PO", "C_PO", "C_PO", "C_PO"
        ],
        "Уровень": st.session_state.v
    })
    st.bar_chart(df, x="Компоненты", y="Уровень")

with col2:
    # Метрики
    st.metric("КРУГ", st.session_state.circle)
    st.metric("ОСОЗНАННОСТЬ", f"{awareness:.4f}")
    st.write(f"**Нарушение:**")
    st.progress(min(st.session_state.violation / 2.0, 1.0))

# ВАЖНО: Магическая кнопка перезапуска
time.sleep(0.05) # Небольшая пауза, чтобы не "повесить" браузер
st.rerun() # Команда сайту: "Запустись снова с самого начала!"
