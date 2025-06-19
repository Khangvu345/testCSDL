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

class MonHoc(MonHocBase):
    MaMH: str
