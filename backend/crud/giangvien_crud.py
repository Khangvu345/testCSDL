# backend/crud/giangvien_crud.py

def get_teacher_classes(db_connection, ma_gv: str):
    """Lấy danh sách lớp tín chỉ của giảng viên."""
    cursor = db_connection.cursor()
    query = """
        SELECT ltc.MaLTC, mh.TenMH, hk.TenHK, ltc.Nhom
        FROM loptinchi ltc
        JOIN monhoc mh ON ltc.MaMH = mh.MaMH
        JOIN hocky hk ON ltc.MaHK = hk.MaHK
        WHERE ltc.MaGV = %s
    """
    cursor.execute(query, (ma_gv,))
    results = cursor.fetchall()
    cursor.close()
    return results

def get_students_in_class(db_connection, ma_ltc: int):
    """Lấy danh sách sinh viên và điểm trong một lớp tín chỉ."""
    cursor = db_connection.cursor()
    query = """
        SELECT sv.MaSV, sv.HoTen, bd.DiemCC, bd.DiemGK, bd.DiemCK, bd.DiemHe10
        FROM dangky dk
        JOIN sinhvien sv ON dk.MaSV = sv.MaSV
        LEFT JOIN bangdiem bd ON dk.MaLTC = bd.MaLTC AND dk.MaSV = bd.MaSV
        WHERE dk.MaLTC = %s
    """
    cursor.execute(query, (ma_ltc,))
    results = cursor.fetchall()
    cursor.close()
    return results

def update_student_grade(db_connection, ma_ltc: int, ma_sv: str, diem_cc, diem_gk, diem_ck):
    """Cập nhật hoặc nhập điểm cho sinh viên."""
    diem_he_10 = None
    if diem_cc is not None and diem_gk is not None and diem_ck is not None:
        diem_he_10 = round(0.1 * diem_cc + 0.2 * diem_gk + 0.7 * diem_ck, 1)

    diem_chu = None
    if diem_he_10 is not None:
        if diem_he_10 >= 8.5: diem_chu = 'A'
        elif diem_he_10 >= 7.0: diem_chu = 'B'
        elif diem_he_10 >= 5.5: diem_chu = 'C'
        elif diem_he_10 >= 4.0: diem_chu = 'D'
        else: diem_chu = 'F'

    cursor = db_connection.cursor()
    query = """
        INSERT INTO bangdiem (MaLTC, MaSV, DiemCC, DiemGK, DiemCK, DiemHe10, DiemChu)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        DiemCC = VALUES(DiemCC),
        DiemGK = VALUES(DiemGK),
        DiemCK = VALUES(DiemCK),
        DiemHe10 = VALUES(DiemHe10),
        DiemChu = VALUES(DiemChu)
    """
    params = (ma_ltc, ma_sv, diem_cc, diem_gk, diem_ck, diem_he_10, diem_chu)
    cursor.execute(query, params)
    db_connection.commit()
    cursor.close()
    return {"status": "success", "ma_sv": ma_sv, "diem_he_10": diem_he_10}

def check_teacher_permission_for_class(db_connection, ma_gv: str, ma_ltc: int) -> bool:
    """Kiểm tra xem giảng viên có quyền với lớp tín chỉ này không."""
    cursor = db_connection.cursor()
    query = "SELECT COUNT(*) as count FROM loptinchi WHERE MaLTC = %s AND MaGV = %s"
    cursor.execute(query, (ma_ltc, ma_gv))
    result = cursor.fetchone()
    cursor.close()
    return result['count'] > 0