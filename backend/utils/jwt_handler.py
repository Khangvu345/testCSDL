# backend/utils/jwt_handler.py
# Các hàm tiện ích để tạo và xác thực JWT (JSON Web Token)

from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from jose import JWTError, jwt
from fastapi import HTTPException, status

# TODO: Thay đổi secret key và lưu trữ an toàn, ví dụ trong biến môi trường
SECRET_KEY = "a_very_secret_key_for_jwt" # Thay bằng một chuỗi ngẫu nhiên, phức tạp
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 # Token hết hạn sau 24 giờ

def create_access_token(data: Dict[str, Any]) -> str:
    """
    Tạo một JWT access token mới.

    Args:
        data: Dữ liệu cần đưa vào payload của token (ví dụ: username, role).

    Returns:
        Một chuỗi JWT.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Giải mã và xác thực một JWT.

    Args:
        token: Chuỗi JWT cần xác thực.

    Returns:
        Payload của token nếu hợp lệ, None nếu không.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise credentials_exception