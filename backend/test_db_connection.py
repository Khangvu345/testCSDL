# backend/test_db_connection.py
# Tệp này đã được cập nhật để sử dụng thư viện PyMySQL.

import pymysql.cursors

# Chúng ta import trực tiếp config để kiểm tra
try:
    from config import DB_CONFIG

    print("✓ Đã tải cấu hình DB thành công.")
    print(f"  - Host: {DB_CONFIG.get('host')}")
    print(f"  - User: {DB_CONFIG.get('user')}")
    print(f"  - Database: {DB_CONFIG.get('database')}")
    # Không in mật khẩu để bảo mật
except ImportError:
    print("✗ LỖI: Không tìm thấy tệp config.py hoặc biến DB_CONFIG.")
    exit()

connection = None  # Khởi tạo biến connection
try:
    print("\nĐang thử kết nối đến MySQL bằng thư viện PyMySQL...")

    # Cấu hình kết nối cho PyMySQL
    pymysql_config = {
        'host': DB_CONFIG.get('host'),
        'user': DB_CONFIG.get('user'),
        'password': DB_CONFIG.get('password'),
        'database': DB_CONFIG.get('database'),
        'cursorclass': pymysql.cursors.DictCursor,  # Giống dictionary=True
        'connect_timeout': 10
    }

    # Thử kết nối
    connection = pymysql.connect(**pymysql_config)

    print("✓✓✓ KẾT NỐI THÀNH CÔNG!")

    with connection.cursor() as cursor:
        # Lấy phiên bản MySQL
        cursor.execute("SELECT version()")
        version = cursor.fetchone()
        print(f"    -> Phiên bản MySQL Server: {version['version()']}")

        # Lấy database hiện tại
        cursor.execute("SELECT DATABASE();")
        db_name = cursor.fetchone()
        print(f"    -> Bạn đang kết nối đến database: {db_name['DATABASE()']}")

        print("\n    -> Thử truy vấn bảng 'taikhoan'...")
        cursor.execute("SELECT * FROM taikhoan LIMIT 1;")
        record = cursor.fetchone()
        print(f"    -> Lấy được dữ liệu mẫu: {record}")
        print("\n==> Mọi thứ đều hoạt động hoàn hảo!")

except Exception as e:
    print("\n✗✗✗ KẾT NỐI THẤT BẠI!")
    print(f"    Chi tiết lỗi từ PyMySQL: {e}")

finally:
    # Đảm bảo connection luôn được đóng
    if connection:
        connection.close()
        print("\nĐã đóng kết nối.")
