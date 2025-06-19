# backend/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from schemas.token import Token
from crud import user_crud
from utils import jwt_handler
from routers.dependencies import get_db  # Sửa import

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/token", response_model=Token)
def login_for_access_token(db=Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = user_crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_data = {"sub": user["Username"], "role": user["Role"], "user_id": user["UserID"]}
    access_token = jwt_handler.create_access_token(data=token_data)

    return {"access_token": access_token, "token_type": "bearer"}
