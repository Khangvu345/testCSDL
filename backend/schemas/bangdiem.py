from pydantic import BaseModel
from typing import Optional

class DiemMonHoc(BaseModel): #sinh viên xem điểm
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

class DiemTongKetKy(BaseModel): #sinh viên xem điểm tổng kết
    MaKy: str
    DiemTBKyHe10: Optional[float] = None
    DiemTBKyHe4: Optional[float] = None
    DiemTBKyChu: Optional[str] = None
    SoTCDatKy: Optional[int] = None
    XepLoaiHocLucKy: Optional[str] = None

class DiemUpdateRequest(BaseModel): #giảng viên nhập điểm
    MaSV: str
    DiemChuyenCan: Optional[float] = None
    DiemGiuaKy: Optional[float] = None
    DiemCuoiKy: Optional[float] = None
    DiemThucHanh: Optional[float] = None
