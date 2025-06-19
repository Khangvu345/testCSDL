# Chạy tệp này để tạo một chuỗi mật khẩu đã được mã hóa bằng bcrypt.
from utils.security import get_password_hash
import sys

# Lấy mật khẩu từ dòng lệnh, nếu không có thì dùng '123' làm mặc định
password_to_hash = "123"
if len(sys.argv) > 1:
    password_to_hash = sys.argv[1]

# Mã hóa mật khẩu
hashed_password = get_password_hash(password_to_hash)

print("="*50)
print(f"Mật khẩu thuần túy: '{password_to_hash}'")
print(f"Mật khẩu đã mã hóa (Hashed Password):")
print(f"==> {hashed_password}")
print("="*50)
print("\n=> HÃY SAO CHÉP CHUỖI MÃ HÓA Ở TRÊN VÀ CẬP NHẬT VÀO DATABASE CỦA BẠN.")

