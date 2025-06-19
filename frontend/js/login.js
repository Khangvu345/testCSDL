const API_BASE_URL = 'http://127.0.0.1:8000';

document.getElementById('loginForm').addEventListener('submit', async (event) => {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const errorMessage = document.getElementById('error-message');

    // Dữ liệu form cần được gửi dưới dạng x-www-form-urlencoded
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    try {
        const response = await fetch(`${API_BASE_URL}/auth/token`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: formData,
        });

        const data = await response.json();

        if (!response.ok) {
            errorMessage.textContent = data.detail || 'Đăng nhập thất bại.';
            return;
        }

        // Lưu token vào localStorage
        localStorage.setItem('accessToken', data.access_token);

        // Decode token để lấy role (cách đơn giản, không an toàn cho production)
        const payload = JSON.parse(atob(data.access_token.split('.')[1]));
        const role = payload.role;

        // Chuyển hướng dựa trên role
        switch (role) {
            case 'student':
                window.location.href = 'student/dashboard.html';
                break;
            case 'teacher':
                window.location.href = 'teacher/dashboard.html';
                break;
            case 'manager':
                // window.location.href = 'manager/dashboard.html';
                alert('Chức năng Quản lý chưa được triển khai ở Frontend.');
                break;
            default:
                errorMessage.textContent = 'Vai trò không xác định.';
        }

    } catch (error) {
        console.error('Lỗi đăng nhập:', error);
        errorMessage.textContent = 'Đã xảy ra lỗi kết nối. Vui lòng thử lại.';
    }
});
