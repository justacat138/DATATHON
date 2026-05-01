# 📊 PPAP Team – Data Analysis & Machine Learning Project

---

## 👥 Team Members
- Trần Phương Phương  
- Nguyễn Phạm Bảo Lam  
- Nguyễn Anh Thư  

---

## 📂 Project Structure

Dự án được tổ chức theo các thư mục chính như sau:

---

### 1. 📁 EDA/ – Exploratory Data Analysis

Thư mục này chứa các script phục vụ cho việc khám phá và phân tích dữ liệu:

- `Sale performance.py` – Phân tích hiệu suất bán hàng theo thời gian và khu vực  
- `aov.py` – Tính toán và phân tích **Average Order Value (AOV)**  
- `customer demographics.py` – Phân tích đặc điểm nhân khẩu học khách hàng  
- `inventory.py` – Phân tích và quản lý tồn kho  
- `perceptions.py` – Phân tích cảm nhận của khách hàng  
- `promotions.py` – Đánh giá hiệu quả các chương trình khuyến mãi  
- `returns.py` – Phân tích tỷ lệ và nguyên nhân hàng hoàn trả  
- `shipments.py` – Phân tích quy trình và thời gian vận chuyển  
- `baseline.ipynb` – Notebook phân tích ban đầu, định hướng mô hình  

---

### 2. 📁 Model/ – Machine Learning & Evaluation

Thư mục trung tâm cho việc xây dựng và đánh giá mô hình:

#### 📌 Main Notebook
- `datathon.ipynb`
  - Tiền xử lý dữ liệu  
  - Huấn luyện mô hình  
  - Tinh chỉnh tham số  
  - Dự báo kết quả  

#### 📊 Model Interpretation & Visualization
- `feature_importance_v8.png` – Độ quan trọng của đặc trưng  
- `validation_v8.png` – Kết quả đánh giá trên tập validation  

#### 🔍 SHAP Explainability
- `shap_summary.png` – Tổng quan ảnh hưởng của các feature  
- `shap_bar.png` – Feature importance dạng thanh  
- `shap_waterfall.png` – Giải thích dự đoán cụ thể  
- `shap_dependence.png` – Mối quan hệ giữa feature và output  

---

### 3. 📁 Trắc nghiệm/

- `DATATHON.py` – Xử lý các câu hỏi và bài kiểm tra liên quan đến cuộc thi  

---

## ⚙️ Setup & Reproducibility

### 🔹 1. Environment Setup
Yêu cầu: **Python ≥ 3.8**

Khuyến nghị sử dụng virtual environment:

```bash
# Tạo môi trường ảo
python -m venv venv

# Kích hoạt (Windows)
venv\Scripts\activate

# Kích hoạt (Mac/Linux)
source venv/bin/activate
