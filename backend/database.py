# backend/database.py
# Quản lý kết nối đến database (ĐÃ CẬP NHẬT ĐỂ DÙNG PyMySQL)

import pymysql.cursors
from contextlib import contextmanager
from config import DB_CONFIG


# PyMySQL không có connection pool tích hợp sẵn như mysql-connector.
# Đối với ứng dụng này, chúng ta sẽ tạo một kết nối mới cho mỗi request,
# và FastAPI quản lý dependency này rất hiệu quả.

@contextmanager
def get_db_connection():
    """
    Cung cấp một connection PyMySQL.
    Sử dụng context manager để đảm bảo connection luôn được đóng.
    """

    # Cấu hình kết nối cho PyMySQL
    pymysql_config = {
        'host': DB_CONFIG.get('host'),
        'user': DB_CONFIG.get('user'),
        'password': DB_CONFIG.get('password'),
        'database': DB_CONFIG.get('database'),
        'cursorclass': pymysql.cursors.DictCursor,  # Tự động trả về kết quả dạng dictionary
        'connect_timeout': 10
    }

    connection = None
    try:
        # Tạo kết nối mới
        connection = pymysql.connect(**pymysql_config)
        yield connection
    except Exception as e:
        print(f"Lỗi kết nối CSDL: {e}")
        raise
    finally:
        if connection:
            connection.close()