# backend/crud/user_crud.py
from utils.security import verify_password

def get_user_from_db(db_connection, username: str):
    """Lấy thông tin tài khoản từ DB bằng username."""
    # Với PyMySQL đã cấu hình DictCursor, không cần tham số dictionary=True
    cursor = db_connection.cursor()
    query = "SELECT Username, HashedPassword, Role, UserID FROM taikhoan WHERE Username = %s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()
    cursor.close()
    return user

def authenticate_user(db_connection, username: str, password: str):
    """Xác thực người dùng."""
    user = get_user_from_db(db_connection, username)
    if not user:
        return None
    if not verify_password(password, user["HashedPassword"]):
        return None
    return user
