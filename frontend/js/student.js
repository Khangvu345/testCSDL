const API_BASE_URL_STUDENT = 'http://127.0.0.1:8000';
const token_student = localStorage.getItem('accessToken');
let allGradesData_student = [];

function logout_student() { localStorage.removeItem('accessToken'); window.location.replace('../index.html'); }

async function fetchWithAuth_student(url, options = {}) {
    if (!token_student) { logout_student(); return Promise.reject("No token"); }
    const headers = { 'Content-Type': 'application/json', ...options.headers, 'Authorization': `Bearer ${token_student}` };
    const response = await fetch(url, { ...options, headers });
    if (response.status === 401) { logout_student(); throw new Error("Phiên đăng nhập đã hết hạn."); }
    if (!response.ok) { const errorData = await response.json().catch(() => ({ detail: 'Lỗi không xác định' })); throw new Error(errorData.detail); }
    return response.json();
}
async function loadProgress() {
    try {
        const progress = await fetchWithAuth_student(`${API_BASE_URL_STUDENT}/api/sinhvien/me/tien-do-hoc-tap`);
        document.getElementById('progress-info').innerHTML = `<p><strong>Số tín chỉ đã đạt:</strong> ${progress.tong_tin_chi_dat} / ${progress.tong_tin_chi_chuong_trinh}</p>`;
    } catch (error) { document.getElementById('progress-info').innerHTML = `<p style="color:red;">Lỗi: ${error.message}</p>`; }
}
async function loadSemesters() {
    const select = document.getElementById('semester-select');
    try {
        const semesters = await fetchWithAuth_student(`${API_BASE_URL_STUDENT}/api/manager/ky-hoc`);
        select.innerHTML = semesters.length > 0 ? semesters.map(s => `<option value="${s.MaKy}">${s.TenKy} - ${s.NamHoc}</option>`).join('') : '<option value="">Không có dữ liệu</option>';
    } catch (error) { select.innerHTML = `<option value="">Lỗi tải kỳ học</option>`; }
}
async function viewSemesterSummary() {
    const ma_ky = document.getElementById('semester-select').value;
    const summaryDiv = document.getElementById('semester-summary');
    if (!ma_ky) return;
    summaryDiv.innerHTML = `<p>Đang tải...</p>`;
    summaryDiv.style.display = 'block';
    try {
        const summary = await fetchWithAuth_student(`${API_BASE_URL_STUDENT}/api/sinhvien/me/diem-tong-ket/${ma_ky}`);
        summaryDiv.innerHTML = `<h4>Kết quả học tập kỳ: ${ma_ky}</h4><p><strong>Điểm TB (10):</strong> ${summary.DiemTBKyHe10}</p><p><strong>Điểm TB (4):</strong> ${summary.DiemTBKyHe4}</p><p><strong>Tín chỉ đạt:</strong> ${summary.SoTCDatKy}</p><p><strong>Xếp loại:</strong> ${summary.XepLoaiHocLucKy}</p>`;
    } catch (error) { summaryDiv.innerHTML = `<p style="color:red;">Lỗi: ${error.message}</p>`; }
}
async function loadAndPopulateCourses() {
    const select = document.getElementById('course-select');
    try {
        allGradesData_student = await fetchWithAuth_student(`${API_BASE_URL_STUDENT}/api/sinhvien/me/diem-chi-tiet`);
        select.innerHTML = '<option value="">-- Chọn lớp --</option>';
        if (allGradesData_student.length > 0) {
            select.innerHTML += allGradesData_student.map(g => `<option value="${g.MaLopTC}">${g.TenMH} (${g.MaLopTC})</option>`).join('');
        }
    } catch (error) { select.innerHTML = `<option value="">Lỗi tải môn học</option>`; }
}
function displayCourseDetails() {
    const ma_ltc = document.getElementById('course-select').value;
    const detailsDiv = document.getElementById('course-details');
    if (!ma_ltc) { detailsDiv.style.display = 'none'; return; }
    const grade = allGradesData_student.find(g => g.MaLopTC === ma_ltc);
    if (!grade) { detailsDiv.innerHTML = '<p>Không tìm thấy dữ liệu.</p>'; detailsDiv.style.display = 'block'; return; }
    detailsDiv.innerHTML = `<h4>Chi tiết điểm: ${grade.TenMH}</h4><table><tbody>
        <tr><th>Điểm chuyên cần:</th><td>${grade.DiemChuyenCan ?? 'N/A'}</td></tr>
        <tr><th>Điểm giữa kỳ:</th><td>${grade.DiemGiuaKy ?? 'N/A'}</td></tr>
        <tr><th>Điểm cuối kỳ:</th><td>${grade.DiemCuoiKy ?? 'N/A'}</td></tr>
        <tr><th>Điểm thực hành:</th><td>${grade.DiemThucHanh ?? 'N/A'}</td></tr>
        <tr style="font-weight: bold;"><th>Tổng kết (10):</th><td>${grade.DiemTongKetHe10 ?? 'N/A'}</td></tr>
        <tr><th>Điểm chữ:</th><td>${grade.DiemChu ?? 'N/A'}</td></tr>
        <tr><th>Trạng thái:</th><td>${grade.TrangThaiQuaMon ?? 'N/A'}</td></tr>
    </tbody></table>`;
    detailsDiv.style.display = 'block';
}
document.addEventListener('DOMContentLoaded', () => {
    if (!token_student) { logout_student(); return; }
    document.getElementById('logoutBtn').addEventListener('click', logout_student);
    document.getElementById('viewSummaryBtn').addEventListener('click', viewSemesterSummary);
    document.getElementById('course-select').addEventListener('change', displayCourseDetails);
    loadProgress();
    loadSemesters();
    loadAndPopulateCourses();
});
