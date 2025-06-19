from pydantic import BaseModel
from typing import Optional
from datetime import date

class KyHocUpdate(BaseModel):
    TenKy: Optional[str] = None
    NamHoc: Optional[int] = None
    NgayBatDau: Optional[date] = None
    NgayKetThuc: Optional[date] = None