from backend.database import SessionLocal
from backend.models.workscore_result import WorkScoreResult
from backend.schemas.workscore_result import WorkScoreResultCreate, WorkScoreResultOut
from typing import List
from datetime import date

def create_workscore(data: WorkScoreResultCreate) -> WorkScoreResultOut:
    db = SessionLocal()
    new_result = WorkScoreResult(
        employee_id=data.employee_id,
        warehouse_id=data.warehouse_id,
        date=data.date,
        score=data.score,
        wms_usage=data.wms_usage,
        time_in_zone=data.time_in_zone,
        task_accuracy=data.task_accuracy,
        trajectory_deviation=data.trajectory_deviation
    )
    db.add(new_result)
    db.commit()
    db.refresh(new_result)
    db.close()
    return new_result

def get_workscores_filtered(
    employee_id: int = None,
    warehouse_id: int = None,
    date_query: date = None
) -> List[WorkScoreResultOut]:
    db = SessionLocal()
    query = db.query(WorkScoreResult)

    if employee_id is not None:
        query = query.filter(WorkScoreResult.employee_id == employee_id)
    if warehouse_id is not None:
        query = query.filter(WorkScoreResult.warehouse_id == warehouse_id)
    if date_query is not None:
        query = query.filter(WorkScoreResult.date == date_query)

    results = query.all()
    db.close()
    return results
