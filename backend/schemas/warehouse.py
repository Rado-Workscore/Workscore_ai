from pydantic import BaseModel

class WarehouseCreate(BaseModel):
    name: str
    location: str | None = None

class WarehouseOut(BaseModel):
    id: int
    name: str
    location: str | None = None

    class Config:
        from_attributes = True  # Pydantic v2-ում orm_mode-ի փոխարեն
