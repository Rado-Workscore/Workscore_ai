from backend.database import SessionLocal
from backend.models.warehouse import Warehouse
from backend.schemas.warehouse import WarehouseCreate, WarehouseOut
from typing import List

def create_warehouse(data: WarehouseCreate) -> WarehouseOut:
    db = SessionLocal()
    new_warehouse = Warehouse(
        name=data.name,
        location=data.location
    )
    db.add(new_warehouse)
    db.commit()
    db.refresh(new_warehouse)
    db.close()
    return new_warehouse

def get_all_warehouses() -> List[WarehouseOut]:
    db = SessionLocal()
    warehouses = db.query(Warehouse).all()
    db.close()
    return warehouses
