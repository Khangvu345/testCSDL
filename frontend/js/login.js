const API_BASE_URL = 'http://127.0.0.1:8000';
document.getElementById('loginForm').addEventListener('submit', async(event) => {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const errorMessage = document.getElementById('error-message');
    errorMessage.textContent = '';
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);
    try {
        const response = await fetch(`${API_BASE_URL}/auth/token`, { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: formData, });
        const data = await response.json();
        if (!response.ok) { errorMessage.textContent = data.detail || 'Đăng nhập thất bại.'; return; }
        localStorage.setItem('accessToken', data.access_token);
        const payload = JSON.parse(atob(data.access_token.split('.')[1]));
        switch (payload.role) {
            case 'student': window.location.replace('student/dashboard.html'); break;
            case 'teacher': window.location.replace('teacher/dashboard.html'); break;
            case 'manager': alert('Chức năng Quản lý chưa có giao diện.'); break;
            default: errorMessage.textContent = 'Vai trò không xác định.';
        }
    } catch (error) {
        console.error('Lỗi đăng nhập:', error);
        errorMessage.textContent = 'Lỗi kết nối. Vui lòng đảm bảo server backend đang chạy.';
    }
});