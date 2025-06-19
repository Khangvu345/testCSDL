from pydantic import BaseModel
from typing import Optional

class LopTCBase(BaseModel):
    MaMH: str
    MaGV: str
    MaKy: str

class LopTCCreate(LopTCBase):
    MaLopTC: str

class LopTCUpdate(BaseModel):
    MaMH: Optional[str] = None
    MaGV: Optional[str] = None
    MaKy: Optional[str] = None

class LopTC(LopTCBase):
    MaLopTC: str