import json
import datetime
from datetime import timezone
from sqlalchemy import text
from backend.database.init_db import engine

now = datetime.datetime.now(timezone.utc)


def get_all_earthquakes():
    query = text("""
    SELECT
        id,
        magnitude,
        place,
        time,
        depth_km,
        ST_AsGeoJSON(geometry) AS geometry
    FROM earthquakes
    """)

    with engine.connect() as conn:
        res = conn.execute(query).fetchall()

        if not res:
            raise ValueError("No earthquakes found")

        earthquakes = [dict(row._mapping) for row in res]

        for earthquake in earthquakes:
            earthquake["geometry"] = json.loads(earthquake["geometry"])

    return earthquakes


def get_all_faults(limit: int):
    query = text("""
    SELECT
        catalog_id,
        catalog_name,
        name,
        slip_type,
        last_movement,
        net_slip_rate_most_likely_mm,
        net_slip_rate_min_mm,
        net_slip_rate_max_mm,
        ST_AsGeoJSON(geometry) AS geometry
    FROM faults
    LIMIT :limit
    """)

    with engine.connect() as conn:
        res = conn.execute(query, {"limit": limit}).fetchall()

        if not res:
            raise ValueError("No faults found")

        faults = [dict(row._mapping) for row in res]

        for fault in faults:
            fault["geometry"] = json.loads(fault["geometry"])

    return faults


def get_earthquake_by_id(quake_id: str):
    query = text("""
    SELECT 
        id,
        magnitude,
        place,
        time,
        depth_km,
        ST_AsGeoJSON(geometry) AS geometry
    FROM earthquakes
    WHERE id = :quake_id
    """)

    with engine.connect() as conn:
        res = conn.execute(query, {"quake_id": quake_id}).one()

        if not res:
            raise ValueError(f"No earthquakes with id {quake_id} found")

        earthquake = dict(res._mapping)
        earthquake["geometry"] = json.loads(earthquake["geometry"])

    return earthquake


# def get_fault_info(fault_id: str):
#     query = text("""
#     SELECT
#         catalog_id,
#         name,
#         last_movement,
#         slip_type,
#         net_slip_rate,
#         notes,
#         ST_Union(geometry) AS geometry
#     FROM faults
#     WHERE catalog_id = :fault_id
#     GROUP BY
#         catalog_id,
#         name,
#         last_movement,
#         slip_type,
#         net_slip_rate,
#         notes
# """)

#     with engine.connect() as conn:
#         res = conn.execute(query, {"fault_id": fault_id}).fetchall()
#         print("$$$$$$$$$$$", res)


# def get_distance(quake_id: str):
#     query = text("""
#         SELECT
#             e.id,
#             f.name,
#             f.catalog_id,
#             f.last_movement,
#             f.slip_type,
#                  f.net_slip_rate,
#             e.magnitude,
#             ST_Distance(
#             e.geometry::geography,
#             f.geometry::geography
#         ) AS distance_m
#         FROM earthquakes e
#         JOIN faults f
#         ON ST_DWithin(
#                  e.geometry::geography,
#                  f.geometry::geography,
#                  100000
#         )
#         WHERE e.id = :quake_id
#         ORDER BY distance_m ASC
#         LIMIT 10
#     """)

#     with engine.connect() as conn:
#         res = conn.execute(query, {"quake_id": quake_id}).fetchone()
#         print("$$$$$$$$$$$", res)


# get_distance("us7000rlkk")
# get_earthqauke_info("us7000rlkk")
# get_fault_info("SA_410")
