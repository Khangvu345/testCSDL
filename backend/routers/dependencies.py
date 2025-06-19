# backend/routers/dependencies.py
# Tập trung các dependency cho việc xác thực và phân quyền
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from database import get_db_connection
from utils import jwt_handler
from schemas.token import TokenData
from crud import user_crud

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_db():
    """Dependency để lấy kết nối DB."""
    with get_db_connection() as db:
        yield db


def get_current_user(db=Depends(get_db), token: str = Depends(oauth2_scheme)) -> TokenData:
    """Dependency để lấy thông tin user từ token."""
    payload = jwt_handler.verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    username = payload.get("sub")
    role = payload.get("role")
    user_id = payload.get("user_id")

    if username is None or role is None or user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = user_crud.get_user_from_db(db, username=username)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return TokenData(username=username, role=role, user_id=user_id)


def require_role(required_role: str):
    """Factory dependency để yêu cầu một role cụ thể."""

    def role_checker(current_user: TokenData = Depends(get_current_user)) -> TokenData:
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operation not permitted. Requires '{required_role}' role."
            )
        return current_user

    return role_checker
