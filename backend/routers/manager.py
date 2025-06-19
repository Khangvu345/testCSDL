from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from schemas.khoa import Khoa, KhoaCreate, KhoaUpdate
from schemas.chuyennganh import ChuyenNganh, ChuyenNganhCreate, ChuyenNganhUpdate
from schemas.lophc import LopHC, LopHCCreate, LopHCUpdate
from schemas.sinhvien import SinhVien, SinhVienCreate, SinhVienBase
from schemas.giangvien import GiangVien, GiangVienCreate, GiangVienBase
from schemas.monhoc import MonHoc, MonHocCreate, MonHocBase
from schemas.kyhoc import KyHoc, KyHocCreate, KyHocUpdate
from schemas.loptc import LopTC, LopTCCreate, LopTCUpdate
from schemas.user import TaiKhoan, TaiKhoanCreate, TaiKhoanUpdate
from crud import manager_crud
from routers.dependencies import get_db, require_role
import csv
import io
from starlette.responses import StreamingResponse
router = APIRouter(prefix="/api/manager", tags=["Manager (Admin)"], dependencies=[Depends(require_role("manager"))])

# --- API cho KHOA ---
@router.post("/khoa", response_model=Khoa, summary="Tạo Khoa mới")
def create_new_khoa(data: KhoaCreate, db=Depends(get_db)): return manager_crud.create_khoa(db, data.dict())
@router.get("/khoa", response_model=List[Khoa], summary="Lấy danh sách Khoa")
def get_all_khoa_api(db=Depends(get_db)): return manager_crud.get_all_khoa(db)
@router.put("/khoa/{ma_khoa}", response_model=Khoa, summary="Cập nhật thông tin Khoa")
def update_khoa_api(ma_khoa: str, data: KhoaUpdate, db=Depends(get_db)): return manager_crud.update_khoa(db, ma_khoa, data.dict(exclude_unset=True))
@router.delete("/khoa/{ma_khoa}", summary="Xóa Khoa")
def delete_khoa_api(ma_khoa: str, db=Depends(get_db)): return manager_crud.delete_khoa(db, ma_khoa)

# --- API cho CHUYÊN NGÀNH ---
@router.post("/chuyen-nganh", response_model=ChuyenNganh, summary="Tạo Chuyên ngành mới")
def create_new_chuyen_nganh(data: ChuyenNganhCreate, db=Depends(get_db)): return manager_crud.create_chuyen_nganh(db, data.dict())
@router.get("/chuyen-nganh", response_model=List[ChuyenNganh], summary="Lấy danh sách Chuyên ngành")
def get_all_chuyen_nganh_api(db=Depends(get_db)): return manager_crud.get_all_chuyen_nganh(db)
@router.put("/chuyen-nganh/{ma_cn}", response_model=ChuyenNganh, summary="Cập nhật Chuyên ngành")
def update_chuyen_nganh_api(ma_cn: str, data: ChuyenNganhUpdate, db=Depends(get_db)): return manager_crud.update_chuyen_nganh(db, ma_cn, data.dict(exclude_unset=True))
@router.delete("/chuyen-nganh/{ma_cn}", summary="Xóa Chuyên ngành")
def delete_chuyen_nganh_api(ma_cn: str, db=Depends(get_db)): return manager_crud.delete_chuyen_nganh(db, ma_cn)

# --- API cho LỚP HÀNH CHÍNH ---
@router.post("/lop-hanh-chinh", response_model=LopHC, summary="Tạo Lớp hành chính mới")
def create_new_lop_hc(data: LopHCCreate, db=Depends(get_db)): return manager_crud.create_lop_hc(db, data.dict())
@router.get("/lop-hanh-chinh", response_model=List[LopHC], summary="Lấy danh sách Lớp hành chính")
def get_all_lop_hc_api(db=Depends(get_db)): return manager_crud.get_all_lop_hc(db)
@router.put("/lop-hanh-chinh/{ma_lop}", response_model=LopHC, summary="Cập nhật Lớp hành chính")
def update_lop_hc_api(ma_lop: str, data: LopHCUpdate, db=Depends(get_db)): return manager_crud.update_lop_hc(db, ma_lop, data.dict(exclude_unset=True))
@router.delete("/lop-hanh-chinh/{ma_lop}", summary="Xóa Lớp hành chính")
def delete_lop_hc_api(ma_lop: str, db=Depends(get_db)): return manager_crud.delete_lop_hc(db, ma_lop)

# --- API cho SINH VIÊN ---
@router.post("/sinh-vien", response_model=SinhVien, summary="Tạo Sinh viên mới")
def create_new_sinh_vien(data: SinhVienCreate, db=Depends(get_db)): return manager_crud.create_sinh_vien(db, data.dict())
@router.get("/sinh-vien", response_model=List[SinhVien], summary="Lấy danh sách Sinh viên")
def get_all_sinh_vien_api(db=Depends(get_db)): return manager_crud.get_all_sinh_vien(db)
@router.get("/sinh-vien/{ma_sv}", response_model=SinhVien, summary="Lấy thông tin một Sinh viên")
def get_sinh_vien_by_id_api(ma_sv: str, db=Depends(get_db)): return manager_crud.get_sinh_vien_by_id(db, ma_sv)
@router.put("/sinh-vien/{ma_sv}", response_model=SinhVien, summary="Cập nhật thông tin Sinh viên")
def update_sinh_vien_api(ma_sv: str, data: SinhVienBase, db=Depends(get_db)): return manager_crud.update_sinh_vien(db, ma_sv, data.dict(exclude_unset=True))
@router.delete("/sinh-vien/{ma_sv}", summary="Xóa Sinh viên")
def delete_sinh_vien_api(ma_sv: str, db=Depends(get_db)): return manager_crud.delete_sinh_vien(db, ma_sv)

# --- API cho GIẢNG VIÊN ---
@router.post("/giang-vien", response_model=GiangVien, summary="Tạo Giảng viên mới")
def create_new_giang_vien(data: GiangVienCreate, db=Depends(get_db)): return manager_crud.create_giang_vien(db, data.dict())
@router.get("/giang-vien", response_model=List[GiangVien], summary="Lấy danh sách Giảng viên")
def get_all_giang_vien_api(db=Depends(get_db)): return manager_crud.get_all_giang_vien(db)
@router.put("/giang-vien/{ma_gv}", response_model=GiangVien, summary="Cập nhật thông tin Giảng viên")
def update_giang_vien_api(ma_gv: str, data: GiangVienBase, db=Depends(get_db)): return manager_crud.update_giang_vien(db, ma_gv, data.dict(exclude_unset=True))
@router.delete("/giang-vien/{ma_gv}", summary="Xóa Giảng viên")
def delete_giang_vien_api(ma_gv: str, db=Depends(get_db)): return manager_crud.delete_giang_vien(db, ma_gv)

# --- API cho MÔN HỌC ---
@router.post("/mon-hoc", response_model=MonHoc, summary="Tạo Môn học mới")
def create_new_mon_hoc(data: MonHocCreate, db=Depends(get_db)): return manager_crud.create_mon_hoc(db, data.dict())
@router.get("/mon-hoc", response_model=List[MonHoc], summary="Lấy danh sách Môn học")
def get_all_mon_hoc_api(db=Depends(get_db)): return manager_crud.get_all_mon_hoc(db)
@router.put("/mon-hoc/{ma_mh}", response_model=MonHoc, summary="Cập nhật Môn học")
def update_mon_hoc_api(ma_mh: str, data: MonHocBase, db=Depends(get_db)): return manager_crud.update_mon_hoc(db, ma_mh, data.dict(exclude_unset=True))
@router.delete("/mon-hoc/{ma_mh}", summary="Xóa Môn học")
def delete_mon_hoc_api(ma_mh: str, db=Depends(get_db)): return manager_crud.delete_mon_hoc(db, ma_mh)

# --- API cho KỲ HỌC ---
@router.post("/ky-hoc", response_model=KyHoc, summary="Tạo Kỳ học mới")
def create_new_ky_hoc(data: KyHocCreate, db=Depends(get_db)): return manager_crud.create_ky_hoc(db, data.dict())
@router.get("/ky-hoc", response_model=List[KyHoc], summary="Lấy danh sách Kỳ học")
def get_all_ky_hoc_api(db=Depends(get_db)): return manager_crud.get_all_ky_hoc(db)
@router.put("/ky-hoc/{ma_ky}", response_model=KyHoc, summary="Cập nhật Kỳ học")
def update_ky_hoc_api(ma_ky: str, data: KyHocUpdate, db=Depends(get_db)): return manager_crud.update_ky_hoc(db, ma_ky, data.dict(exclude_unset=True))
@router.delete("/ky-hoc/{ma_ky}", summary="Xóa Kỳ học")
def delete_ky_hoc_api(ma_ky: str, db=Depends(get_db)): return manager_crud.delete_ky_hoc(db, ma_ky)

# --- API cho LỚP TÍN CHỈ ---
@router.post("/lop-tin-chi", response_model=LopTC, summary="Tạo Lớp tín chỉ mới")
def create_new_lop_tc(data: LopTCCreate, db=Depends(get_db)): return manager_crud.create_lop_tc(db, data.dict())
@router.get("/lop-tin-chi", summary="Lấy danh sách Lớp tín chỉ (chi tiết)")
def get_all_lop_tc_api(db=Depends(get_db)): return manager_crud.get_all_lop_tc(db)
@router.put("/lop-tin-chi/{ma_ltc}", response_model=LopTC, summary="Cập nhật Lớp tín chỉ")
def update_lop_tc_api(ma_ltc: str, data: LopTCUpdate, db=Depends(get_db)): return manager_crud.update_lop_tc(db, ma_ltc, data.dict(exclude_unset=True))
@router.delete("/lop-tin-chi/{ma_ltc}", summary="Xóa Lớp tín chỉ")
def delete_lop_tc_api(ma_ltc: str, db=Depends(get_db)): return manager_crud.delete_lop_tc(db, ma_ltc)

# --- API Quản lý TÀI KHOẢN ---
@router.post("/tai-khoan", response_model=TaiKhoan, summary="Tạo tài khoản người dùng mới")
def create_new_account(data: TaiKhoanCreate, db=Depends(get_db)): return manager_crud.create_user_account(db, data.dict())
@router.get("/tai-khoan", response_model=List[TaiKhoan], summary="Lấy danh sách tất cả tài khoản")
def get_all_accounts_api(db=Depends(get_db)): return manager_crud.get_all_accounts(db)
@router.put("/tai-khoan/{username}", response_model=TaiKhoan, summary="Cập nhật tài khoản (đổi mật khẩu, vai trò)")
def update_account_api(username: str, data: TaiKhoanUpdate, db=Depends(get_db)): return manager_crud.update_user_account(db, username, data.dict(exclude_unset=True))
@router.delete("/tai-khoan/{username}", summary="Xóa tài khoản người dùng")
def delete_account_api(username: str, db=Depends(get_db)): return manager_crud.delete_user_account(db, username)

# --- API cho Báo cáo ---
@router.get("/reports/grades/{ma_ltc}/csv", summary="Xuất báo cáo điểm của lớp tín chỉ ra file CSV")
def export_grades_to_csv(ma_ltc: str, db=Depends(get_db)):
    grades_data = manager_crud.get_grades_for_report(db, ma_ltc)
    if not grades_data: raise HTTPException(status_code=404, detail="Không có dữ liệu điểm cho lớp tín chỉ này.")
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(grades_data[0].keys())
    for row in grades_data: writer.writerow(row.values())
    output.seek(0)
    response = StreamingResponse(iter([output.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = f"attachment; filename=BangDiem_{ma_ltc}.csv"
    return response
