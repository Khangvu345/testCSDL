from pydantic import BaseModel
from typing import Optional

class UserLogin(BaseModel):
    username: str
    password: str

class TaiKhoanBase(BaseModel):
    Role: str
    UserID: str

class TaiKhoanCreate(TaiKhoanBase):
    Username: str
    Password: str

class TaiKhoanUpdate(BaseModel):
    Password: Optional[str] = None
    Role: Optional[str] = None
    UserID: Optional[str] = None

class TaiKhoan(TaiKhoanBase):
    Username: str
