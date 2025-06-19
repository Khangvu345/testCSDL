def get_teacher_classes(db_connection, ma_gv: str):
    """Lấy danh sách lớp tín chỉ của giảng viên."""
    with db_connection.cursor() as cursor:
        query = """
            SELECT ltc.MaLopTC, mh.TenMH, kh.TenKy
            FROM LopTC ltc
            JOIN MonHoc mh ON ltc.MaMH = mh.MaMH
            JOIN KyHoc kh ON ltc.MaKy = kh.MaKy
            WHERE ltc.MaGV = %s
        """
        cursor.execute(query, (ma_gv,))
        return cursor.fetchall()

def get_students_in_class(db_connection, ma_ltc: str):
    """Lấy danh sách sinh viên và điểm trong một lớp tín chỉ."""
    with db_connection.cursor() as cursor:
        query = """
            SELECT 
                sv.MaSV, sv.HoTen, bd.DiemChuyenCan, bd.DiemGiuaKy, 
                bd.DiemCuoiKy, bd.DiemThucHanh, bd.DiemTongKetHe10, bd.TrangThaiQuaMon
            FROM BangDiem bd
            JOIN SinhVien sv ON bd.MaSV = sv.MaSV
            WHERE bd.MaLopTC = %s
        """
        cursor.execute(query, (ma_ltc,))
        return cursor.fetchall()

def update_student_grade(db_connection, ma_ltc: str, ma_sv: str, diem_data: dict):
    """Cập nhật điểm cho sinh viên với logic tính điểm động."""
    with db_connection.cursor() as cursor:
        # 1. Lấy hệ số môn học
        get_coeffs_query = """
            SELECT mh.HeSoChuyenCan, mh.HeSoGiuaKy, mh.HeSoCuoiKy, mh.HeSoThucHanh
            FROM LopTC ltc JOIN MonHoc mh ON ltc.MaMH = mh.MaMH
            WHERE ltc.MaLopTC = %s
        """
        cursor.execute(get_coeffs_query, (ma_ltc,))
        coeffs = cursor.fetchone()
        if not coeffs:
            raise ValueError(f"Không tìm thấy hệ số cho Lớp TC {ma_ltc}")

        # 2. Tính điểm tổng kết
        diem_tong_ket = 0.0
        tong_he_so = 0.0
        diem_thanh_phan = {
            'DiemChuyenCan': (diem_data.get('DiemChuyenCan'), coeffs.get('HeSoChuyenCan')),
            'DiemGiuaKy': (diem_data.get('DiemGiuaKy'), coeffs.get('HeSoGiuaKy')),
            'DiemCuoiKy': (diem_data.get('DiemCuoiKy'), coeffs.get('HeSoCuoiKy')),
            'DiemThucHanh': (diem_data.get('DiemThucHanh'), coeffs.get('HeSoThucHanh')),
        }

        for diem, he_so in diem_thanh_phan.values():
            if diem is not None and he_so is not None:
                diem_tong_ket += diem * he_so
                tong_he_so += he_so

        final_score_10 = round(diem_tong_ket / tong_he_so, 1) if tong_he_so > 0 else 0.0

        # 3. Quy đổi
        if final_score_10 >= 9.0:
            diem_chu, final_score_4 = 'A+', 4.0
        elif final_score_10 >= 8.5:
            diem_chu, final_score_4 = 'A', 3.7
        elif final_score_10 >= 8.0:
            diem_chu, final_score_4 = 'B+', 3.5
        elif final_score_10 >= 7.0:
            diem_chu, final_score_4 = 'B', 3.0
        elif final_score_10 >= 6.5:
            diem_chu, final_score_4 = 'C+', 2.5
        elif final_score_10 >= 5.5:
            diem_chu, final_score_4 = 'C', 2.0
        elif final_score_10 >= 5.0:
            diem_chu, final_score_4 = 'D+', 1.5
        elif final_score_10 >= 4.0:
            diem_chu, final_score_4 = 'D', 1.0
        else:
            diem_chu, final_score_4 = 'F', 0.0
        trang_thai = 'Đạt' if final_score_10 >= 4.0 else 'Trượt'

        # 4. Cập nhật Database
        update_query = """
            INSERT INTO BangDiem (MaSV, MaLopTC, DiemChuyenCan, DiemGiuaKy, DiemCuoiKy, DiemThucHanh, DiemTongKetHe10, DiemTongKetHe4, DiemChu, TrangThaiQuaMon)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            DiemChuyenCan = VALUES(DiemChuyenCan), DiemGiuaKy = VALUES(DiemGiuaKy), DiemCuoiKy = VALUES(DiemCuoiKy),
            DiemThucHanh = VALUES(DiemThucHanh), DiemTongKetHe10 = VALUES(DiemTongKetHe10), DiemTongKetHe4 = VALUES(DiemTongKetHe4),
            DiemChu = VALUES(DiemChu), TrangThaiQuaMon = VALUES(TrangThaiQuaMon)
        """
        params = (
        ma_sv, ma_ltc, diem_data.get('DiemChuyenCan'), diem_data.get('DiemGiuaKy'), diem_data.get('DiemCuoiKy'),
        diem_data.get('DiemThucHanh'), final_score_10, final_score_4, diem_chu, trang_thai)
        cursor.execute(update_query, params)
        db_connection.commit()

    return {"status": "success", "ma_sv": ma_sv, "diem_he_10": final_score_10}


def delete_student_grade(db_connection, ma_ltc: str, ma_sv: str):
    """Xóa hoàn toàn bản ghi điểm của một sinh viên khỏi lớp tín chỉ."""
    with db_connection.cursor() as cursor:
        query = "DELETE FROM BangDiem WHERE MaSV = %s AND MaLopTC = %s"
        cursor.execute(query, (ma_sv, ma_ltc))
        db_connection.commit()
        return {"status": "deleted", "deleted_rows": cursor.rowcount}


def check_teacher_permission_for_class(db_connection, ma_gv: str, ma_ltc: str) -> bool:
    """Kiểm tra xem giảng viên có quyền với lớp tín chỉ này không."""
    with db_connection.cursor() as cursor:
        query = "SELECT COUNT(*) as count FROM LopTC WHERE MaLopTC = %s AND MaGV = %s"
        cursor.execute(query, (ma_ltc, ma_gv))
        result = cursor.fetchone()
        return result['count'] > 0
