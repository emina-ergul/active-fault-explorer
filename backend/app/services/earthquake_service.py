from backend.database.init_db import engine
from sqlalchemy import text

conn = engine.connect()


def get_all_earthquakes():
    query = text("""
        SELECT
            *
        FROM earthquakes
    """)
    res = conn.execute(query).fetchall()

    if not res:
        raise ValueError("No earthquakes found in the database.")

    return [dict(row._mapping) for row in res]
