from pydantic import BaseModel

# 🧾 Վերծանված թոքենի տվյալները
class TokenData(BaseModel):
    username: str
    role: str

# 📤 Թոքենի պատասխան՝ login-ից հետո
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
