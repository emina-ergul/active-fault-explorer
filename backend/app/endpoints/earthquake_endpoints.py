import datetime

from queries.queries import (
    get_all_earthquakes,
    get_earthquake_by_id,
    # get_all_quakes_within_fault_distance,
)
from fastapi import APIRouter
from fastapi.exceptions import HTTPException

router = APIRouter(prefix="/earthquakes", tags=["Earthquakes"])


@router.get("/")
def get_earthquakes(
    start_year: str = datetime.datetime.now().year - 5,
    end_year: str = datetime.datetime.now().year,
    min_magnitude: float = 3.5,
    limit: int = 2500,
):
    try:
        if min_magnitude < 3.5:
            raise HTTPException(
                status_code=400,
                detail="Minimum magnitude must be greater than or equal to 3.5",
            )
        if end_year is not None and start_year is None:
            raise HTTPException(
                status_code=400,
                detail="Start year must be provided if end year is provided",
            )
        if start_year is not None and end_year is not None:
            if start_year > end_year:
                raise HTTPException(
                    status_code=400,
                    detail="Start year must be less than or equal to end year",
                )
        start_year = f"{start_year}-01-01"
        end_year = f"{int(end_year) +1}-01-01"
        res = get_all_earthquakes(start_year, end_year, min_magnitude, limit)
        return res
    except HTTPException:
        raise


@router.get("/earthquake/{quake_id}")
def get_earthquake(quake_id: str):
    try:
        res = get_earthquake_by_id(quake_id)
        return res
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# @router.get("/within-fault-distance/{fault_id}/{distance_km}")
# def get_earthquakes_within_fault_distance(fault_id: str, distance_km: int):
#     try:
#         res = get_all_quakes_within_fault_distance(fault_id, distance_km)
#         return res
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))
