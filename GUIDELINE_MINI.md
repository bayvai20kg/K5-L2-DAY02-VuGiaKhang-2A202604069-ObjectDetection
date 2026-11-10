# Mini guideline — bài làm cá nhân

- **Học viên**: Vũ Gia Khang
- **MSSV**: 2A202604069
- **Lớp**: K5 - Level 2 (VinAI In Action)

---

## 1. Định nghĩa lớp

| Lớp (ID) | Định nghĩa của bạn | Ví dụ / Điểm phân biệt (Ranh giới lớp) |
| :---: | --- | --- |
| **`car` (0)** | Phương tiện giao thông đường bộ 4 bánh, kích thước từ nhỏ đến vừa, dùng chở người cá nhân/gia đình (bao gồm Sedan, Hatchback, Coupe, SUV/Crossover). | - Chiều dài thường gấp 2 – 2.5 lần chiều rộng (hình chữ nhật thuôn dài khi nhìn từ trên xuống).<br>- Có nắp ca-pô/mui trước rõ rệt; Sedan có cấu trúc 3 khoang (đầu - khoang lái - cốp).<br>- **Phân biệt**: Không có thùng hàng hở như `truck` và không có thân xe dạng khối hộp cao đuôi dựng đứng như `van`/`bus`. |
| **`truck` (1)** | Phương tiện giao thông dùng để chở hàng hóa, kích thước từ trung bình đến rất lớn, từ 4 bánh trở lên (xe tải nhẹ, xe tải nặng, xe đầu kéo/container, bán tải). | - Đặc điểm nhận dạng rõ nhất là cấu trúc tách biệt giữa **Cabin (đầu xe kéo)** và **Thùng chứa hàng** phía sau (thùng kín, thùng mui bạt, thùng lửng hoặc container).<br>- Nhìn từ phía sau là thùng hàng vuông vức.<br>- **Phân biệt**: Xe bán tải (pickup truck) có thùng hàng hở phía sau được tính là `truck`. |
| **`bus` (2)** | Phương tiện giao thông công cộng chở số lượng lớn hành khách, từ 4 bánh trở lên (xe khách, bus đô thị, xe buýt 2 tầng). | - Chiều dài xe vượt trội so với chiều rộng.<br>- Thân xe dạng khối hộp dài, trần cao, có nhiều hàng cửa sổ kính lớn dọc thân xe cho hành khách.<br>- **Phân biệt**: Khác `van` ở kích thước lớn hơn rõ rệt và chở số lượng khách lớn (thường $\ge 24$ chỗ). |
| **`van` (3)** | Phương tiện giao thông hình khối hộp (1 khối hoặc 1.5 khối) từ 4 bánh trở lên, dùng chở hàng nhỏ hoặc chở người (thường từ 6 – 16 chỗ, minivan, MPV cỡ lớn, panel van). | - Mui xe rất ngắn hoặc dốc thẳng liền với kính chắn gió (không có mui dài như sedan).<br>- Thân xe cao từ trước ra sau, trần phẳng, đuôi xe dựng đứng vuông góc.<br>- Thường có cửa trượt bên hông hoặc cửa đôi mở ngang phía sau.<br>- **Phân biệt**: Minivan/MPV 7 chỗ dù chở gia đình nhưng thân xe dạng hộp đuôi vuông thì gán `van`. |

---

## 2. Quy tắc chung

- **Quy tắc box ôm sát**: Bounding box phải là hình chữ nhật nhỏ nhất bao quanh khít toàn bộ phần thân xe nhìn thấy được (tính cả bánh xe tiếp đất, cản trước/sau, mép ngoài gương chiếu hậu). Tuyệt đối không lấy dư mặt đường, bóng râm hay vỉa hè.
- **Vật thể bị che khuất (Occlusion)**: Nếu xe bị xe khác hoặc chướng ngại vật che một phần nhưng vẫn quan sát được $\ge 30\%$ diện tích và đủ đặc điểm nhận diện lớp thì vẽ box ôm khít **phần nhìn thấy được**. Nếu bị che khuất quá nặng ($> 70\%$) chỉ còn lại một góc nhỏ không xác định được loại xe thì bỏ qua.
- **Vật thể bị cắt bởi rìa ảnh (Truncation)**: Box kéo chạm đúng mép biên ảnh tại vị trí bị cắt, tọa độ clamped trong $[0.001, 0.999]$; **không suy đoán** hoặc mở rộng box ra ngoài biên ảnh.
- **Hai xe chồng lên nhau / nối đuôi**: Vẽ hai box độc lập cho từng xe dựa trên phần nhìn thấy của mỗi xe. Tuyệt đối không vẽ một box gộp chung.
- **Ngưỡng kích thước tối thiểu**: Chỉ gán nhãn cho xe có kích thước từ $\ge 15 \times 15$ pixel. Các đốm xe mờ nhòe ở chân trời xa (dưới 10 pixel) bỏ qua để tránh tạo False Positive và gây nhiễu cho mô hình.
- **Xe đang đỗ**: Vẫn gán box và phân lớp bình thường.
- **Đối tượng loại trừ**: Không gán xe máy, xe đạp, người đi bộ, phản chiếu qua gương/kính, hoặc hình vẽ xe trên biển quảng cáo.

---

## 3. Ghi lại quyết định cho ít nhất ba ca mơ hồ

| Ảnh | Tình huống | Quyết định cuối | Lý do theo schema |
| :---: | --- | --- | --- |
| **`drive_003.jpg`** | Xe tải ở mép phải ảnh bị cắt khung hình, chỉ nhìn thấy nửa cabin đầu xe và một phần thùng hàng. | **Vẽ box** chạm mép phải ảnh, gán nhãn `truck`. | Vẫn nhận diện rõ cabin xe tải và phần thùng hàng đặc trưng; box chạm đúng rìa ảnh theo quy tắc truncation. |
| **`drive_002.jpg`** | Ở góc phải xa có một xe bus và một xe car đi song song chồng lấn lên nhau, bị che khuất một phần. | **Vẽ hai box riêng biệt**: 1 box `bus` và 1 box `car`. | Cả hai xe đều nhận diện được loại phương tiện; vẽ box riêng bao quanh phần nhìn thấy của từng xe theo quy tắc hai xe chồng lên nhau. |
| **`drive_001.jpg`** | Ở hậu cảnh phía xa (tọa độ góc phải trên) có các đốm xe rất nhỏ, mờ, chỉ chiếm vài pixel. | **Không vẽ box**. | Kích thước quá nhỏ, mờ nhòe, không thể quan sát chắc chắn để phân loại chính xác giữa `car` hay `van`. Bỏ qua để tránh tạo false positive theo quy định schema. |

---

## 4. Phần cần giảng viên làm rõ

1. **Ngưỡng kích thước tối thiểu cho xe hậu cảnh**: Đề xuất quy định rõ ngưỡng pixel cứng (ví dụ: tối thiểu $15 \times 15$ pixel) để loại bỏ các xe mờ xa chân trời đồng nhất giữa các annotator.
2. **Quy ước cho dòng xe bán tải (Pickup truck)**: Xác nhận lại xe bán tải thống nhất gán `truck` (theo kết cấu có thùng chở hàng rời) hay tính là `car` (theo mục đích sử dụng gia đình).
3. **Quy ước cho các xe chuyên dụng**: Thống nhất tiêu chuẩn gán cho xe cứu thương (dạng minivan $\rightarrow$ `van`) và xe cứu hỏa / xe bồn (khung gầm xe tải $\rightarrow$ `truck`).
