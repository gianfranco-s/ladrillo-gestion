import os
import pandas as pd

from db.models import BuildingMaterial


DATA_DIR = os.getenv("DATA_DIR", "/tmp")
DATA_FILE = os.path.join(DATA_DIR, "test_data.csv")
data_store = pd.read_csv(DATA_FILE).to_dict(orient="records")


def list_projects(data: list[dict] = data_store):
    return sorted({rec["project_id"] for rec in data})


def fetch_project_data(project_id: str, data: list[dict] = data_store) -> pd.DataFrame:
    return pd.DataFrame([rec for rec in data if rec["project_id"] == project_id])


def insert_building_material(new_record: BuildingMaterial) -> None:
    """
    Append new_record to in-memory store and to the CSV file.
    Assumes the CSV already exists and has a header row.
    """
    _insert_data_in_memory(new_record.to_dict())
    _insert_data_to_file(new_record.to_dict())


def _insert_data_in_memory(new_record: dict, data: list[dict] = data_store) -> None:
    data_store.append(new_record)


def _insert_data_to_file(new_record: dict, data_file: str = DATA_FILE) -> None:
    pd.DataFrame([new_record]).to_csv(
        data_file,
        mode="a",
        header=False,
        index=False
    )


def get_aggregated_spending_data(dataset: pd.DataFrame, selected_phases: list[str]) -> pd.DataFrame:
    df = dataset.copy()
    df = df[df["phase"].isin(selected_phases)]

    for col in ("date_use_intended", "date_use_real", "date_bought", "fecha_uso", "fecha_compra"):
        if col in df.columns:
            df[col.replace("fecha_", "date_")] = pd.to_datetime(df[col])

    df["total_price"] = (
        df["total_price"]
          .astype(str)
          .str.replace(r"[\$,]", "", regex=True)
          .astype(float)
    )

    df["week_intended"] = df["date_use_intended"].dt.to_period("W").apply(lambda r: r.start_time)
    df["week_real"] = df["date_use_real"].dt.to_period("W").apply(lambda r: r.start_time)

    # Aggregate weekly spending
    weekly_intended = (
        df.groupby("week_intended")["total_price"]
          .sum()
          .reset_index()
          .rename(columns={"week_intended": "week"})
    )
    weekly_real = (
        df.groupby("week_real")["total_price"]
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

    # Melt for superimposed chart
    long = combined.melt(
        id_vars="week",
        value_vars=["total_price_intended", "total_price_real"],
        var_name="Spending Type",
        value_name="Spending",
    )
    long["Spending Type"] = long["Spending Type"].map({
        "total_price_intended": "Intended",
        "total_price_real": "Real",
    })
    return long


def compute_progress(project_data: pd.DataFrame) -> float:
    total = len(project_data)
    if total == 0:
        return 0.0
    completed = project_data["date_use_real"].notna().sum() if "date_use_real" in project_data.columns else 0
    return completed / total if total > 0 else 0.0
