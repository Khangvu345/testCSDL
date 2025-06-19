from utils.security import verify_password

def get_user_from_db(db_connection, username: str):
    with db_connection.cursor() as cursor:
        query = "SELECT Username, HashedPassword, Role, UserID FROM taikhoan WHERE Username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()
    return user

def authenticate_user(db_connection, username: str, password: str):
    user = get_user_from_db(db_connection, username)
    if not user:
        return None
    if not verify_password(password, user["HashedPassword"]):
        return None
    return user