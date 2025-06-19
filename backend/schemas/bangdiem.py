from pydantic import BaseModel
from typing import Optional

class DiemMonHoc(BaseModel):
    MaLopTC: str
    MaMH: str
    TenMH: str
    SoTinChi: int
    DiemChuyenCan: Optional[float] = None
    DiemGiuaKy: Optional[float] = None
    DiemCuoiKy: Optional[float] = None
    DiemThucHanh: Optional[float] = None
    DiemTongKetHe10: Optional[float] = None
    DiemChu: Optional[str] = None
    TrangThaiQuaMon: Optional[str] = None

class DiemTongKetKy(BaseModel):
    MaKy: str
    DiemTBKyHe10: Optional[float] = None
    DiemTBKyHe4: Optional[float] = None
    DiemTBKyChu: Optional[str] = None
    SoTCDatKy: Optional[int] = None
    XepLoaiHocLucKy: Optional[str] = None

class DiemUpdateRequest(BaseModel):
    MaSV: str
    DiemChuyenCan: Optional[float] = None
    DiemGiuaKy: Optional[float] = None
    DiemCuoiKy: Optional[float] = None
    DiemThucHanh: Optional[float] = None
