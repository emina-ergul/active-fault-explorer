from sqlalchemy import text
from backend.database.init_db import engine


def get_distance(quake_id: str):
    query = text("""
        SELECT
            f.name,
            e.id,
            e.magnitude,
            ST_Distance(
            e.geometry::geography,
            f.geometry::geography
        ) AS distance_m
        FROM earthquakes e
        JOIN faults f
        ON ST_DWithin(
                 e.geometry::geography,
                 f.geometry::geography,
                 100000
        )
        WHERE e.id = :quake_id
        ORDER BY distance_m ASC
        LIMIT 1
    """)

    with engine.connect() as conn:
        res = conn.execute(query, {"quake_id": quake_id}).fetchone()
        print("$$$$$$$$$$$", res)


get_distance("us7000rlkk")
