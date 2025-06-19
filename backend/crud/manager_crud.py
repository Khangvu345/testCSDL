def _build_update_query(table_name: str, data: dict, key_column: str, key_value):
    """Hàm nội bộ để xây dựng câu lệnh UPDATE động, an toàn."""
    # Lọc ra các trường có giá trị khác None để cập nhật
    fields_to_update = {k: v for k, v in data.items() if v is not None}
    if not fields_to_update:
        return None, None

    set_clause = ", ".join([f"{key} = %s" for key in fields_to_update.keys()])
    params = list(fields_to_update.values())
    params.append(key_value)
    query = f"UPDATE {table_name} SET {set_clause} WHERE {key_column} = %s"
    return query, params


# ----- CRUD chung cho các bảng đơn giản -----
def _create_entity(db, table_name, data: dict):
    with db.cursor() as cursor:
        cols = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        sql = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"
        cursor.execute(sql, list(data.values()))
        db.commit()
    return data


def _get_all_entities(db, table_name):
    with db.cursor() as cursor:
        cursor.execute(f"SELECT * FROM {table_name}")
        return cursor.fetchall()


def _get_entity_by_id(db, table_name, key_column, key_value):
    with db.cursor() as cursor:
        cursor.execute(f"SELECT * FROM {table_name} WHERE {key_column} = %s", (key_value,))
        return cursor.fetchone()


def _delete_entity_by_id(db, table_name, key_column, key_value):
    with db.cursor() as cursor:
        cursor.execute(f"DELETE FROM {table_name} WHERE {key_column} = %s", (key_value,))
        db.commit()
        return {key_column: key_value, "status": "deleted"}


# ----- Quản lý Khoa -----
def create_khoa(db, data: dict): return _create_entity(db, "Khoa", data)


def get_all_khoa(db): return _get_all_entities(db, "Khoa")


def get_khoa_by_id(db, ma_khoa: str): return _get_entity_by_id(db, "Khoa", "MaKhoa", ma_khoa)


def update_khoa(db, ma_khoa: str, data: dict):
    query, params = _build_update_query("Khoa", data, "MaKhoa", ma_khoa)
    if query:
        with db.cursor() as cursor: cursor.execute(query, params); db.commit()
    return get_khoa_by_id(db, ma_khoa)


def delete_khoa(db, ma_khoa: str): return _delete_entity_by_id(db, "Khoa", "MaKhoa", ma_khoa)


# ----- Quản lý Chuyên Ngành -----
def create_chuyen_nganh(db, data: dict): return _create_entity(db, "ChuyenNganh", data)


def get_all_chuyen_nganh(db): return _get_all_entities(db, "ChuyenNganh")


def update_chuyen_nganh(db, ma_cn: str, data: dict):
    query, params = _build_update_query("ChuyenNganh", data, "MaChuyenNganh", ma_cn)
    if query:
        with db.cursor() as cursor: cursor.execute(query, params); db.commit()
    return _get_entity_by_id(db, "ChuyenNganh", "MaChuyenNganh", ma_cn)


def delete_chuyen_nganh(db, ma_cn: str): return _delete_entity_by_id(db, "ChuyenNganh", "MaChuyenNganh", ma_cn)


# ----- Quản lý Lớp Hành Chính -----
def create_lop_hc(db, data: dict): return _create_entity(db, "LopHC", data)


def get_all_lop_hc(db): return _get_all_entities(db, "LopHC")


def update_lop_hc(db, ma_lop: str, data: dict):
    query, params = _build_update_query("LopHC", data, "MaLopHC", ma_lop)
    if query:
        with db.cursor() as cursor: cursor.execute(query, params); db.commit()
    return _get_entity_by_id(db, "LopHC", "MaLopHC", ma_lop)


def delete_lop_hc(db, ma_lop: str): return _delete_entity_by_id(db, "LopHC", "MaLopHC", ma_lop)


# ----- Quản lý Sinh Viên -----
def create_sinh_vien(db, data: dict): return _create_entity(db, "SinhVien", data)


def get_all_sinh_vien(db): return _get_all_entities(db, "SinhVien")


def get_sinh_vien_by_id(db, ma_sv: str): return _get_entity_by_id(db, "SinhVien", "MaSV", ma_sv)


def update_sinh_vien(db, ma_sv: str, data: dict):
    query, params = _build_update_query("SinhVien", data, "MaSV", ma_sv)
    if query:
        with db.cursor() as cursor: cursor.execute(query, params); db.commit()
    return get_sinh_vien_by_id(db, ma_sv)


def delete_sinh_vien(db, ma_sv: str): return _delete_entity_by_id(db, "SinhVien", "MaSV", ma_sv)


# ----- Quản lý Giảng Viên -----
def create_giang_vien(db, data: dict): return _create_entity(db, "GiangVien", data)


def get_all_giang_vien(db): return _get_all_entities(db, "GiangVien")


def get_giang_vien_by_id(db, ma_gv: str): return _get_entity_by_id(db, "GiangVien", "MaGV", ma_gv)


def update_giang_vien(db, ma_gv: str, data: dict):
    query, params = _build_update_query("GiangVien", data, "MaGV", ma_gv)
    if query:
        with db.cursor() as cursor: cursor.execute(query, params); db.commit()
    return get_giang_vien_by_id(db, ma_gv)


def delete_giang_vien(db, ma_gv: str): return _delete_entity_by_id(db, "GiangVien", "MaGV", ma_gv)


# ----- Quản lý Môn Học -----
def create_mon_hoc(db, data: dict): return _create_entity(db, "MonHoc", data)


def get_all_mon_hoc(db): return _get_all_entities(db, "MonHoc")


def get_mon_hoc_by_id(db, ma_mh: str): return _get_entity_by_id(db, "MonHoc", "MaMH", ma_mh)


def update_mon_hoc(db, ma_mh: str, data: dict):
    query, params = _build_update_query("MonHoc", data, "MaMH", ma_mh)
    if query:
        with db.cursor() as cursor: cursor.execute(query, params); db.commit()
    return get_mon_hoc_by_id(db, ma_mh)


def delete_mon_hoc(db, ma_mh: str): return _delete_entity_by_id(db, "MonHoc", "MaMH", ma_mh)


# ----- Quản lý Kỳ Học -----
def create_ky_hoc(db, data: dict): return _create_entity(db, "KyHoc", data)


def get_all_ky_hoc(db): return _get_all_entities(db, "KyHoc")


def update_ky_hoc(db, ma_ky: str, data: dict):
    query, params = _build_update_query("KyHoc", data, "MaKy", ma_ky)
    if query:
        with db.cursor() as cursor: cursor.execute(query, params); db.commit()
    return _get_entity_by_id(db, "KyHoc", "MaKy", ma_ky)


def delete_ky_hoc(db, ma_ky: str): return _delete_entity_by_id(db, "KyHoc", "MaKy", ma_ky)


# ----- Quản lý Lớp Tín Chỉ -----
def create_lop_tc(db, data: dict): return _create_entity(db, "LopTC", data)


def get_all_lop_tc(db):
    with db.cursor() as cursor:
        # Join để lấy thông tin chi tiết hơn
        sql = """SELECT ltc.MaLopTC, mh.TenMH, gv.HoVaTen, kh.TenKy 
                 FROM LopTC ltc 
                 JOIN MonHoc mh ON ltc.MaMH = mh.MaMH
                 JOIN GiangVien gv ON ltc.MaGV = gv.MaGV
                 JOIN KyHoc kh ON ltc.MaKy = kh.MaKy"""
        cursor.execute(sql)
        return cursor.fetchall()


def update_lop_tc(db, ma_ltc: str, data: dict):
    query, params = _build_update_query("LopTC", data, "MaLopTC", ma_ltc)
    if query:
        with db.cursor() as cursor: cursor.execute(query, params); db.commit()
    return _get_entity_by_id(db, "LopTC", "MaLopTC", ma_ltc)


def delete_lop_tc(db, ma_ltc: str): return _delete_entity_by_id(db, "LopTC", "MaLopTC", ma_ltc)


# ----- Quản lý Tài Khoản Người Dùng -----
def create_user_account(db, data: dict):
    """Tạo tài khoản mới với mật khẩu đã được hash."""
    hashed_password = get_password_hash(data['Password'])
    with db.cursor() as cursor:
        sql = "INSERT INTO taikhoan (Username, HashedPassword, Role, UserID) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (data['Username'], hashed_password, data['Role'], data['UserID']))
        db.commit()
    return get_user_from_db(db, data['Username'])


def get_all_accounts(db): return _get_all_entities(db, "taikhoan")


def update_user_account(db, username: str, data: dict):
    # Nếu có mật khẩu mới, hash nó trước khi cập nhật
    if data.get("Password"):
        data["HashedPassword"] = get_password_hash(data.pop("Password"))

    query, params = _build_update_query("taikhoan", data, "Username", username)
    if query:
        with db.cursor() as cursor: cursor.execute(query, params); db.commit()
    return get_user_from_db(db, username)


def delete_user_account(db, username: str): return _delete_entity_by_id(db, "taikhoan", "Username", username)


# ----- Chức năng Báo cáo -----
def get_grades_for_report(db, ma_ltc: str):
    """Lấy toàn bộ bảng điểm của một lớp tín chỉ để xuất báo cáo."""
    with db.cursor() as cursor:
        query = """
            SELECT 
                sv.MaSV, sv.HoTen, sv.Email,
                bd.DiemChuyenCan, bd.DiemGiuaKy, bd.DiemCuoiKy, bd.DiemThucHanh,
                bd.DiemTongKetHe10, bd.DiemChu, bd.TrangThaiQuaMon
            FROM BangDiem bd
            JOIN SinhVien sv ON bd.MaSV = sv.MaSV
            WHERE bd.MaLopTC = %s
            ORDER BY sv.MaSV
        """
        cursor.execute(query, (ma_ltc,))
        return cursor.fetchall()

