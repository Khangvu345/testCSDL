from fastapi import APIRouter, Depends
from typing import List
from schemas.bangdiem import DiemMonHoc, DiemTongKetKy
from schemas.token import TokenData
from crud import sinhvien_crud
from routers.dependencies import get_db, require_role
router = APIRouter(prefix="/api/sinhvien", tags=["Student"])
student_dependency = Depends(require_role("student"))

@router.get("/me/diem-chi-tiet", response_model=List[DiemMonHoc], summary="Xem bảng điểm chi tiết các môn đã học")
def read_student_grades(current_user: TokenData = student_dependency, db=Depends(get_db)):
    """API cho sinh viên xem bảng điểm chi tiết của tất cả các môn học."""
    return sinhvien_crud.get_student_grades_by_id(db, ma_sv=current_user.user_id)

@router.get("/me/diem-tong-ket/{ma_ky}", response_model=DiemTongKetKy, summary="Xem bảng điểm tổng kết của một kỳ học cụ thể")
def read_student_semester_summary(ma_ky: str, current_user: TokenData = student_dependency, db=Depends(get_db)):
    """API cho sinh viên xem bảng điểm tổng kết được TÍNH TOÁN ĐỘNG cho một kỳ học cụ thể."""
    return sinhvien_crud.calculate_student_summary_for_semester(db, ma_sv=current_user.user_id, ma_ky=ma_ky)

@router.get("/me/tien-do-hoc-tap", summary="Xem tổng số tín chỉ đã đạt")
def read_student_progress(current_user: TokenData = student_dependency, db=Depends(get_db)):
    """API cho sinh viên xem tổng số tín chỉ tích lũy đã đạt được."""
    credits_earned = sinhvien_crud.get_student_credits_earned(db, ma_sv=current_user.user_id)
    # Giả định chương trình học có 120 tín chỉ để tính %
    total_program_credits = 120
    return {
        "tong_tin_chi_dat": credits_earned,
        "tong_tin_chi_chuong_trinh": total_program_credits,
        "phan_tram_hoan_thanh": round((credits_earned / total_program_credits) * 100, 2) if total_program_credits > 0 else 0
    }

