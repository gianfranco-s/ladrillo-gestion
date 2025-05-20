from datetime import datetime

import streamlit as st
import pandas as pd
import plotly.express as px

from db_mock import list_projects, fetch_project_data, insert_data
from db.models import ConstructionPhase

st.set_page_config(layout="wide", page_title="🏗️ Ladrillo Gestión")

st.sidebar.header("Select Project")
projects = list_projects()
selected = st.sidebar.selectbox("Project ID", projects if projects else ["(none)"])

phase_options = [ConstructionPhase[mn].value for mn in ConstructionPhase._member_names_]
selected_phases = st.sidebar.multiselect(
    "Construction Phases",
    options=phase_options,
    default=phase_options
)

st.title(f"🏗️ Project: {selected}")

if selected != "(none)":
    df = fetch_project_data(selected)

    # ── Phase filtering ───────────────────────────────────────────────────────
    if "phase" in df.columns:
        df = df[df["phase"].isin(selected_phases)]
    else:
        st.warning("No `phase` column found to filter on.")

    # ── Parse date columns ────────────────────────────────────────────────────
    for col in ("date_use_intended", "date_use_real", "date_bought", "fecha_uso", "fecha_compra"):
        if col in df.columns:
            df[col.replace("fecha_", "date_")] = pd.to_datetime(df[col])

    # ── Clean spending column ──────────────────────────────────────────────────
    if "total_materials" not in df.columns:
        st.error("Missing `total_materials` column.")
        st.stop()

    df["total_materials"] = (
        df["total_materials"]
          .astype(str)
          .str.replace(r"[\$,]", "", regex=True)
          .astype(float)
    )

    # ── Compute ISO-week start dates ──────────────────────────────────────────
    df["week_intended"] = df["date_use_intended"].dt.to_period("W").apply(lambda r: r.start_time)
    df["week_real"]     = df["date_use_real"].dt.to_period("W").apply(lambda r: r.start_time)

    # ── Aggregate weekly spending ─────────────────────────────────────────────
    weekly_intended = (
        df.groupby("week_intended")["total_materials"]
          .sum()
          .reset_index()
          .rename(columns={"week_intended": "week"})
    )
    weekly_real = (
        df.groupby("week_real")["total_materials"]
          .sum()
          .reset_index()
          .rename(columns={"week_real": "week"})
    )
    combined = pd.merge(
        weekly_intended,
        weekly_real,
        on="week",
        how="outer",
        suffixes=("_intended", "_real"),
    ).sort_values("week").fillna(0)

    # ── Melt for superimposed chart ────────────────────────────────────────────
    long = combined.melt(
        id_vars="week",
        value_vars=["total_materials_intended", "total_materials_real"],
        var_name="Spending Type",
        value_name="Spending",
    )
    long["Spending Type"] = long["Spending Type"].map({
        "total_materials_intended": "Intended",
        "total_materials_real": "Real",
    })

    # ── Plot at the top ───────────────────────────────────────────────────────
    st.subheader("📊 Weekly Materials Spending (Intended vs. Real)")
    fig = px.line(
        long,
        x="week",
        y="Spending",
        color="Spending Type",
        markers=True,
        labels={
            "week": "Week Start",
            "Spending": "Materials Spending (USD)",
            "Spending Type": ""
        },
    )
    fig.update_xaxes(dtick="W1", tickformat="%Y-%m-%d")
    fig.update_layout(legend_title_text="")
    st.plotly_chart(fig, use_container_width=True)

    # ── Toggleable data table ─────────────────────────────────────────────────
    if st.checkbox("Show data table"):
        st.subheader("📋 Loaded Data")
        st.dataframe(df)
    
    # ── Add New Data Row Form ───────────────────────────────────────────────
    st.subheader("➕ Add New Data Row")
    with st.expander("Click to add a new record"):
        with st.form("add_row_form"):
            phase = st.selectbox("Construction Phase", phase_options)
            floor_nr = st.number_input("Floor Number", min_value=0, step=1, value=0)
            material_id = st.text_input("Material ID (integer)")
            total_price = st.number_input("Total Building Materials Price (USD)", min_value=0.0, value=0.0)
            date_bought = st.date_input("Date Bought", value=datetime.today())
            date_use_intended = st.date_input("Date Intended for Use", value=datetime.today())
            date_use_real = st.date_input("Date Realized Use", value=datetime.today())
            submitted = st.form_submit_button("Save Row")

        if submitted:
            new_record = {
                "project_id": selected,
                "construction_phase": phase,
                "floor_nr": floor_nr,
                "material_id": material_id,
                "total_price": total_price,
                "date_bought": date_bought.strftime("%Y-%m-%d"),
                "date_use_intended": date_use_intended.strftime("%Y-%m-%d"),
                "date_use_real": date_use_real.strftime("%Y-%m-%d"),
            }

            insert_data(new_record)
            st.success("✅ New row added!")
            st.rerun()

else:
    st.info("Upload data to begin or create records via the uploader.")
