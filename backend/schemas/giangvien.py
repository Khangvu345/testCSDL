# backend/schemas/giangvien.py
from pydantic import BaseModel
from typing import Optional

class SinhVienTrongLopTC(BaseModel):
    MaSV: str
    HoTen: str
    DiemCC: Optional[float] = None
    DiemGK: Optional[float] = None
    DiemCK: Optional[float] = None
    DiemHe10: Optional[float] = None

class LopTinChiGV(BaseModel):
    MaLTC: int
    TenMH: str
    TenHK: str
    Nhom: int
