from pydantic import BaseModel
from typing import Optional

class ChuyenNganhUpdate(BaseModel):
    TenChuyenNganh: Optional[str] = None;
    MaKhoa: Optional[str] = None