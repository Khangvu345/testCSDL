# backend/schemas/bangdiem.py
from pydantic import BaseModel
from typing import Optional

class DiemMonHoc(BaseModel):
    MaMH: str
    TenMH: str
    SoTinChi: int
    DiemCC: Optional[float] = None
    DiemGK: Optional[float] = None
    DiemCK: Optional[float] = None
    DiemHe10: Optional[float] = None
    DiemChu: Optional[str] = None

class DiemTongKetKy(BaseModel):
    MaHK: str
    TenHK: str
    NamHoc: str
    DiemTBKyHe10: float
    DiemTBKyHe4: float
    SoTinChiDatKy: int
    SoTinChiTichLuy: int

class TienDoHocTap(BaseModel):
    tong_tin_chi_dat: int
    tong_tin_chi_chuong_trinh: int
    phan_tram_hoan_thanh: float
