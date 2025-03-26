from jose import jwt, JWTError
from datetime import datetime, timedelta
from backend.auth.schemas import TokenData

# ⚙️ Քոնֆիգներ
SECRET_KEY = "secret123"  # ⛔ փոխել .env-ում՝ ապագայում
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# 🔐 Թոքենի ստեղծում
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

# 🔍 Թոքենի վերծանում / վավերացում
def decode_access_token(token: str) -> TokenData | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None or role is None:
            return None
        return TokenData(username=username, role=role)
    except JWTError:
        return None
