const API_BASE_URL = 'http://127.0.0.1:8000';
const token = localStorage.getItem('accessToken');
let currentLtcId = null;

function logout() {
    localStorage.removeItem('accessToken');
    window.location.href = '../index.html';
}

async function fetchWithAuth(url, options = {}) {
    if (!token) { logout(); return Promise.reject("No token"); }
    const headers = { 'Content-Type': 'application/json', ...options.headers, 'Authorization': `Bearer ${token}` };
    const response = await fetch(url, { ...options, headers });
    if (response.status === 401) { logout(); throw new Error("Phiên đăng nhập đã hết hạn."); }
    if (response.status === 204 || (response.status === 200 && options.method === 'DELETE')) { return { status: 'success' }; }
    const responseData = await response.json().catch(() => ({}));
    if (!response.ok) { throw new Error(responseData.detail || 'Có lỗi xảy ra'); }
    return responseData;
}

async function loadTeacherClasses() {
    const classesDiv = document.getElementById('classes-list');
    try {
        const classes = await fetchWithAuth(`${API_BASE_URL}/api/giangvien/me/lop-tin-chi`);
        if (classes.length === 0) {
            classesDiv.innerHTML = '<p>Bạn chưa được phân công lớp nào.</p>';
            return;
        }
        classesDiv.innerHTML = classes.map(cls => `
            <div class="class-item" data-ltcid="${cls.MaLopTC}" data-classname="${cls.TenMH} - ${cls.TenKy}">
                ${cls.TenMH} (${cls.TenKy})
            </div>`).join('');
        classesDiv.querySelectorAll('.class-item').forEach(item => {
            item.addEventListener('click', (e) => {
                document.querySelectorAll('.class-item').forEach(i => i.classList.remove('active'));
                e.currentTarget.classList.add('active');
                currentLtcId = e.currentTarget.dataset.ltcid;
                document.getElementById('current-class-title').textContent = `Lớp: ${e.currentTarget.dataset.classname}`;
                loadStudentsInClass(currentLtcId);
            });
        });
    } catch (error) {
        classesDiv.innerHTML = `<p style="color:red;">Lỗi tải danh sách lớp: ${error.message}</p>`;
    }
}

async function loadStudentsInClass(maLtc) {
    const studentsDiv = document.getElementById('students-list');
    studentsDiv.innerHTML = '<p>Đang tải danh sách sinh viên...</p>';
    try {
        const students = await fetchWithAuth(`${API_BASE_URL}/api/giangvien/lop-tin-chi/${maLtc}/danh-sach-sinh-vien`);
        let tableHTML = `
            <table><thead><tr>
                <th>Mã SV</th><th>Họ Tên</th><th>Điểm CC</th><th>Điểm GK</th><th>Điểm CK</th><th>Điểm TH</th><th>Tổng kết</th><th>Hành động</th>
            </tr></thead><tbody>`;
        students.forEach(sv => {
            tableHTML += `
                <tr data-masv="${sv.MaSV}">
                    <td>${sv.MaSV}</td><td>${sv.HoTen}</td>
                    <td><input type="number" class="grade-input" id="cc-${sv.MaSV}" value="${sv.DiemChuyenCan ?? ''}"></td>
                    <td><input type="number" class="grade-input" id="gk-${sv.MaSV}" value="${sv.DiemGiuaKy ?? ''}"></td>
                    <td><input type="number" class="grade-input" id="ck-${sv.MaSV}" value="${sv.DiemCuoiKy ?? ''}"></td>
                    <td><input type="number" class="grade-input" id="th-${sv.MaSV}" value="${sv.DiemThucHanh ?? ''}"></td>
                    <td><b>${sv.DiemTongKetHe10 ?? 'N/A'}</b></td>
                    <td class="action-buttons">
                        <button class="save-btn" data-masv="${sv.MaSV}">Lưu</button>
                        <button class="delete-btn" data-masv="${sv.MaSV}">Xóa</button>
                    </td>
                </tr>`;
        });
        studentsDiv.innerHTML = tableHTML + '</tbody></table>';

        document.querySelectorAll('.save-btn').forEach(b => b.addEventListener('click', handleSaveGrade));
        document.querySelectorAll('.delete-btn').forEach(b => b.addEventListener('click', handleDeleteGrade));
    } catch (error) {
        studentsDiv.innerHTML = `<p style="color:red;">Lỗi tải danh sách sinh viên: ${error.message}</p>`;
    }
}

async function handleSaveGrade(event) {
    const maSV = event.target.dataset.masv;
    const getValue = (id) => {
        const val = document.getElementById(id).value;
        return val === '' ? null : parseFloat(val);
    };

    const gradeData = {
        MaSV: maSV,
        DiemChuyenCan: getValue(`cc-${maSV}`),
        DiemGiuaKy: getValue(`gk-${maSV}`),
        DiemCuoiKy: getValue(`ck-${maSV}`),
        DiemThucHanh: getValue(`th-${maSV}`)
    };

    try {
        await fetchWithAuth(`${API_BASE_URL}/api/giangvien/lop-tin-chi/${currentLtcId}/nhap-diem`, {
            method: 'POST',
            body: JSON.stringify(gradeData)
        });
        alert(`Đã cập nhật điểm cho sinh viên ${maSV}.`);
        loadStudentsInClass(currentLtcId);
    } catch (error) {
        alert(`Lỗi lưu điểm: ${error.message}`);
    }
}

async function handleDeleteGrade(event) {
    const maSV = event.target.dataset.masv;
    if (confirm(`Bạn có chắc chắn muốn xóa toàn bộ điểm của sinh viên ${maSV} khỏi lớp này?`)) {
        try {
            await fetchWithAuth(`${API_BASE_URL}/api/giangvien/lop-tin-chi/${currentLtcId}/xoa-diem/${maSV}`, {
                method: 'DELETE'
            });
            alert(`Đã xóa điểm của sinh viên ${maSV}.`);
            loadStudentsInClass(currentLtcId);
        } catch (error) {
            alert(`Lỗi xóa điểm: ${error.message}`);
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    if (!token) { logout(); return; }
    document.getElementById('logoutBtn').addEventListener('click', logout);
    loadTeacherClasses();
});
