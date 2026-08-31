from backend.queries.queries import get_all_faults
from fastapi import APIRouter

router = APIRouter(prefix="/faults", tags=["Faults"])


@router.get("/")
def get_faults(limit: int = 100, offset: int = 0):
    res = get_all_faults(limit=limit)
    return res
