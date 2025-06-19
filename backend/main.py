# backend/main.py
# Entry point của ứng dụng FastAPI

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import các router từ các module khác
from routers import auth, sinhvien, giangvien, manager

# Khởi tạo ứng dụng FastAPI
app = FastAPI(
    title="Student Grade Management API",
    description="API để quản lý điểm sinh viên.",
    version="1.0.0",
)

# Cấu hình CORS (Cross-Origin Resource Sharing)
# Thay đổi quan trọng ở đây!
# Sử dụng ["*"] để cho phép TẤT CẢ các nguồn kết nối.
# Đây là cách thiết lập tiện lợi cho môi trường phát triển (development).
# Khi triển khai lên server thật (production), bạn nên liệt kê cụ thể các domain được phép.
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Cho phép tất cả các method (GET, POST, etc.)
    allow_headers=["*"], # Cho phép tất cả các header
)

# Thêm các router vào ứng dụng
app.include_router(auth.router)
app.include_router(sinhvien.router)
app.include_router(giangvien.router)
app.include_router(manager.router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to Student Grade Management API!"}