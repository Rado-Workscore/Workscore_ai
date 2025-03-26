from fastapi import APIRouter, Depends, HTTPException, Path
from typing import List

from backend.schemas.warehouse import WarehouseCreate, WarehouseOut
from backend.auth.dependencies import get_current_user, TokenData
from backend.services.warehouse_service import create_warehouse, get_all_warehouses

router = APIRouter(
    prefix="/warehouses",
    tags=["Warehouses"]
)

# 🟢 Ստեղծում
@router.post("/create", response_model=WarehouseOut)
def create_new_warehouse(
    data: WarehouseCreate,
    current_user: TokenData = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Միայն ադմինը կարող է ստեղծել պահեստ։")
    return create_warehouse(data)

# 🔵 Բերում
@router.get("/", response_model=List[WarehouseOut])
def get_warehouses(current_user: TokenData = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Միայն ադմինը կարող է տեսնել պահեստների ցանկը։")
    return get_all_warehouses()

# 🟡 Խմբագրում (սիմուլյացիա)
@router.patch("/update/{warehouse_id}", response_model=WarehouseOut)
def update_warehouse(
    warehouse_id: int = Path(..., description="Խմբագրվող պահեստի ID-ն"),
    data: WarehouseCreate = Depends(),
    current_user: TokenData = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Միայն ադմինն ունի պահեստ խմբագրելու իրավունք։")

    # ⛔ Սա սիմուլյացիա է, դեռ բազայի մեջ չենք խմբագրում
    return {
        "id": warehouse_id,
        "name": data.name,
        "location": data.location
    }

