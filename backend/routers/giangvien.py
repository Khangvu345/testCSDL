# backend/routers/giangvien.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from schemas.giangvien import LopTinChiGV, SinhVienTrongLopTC
from schemas.loptc import DiemUpdateRequest
from schemas.token import TokenData  # Import TokenData
from crud import giangvien_crud
from routers.dependencies import require_role, get_db  # Sửa import

router = APIRouter(prefix="/api/giangvien", tags=["Teacher"])
teacher_dependency = Depends(require_role("teacher"))


@router.get("/me/classes", response_model=List[LopTinChiGV])
def read_teacher_classes(current_user: TokenData = teacher_dependency, db=Depends(get_db)):
    """API cho giảng viên xem các lớp tín chỉ mình đang dạy."""
    classes = giangvien_crud.get_teacher_classes(db, ma_gv=current_user.user_id)
    return classes


@router.get("/classes/{ma_ltc}/students", response_model=List[SinhVienTrongLopTC])
def read_students_in_class(ma_ltc: int, current_user: TokenData = teacher_dependency, db=Depends(get_db)):
    """API cho giảng viên xem danh sách sinh viên trong lớp tín chỉ."""
    if not giangvien_crud.check_teacher_permission_for_class(db, current_user.user_id, ma_ltc):
        raise HTTPException(status_code=403, detail="Not authorized to access this class")
    students = giangvien_crud.get_students_in_class(db, ma_ltc=ma_ltc)
    return students


@router.post("/classes/{ma_ltc}/grades", status_code=status.HTTP_200_OK)
def update_grade_for_student(ma_ltc: int, grade_data: DiemUpdateRequest, current_user: TokenData = teacher_dependency,
                             db=Depends(get_db)):
    """API cho giảng viên nhập/sửa điểm cho sinh viên."""
    if not giangvien_crud.check_teacher_permission_for_class(db, current_user.user_id, ma_ltc):
        raise HTTPException(status_code=403, detail="Not authorized to modify grades for this class")

    result = giangvien_crud.update_student_grade(
        db_connection=db,
        ma_ltc=ma_ltc,
        ma_sv=grade_data.MaSV,
        diem_cc=grade_data.DiemCC,
        diem_gk=grade_data.DiemGK,
        diem_ck=grade_data.DiemCK
    )
    return result
