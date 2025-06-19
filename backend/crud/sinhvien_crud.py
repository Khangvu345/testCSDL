# backend/crud/sinhvien_crud.py

def get_student_grades_by_id(db_connection, ma_sv: str):
    """Lấy bảng điểm chi tiết của sinh viên."""
    cursor = db_connection.cursor()
    query = """
        SELECT mh.MaMH, mh.TenMH, mh.SoTinChi, bd.DiemCC, bd.DiemGK, bd.DiemCK, bd.DiemHe10, bd.DiemChu
        FROM bangdiem bd
        JOIN loptinchi ltc ON bd.MaLTC = ltc.MaLTC
        JOIN monhoc mh ON ltc.MaMH = mh.MaMH
        WHERE bd.MaSV = %s
    """
    cursor.execute(query, (ma_sv,))
    results = cursor.fetchall()
    cursor.close()
    return results

def get_student_credits_earned(db_connection, ma_sv: str):
    """Tính tổng số tín chỉ sinh viên đã đạt."""
    cursor = db_connection.cursor()
    query = """
        SELECT SUM(mh.SoTinChi) as TongTinChiDat
        FROM bangdiem bd
        JOIN loptinchi ltc ON bd.MaLTC = ltc.MaLTC
        JOIN monhoc mh ON ltc.MaMH = mh.MaMH
        WHERE bd.MaSV = %s AND bd.DiemChu != 'F' AND bd.DiemChu IS NOT NULL
    """
    cursor.execute(query, (ma_sv,))
    result = cursor.fetchone()
    cursor.close()
    # Truy cập bằng key vì đang dùng DictCursor
    return result['TongTinChiDat'] if result and result['TongTinChiDat'] is not None else 0
