from pydantic import BaseModel

class KhoaBase(BaseModel):
    TenKhoa: str

class KhoaCreate(KhoaBase):
    MaKhoa: str

class Khoa(KhoaBase):
    MaKhoa: str
