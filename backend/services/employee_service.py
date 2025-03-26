from backend.database import SessionLocal
from backend.models.employee import Employee
from backend.schemas.employee import EmployeeCreate, EmployeeOut
from typing import List
from backend.auth.utils import hash_password


def create_employee(data: EmployeeCreate) -> EmployeeOut:
    db = SessionLocal()
    new_employee = Employee(
        full_name=data.full_name,
        position=data.position,
        username=data.username,
        email=data.email,
        hashed_password=hash_password(data.password)  # ⚠️ hashing դեռ չենք արել

    )
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    db.close()

    return new_employee



def get_all_employees() -> List[EmployeeOut]:
    db = SessionLocal()
    employees = db.query(Employee).all()
    db.close()
    return employees

def get_employees_by_warehouse(warehouse_id: int) -> List[EmployeeOut]:
    db = SessionLocal()
    employees = db.query(Employee).filter(Employee.warehouse_id == warehouse_id).all()
    db.close()
    return employees    
