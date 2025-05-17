import pandas as pd

encrypted_store = pd.read_csv("/tmp/test_data.csv").to_dict(orient='records')


def list_projects(data: list[dict] = encrypted_store) -> list:
    """
    Return a list of distinct 'proyecto' values from the in-memory store.
    """
    return list({rec.get('proyecto') for rec in data})


def fetch_project_data(proyecto: str, data: list[dict] = encrypted_store) -> pd.DataFrame:
    """
    Fetch records matching the given project from the in-memory store.
    Returns a pandas DataFrame.
    """
    filtered = [rec for rec in data if rec.get('proyecto') == proyecto]
    return pd.DataFrame(filtered)
