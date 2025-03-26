from pydantic import BaseModel
from datetime import date

class WorkScoreResultCreate(BaseModel):
    employee_id: int
    warehouse_id: int
    date: date
    score: int
    wms_usage: float = 0.0
    time_in_zone: float = 0.0
    task_accuracy: float = 0.0
    trajectory_deviation: float = 0.0

class WorkScoreResultOut(BaseModel):
    id: int
    employee_id: int
    warehouse_id: int
    date: date
    score: int
    wms_usage: float
    time_in_zone: float
    task_accuracy: float
    trajectory_deviation: float

    class Config:
        from_attributes = True  # Pydantic V2-ում orm_mode-ի փոխարեն
