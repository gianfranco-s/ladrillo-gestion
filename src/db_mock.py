import pandas as pd

# In-memory store for mock records
encrypted_store = []  # module-level store for records


def reset_data():
    """Clear all stored records (for test setup)."""
    encrypted_store.clear()


def insert_records(df: pd.DataFrame) -> int:
    """
    Mock insert: add DataFrame records to in-memory list.
    Returns the number of records inserted.
    """
    records = df.to_dict(orient='records')
    encrypted_store.extend(records)
    return len(records)


def list_projects() -> list:
    """
    Return a list of distinct 'proyecto' values from the in-memory store.
    """
    return list({rec.get('proyecto') for rec in encrypted_store})


def fetch_project_data(proyecto: str) -> pd.DataFrame:
    """
    Fetch records matching the given project from the in-memory store.
    Returns a pandas DataFrame.
    """
    filtered = [rec for rec in encrypted_store if rec.get('proyecto') == proyecto]
    return pd.DataFrame(filtered)
