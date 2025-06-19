from pydantic import BaseModel
from typing import Optional

class LopHCUpdate(BaseModel):
    MaKhoaQuanLy: Optional[str] = None