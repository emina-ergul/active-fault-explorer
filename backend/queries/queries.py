import datetime
from datetime import timezone
from sqlalchemy import text
from backend.database.init_db import engine

now = datetime.datetime.now(timezone.utc)


def get_earthqauke_info(quake_id: str):
    query = text("""
    SELECT * 
    FROM earthquakes
    WHERE id = :quake_id 
    """)

    with engine.connect() as conn:
        res = conn.execute(query, {"quake_id": quake_id}).fetchall()
        print(res)


def get_fault_info(fault_id: str):
    query = text("""
    SELECT
        catalog_id,
        name,
        last_movement,
        slip_type,
        net_slip_rate,
        notes,
        ST_Union(geometry) AS geometry
    FROM faults
    WHERE catalog_id = :fault_id
    GROUP BY
        catalog_id,
        name,
        last_movement,
        slip_type,
        net_slip_rate,
        notes
""")

    with engine.connect() as conn:
        res = conn.execute(query, {"fault_id": fault_id}).fetchall()
        print("$$$$$$$$$$$", res)


def get_distance(quake_id: str):
    query = text("""
        SELECT
            e.id,
            f.name,
            f.catalog_id,
            f.last_movement,
            f.slip_type,
                 f.net_slip_rate,
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
        LIMIT 10
    """)

    with engine.connect() as conn:
        res = conn.execute(query, {"quake_id": quake_id}).fetchone()
        print("$$$$$$$$$$$", res)


get_distance("us7000rlkk")
get_earthqauke_info("us7000rlkk")
get_fault_info("SA_410")
