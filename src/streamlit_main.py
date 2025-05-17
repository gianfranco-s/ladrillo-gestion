import streamlit as st
import pandas as pd
import plotly.express as px
from db_mock import list_projects, fetch_project_data

st.set_page_config(layout="wide", page_title="🏗️ Ladrillo Gestión")

# ── Sidebar: project selector & upload ────────────────────────────────────────
st.sidebar.header("📁 Selecciona Proyecto")
projects = list_projects()
selected = st.sidebar.selectbox("Proyecto", projects if projects else ["(ninguno)"])

# ── Main view ────────────────────────────────────────────────────────────────
st.title(f"🏗️ Proyecto: {selected}")
if selected and selected != "(ninguno)":
    df = fetch_project_data(selected)

    # Ensure date columns are datetime
    if 'fecha_uso' in df.columns:
        df['fecha_uso'] = pd.to_datetime(df['fecha_uso'])
    if 'fecha_compra' in df.columns:
        df['fecha_compra'] = pd.to_datetime(df['fecha_compra'])

    st.subheader("📋 Datos cargados")
    st.dataframe(df)

    # Weekly usage based on fecha_uso
    df['semana'] = df['fecha_uso'].dt.isocalendar().week
    weekly = df.groupby('semana')['cantidad_usada'].sum().reset_index()
    fig = px.line(
        weekly,
        x='semana',
        y='cantidad_usada',
        labels={'semana': 'Semana (entero)', 'cantidad_usada': 'Cantidad usada'},
        markers=True
    )
    # ensure integer ticks on x-axis
    fig.update_xaxes(tickmode='linear', dtick=1)
    st.subheader("📊 Consumo semanal")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Sube datos para empezar o crea registros a través del uploader.")
