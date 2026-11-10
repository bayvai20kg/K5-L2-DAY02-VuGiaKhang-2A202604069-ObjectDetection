# Mini guideline — bài làm cá nhân

> Điền nội dung này trước khi bắt đầu gán nhãn. Giữ lại các quyết định sau khi self-QC.

## Định nghĩa lớp

| Lớp | Định nghĩa của bạn | Ví dụ/điểm phân biệt |
| --- | --- | --- |
| `car` | Phương tiện giao thông đường bộ 4 bánh, kích thước từ nhỏ đến vừa, dùng chở người cá nhân/gia đình (bao gồm Sedan, Hatchback, Coupe, SUV/Crossover). | Chiều dài thường gấp 2 – 2.5 lần chiều rộng (hình chữ nhật thuôn dài khi nhìn từ trên xuống). Có mui trước rõ rệt. Sedan có cấu trúc 3 khoang (đầu - khoang lái - cốp). Không có thùng hàng hở như truck và không có thân xe dạng khối hộp cao như van/bus. |
| `truck` | Phương tiện giao thông dùng để chở hàng hóa, kích thước từ trung bình đến rất lớn, từ 4 bánh trở lên (bao gồm xe tải nhẹ, xe tải nặng, xe đầu kéo/container). | Đặc điểm nhận dạng rõ nhất là cấu trúc tách biệt giữa **Cabin (đầu xe kéo)** và **Thùng chứa hàng** phía sau (thùng kín, thùng mui bạt, thùng lửng hoặc container). Nhìn từ phía sau là thùng hàng vuông vức. |
| `bus` | Phương tiện giao thông công cộng chở số lượng lớn hành khách, từ 4 bánh trở lên (xe khách, bus đô thị, xe buýt 2 tầng). | Chiều dài xe vượt trội so với chiều rộng. Thân xe dạng khối hộp dài, trần cao, có nhiều hàng cửa sổ kính lớn dọc thân xe cho hành khách. |
| `van` | Phương tiện giao thông hình khối hộp (1 khối hoặc 1.5 khối) từ 4 bánh trở lên, dùng chở hàng nhỏ hoặc chở người (thường từ 6 – 16 chỗ, minivan, MPV cỡ lớn, panel van). | Mui xe rất ngắn hoặc dốc thẳng liền với kính chắn gió (không có mui dài như sedan). Thân xe cao từ trước ra sau, đuôi xe dựng đứng vuông góc. Thường có cửa trượt bên hông hoặc cửa đôi mở ngang phía sau. |

## Quy tắc chung

- **Quy tắc box ôm sát**: Bounding box phải là hình chữ nhật nhỏ nhất bao quanh khít toàn bộ phần thân xe nhìn thấy được (tính cả bánh xe, cản trước/sau, mép ngoài gương chiếu hậu). Tuyệt đối không lấy dư mặt đường, vỉa hè hay bầu trời.
- **Vật thể bị che khuất (Occlusion)**: Nếu xe bị xe khác hoặc chướng ngại vật che một phần nhưng vẫn đủ đặc điểm nhận diện lớp thì vẽ box ôm khít **phần nhìn thấy được**. Nếu bị che khuất gần hết (chỉ thấy một góc nhỏ không xác định được loại xe) thì bỏ qua.
- **Vật thể bị cắt bởi rìa ảnh (Truncation)**: Box kéo chạm đúng mép biên ảnh tại vị trí bị cắt; **không suy đoán** hoặc mở rộng box ra ngoài biên ảnh. Nếu xe bị cắt chỉ còn lại một mảnh quá nhỏ không rõ đặc điểm thì bỏ qua.
- **Hai xe chồng lên nhau**: Vẽ hai box độc lập cho từng xe dựa trên phần nhìn thấy của mỗi xe.
- **Xe đang đỗ**: Vẫn gán box và phân lớp bình thường.
- **Đối tượng loại trừ**: Không gán xe máy, xe đạp, người đi bộ, phản chiếu qua gương/kính, hoặc hình vẽ xe trên biển quảng cáo.

## Ghi lại quyết định cho ít nhất ba ca mơ hồ

| Ảnh | Tình huống | Quyết định cuối | Lý do theo schema |
| --- | --- | --- | --- |
| `drive_003.jpg` | Xe tải ở mép phải ảnh bị cắt khung hình, chỉ nhìn thấy nửa cabin đầu xe và một phần thùng hàng. | **Vẽ box** chạm mép phải ảnh, gán nhãn `truck`. | Vẫn nhận diện rõ cabin xe tải và phần thùng hàng đặc trưng; box chạm đúng rìa ảnh theo quy tắc truncation. |
| `drive_002.jpg` | Ở góc phải xa có một xe bus và một xe car đi song song chồng lấn lên nhau, bị che khuất một phần. | **Vẽ hai box riêng biệt**: 1 box `bus` và 1 box `car`. | Cả hai xe đều nhận diện được loại phương tiện; vẽ box riêng bao quanh phần nhìn thấy của từng xe theo quy tắc hai xe chồng lên nhau. |
| `drive_001.jpg` | Ở hậu cảnh phía xa (tọa độ góc phải trên) có các đốm xe rất nhỏ, mờ, chỉ chiếm vài pixel. | **Không vẽ box**. | Kích thước quá nhỏ, mờ nhòe, không thể quan sát chắc chắn để phân loại chính xác giữa `car` hay `van`. Bỏ qua để tránh tạo false positive theo quy định schema. |
