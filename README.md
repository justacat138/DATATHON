
Tên đội: PPAP

Thành viên:

Trần Phương Phương

Nguyễn Phạm Bảo Lam

Nguyễn Anh Thư

📂 Cấu trúc thư mục Github
Dưới đây là mô tả chi tiết vai trò của từng tệp tin trong project:

1. Thư mục EDA/ (Exploratory Data Analysis)
Thư mục này chứa các mã nguồn dùng để khám phá và phân tích dữ liệu trực quan:

Sale performance.py: Phân tích hiệu suất bán hàng theo thời gian và khu vực.

aov.py: Tính toán và phân tích Giá trị đơn hàng trung bình (Average Order Value).

customer demographics.py: Phân tích đặc điểm nhân khẩu học của khách hàng.

inventory.py: Quản lý và phân tích tình trạng tồn kho.

perceptions.py: Phân tích cảm hồi/nhận thức của khách hàng về sản phẩm.

promotions.py: Đánh giá hiệu quả của các chương trình khuyến mãi.

returns.py: Thống kê và tìm hiểu nguyên nhân tỉ lệ hàng trả về.

shipments.py: Phân tích quy trình và thời gian vận chuyển đơn hàng.

baseline.ipynb: File Notebook chứa các phân tích cơ bản ban đầu để định hướng mô hình.

2. Thư mục Model/
Thư mục trọng tâm chứa các thử nghiệm về học máy và đánh giá mô hình:

datathon.ipynb: Notebook chính thực hiện huấn luyện mô hình, tinh chỉnh tham số và dự báo.

Các file hình ảnh (.png):

feature_importance_v8.png: Biểu đồ mức độ quan trọng của các đặc trưng.

shap_summary.png, shap_bar.png, shap_waterfall.png, shap_dependence.png: Các biểu đồ giải thích mô hình bằng giá trị SHAP (giúp hiểu rõ tại sao mô hình đưa ra quyết định).

validation_v8.png: Biểu đồ đánh giá kết quả trên tập kiểm thử (Validation).

3. Thư mục Trắc nghiệm/
DATATHON.py: File xử lý các câu hỏi hoặc bài kiểm tra liên quan đến nội dung cuộc thi.

🛠 Hướng dẫn cài đặt và chạy lại (Reproduce)
Để chạy lại dự án này trên máy tính cá nhân, vui lòng làm theo các bước sau:

Bước 1: Chuẩn bị môi trường
Yêu cầu máy tính đã cài đặt Python 3.8+. Bạn nên sử dụng môi trường ảo (virtualenv hoặc conda).

Bash
# Tạo môi trường ảo
python -m venv venv

# Kích hoạt môi trường (Windows)
venv\Scripts\activate

# Kích hoạt môi trường (Mac/Linux)
source venv/bin/activate
Bước 2: Cài đặt thư viện cần thiết
Cài đặt các thư viện phổ biến dùng trong dự án (Pandas, Numpy, Scikit-learn, XGBoost/LightGBM, Matplotlib, SHAP...):

Bash
pip install pandas numpy matplotlib seaborn scikit-learn shap jupyter
Bước 3: Chạy phân tích EDA
Bạn có thể chạy các file .py trong thư mục EDA để xem kết quả phân tích:

Bash
python EDA/"Sale performance.py"
Bước 4: Chạy Mô hình
Mở công cụ Jupyter Notebook hoặc VS Code.

Mở file Model/datathon.ipynb.

Đảm bảo file dữ liệu đầu vào (dataset) đã được đặt đúng đường dẫn trong code.

Chọn Run All Cells để thực thi toàn bộ quy trình từ xử lý dữ liệu đến huấn luyện mô hình.
