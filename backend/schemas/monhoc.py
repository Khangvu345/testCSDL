from pydantic import BaseModel
from typing import Optional

class MonHocBase(BaseModel):
    TenMH: str
    SoTinChi: int
    LoaiMH: Optional[str] = None
    HeSoChuyenCan: Optional[str] = None
    HeSoGiuaKy: Optional[str] = None
    HeSoCuoiKy: Optional[str] = None
    HeSoThucHanh: Optional[str] = None
    MaKhoa: str

class MonHocCreate(MonHocBase):
    MaMH: str

class MonHocUpdate(MonHocBase):
    TenMH: Optional[str] = None
    SoTinChi: Optional[int] = None
    # Các trường khác có thể được thêm vào đây nếu muốn cập nhật

class MonHoc(MonHocBase):
    MaMH: str
