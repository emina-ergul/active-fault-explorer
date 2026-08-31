from backend.queries.queries import get_all_earthquakes, get_earthquake_by_id
from fastapi import APIRouter

router = APIRouter(prefix="/earthquakes", tags=["Earthquakes"])


@router.get("/")
def get_earthquakes():
    try:
        res = get_all_earthquakes()
        return {"earthquakes": res}
    except ValueError as e:
        return {"error": str(e)}


@router.get("/earthquake/{quake_id}")
def get_earthquake(quake_id: str):
    try:
        res = get_earthquake_by_id(quake_id)
        return {"earthquake": res}
    except ValueError as e:
        return {"error": str(e)}
