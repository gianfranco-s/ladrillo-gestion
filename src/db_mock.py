import os
import pandas as pd

from db.models import BuildingMaterial


DATA_DIR = os.getenv("DATA_DIR", "/tmp")
DATA_FILE = os.path.join(DATA_DIR, "test_data.csv")


def _fetch_column_order(data_file: str = DATA_FILE) -> list[str]:
    if not os.path.exists(data_file):
        return []
    return pd.read_csv(data_file, nrows=0).columns.tolist()


def _fetch_data_from_file(data_file: str = DATA_FILE) -> list[dict]:
    if not os.path.exists(data_file):
        return []
    return pd.read_csv(data_file).to_dict(orient="records")

data_store = _fetch_data_from_file()
COLUMN_ORDER = _fetch_column_order()

def list_projects(data: list[dict] = data_store):
    return sorted({rec["project_id"] for rec in data})


def fetch_project_data(project_id: str) -> pd.DataFrame:
    data_store = _fetch_data_from_file()
    return pd.DataFrame([rec for rec in data_store if rec["project_id"] == project_id])


def insert_building_material(new_record: BuildingMaterial) -> None:
    """
    Append new_record to in-memory store and to the CSV file.
    Assumes the CSV already exists and has a header row.
    """
    _insert_data_in_memory(new_record.to_dict())
    _insert_data_to_file(new_record.to_dict())


def _insert_data_in_memory(new_record: dict, data: list[dict] = data_store) -> None:
    data.append(new_record)


def _insert_data_to_file(new_record: dict, data_file: str = DATA_FILE, column_order: list = COLUMN_ORDER) -> None:
    df_new = pd.DataFrame([new_record])

    # Reindex to match header exactly (missing keys → NaN, extra keys dropped)
    df_new = df_new.reindex(columns=column_order)

    df_new.to_csv(
        data_file,
        mode="a",        # append row
        header=False,    # no header line
        index=False
    )


def get_aggregated_spending_data(dataset: pd.DataFrame, selected_phases: list[str]) -> pd.DataFrame:
    df = dataset.copy()
    df = df[df["phase"].isin(selected_phases)]

    # ensure all three date columns are real datetimes, NaT on bad/missing
    for dc in ("date_bought", "date_use_intended", "date_use_real"):
        if dc in df.columns:
            df[dc] = pd.to_datetime(df[dc], errors="coerce")

    df["total_price"] = (
        df["total_price"]
          .astype(str)
          .str.replace(r"[\$,]", "", regex=True)
          .astype(float)
    )

    # — compute ISO-week start times, safely
    df["week_intended"] = df["date_use_intended"].dt.to_period("W").dt.start_time
    df["week_real"] = df["date_use_real"].dt.to_period("W").dt.start_time
    
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


def compute_progress(selected_project: str) -> float:
    project_data = fetch_project_data(selected_project)
    total = len(project_data)
    if total == 0:
        return 0.0
    completed = project_data["date_use_real"].notna().sum() if "date_use_real" in project_data.columns else 0
    return completed / total if total > 0 else 0.0
