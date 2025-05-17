import streamlit as st
import pandas as pd
import plotly.express as px

# ── In-memory store ───────────────────────────────────────────────────────────
encrypted_store = pd.read_csv("/tmp/test_data.csv").to_dict(orient="records")

def list_projects(data=encrypted_store):
    return sorted({rec["project_id"] for rec in data})

def fetch_project_data(project_id, data=encrypted_store):
    return pd.DataFrame([rec for rec in data if rec["project_id"] == project_id])


# ── App config ────────────────────────────────────────────────────────────────
st.set_page_config(layout="wide", page_title="🏗️ Ladrillo Gestión")

# ── Sidebar ──────────────────────────────────────────────────────────────────
st.sidebar.header("Select Project")
projects = list_projects()
selected = st.sidebar.selectbox("Project ID", projects if projects else ["(none)"])

# ── Main view ────────────────────────────────────────────────────────────────
st.title(f"🏗️ Project: {selected}")

if selected != "(none)":
    df = fetch_project_data(selected)

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

    # ── Compute ISO‐week start dates ──────────────────────────────────────────
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
    st.subheader("📊 Weekly Spending Evolution (Intended vs. Real)")
    fig = px.line(
        long,
        x="week",
        y="Spending",
        color="Spending Type",
        markers=True,
        labels={"week": "Week Start", "Spending": "Total Spending (USD)", "Spending Type": ""},
    )
    fig.update_xaxes(dtick="W1", tickformat="%Y-%m-%d")
    fig.update_layout(legend_title_text="")
    st.plotly_chart(fig, use_container_width=True)

    # ── Toggleable data table ─────────────────────────────────────────────────
    if st.checkbox("Show data table"):
        st.subheader("📋 Loaded Data")
        st.dataframe(df)

else:
    st.info("Upload data to begin or create records via the uploader.")
