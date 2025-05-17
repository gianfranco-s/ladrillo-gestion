import pandas as pd
from sqlalchemy import create_engine, text

# In-memory SQLite for PoC; swap URL later for Postgres/MySQL
ENGINE = create_engine("sqlite:///./data/dashboard.db", echo=False)

def load_or_create_db():
    # on first run, create table
    with ENGINE.begin() as conn:
        conn.execute(text(
            """
            CREATE TABLE IF NOT EXISTS mediciones (
                proyecto TEXT,
                fecha TEXT,
                material TEXT,
                cantidad_usada REAL,
                proveedor TEXT
            )
            """
            )
        )

def insert_records(df: pd.DataFrame) -> int:
    """Append to mediciones; returns number inserted."""
    df.to_sql("mediciones", ENGINE, if_exists="append", index=False)
    return len(df)

def query_project_data(query: str, params: dict = None):
    with ENGINE.connect() as conn:
        result = conn.execute(text(query), params or {})
        return [row[0] for row in result] if query.lower().strip().startswith("select distinct") else pd.DataFrame(result.fetchall(), columns=result.keys())
