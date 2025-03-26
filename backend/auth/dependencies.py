from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from typing import Optional
from backend.auth.jwt_handler import decode_access_token
from backend.auth.schemas import TokenData
# Քո գաղտնի բանալին
SECRET_KEY = "secret123"  # ⛔ Շուտով փոխարինենք .env-ով
ALGORITHM = "HS256"

# Էնդփոյնթ, որտեղից կստանան թոքենը (կարևոր չէ հիմա)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/employees/login")

# Pydantic սխեմա՝ թոքենից ստացված տվյալների համար
class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None  # 👈 admin, manager, etc.

# Ֆունկցիա՝ ստանալու համար "current_user" token-ից
def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Չհաջողվեց նույնականացնել։",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")

        if username is None or role is None:
            raise credentials_exception
        return TokenData(username=username, role=role)
    except JWTError:
        raise credentials_exception

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# ✅ Վերադարձնում է TokenData՝ username և role
def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    token_data = decode_access_token(token)
    if not token_data:
        raise HTTPException(status_code=401, detail="Թոքենը անվավեր է։")
    return token_data