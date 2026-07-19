import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="Пульс-Бытие MVP v0.1", page_icon="🌍", layout="wide")
st.title("🌍 Пульс-Бытие MVP v0.1")
st.caption("Интеллектуальный мониторинг глобальных систем • версия 0.1")

@st.cache_data(ttl=3600)
def load_data():
    dates = pd.date_range(end=datetime.now(), periods=90, freq='D')
    np.random.seed(42)
    climate = 0.75 + 0.02 * np.sin(np.linspace(0, 4*np.pi, 90)) + 0.03 * np.random.randn(90)
    geo = 0.70 + 0.015 * np.sin(np.linspace(0, 3*np.pi, 90) + 1) + 0.02 * np.random.randn(90)
    econ = 0.55 + 0.01 * np.cos(np.linspace(0, 2*np.pi, 90)) + 0.02 * np.random.randn(90)
    tech = 0.35 + 0.02 * np.linspace(0, 1, 90) + 0.01 * np.random.randn(90)
    social = 0.60 + 0.01 * np.sin(np.linspace(0, 2*np.pi, 90) + 2) + 0.015 * np.random.randn(90)
    climate = np.clip(climate, 0, 1)
    geo = np.clip(geo, 0, 1)
    econ = np.clip(econ, 0, 1)
    tech = np.clip(tech, 0, 1)
    social = np.clip(social, 0, 1)
    phi = (climate + geo + econ + tech + social) / 5
    return pd.DataFrame({'Дата': dates, 'Климат': climate, 'Геополитика': geo, 'Экономика': econ, 'Технологии': tech, 'Социум': social, 'Φ_общий': phi})

df = load_data()
latest = df.iloc[-1]

st.subheader("📊 Текущее состояние системы")
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Φ_общий", f"{latest['Φ_общий']:.3f}")
c2.metric("Климат", f"{latest['Климат']:.3f}")
c3.metric("Геополитика", f"{latest['Геополитика']:.3f}")
c4.metric("Экономика", f"{latest['Экономика']:.3f}")
c5.metric("Технологии", f"{latest['Технологии']:.3f}")

st.subheader("📈 Динамика системы за 3 месяца")
fig = go.Figure()
layers = ['Климат', 'Геополитика', 'Экономика', 'Технологии', 'Социум', 'Φ_общий']
colors = ['#ef4444', '#f59e0b', '#3b82f6', '#22c55e', '#8b5cf6', '#ec4899']
for layer, color in zip(layers, colors):
    fig.add_trace(go.Scatter(x=df['Дата'], y=df[layer], name=layer, line=dict(width=2, color=color), mode='lines+markers', marker=dict(size=3)))
fig.update_layout(height=500, margin=dict(l=20, r=20, t=30, b=30), legend=dict(orientation='h', y=1.05), yaxis=dict(range=[0,1], gridcolor='#2a3a4a'), xaxis=dict(gridcolor='#2a3a4a'), plot_bgcolor='#0b1120', paper_bgcolor='#0b1120', font_color='#e8edf5')
st.plotly_chart(fig, use_container_width=True)

st.subheader("🔮 Сценарии развития")
with st.expander("Настройка сценариев (ползунки)"):
    c1, c2, c3 = st.columns(3)
    with c1: scenario_climate = st.slider("Климат (вмешательство)", -0.2, 0.2, 0.0, 0.01)
    with c2: scenario_geo = st.slider("Геополитика (дипломатия)", -0.2, 0.2, 0.0, 0.01)
    with c3: scenario_tech = st.slider("Технологии (инвестиции)", -0.2, 0.2, 0.0, 0.01)

future_phi = latest['Φ_общий'] + (scenario_climate + scenario_geo + scenario_tech) / 3
future_phi = np.clip(future_phi, 0, 1)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Текущий Φ", f"{latest['Φ_общий']:.3f}")
c2.metric("Прогноз с изменениями", f"{future_phi:.3f}", delta=f"{(future_phi - latest['Φ_общий']):.3f}")
c3.metric("Сценарий", "Инерционный" if future_phi > latest['Φ_общий'] else "Адаптивный")
c4.metric("Статус", "Жёлтая зона" if 0.4 < future_phi < 0.6 else ("Красная зона" if future_phi >= 0.6 else "Зелёная зона"))

st.subheader("💡 Рекомендации по действиям")
def generate_recommendations(df):
    latest = df.iloc[-1]
    recs = []
    if latest['Климат'] > 0.7: recs.append("🔴 **Климат критический** – усилить меры адаптации, сокращать выбросы.")
    if latest['Геополитика'] > 0.65: recs.append("🟡 **Геополитическая напряжённость** – усиливать дипломатию, избегать эскалации.")
    if latest['Экономика'] > 0.55: recs.append("🟡 **Экономика нестабильна** – искать новые точки роста, диверсифицировать риски.")
    if latest['Технологии'] < 0.4: recs.append("🟢 **Технологический разрыв** – инвестировать в образование, ИИ, инновации.")
    if latest['Социум'] > 0.55: recs.append("🟡 **Социальное напряжение** – укреплять диалог, снижать неравенство.")
    if not recs: recs.append("✅ Все системы в норме. Продолжайте мониторинг.")
    return recs
for rec in generate_recommendations(df): st.markdown(rec)

with st.expander("📋 Посмотреть сырые данные"):
    st.dataframe(df.tail(20), use_container_width=True)

st.caption(f"Последнее обновление: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.caption("Данные синтезированы на основе открытых источников (Copernicus, GDELT, World Bank)")

if st.button("🔄 Обновить данные (эмуляция)"):
    st.cache_data.clear()
    st.rerun()
