from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from backend.database import SessionLocal
from backend.models.employee import Employee
from backend.auth.utils import verify_password
from backend.auth.jwt_handler import create_access_token
from backend.auth.schemas import TokenResponse

@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = SessionLocal()
    user = db.query(Employee).filter(Employee.username == form_data.username).first()
    db.close()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Սխալ մուտքանուն կամ գաղտնաբառ։")

    token = create_access_token({
        "sub": user.username,
        "role": "admin"  # ⛔ ապագայում սա կվերցնենք user.role դաշտից
    })

    return {"access_token": token, "token_type": "bearer"}

