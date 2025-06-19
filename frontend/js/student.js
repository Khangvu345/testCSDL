const API_BASE_URL = 'http://127.0.0.1:8000';
const token = localStorage.getItem('accessToken');
let allGradesData = []; // Biến toàn cục để lưu trữ dữ liệu điểm chi tiết

function logout() {
    localStorage.removeItem('accessToken');
    window.location.href = '../index.html';
}

async function fetchWithAuth(url, options = {}) {
    if (!token) {
        logout();
        return Promise.reject("No token"); // Ngừng thực thi nếu không có token
    }
    const headers = { 'Content-Type': 'application/json', ...options.headers, 'Authorization': `Bearer ${token}` };
    const response = await fetch(url, { ...options, headers });
    if (response.status === 401) {
        logout();
        throw new Error("Phiên đăng nhập đã hết hạn.");
    }
    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Lỗi không xác định từ server' }));
        throw new Error(errorData.detail);
    }
    return response.json();
}

async function loadProgress() {
    const progressDiv = document.getElementById('progress-info');
    try {
        const progress = await fetchWithAuth(`${API_BASE_URL}/api/sinhvien/me/tien-do-hoc-tap`);
        progressDiv.innerHTML = `
            <p><strong>Số tín chỉ đã đạt:</strong> ${progress.tong_tin_chi_dat} / ${progress.tong_tin_chi_chuong_trinh}</p>
            <p><strong>Hoàn thành:</strong> ${progress.phan_tram_hoan_thanh}%</p>`;
    } catch (error) {
        console.error("Lỗi tải tiến độ:", error);
        progressDiv.innerHTML = `<p style="color:red;">Lỗi tải tiến độ: ${error.message}</p>`;
    }
}

async function loadSemesters() {
    const select = document.getElementById('semester-select');
    try {
        const semesters = await fetchWithAuth(`${API_BASE_URL}/api/manager/ky-hoc`); // API của Admin để lấy danh sách
        if (semesters.length > 0) {
            select.innerHTML = semesters.map(s => `<option value="${s.MaKy}">${s.TenKy} - ${s.NamHoc}</option>`).join('');
        } else {
            select.innerHTML = '<option value="">Không có dữ liệu</option>';
        }
    } catch (error) {
        console.error("Lỗi tải kỳ học:", error);
        select.innerHTML = `<option value="">Lỗi tải kỳ học</option>`;
    }
}

async function viewSemesterSummary() {
    const ma_ky = document.getElementById('semester-select').value;
    const summaryDiv = document.getElementById('semester-summary');
    if (!ma_ky) {
        alert('Vui lòng chọn một kỳ học.');
        return;
    }

    summaryDiv.innerHTML = `<p>Đang tải dữ liệu điểm kỳ ${ma_ky}...</p>`;
    summaryDiv.style.display = 'block';

    try {
        const summary = await fetchWithAuth(`${API_BASE_URL}/api/sinhvien/me/diem-tong-ket/${ma_ky}`);
        summaryDiv.innerHTML = `
            <h4>Kết quả học tập kỳ: ${ma_ky}</h4>
            <p><strong>Điểm trung bình (Hệ 10):</strong> ${summary.DiemTBKyHe10}</p>
            <p><strong>Điểm trung bình (Hệ 4):</strong> ${summary.DiemTBKyHe4}</p>
            <p><strong>Số tín chỉ đạt trong kỳ:</strong> ${summary.SoTCDatKy}</p>
            <p><strong>Xếp loại học lực:</strong> ${summary.XepLoaiHocLucKy}</p>`;
    } catch (error) {
        console.error("Lỗi xem điểm tổng kết:", error);
        summaryDiv.innerHTML = `<p style="color:red;">Lỗi xem điểm tổng kết: ${error.message}</p>`;
    }
}

async function loadAndPopulateCourses() {
    const select = document.getElementById('course-select');
    try {
        allGradesData = await fetchWithAuth(`${API_BASE_URL}/api/sinhvien/me/diem-chi-tiet`);
        if (allGradesData.length > 0) {
            select.innerHTML = '<option value="">-- Vui lòng chọn một lớp --</option>'; // Reset
            select.innerHTML += allGradesData.map(grade =>
                `<option value="${grade.MaLopTC}">${grade.TenMH} (${grade.MaLopTC})</option>`
            ).join('');
        } else {
            select.innerHTML = '<option value="">Chưa đăng ký môn nào</option>';
        }
    } catch (error) {
        console.error("Lỗi tải danh sách môn học:", error);
        select.innerHTML = `<option value="">Lỗi tải môn học</option>`;
    }
}

function displayCourseDetails() {
    const ma_ltc = document.getElementById('course-select').value;
    const detailsDiv = document.getElementById('course-details');

    if (!ma_ltc) {
        detailsDiv.style.display = 'none';
        return;
    }

    const grade = allGradesData.find(g => g.MaLopTC === ma_ltc);
    if (!grade) {
        detailsDiv.innerHTML = '<p>Không tìm thấy dữ liệu điểm cho môn này.</p>';
        detailsDiv.style.display = 'block';
        return;
    }

    detailsDiv.innerHTML = `
        <h4>Chi tiết điểm: ${grade.TenMH} (${grade.MaLopTC})</h4>
        <table id="course-details-table">
            <tbody>
                <tr><th>Điểm chuyên cần:</th><td>${grade.DiemChuyenCan ?? 'Chưa có'}</td></tr>
                <tr><th>Điểm giữa kỳ:</th><td>${grade.DiemGiuaKy ?? 'Chưa có'}</td></tr>
                <tr><th>Điểm cuối kỳ:</th><td>${grade.DiemCuoiKy ?? 'Chưa có'}</td></tr>
                <tr><th>Điểm thực hành:</th><td>${grade.DiemThucHanh ?? 'Chưa có'}</td></tr>
                <tr style="font-weight: bold;"><th>Điểm tổng kết (Hệ 10):</th><td>${grade.DiemTongKetHe10 ?? 'N/A'}</td></tr>
                <tr><th>Điểm chữ:</th><td>${grade.DiemChu ?? 'N/A'}</td></tr>
                <tr><th>Trạng thái:</th><td>${grade.TrangThaiQuaMon ?? 'N/A'}</td></tr>
            </tbody>
        </table>`;
    detailsDiv.style.display = 'block';
}

document.addEventListener('DOMContentLoaded', () => {
    if (!token) { logout(); return; }

    document.getElementById('logoutBtn').addEventListener('click', logout);
    document.getElementById('viewSummaryBtn').addEventListener('click', viewSemesterSummary);
    document.getElementById('course-select').addEventListener('change', displayCourseDetails);

    loadProgress();
    loadSemesters();
    loadAndPopulateCourses();
});