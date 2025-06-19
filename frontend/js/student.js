const API_BASE_URL = 'http://127.0.0.1:8000';
const token = localStorage.getItem('accessToken');

function logout() {
    localStorage.removeItem('accessToken');
    window.location.href = '../index.html';
}

async function fetchWithAuth(url, options = {}) {
    const headers = {
        ...options.headers,
        'Authorization': `Bearer ${token}`
    };

    const response = await fetch(url, { ...options, headers });

    if (response.status === 401) {
        // Token hết hạn hoặc không hợp lệ
        logout();
    }

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Có lỗi xảy ra');
    }

    return response.json();
}


async function loadGrades() {
    const tableBody = document.getElementById('gradesTableBody');
    try {
        const grades = await fetchWithAuth(`${API_BASE_URL}/api/sinhvien/me/grades`);
        if (grades.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="8" style="text-align:center;">Chưa có dữ liệu điểm.</td></tr>';
            return;
        }

        tableBody.innerHTML = ''; // Xóa nội dung cũ
        grades.forEach(grade => {
            const row = `
                <tr>
                    <td>${grade.MaMH}</td>
                    <td>${grade.TenMH}</td>
                    <td>${grade.SoTinChi}</td>
                    <td>${grade.DiemCC ?? 'N/A'}</td>
                    <td>${grade.DiemGK ?? 'N/A'}</td>
                    <td>${grade.DiemCK ?? 'N/A'}</td>
                    <td>${grade.DiemHe10 ?? 'N/A'}</td>
                    <td>${grade.DiemChu ?? 'N/A'}</td>
                </tr>
            `;
            tableBody.innerHTML += row;
        });
    } catch (error) {
        console.error('Lỗi tải điểm:', error);
        tableBody.innerHTML = `<tr><td colspan="8" style="text-align:center;">${error.message}</td></tr>`;
    }
}

async function loadProgress() {
    const progressDiv = document.getElementById('progress-info');
    try {
        const progress = await fetchWithAuth(`${API_BASE_URL}/api/sinhvien/me/progress`);
        progressDiv.innerHTML = `
            <p><strong>Số tín chỉ đã đạt:</strong> ${progress.tong_tin_chi_dat} / ${progress.tong_tin_chi_chuong_trinh}</p>
            <p><strong>Hoàn thành:</strong> ${progress.phan_tram_hoan_thanh}%</p>
        `;
    } catch (error) {
        console.error('Lỗi tải tiến độ:', error);
        progressDiv.innerHTML = `<p>${error.message}</p>`;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    if (!token) {
        logout();
        return;
    }

    const payload = JSON.parse(atob(token.split('.')[1]));
    document.getElementById('welcomeMessage').textContent = `Chào mừng, ${payload.sub} (SV: ${payload.user_id})`;


    document.getElementById('logoutBtn').addEventListener('click', logout);

    loadGrades();
    loadProgress();
});