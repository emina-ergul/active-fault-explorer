from queries.queries import get_fault_count, get_all_faults, get_fault_by_id
from fastapi import APIRouter
from fastapi.exceptions import HTTPException

router = APIRouter(prefix="/faults", tags=["Faults"])


@router.get("/count")
def get_fault_count_endpoint():
    try:
        res = get_fault_count()
        return {"count": res}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/")
def get_faults_endpoint():
    try:
        res = get_all_faults(min_lon=-180, min_lat=-90, max_lon=180, max_lat=90)
        return res
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{fault_id}")
def get_fault_endpoint(fault_id: str):
    try:
        res = get_fault_by_id(fault_id=fault_id)
        return res
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
