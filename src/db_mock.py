import os
import pandas as pd


DATA_DIR = os.getenv("DATA_DIR", "/tmp")
data_store = pd.read_csv(f"{DATA_DIR}/test_data.csv").to_dict(orient="records")


def list_projects(data: list[dict] = data_store):
    return sorted({rec["project_id"] for rec in data})


def fetch_project_data(project_id: str, data: list[dict] = data_store) -> pd.DataFrame:
    return pd.DataFrame([rec for rec in data if rec["project_id"] == project_id])


def insert_data(new_record: dict, data: list[dict] = data_store) -> None:
    data.append(new_record)
