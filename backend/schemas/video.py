from pydantic import BaseModel
from datetime import datetime

class VideoCreate(BaseModel):
    filename: str
    warehouse_id: int
    camera_id: int

class VideoOut(BaseModel):
    id: int
    filename: str
    warehouse_id: int
    camera_id: int
    uploaded_at: datetime
    is_processed: bool

    class Config:
        from_attributes = True  # Pydantic v2-ի համար
