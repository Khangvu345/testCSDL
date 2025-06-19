from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class GiangVienBase(BaseModel):
    HoVaTen: str
    MaKhoaCongTac: Optional[str] = None
    NgaySinh: Optional[date] = None
    GioiTinh: Optional[str] = None
    SDT: Optional[str] = None
    Email: Optional[EmailStr] = None

class GiangVienCreate(GiangVienBase):
    MaGV: str

class GiangVien(GiangVienBase):
    MaGV: str

class LopTinChiGV(BaseModel):
    MaLopTC: str
    TenMH: str
    TenKy: str

class SinhVienTrongLopTC(BaseModel):
    MaSV: str
    HoTen: str
    DiemChuyenCan: Optional[float] = None
    DiemGiuaKy: Optional[float] = None
    DiemCuoiKy: Optional[float] = None
    DiemThucHanh: Optional[float] = None
    DiemTongKetHe10: Optional[float] = None
    TrangThaiQuaMon: Optional[str] = None
