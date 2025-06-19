const API_BASE_URL = 'http://127.0.0.1:8000';
const token = localStorage.getItem('accessToken');
let currentLtcId = null;

function logout() {
    localStorage.removeItem('accessToken');
    window.location.href = '../index.html';
}

async function fetchWithAuth(url, options = {}) {
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers,
        'Authorization': `Bearer ${token}`
    };

    const response = await fetch(url, { ...options, headers });

    if (response.status === 401) {
        logout();
    }

    const responseData = await response.json();
    if (!response.ok) {
        throw new Error(responseData.detail || 'Có lỗi xảy ra');
    }

    return responseData;
}

async function loadTeacherClasses() {
    const classesDiv = document.getElementById('classes-list');
    try {
        const classes = await fetchWithAuth(`${API_BASE_URL}/api/giangvien/me/classes`);
        if (classes.length === 0) {
            classesDiv.innerHTML = '<p>Bạn chưa được phân công lớp nào.</p>';
            return;
        }

        classesDiv.innerHTML = ''; // Xóa nội dung cũ
        classes.forEach(cls => {
            const classElement = document.createElement('div');
            classElement.className = 'class-item';
            classElement.textContent = `${cls.TenMH} - Nhóm ${cls.Nhom} (${cls.TenHK})`;
            classElement.dataset.ltcid = cls.MaLTC;
            classElement.addEventListener('click', () => {
                document.querySelectorAll('.class-item').forEach(item => item.classList.remove('active'));
                classElement.classList.add('active');
                currentLtcId = cls.MaLTC;
                document.getElementById('current-class-title').textContent = `Lớp: ${cls.TenMH} - Nhóm ${cls.Nhom}`;
                loadStudentsInClass(cls.MaLTC);
            });
            classesDiv.appendChild(classElement);
        });
    } catch (error) {
        console.error('Lỗi tải danh sách lớp:', error);
        classesDiv.innerHTML = `<p style="color:red;">${error.message}</p>`;
    }
}

async function loadStudentsInClass(maLtc) {
    const studentsDiv = document.getElementById('students-list');
    studentsDiv.innerHTML = '<p>Đang tải danh sách sinh viên...</p>';
    try {
        const students = await fetchWithAuth(`${API_BASE_URL}/api/giangvien/classes/${maLtc}/students`);

        let tableHTML = `
            <table>
                <thead>
                    <tr>
                        <th>Mã SV</th>
                        <th>Họ Tên</th>
                        <th>Điểm CC</th>
                        <th>Điểm GK</th>
                        <th>Điểm CK</th>
                        <th>Hành động</th>
                    </tr>
                </thead>
                <tbody>
        `;
        students.forEach(sv => {
            tableHTML += `
                <tr data-masv="${sv.MaSV}">
                    <td>${sv.MaSV}</td>
                    <td>${sv.HoTen}</td>
                    <td><input type="number" class="grade-input" id="cc-${sv.MaSV}" step="0.1" min="0" max="10" value="${sv.DiemCC ?? ''}"></td>
                    <td><input type="number" class="grade-input" id="gk-${sv.MaSV}" step="0.1" min="0" max="10" value="${sv.DiemGK ?? ''}"></td>
                    <td><input type="number" class="grade-input" id="ck-${sv.MaSV}" step="0.1" min="0" max="10" value="${sv.DiemCK ?? ''}"></td>
                    <td><button class="save-grade-btn" data-masv="${sv.MaSV}">Lưu</button></td>
                </tr>
            `;
        });
        tableHTML += '</tbody></table>';
        studentsDiv.innerHTML = tableHTML;

        // Add event listeners to save buttons
        document.querySelectorAll('.save-grade-btn').forEach(button => {
            button.addEventListener('click', handleSaveGrade);
        });

    } catch (error) {
        console.error('Lỗi tải danh sách sinh viên:', error);
        studentsDiv.innerHTML = `<p style="color:red;">${error.message}</p>`;
    }
}

async function handleSaveGrade(event) {
    const maSV = event.target.dataset.masv;
    const diemCC = document.getElementById(`cc-${maSV}`).value;
    const diemGK = document.getElementById(`gk-${maSV}`).value;
    const diemCK = document.getElementById(`ck-${maSV}`).value;

    const gradeData = {
        MaSV: maSV,
        DiemCC: diemCC === '' ? null : parseFloat(diemCC),
        DiemGK: diemGK === '' ? null : parseFloat(diemGK),
        DiemCK: diemCK === '' ? null : parseFloat(diemCK)
    };

    try {
        const result = await fetchWithAuth(`${API_BASE_URL}/api/giangvien/classes/${currentLtcId}/grades`, {
            method: 'POST',
            body: JSON.stringify(gradeData)
        });
        alert(`Đã cập nhật điểm cho sinh viên ${maSV} thành công!`);
        // Optional: reload the student list to show calculated score
        loadStudentsInClass(currentLtcId);

    } catch (error) {
        console.error('Lỗi lưu điểm:', error);
        alert(`Lỗi: ${error.message}`);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    if (!token) {
        logout();
        return;
    }

    const payload = JSON.parse(atob(token.split('.')[1]));
    document.getElementById('welcomeMessage').textContent = `Chào mừng, ${payload.sub} (GV: ${payload.user_id})`;

    document.getElementById('logoutBtn').addEventListener('click', logout);

    loadTeacherClasses();
});