from passlib.context import CryptContext

# 🛡️ Ստեղծում ենք hashing engine
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🔐 Hash ֆունկցիա
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# ✅ Verify ֆունկցիա
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
