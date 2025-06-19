# backend/routers/sinhvien.py
from fastapi import APIRouter, Depends
from typing import List
from schemas.bangdiem import DiemMonHoc, TienDoHocTap
from schemas.token import TokenData # Import TokenData
from crud import sinhvien_crud
from routers.dependencies import require_role, get_db # Sửa import

router = APIRouter(prefix="/api/sinhvien", tags=["Student"])
student_dependency = Depends(require_role("student"))

@router.get("/me/grades", response_model=List[DiemMonHoc])
def read_student_grades(current_user: TokenData = student_dependency, db=Depends(get_db)):
    """API cho sinh viên xem bảng điểm cá nhân."""
    grades = sinhvien_crud.get_student_grades_by_id(db, ma_sv=current_user.user_id)
    return grades

@router.get("/me/progress", response_model=TienDoHocTap)
def read_student_progress(current_user: TokenData = student_dependency, db=Depends(get_db)):
    """API cho sinh viên xem tiến độ học tập (số tín chỉ đã đạt)."""
    credits_earned = sinhvien_crud.get_student_credits_earned(db, ma_sv=current_user.user_id)
    total_credits_program = 120 # Giả định chương trình học có 120 tín chỉ
    return {
        "tong_tin_chi_dat": credits_earned,
        "tong_tin_chi_chuong_trinh": total_credits_program,
        "phan_tram_hoan_thanh": round((credits_earned / total_credits_program) * 100, 2)
    }
