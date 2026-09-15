from backend.queries.queries import (
    get_all_earthquakes,
    get_earthquake_by_id,
    get_all_quakes_within_fault_distance,
)
from fastapi import APIRouter
from fastapi.exceptions import HTTPException

router = APIRouter(prefix="/earthquakes", tags=["Earthquakes"])


@router.get("/")
def get_earthquakes(magnitude: float = 0.0):
    try:
        res = get_all_earthquakes(magnitude)
        return res
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/earthquake/{quake_id}")
def get_earthquake(quake_id: str):
    try:
        res = get_earthquake_by_id(quake_id)
        return res
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/within-fault-distance/{fault_id}/{distance_km}")
def get_earthquakes_within_fault_distance(fault_id: str, distance_km: int):
    try:
        res = get_all_quakes_within_fault_distance(fault_id, distance_km)
        return res
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
