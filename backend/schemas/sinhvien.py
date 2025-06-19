from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class SinhVienBase(BaseModel):
    HoTen: str
    MaLopHC: Optional[str] = None
    MaChuyenNganh: Optional[str] = None
    NgaySinh: Optional[date] = None
    GioiTinh: Optional[str] = None
    SDT: Optional[str] = None
    Email: Optional[EmailStr] = None
    NamNhapHoc: Optional[int] = None

class SinhVienCreate(SinhVienBase):
    MaSV: str

class SinhVien(SinhVienBase):
    MaSV: str