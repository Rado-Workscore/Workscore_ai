from pydantic import BaseModel, EmailStr

class EmployeeCreate(BaseModel):
    full_name: str
    position: str | None = None
    username: str
    email: EmailStr
    password: str

class EmployeeOut(BaseModel):
    id: int
    full_name: str
    position: str | None = None
    username: str
    email: EmailStr
    is_active: int

    class Config:
        orm_mode = True

class EmployeeLogin(BaseModel):
    username: str
    password: str
