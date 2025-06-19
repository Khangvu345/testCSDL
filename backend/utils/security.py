# backend/utils/security.py
# Các hàm tiện ích liên quan đến bảo mật (hash mật khẩu)

from passlib.context import CryptContext

# Sử dụng bcrypt, một thuật toán hash mật khẩu mạnh mẽ và phổ biến
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Xác minh mật khẩu thuần túy với mật khẩu đã được hash.

    Args:
        plain_password: Mật khẩu người dùng nhập vào.
        hashed_password: Mật khẩu đã được hash lưu trong DB.

    Returns:
        True nếu mật khẩu khớp, False nếu không.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hash một mật khẩu thuần túy.

    Args:
        password: Mật khẩu cần hash.

    Returns:
        Chuỗi mật khẩu đã được hash.
    """
    return pwd_context.hash(password)