import json
import datetime
from datetime import timezone
from sqlalchemy import text
from backend.database.init_db import engine


def get_all_earthquakes(
    start_year: str, end_year: str, min_magnitude: float, limit: int
):
    now = datetime.datetime.now(timezone.utc)

    query = text("""
        SELECT
            id,
            magnitude,
            place,
            time,
            depth_km,
            ST_AsGeoJSON(geometry) AS geometry
        FROM earthquakes
        WHERE time >= :start_time AND time <= :end_time
        AND time <= :now
        AND magnitude >= :min_magnitude
        ORDER BY time DESC
        LIMIT :limit
    """)

    with engine.connect() as conn:
        res = conn.execute(
            query,
            {
                "start_time": start_year,
                "end_time": end_year,
                "min_magnitude": min_magnitude,
                "limit": limit,
                "now": now,
            },
        ).fetchall()

        earthquakes = []

        for row in res:
            earthquake = dict(row._mapping)

            if earthquake["geometry"]:
                earthquake["geometry"] = json.loads(earthquake["geometry"])

            earthquakes.append(earthquake)

        return earthquakes


def get_all_faults(min_lon: float, min_lat: float, max_lon: float, max_lat: float):
    query = text("""
        SELECT
            id,
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
        WHERE ST_Intersects(geometry, ST_MakeEnvelope(:min_lon, :min_lat, :max_lon, :max_lat, 4326))
    """)

    with engine.connect() as conn:
        res = conn.execute(
            query,
            {
                "min_lon": min_lon,
                "min_lat": min_lat,
                "max_lon": max_lon,
                "max_lat": max_lat,
            },
        ).fetchall()

        faults = []

        for row in res:
            fault = dict(row._mapping)

            if fault["geometry"]:
                fault["geometry"] = json.loads(fault["geometry"])

            faults.append(fault)

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


def get_fault_by_id(fault_id: str):  # catalog id
    if not fault_id:
        raise ValueError("Fault ID is missing")

    query = text("""
        SELECT
            id,
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
