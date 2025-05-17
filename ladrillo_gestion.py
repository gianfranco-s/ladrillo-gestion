import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_or_create_db, insert_records, query_project_data

# ── Ensure our SQLite table exists ─────────────────────────────────────────────
load_or_create_db()

st.set_page_config(layout="wide", page_title="🏗️ Proyecto Dashboard")

# --- Sidebar: select project ---
projects = query_project_data("SELECT DISTINCT proyecto FROM mediciones")
selected_project = st.sidebar.selectbox("📁 Selecciona Proyecto", projects)

# ── Upload form ────────────────────────────────────────────────────────────────
st.sidebar.header("➕ Cargar Datos (CSV)")

uploaded = st.sidebar.file_uploader("Sube tu CSV de consumos/mediciones", type="csv")
if uploaded is not None:
    try:
        # 1) Read into a DataFrame
        df_new = pd.read_csv(uploaded)
        
        # 2) Show a quick preview so you know Streamlit actually read it
        st.sidebar.write("✅ Leído correctamente, primeras filas:")
        st.sidebar.dataframe(df_new.head())
        
        # 3) Insert into your DB
        count = insert_records(df_new)
        st.sidebar.success(f"{count} registros cargados en la base de datos.")
        
    except Exception as e:
        # If something goes wrong, show the exception
        st.sidebar.error(f"❌ Error al procesar el CSV: {e}")

# --- Main: show table ---
st.title(f"⚙️ {selected_project}")
df = query_project_data(
    """
    SELECT fecha, material, cantidad_usada, proveedor
    FROM mediciones
    WHERE proyecto = :proj
    """, params={"proj": selected_project}
)
st.dataframe(df, use_container_width=True)

# --- Weekly progress chart ---
st.subheader("📊 Consumo semanal")
df["semana"] = pd.to_datetime(df["fecha"]).dt.isocalendar().week
weekly = df.groupby("semana")["cantidad_usada"].sum().reset_index()
fig = px.line(weekly, x="semana", y="cantidad_usada",
              labels={"cantidad_usada":"Cantidad (MXN)", "semana":"Semana"})
st.plotly_chart(fig, use_container_width=True)
