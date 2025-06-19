def get_student_grades_by_id(db_connection, ma_sv: str):
    """Lấy bảng điểm chi tiết của sinh viên. Dùng with không cần đóng trỏ """
    with db_connection.cursor() as cursor:
        query = """
              SELECT 
                  ltc.MaLopTC, mh.MaMH, mh.TenMH, mh.SoTinChi,
                  bd.DiemChuyenCan, bd.DiemGiuaKy, bd.DiemCuoiKy, bd.DiemThucHanh,
                  bd.DiemTongKetHe10, bd.DiemChu, bd.TrangThaiQuaMon
              FROM BangDiem bd
              JOIN LopTC ltc ON bd.MaLopTC = ltc.MaLopTC
              JOIN MonHoc mh ON ltc.MaMH = mh.MaMH
              WHERE bd.MaSV = %s
          """
        cursor.execute(query, (ma_sv,))
        return cursor.fetchall()


def calculate_student_summary_for_semester(db_connection, ma_sv: str, ma_ky: str):
    """ Tính toán động bảng điểm 1 kì  """
    with db_connection.cursor() as cursor:
        query = """
            SELECT
                SUM(bd.DiemTongKetHe10 * mh.SoTinChi) AS TongDiemNhanHeSo,
                SUM(mh.SoTinChi) AS TongHeSoTinChi,
                SUM(CASE WHEN bd.TrangThaiQuaMon = 'Đạt' THEN mh.SoTinChi ELSE 0 END) AS SoTCDatKy
            FROM BangDiem bd
            JOIN LopTC ltc ON bd.MaLopTC = ltc.MaLopTC
            JOIN MonHoc mh ON ltc.MaMH = mh.MaMH
            WHERE bd.MaSV = %s AND ltc.MaKy = %s AND bd.DiemTongKetHe10 IS NOT NULL
        """
        cursor.execute(query, (ma_sv, ma_ky))
        result_raw = cursor.fetchone()

        # Nếu không có môn nào có điểm trong kỳ, trả về kết quả rỗng
        if not result_raw or result_raw['TongHeSoTinChi'] is None:
            return {
                "MaKy": ma_ky, "DiemTBKyHe10": 0, "DiemTBKyHe4": 0, "DiemTBKyChu": 'F',
                "SoTCDatKy": 0, "XepLoaiHocLucKy": 'Kém'
            }

        # Tính toán điểm trung bình
        diem_tb_ky_he_10 = 0.0
        if result_raw['TongHeSoTinChi'] > 0:
            diem_tb_ky_he_10 = round(result_raw['TongDiemNhanHeSo'] / result_raw['TongHeSoTinChi'], 2)

        if diem_tb_ky_he_10 >= 9.0:
            diem_tb_ky_he_4, diem_tb_ky_chu, xep_loai = 4.0, 'A+', 'Giỏi'
        elif diem_tb_ky_he_10 >= 8.5:
            diem_tb_ky_he_4, diem_tb_ky_chu, xep_loai = 3.7, 'A', 'Giỏi'
        elif diem_tb_ky_he_10 >= 8.0:
            diem_tb_ky_he_4, diem_tb_ky_chu, xep_loai = 3.5, 'B+', 'Khá'
        elif diem_tb_ky_he_10 >= 7.0:
            diem_tb_ky_he_4, diem_tb_ky_chu, xep_loai = 3.0, 'B', 'Khá'
        elif diem_tb_ky_he_10 >= 6.5:
            diem_tb_ky_he_4, diem_tb_ky_chu, xep_loai = 2.5, 'C+', 'Trung bình'
        elif diem_tb_ky_he_10 >= 5.5:
            diem_tb_ky_he_4, diem_tb_ky_chu, xep_loai = 2.0, 'C', 'Trung bình'
        elif diem_tb_ky_he_10 >= 5.0:
            diem_tb_ky_he_4, diem_tb_ky_chu, xep_loai = 1.5, 'D+', 'Trung bình yếu'
        elif diem_tb_ky_he_10 >= 4.0:
            diem_tb_ky_he_4, diem_tb_ky_chu, xep_loai = 1.0, 'D', 'Trung bình yếu'
        else:
            diem_tb_ky_he_4, diem_tb_ky_chu, xep_loai = 0.0, 'F', 'Kém'

        summary = {
            "MaKy": ma_ky,
            "DiemTBKyHe10": diem_tb_ky_he_10,
            "DiemTBKyHe4": diem_tb_ky_he_4,
            "DiemTBKyChu": diem_tb_ky_chu,
            "SoTCDatKy": int(result_raw['SoTCDatKy']),
            "XepLoaiHocLucKy": xep_loai
        }
    return summary


def get_student_credits_earned(db_connection, ma_sv: str):
    """Tính tổng số tín chỉ sinh viên đã đạt trong toàn bộ quá trình học."""
    with db_connection.cursor() as cursor:
        query = """
            SELECT SUM(mh.SoTinChi) as TongTinChiDat
            FROM BangDiem bd
            JOIN LopTC ltc ON bd.MaLopTC = ltc.MaLopTC
            JOIN MonHoc mh ON ltc.MaMH = mh.MaMH
            WHERE bd.MaSV = %s AND bd.TrangThaiQuaMon = 'Đạt'
        """
        cursor.execute(query, (ma_sv,))
        result = cursor.fetchone()
        return result['TongTinChiDat'] if result and result['TongTinChiDat'] is not None else 0