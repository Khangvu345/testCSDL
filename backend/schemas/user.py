from pydantic import BaseModel
from typing import Optional

class UserLogin(BaseModel):
    username: str
    password: str

class TaiKhoanUpdate(BaseModel):
    Password: Optional[str] = None
    Role: Optional[str] = None
    UserID: Optional[str] = None