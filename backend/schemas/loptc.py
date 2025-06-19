# backend/schemas/loptc.py
from pydantic import BaseModel
from typing import Optional

class DiemUpdateRequest(BaseModel):
    MaSV: str
    DiemCC: Optional[float]
    DiemGK: Optional[float]
    DiemCK: Optional[float]
