import os
import pandas as pd

from db.models import BuildingMaterial


DATA_DIR = os.getenv("DATA_DIR", "/tmp")
DATA_FILE = os.path.join(DATA_DIR, "test_data.csv")

class DBMockFile:
    def __init__(self, data_file: str = DATA_FILE, data_dir: str = DATA_DIR):
        self._data_dir = data_dir
        self._data_file = data_file

        self._load_data_store()

    def _load_data_store(self) -> None:
        if os.path.exists(self._data_file):
            self.data_store = self._fetch_data_from_file(self._data_file)
            self.column_order = self._fetch_column_order(self._data_file)
        else:
            raise FileNotFoundError(f"Data file {self._data_file} not found.")

    @staticmethod
    def _fetch_column_order(data_file: str) -> list[str]:
        return pd.read_csv(data_file, nrows=0).columns.tolist()

    @staticmethod
    def _fetch_data_from_file(data_file) -> list[dict]:
        return pd.read_csv(data_file).to_dict(orient="records")

    def insert_building_material(self, new_record: BuildingMaterial) -> None:
        """
        Append new_record to in-memory store and to the CSV file.
        Assumes the CSV already exists and has a header row.
        """

        df_new = pd.DataFrame([new_record.to_dict()])

        # Reindex to match header exactly (missing keys → NaN, extra keys dropped)
        df_new = df_new.reindex(columns=self.column_order)

        df_new.to_csv(
            self._data_file,
            mode="a",        # append row
            header=False,    # no header line
            index=False
        )

        self._load_data_store()
    

# _db_mock = DBMock()
# data_store = _db_mock.data_store
# COLUMN_ORDER = _db_mock.colum_order


def list_projects(data_store: list[dict]):
    return sorted({rec["project_id"] for rec in data_store})


def fetch_project_data(project_id: str, data_store: list[dict]) -> pd.DataFrame:
    return pd.DataFrame([rec for rec in data_store if rec["project_id"] == project_id])


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


def compute_progress(selected_project: str, project_data: pd.DataFrame) -> float:
    total = len(project_data)
    if total == 0:
        return 0.0
    completed = project_data["date_use_real"].notna().sum() if "date_use_real" in project_data.columns else 0
    return completed / total if total > 0 else 0.0
