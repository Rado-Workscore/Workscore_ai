from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from datetime import date

from backend.schemas.workscore_result import WorkScoreResultCreate, WorkScoreResultOut
from backend.auth.dependencies import get_current_user, TokenData
from backend.services.workscore_service import create_workscore, get_workscores_filtered

router = APIRouter(
    prefix="/workscore",
    tags=["WorkScore"]
)

# 🟢 WorkScore արդյունքի ստեղծում
@router.post("/create", response_model=WorkScoreResultOut)
def create_workscore_route(
    data: WorkScoreResultCreate,
    current_user: TokenData = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Միայն ադմինը կարող է WorkScore մուտքագրել։"
        )

    return create_workscore(data)

# 🔵 WorkScore արդյունքների բերում՝ ըստ ֆիլտրերի
@router.get("/", response_model=List[WorkScoreResultOut])
def get_workscore_results_route(
    employee_id: int = Query(None),
    warehouse_id: int = Query(None),
    date_query: date = Query(None, alias="date"),
    current_user: TokenData = Depends(get_current_user)
):
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(status_code=403, detail="Մուտքը արգելված է։")

    return get_workscores_filtered(employee_id, warehouse_id, date_query)

