# backend/routers/manager.py
from fastapi import APIRouter, Depends
from schemas.token import TokenData # Import TokenData
from routers.dependencies import require_role # Sửa import

router = APIRouter(prefix="/api/manager", tags=["Manager"])
manager_dependency = Depends(require_role("manager"))

@router.get("/dashboard")
def manager_dashboard(current_user: TokenData = manager_dependency):
    """API mẫu cho trang quản lý."""
    return {"message": f"Welcome Manager {current_user.username}!"}
