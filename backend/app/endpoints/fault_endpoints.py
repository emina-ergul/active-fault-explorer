from backend.queries.queries import get_all_faults, get_fault_by_id
from fastapi import APIRouter
from fastapi.exceptions import HTTPException

router = APIRouter(prefix="/faults", tags=["Faults"])


@router.get("/")
def get_faults(limit: int = 100, offset: int = 0):
    try:
        res = get_all_faults(limit=limit)
        return res
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{fault_id}")
def get_fault(fault_id: str):
    try:
        res = get_fault_by_id(fault_id=fault_id)
        return res
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
