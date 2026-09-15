import json
import datetime
from datetime import timezone
from sqlalchemy import text
from backend.database.init_db import engine

now = datetime.datetime.now(timezone.utc)


def get_all_earthquakes(magnitude: float):
    query = text("""
        SELECT
            id,
            magnitude,
            place,
            time,
            depth_km,
            ST_AsGeoJSON(geometry) AS geometry
        FROM earthquakes
        WHERE magnitude >= :magnitude
    """)

    with engine.connect() as conn:
        res = conn.execute(query, {"magnitude": magnitude}).fetchall()

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
    if not quake_id:
        raise ValueError("Quake ID is missing")

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
        res = conn.execute(query, {"quake_id": quake_id}).fetchall()

        if not res:
            raise ValueError(f"No earthquakes with id {quake_id} found")

        for row in res:
            earthquake = dict(row._mapping)
            earthquake["geometry"] = json.loads(earthquake["geometry"])

    return earthquake


def get_fault_by_id(fault_id: str):
    if not fault_id:
        raise ValueError("Fault ID is missing")

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
        WHERE catalog_id = :fault_id
    """)

    with engine.connect() as conn:
        res = conn.execute(query, {"fault_id": fault_id}).fetchall()

        if not res:
            raise ValueError(f"No faults with id {fault_id} found")

        faults = [dict(row._mapping) for row in res]

        for fault in faults:
            fault["geometry"] = json.loads(fault["geometry"])

    return faults


def get_all_quakes_within_fault_distance(fault_id: str, distance_km: int):
    if not fault_id:
        raise ValueError("Fault ID is missing")

    query = text("""
        SELECT
            e.id AS earthquake_id,
            e.magnitude AS earthquake_magnitude,
            e.place AS earthquake_place,
            e.time AS earthquake_time,
            e.depth_km AS earthquake_depth_km,
            f.catalog_id AS fault_catalog_id,
            f.catalog_name AS fault_catalog_name,
            f.slip_type AS fault_slip_type,
            f.last_movement AS fault_last_movement,
            f.net_slip_rate_most_likely_mm AS fault_net_slip_rate_most_likely_mm,
            ST_Distance(e.geometry::geography, f.geometry::geography) / 1000 AS distance_km_from_fault
        FROM earthquakes e
        JOIN faults f 
        ON ST_DWithin(
            e.geometry::geography, 
            f.geometry::geography, 
            :distance_km * 1000
        )
        WHERE f.catalog_id = :fault_id
    """)

    with engine.connect() as conn:
        res = conn.execute(
            query, {"fault_id": fault_id, "distance_km": distance_km}
        ).fetchall()

        if not res:
            raise ValueError(
                f"No earthquakes found within {distance_km} km of fault {fault_id}"
            )

        earthquakes = [dict(row._mapping) for row in res]

        for earthquake in earthquakes:
            earthquake["distance_km_from_fault"] = round(
                earthquake["distance_km_from_fault"], 1
            )
        #     earthquake["geometry"] = json.loads(earthquake["geometry"])

    return earthquakes
