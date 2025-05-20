import time
from datetime import datetime

import streamlit as st
import pandas as pd
import plotly.express as px

from db_mock import (list_projects,
                     get_aggregated_spending_data,
                     insert_building_material,
                     compute_progress,
                     fetch_project_data,)
from db.models import ConstructionPhase, BuildingMaterial

st.set_page_config(layout="wide", page_title="🏗️ Ladrillo Gestión")

st.sidebar.header("Select Project")
projects = list_projects()
selected_project = st.sidebar.selectbox("Project ID", projects if projects else ["(none)"])


st.title(f"🏗️ Project: {selected_project}")

if selected_project != "(none)":
    project_data = fetch_project_data(selected_project)

    progress = compute_progress(project_data)

    st.sidebar.subheader(f"Completion Progress ({progress*100:.1f}%)")
    st.sidebar.progress(progress)

    phase_options = [ConstructionPhase[mn].value for mn in ConstructionPhase._member_names_]
    selected_phases = st.sidebar.multiselect(
        "Construction Phases",
        options=phase_options,
        default=phase_options
    )

    long = get_aggregated_spending_data(project_data, selected_phases)

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

    # Toggle data table
    if st.checkbox("Show data table"):
        st.subheader("📋 Loaded Data")
        st.dataframe(project_data)
    
    # Add New Data Row Form
    with st.expander("Click to add a new record"):
        specify_date_bought = st.checkbox("Specify purchase date", value=True)
        specify_date_intended = st.checkbox("Specify intended use date", value=True)
        specify_date_real = st.checkbox("Specify real use date", value=False)

        with st.form("add_row_form"):
            material_id = st.text_input("Building Material ID (integer)")
            total_price = st.number_input(
                "Total Building Materials Price (USD)", min_value=0.0, value=0.0
            )
            phase = st.selectbox("Construction Phase", phase_options)
            floor_nr = st.number_input("Floor Number", min_value=0, step=1, value=0)

            date_bought = st.date_input("Date Bought", value=datetime.today()) if specify_date_bought else None
            date_use_intended = st.date_input("Date Intended for Use", value=datetime.today()) if specify_date_intended else None
            date_use_real = st.date_input("Date Realized Use", value=datetime.today()) if specify_date_real else None

            submitted = st.form_submit_button("Save Row")

        if submitted:
            bm = BuildingMaterial(
                project_id=selected_project,
                material_id=material_id,
                total_price=total_price,
                phase=phase,
                floor_nr=floor_nr,
                date_bought=date_bought,
                date_use_intended=date_use_intended,
                date_use_real=date_use_real,
            )
            insert_building_material(bm)
            st.success("✅ New row added!")
            time.sleep(1)
            st.rerun()

else:
    st.info("Upload data to begin or create records via the uploader.")
