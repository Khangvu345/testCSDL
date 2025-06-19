from pydantic import BaseModel
from typing import Optional

class LopTCBase(BaseModel):
    MaMH: str
    MaGV: str
    MaKy: str

class LopTCCreate(LopTCBase):
    MaLopTC: str

class LopTC(LopTCBase):
    MaLopTC: str