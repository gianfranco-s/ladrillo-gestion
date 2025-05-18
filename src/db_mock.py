import pandas as pd

encrypted_store = pd.read_csv("/tmp/test_data.csv").to_dict(orient="records")


def list_projects(data=encrypted_store):
    return sorted({rec["project_id"] for rec in data})


def fetch_project_data(project_id: str, data=encrypted_store) -> pd.DataFrame:
    return pd.DataFrame([rec for rec in data if rec["project_id"] == project_id])
