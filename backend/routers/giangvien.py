from fastapi import APIRouter, Depends, status
from typing import List
from schemas.giangvien import LopTinChiGV, SinhVienTrongLopTC
from schemas.bangdiem import DiemUpdateRequest
from schemas.token import TokenData
from crud import giangvien_crud
from routers.dependencies import get_db, require_role
router = APIRouter(prefix="/api/giangvien", tags=["Teacher"])
teacher_dependency = Depends(require_role("teacher"))


@router.get("/me/lop-tin-chi", response_model=List[LopTinChiGV], summary="Xem các lớp tín chỉ đang dạy")
def read_teacher_classes(current_user: TokenData = teacher_dependency, db=Depends(get_db)):
    return giangvien_crud.get_teacher_classes(db, ma_gv=current_user.user_id)


@router.get("/lop-tin-chi/{ma_ltc}/danh-sach-sinh-vien", response_model=List[SinhVienTrongLopTC],
            summary="Xem danh sách sinh viên trong lớp")
def read_students_in_class(ma_ltc: str, current_user: TokenData = teacher_dependency, db=Depends(get_db)):
    if not giangvien_crud.check_teacher_permission_for_class(db, current_user.user_id, ma_ltc):
        raise HTTPException(status_code=403, detail="Not authorized to access this class")
    return giangvien_crud.get_students_in_class(db, ma_ltc=ma_ltc)


@router.post("/lop-tin-chi/{ma_ltc}/nhap-diem", status_code=status.HTTP_200_OK,
             summary="Nhập hoặc sửa điểm cho sinh viên")
def update_grade_for_student(ma_ltc: str, grade_data: DiemUpdateRequest, current_user: TokenData = teacher_dependency,
                             db=Depends(get_db)):
    if not giangvien_crud.check_teacher_permission_for_class(db, current_user.user_id, ma_ltc):
        raise HTTPException(status_code=403, detail="Not authorized to modify grades for this class")
    return giangvien_crud.update_student_grade(db_connection=db, ma_ltc=ma_ltc, ma_sv=grade_data.MaSV,
                                               diem_data=grade_data.dict(exclude={"MaSV"}))


@router.delete("/lop-tin-chi/{ma_ltc}/xoa-diem/{ma_sv}", status_code=status.HTTP_200_OK,
               summary="Xóa điểm của sinh viên")
def delete_grade_for_student(ma_ltc: str, ma_sv: str, current_user: TokenData = teacher_dependency, db=Depends(get_db)):
    if not giangvien_crud.check_teacher_permission_for_class(db, current_user.user_id, ma_ltc):
        raise HTTPException(status_code=403, detail="Not authorized to modify grades for this class")
    return giangvien_crud.delete_student_grade(db, ma_ltc, ma_sv)
