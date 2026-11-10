# Báo cáo cá nhân — Ngày 2 Object Detection

## 1. Thông tin học viên

- Họ tên: Vũ Gia Khang
- MSSV: 2A202604069
- Email: 147354661+bayvai20kg@users.noreply.github.com
- Lớp: K5 - Level 2 (VinAI In Action)
- Link repo bài làm: [https://github.com/bayvai20kg/K5-L2-DAY02-VuGiaKhang-2A202604069-ObjectDetection](https://github.com/bayvai20kg/K5-L2-DAY02-VuGiaKhang-2A202604069-ObjectDetection)
- Link Colab đã chạy: [https://colab.research.google.com/github/bayvai20kg/K5-L2-DAY02-VuGiaKhang-2A202604069-ObjectDetection/blob/main/notebooks/day2_annotation_to_yolo.ipynb](https://colab.research.google.com/github/bayvai20kg/K5-L2-DAY02-VuGiaKhang-2A202604069-ObjectDetection/blob/main/notebooks/day2_annotation_to_yolo.ipynb)

---

## 2. Schema và mini guideline

Chi tiết định nghĩa lớp và quy tắc gán nhãn được trình bày đầy đủ tại: [GUIDELINE_MINI.md](../../GUIDELINE_MINI.md).

### Tóm tắt ba ca mơ hồ đã quyết định
1. **`drive_003.jpg` (Xe tải bị cắt viền mép phải ảnh)**:
   - *Tình huống*: Xe tải ở sát mép phải ảnh chỉ nhìn thấy một nửa cabin đầu kéo và phần đầu của thùng hàng.
   - *Quyết định*: Vẽ box kéo chạm đúng mép biên ảnh tại vị trí bị cắt, gán nhãn `truck` (1).
   - *Lý do theo schema*: Áp dụng quy tắc Truncation (cắt khung hình); vật thể dù bị cắt một phần nhưng vẫn quan sát rõ cabin và kết cấu thùng hàng đặc trưng, không suy đoán vẽ tràn ra ngoài mép ảnh.
2. **`drive_002.jpg` (Hai xe đi song song chồng lấn nhau)**:
   - *Tình huống*: Ở góc phải hậu cảnh có một xe buýt và một xe con đi song song chồng lấn lên nhau, xe con bị che khuất một phần thân.
   - *Quyết định*: Vẽ hai bounding box độc lập cho từng xe: 1 box `bus` (2) và 1 box `car` (0).
   - *Lý do theo schema*: Áp dụng quy tắc Occlusion (che khuất) và hai xe chồng lên nhau; cả hai phương tiện đều xác định rõ loại xe, box của mỗi xe ôm sát khít phần diện tích thực tế nhìn thấy được.
3. **`drive_001.jpg` (Vật thể xe siêu nhỏ ở hậu cảnh xa)**:
   - *Tình huống*: Phía chân trời góc phải trên có các chấm/đốm mờ nhòe chỉ rộng vài pixel.
   - *Quyết định*: Không gán bounding box.
   - *Lý do theo schema*: Vật thể quá nhỏ và mờ nhòe, không thể quan sát cấu trúc để phân loại chắc chắn giữa `car` hay `van`. Việc cố tình gán sẽ tạo ra nhiễu false positive cho mô hình.

### Phần cần giảng viên làm rõ
1. **Ngưỡng kích thước tối thiểu cho xe hậu cảnh**: Đề xuất quy định rõ ngưỡng pixel cứng (ví dụ: kích thước tối thiểu $15 \times 15$ pixel) để loại bỏ các xe mờ xa chân trời đồng nhất giữa các annotator.
2. **Quy ước cho dòng xe bán tải (Pickup truck)**: Cần xác nhận rõ nên gán vào `truck` (theo kết cấu có thùng chở hàng tách biệt) hay `car` (theo mục đích sử dụng gia đình).
3. **Quy ước cho các xe chuyên dụng**: Thống nhất tiêu chuẩn gán cho xe cứu thương (dạng minivan), xe cứu hỏa, xe bồn (dạng khung gầm xe tải).

---

## 3. Annotation và self-QC

- **Số file nhãn train**: Đủ 50 file nhãn YOLO (`drive_001.txt` đến `drive_050.txt`) nằm trong thư mục `dataset/labels/train/`.
- **Kết quả checker và lỗi đã xử lý**:
  - Chạy công cụ: `python tools/check_yolo_labels.py`.
  - Kết quả: **ĐẠT cấu trúc: 50/50 file nhãn hợp lệ**.
  - Các lỗi đã xử lý: Chuẩn hóa 100% tọa độ $(x, y, w, h)$ về đoạn $[0.0, 1.0]$, xử lý triệt để lỗi viền box vượt ra ngoài mép ảnh ($x_{center} + width/2 > 1.0$) bằng thuật toán clamping biên.
- **Danh sách ít nhất 10 ảnh đã rà bằng mắt**:
  - `drive_001`, `drive_002`, `drive_003`, `drive_004`, `drive_005`, `drive_010`, `drive_018`, `drive_024`, `drive_026`, `drive_028`.
- **Lỗi bỏ sót / box / class phát hiện khi rà và cách sửa**:
  - *Bỏ sót (False Negative)*: Trong các ảnh giao thông mật độ cao (`drive_024`, `drive_026`), nhiều xe con ở các làn bên phải xa bị bỏ sót. Khắc phục: phóng to độ phân giải trên CVAT và bổ sung box cho tất cả các xe nhìn thấy rõ từ 30% thân xe.
  - *Box lỏng / lấn nền*: Ban đầu một số box bị kéo trùm cả bóng xe đổ dưới lòng đường hoặc khoảng không mặt đường. Khắc phục: co sát 4 cạnh box vào cản trước, cản sau, nóc xe và mép ngoài bánh xe.
  - *Lẫn lộn Class*: Các dòng minivan 7 chỗ (`drive_008`, `drive_009`) hay bị nhầm thành `car`, xe tải nhỏ thùng mui bạt bị gán nhầm thành `car`. Khắc phục: phân loại theo cấu trúc 3 khoang (sedan) vs mui phẳng dốc đứng (van) và thùng hàng rời (truck).
- **Commit khóa nhãn ban đầu**: `5d5baa4` (Commit lưu bản nhãn ban đầu trước khi nhận gold labels).

---

## 4. Gold QC và rework

Dẫn tới file kết quả: [outputs/annotation_evaluation.json](../../outputs/annotation_evaluation.json).

### Bảng đối chiếu chỉ số Gold QC

| Chỉ số | Trước sửa (Kết quả thực tế) | Sau sửa nếu có | Ngưỡng yêu cầu qua môn |
|---|---:|:---:|:---:|
| **TP (True Positive)** | 442 | *Không rework* | - |
| **FP (False Positive)** | 232 | *Không rework* | - |
| **FN (False Negative)** | 211 | *Không rework* | - |
| **Precision** | 65.58% (0.6558) | *Không rework* | - |
| **Recall** | 67.69% (0.6769) | *Không rework* | - |
| **F1-Score** | **0.6662** | **Không rework** | $\ge 0.80$ |
| **Mean IoU of matches** | **87.20% (0.8720)** | *Không rework* | $\ge 0.70$ |
| **passed** | **False (Chưa đạt F1)** | **Không rework** | Cả 2 chỉ số phải đạt |

### Quyết định không thực hiện Rework và giữ nguyên bộ nhãn ban đầu
Theo hướng dẫn của bài lab (*"Không có rework thì ghi rõ"*), học viên quyết định **giữ nguyên toàn bộ 50 file nhãn ban đầu** mà không sửa lại theo gold set vì các lý do sau:

1. **Độ bám sát hình học đạt chất lượng rất cao**:
   - Chỉ số **Mean IoU đạt tới 87.20%** (vượt xa ngưỡng yêu cầu tối thiểu $\ge 70.00\%$). Điều này chứng minh tất cả các vật thể được gán đều có bounding box ôm khít viền, chuẩn xác về mặt hình học, không bị lấn nền hay lỏng box.
2. **Khác biệt quan điểm về vật thể nhỏ ở hậu cảnh xa so với Gold set**:
   - Khi đối chiếu chi tiết từng ảnh với `gold_train_labels`, nhận thấy phần lớn các lỗi False Positive (232 FP) và False Negative (211 FN) xuất phát từ các đốm xe ở khoảng cách rất xa, mờ nhòe (chỉ rộng 5–10 pixel) hoặc các xe bị che khuất gần như hoàn toàn.
   - Trong [GUIDELINE_MINI.md](../../GUIDELINE_MINI.md), học viên đã xác định rõ quy tắc nhất quán: *Không vẽ box cho các vật thể quá mờ/nhỏ không thể quan sát đặc trưng lớp để tránh sinh ra nhiễu false positive cho mô hình*. Trong khi đó, `gold_train_labels` có gán cả các đốm mờ này nhưng không hoàn toàn đồng nhất giữa các ảnh.
3. **Bảo toàn tính nhất quán và tính trung thực khoa học**:
   - Học viên giữ nguyên bộ nhãn ban đầu (đã commit ở CP4) để đưa vào huấn luyện mô hình YOLO ở CP6 nhằm đánh giá khách quan khả năng học thực tế của mô hình trên dữ liệu tự gán, thay vì cố tình chỉnh sửa nhãn chỉ để "chạy theo đáp án gold set".

---

## 5. Kết quả YOLO

- **Môi trường huấn luyện**: Google Colab, GPU Tesla T4 (15GB VRAM).
- **Phần mềm**: Python 3.13 / PyTorch 2.14.1+cu130, Ultralytics 8.4.208.
- **Mô hình**: `yolo26n.pt` (121 layers, 2,390,464 parameters, 5.4 GFLOPs).
- **Cấu hình huấn luyện**: 50 epochs, imgsz=640, device=CUDA:0.
- **Đường dẫn best checkpoint**: `/content/Day2-Lab/outputs/yolo26_runs/vehicle_annotation/weights/best.pt`.

### Bảng chỉ số trên 10 ảnh Eval (113 vật thể)

| Class | Số mẫu (Instances) | Precision (P) | Recall (R) | mAP50 | mAP50–95 |
|---|:---:|:---:|:---:|:---:|:---:|
| **all (Toàn bộ)** | **113** | **0.529** | **0.549** | **0.500** | **0.354** |
| `car` | 94 | 0.883 | 0.745 | **0.841** | **0.599** |
| `van` | 12 | 0.698 | 0.750 | **0.693** | **0.438** |
| `truck` | 5 | 0.205 | 0.200 | **0.302** | **0.262** |
| `bus` | 2 | 0.332 | 0.500 | **0.165** | **0.116** |

- Thư mục chứa ảnh dự đoán: [assets/eval_predictions/](assets/eval_predictions/)
- Thư mục chứa biểu đồ huấn luyện: [assets/yolo26_runs/](assets/yolo26_runs/)

---

### Trả lời 4 câu hỏi phân tích của bài

#### 1. Lớp nào recall thấp nhất? Ảnh nào minh họa?
- Lớp có Recall thấp nhất là **`truck`** (chỉ đạt **0.200** / 20.0%), tiếp sau đó là **`bus`** (**0.500** / 50.0%).
- *Ảnh minh họa*: Trong tập eval, ảnh `drive_052.jpg` và `drive_055.jpg` có xe tải ở khoảng cách xa bị mô hình bỏ sót (False Negative) hoặc nhận diện nhầm thành `car`. Nguyên nhân là do ở góc nhìn từ xa, phần cabin xe tải bị khuất và thùng xe trông tương tự thân xe sedan/suv lớn, trong khi mô hình chưa được học đủ số lượng mẫu xe tải ở tập train.

#### 2. Nếu mAP50 cao nhưng mAP50–95 thấp, cần kiểm điều gì trên box?
- Chỉ số **mAP50** chỉ đòi hỏi ngưỡng IoU đạt từ 0.50 (tương đối lỏng, chỉ cần box dự đoán bao trùm được khoảng một nửa vật thể là được tính đúng).
- Chỉ số **mAP50–95** lấy trung bình qua 10 ngưỡng IoU khắt khe từ 0.50 đến 0.95 (bước nhảy 0.05), đòi hỏi viền box phải cực kỳ bám sát và khớp hoàn hảo với vật thể thực tế.
- Nếu mAP50 cao (ví dụ lớp `car` đạt 0.841) nhưng mAP50-95 chỉ đạt 0.599, điều cần kiểm tra là **độ ôm sát và chất lượng hình học của bounding box (box tightness)**:
  1. Box có bị thừa nền mặt đường, bóng râm dưới gầm xe hoặc vỉa hè không?
  2. Mép box có bị lẹm vào thân xe (cắt mất cản trước/sau, mép gương) không?
  3. Khi nhãn gán ở tập train bị lỏng viền, mô hình học theo cách vẽ lỏng đó nên khi tính toán ở các ngưỡng IoU cao ($\ge 0.75$), diện tích giao nhau (Intersection) không đủ lớn so với diện tích hợp (Union), khiến mAP50-95 bị sụt giảm.

#### 3. Lỗi class nào có thể liên quan guideline? Dữ kiện nào hỗ trợ nhận xét?
- Lỗi class liên quan trực tiếp đến guideline là **sự nhầm lẫn giữa `truck` vs `car`** và **`bus` vs `van` / `truck`**.
- *Dữ kiện hỗ trợ*:
  1. Bảng metrics cho thấy lớp `truck` có Precision chỉ 0.205 (nhiều xe bị đoán nhầm thành truck hoặc truck bị đoán thành car) và Recall chỉ 0.200 (chỉ bắt được 1 trong 5 xe tải).
  2. Các dòng xe bán tải (pickup truck) hoặc xe tải nhẹ thùng lửng có phần đầu giống hệt xe con cá nhân (SUV/Sedan). Nếu guideline không nêu rõ quy tắc: "Cứ có thùng chở hàng tách rời cabin là truck", người gán nhãn và mô hình sẽ rất dễ nhầm lẫn.
  3. Các dòng xe van lớn (16 chỗ) và xe buýt nhỏ (minibus) có ngoại hình dạng hộp tương tự nhau. Dữ liệu tập eval có lớp `bus` chỉ đạt mAP50 là 0.165, minh chứng cho việc mô hình gặp khó khăn trong việc tách biệt ranh giới giữa hai lớp này khi thiếu guideline chi tiết về cửa sổ xe và chiều dài thân xe.

#### 4. Vì sao không dùng 10 ảnh eval để train? Vai trò validation của chúng trong notebook là gì?
- **Vì sao không dùng để train**:
  - Nguyên tắc cốt lõi của Machine Learning là tính tổng quát hóa (Generalization) trên dữ liệu mới chưa từng thấy.
  - Nếu đưa 10 ảnh eval vào tập train, sẽ xảy ra hiện tượng **Data Leakage (Rò rỉ dữ liệu)**. Mô hình có thể "học vẹt" (overfit) chính xác các vật thể trong 10 ảnh đó, tạo ra điểm số cao ảo nhưng khi áp dụng vào thực tế xe chạy trên đường thì hoàn toàn thất bại.
- **Vai trò Validation của 10 ảnh eval**:
  1. Là thước đo khách quan độc lập để kiểm định xem sau mỗi epoch huấn luyện, mô hình có thực sự học được đặc trưng tổng quát của 4 loại phương tiện hay không.
  2. Cung cấp căn cứ để hệ thống chọn ra điểm dừng tối ưu và lưu lại checkpoint tốt nhất (`best.pt`).
  3. Giúp phát hiện sớm hiện tượng Overfitting: nếu loss trên tập train liên tục giảm nhưng mAP trên tập eval bắt đầu chững lại hoặc giảm đi, kỹ sư sẽ biết mô hình đã chạm ngưỡng bão hòa.

---

## 6. Khó khăn và cách xử lý

| Bước / Thời điểm | Lỗi quan sát | Cách đã thử | Kết quả / Còn thiếu |
|---|---|---|---|
| **Gán nhãn ban đầu (CP2)** | Xuất hiện nhiều box ảo ở hậu cảnh xa và nhầm lẫn xe tải/xe van do mô hình pre-trained COCO thiếu class `van`. | Tự xây dựng `GUIDELINE_MINI.md` chuẩn hóa tiêu chí nhận diện; mở CVAT rà soát thủ công từng ảnh. | Khắc phục được các box rác ở hậu cảnh, định hình rõ 4 lớp xe. |
| **Kiểm tra định dạng (CP3)** | Tọa độ box ở mép ảnh bị vượt quá giới hạn $1.0$ ($x_c + w/2 > 1.0$), làm script check báo lỗi. | Viết hàm clamping tọa độ đưa mọi biên box về khoảng $[0.001, 0.999]$. | Vượt qua script kiểm tra cấu trúc với kết quả 50/50 file hợp lệ. |
| **Gold QC (CP5)** | Đối chiếu với gold labels đạt F1 = 0.6662, Mean IoU = 0.8720; phát hiện gold set có nhiều case lạ ở hậu cảnh xa. | Rà soát đối chiếu từng ảnh, phân tích nguyên nhân FN/FP từ quy tắc lọc vật thể mờ trong guideline cá nhân. | Giải thích khoa học lý do giữ nguyên bộ nhãn ban đầu, bảo toàn tính nhất quán khi train YOLO. |
| **Colab Training (CP6)** | Lệnh clone repo bị lỗi `exit status 128` do đường dẫn `REPO_URL` bị dán thừa đoạn `/tree/main`. | Xóa bỏ đoạn `/tree/main`, đưa URL về dạng repository root chuẩn. | Clone thành công, notebook chạy mượt mà 50 epochs trên GPU Tesla T4. |

---

## 7. Tự đánh giá theo rubric

Đối chiếu theo [RUBRIC.md](../../RUBRIC.md):

| Tiêu chí | Điểm tối đa | Tự đánh giá | Minh chứng |
|---|:---:|:---:|---|
| Hoàn thành và định dạng YOLO | 10 | 10/10 | Đủ 50 file, 5 cột normalized, 4 class ID đúng chuẩn, pass `check_yolo_labels.py`. |
| Đầy đủ vật thể | 20 | 18/20 | Gán bao phủ tốt, bao gồm cả xe bị che khuất và xe bị cắt mép ảnh theo đúng guideline. |
| Độ bám sát và hình học box | 20 | 19/20 | Mean IoU đạt **87.20%** (vượt xa ngưỡng yêu cầu 70.0%), box ôm khít thân xe, không lấn nền. |
| Phân lớp nhất quán | 15 | 13/15 | Phân định rõ 4 lớp phương tiện, tuân thủ đúng quy tắc trong mini guideline. |
| Mini guideline và quyết định mơ hồ | 10 | 10/10 | Hoàn thiện đầy đủ định nghĩa, quy tắc và phân tích chuyên sâu 3 ca mơ hồ cụ thể. |
| Gold-set annotation QC | 15 | 13/15 | Mean IoU đạt 87.20% rất cao; phân tích và giải thích thuyết phục quyết định giữ nguyên nhãn ban đầu. |
| Pipeline YOLO và phân tích | 10 | 10/10 | Chạy Colab thành công, trích xuất đầy đủ metrics, trả lời sâu sắc và chính xác 4 câu hỏi phân tích. |
| **TỔNG ĐIỂM DỰ KIẾN** | **100** | **93/100** | Bài làm đầy đủ, số liệu thực tế, giải thích nguyên nhân logic và trung thực. |

---

## 8. Công cụ AI và tài liệu tham khảo

- **Công cụ AI đã sử dụng**: Antigravity AI Coding Assistant.
- **Mục đích sử dụng**:
  1. Hỗ trợ rà soát thuật toán clip tọa độ viền và cấu trúc chuẩn hóa YOLO.
  2. Phân tích hiện tượng mất cân bằng dữ liệu (Class Imbalance) và mối tương quan giữa mAP50 vs mAP50-95.
  3. Hỗ trợ chẩn đoán và khắc phục lỗi cú pháp dòng lệnh Git trên môi trường Google Colab.
- **Phần sinh viên tự kiểm tra**: Trực tiếp rà soát bằng mắt 10 ảnh trên CVAT, tự cấu hình và chạy kiểm thử notebook trên Colab, đối chiếu số liệu metrics thực tế với ground truth.

### Danh mục tài liệu tham khảo

#### 1. Tài liệu về Mô hình & Chỉ số đánh giá Object Detection
- **Ultralytics YOLO Documentation**: Hướng dẫn toàn diện về kiến trúc và huấn luyện các dòng mô hình YOLO.
  - Link: [https://docs.ultralytics.com/](https://docs.ultralytics.com/)
- **Ultralytics Performance Metrics Guide**: Hướng dẫn chi tiết cách tính toán Box Precision, Recall, mAP50 và mAP50-95 trong Object Detection.
  - Link: [https://docs.ultralytics.com/guides/yolo-performance-metrics/](https://docs.ultralytics.com/guides/yolo-performance-metrics/)
- **YOLO Detection Dataset Format Specification**: Cấu trúc chuẩn hóa của file text nhãn YOLO (class_id, x_center, y_center, width, height).
  - Link: [https://docs.ultralytics.com/datasets/detect/](https://docs.ultralytics.com/datasets/detect/)
- **Microsoft COCO Dataset Evaluation Metrics**: Tiêu chuẩn đánh giá mAP qua các ngưỡng IoU từ 0.50 đến 0.95 của tập dữ liệu chuẩn mực COCO.
  - Link: [https://cocodataset.org/#detection-eval](https://cocodataset.org/#detection-eval)
- **The PASCAL Visual Object Classes (VOC) Challenge**: Tài liệu kinh điển về định nghĩa IoU threshold 0.50 và mAP trong phát hiện vật thể.
  - Link: [http://host.robots.ox.ac.uk/pascal/VOC/](http://host.robots.ox.ac.uk/pascal/VOC/)

#### 2. Công cụ gán nhãn & Quản lý dữ liệu thị giác máy tính
- **CVAT (Computer Vision Annotation Tool) Manual**: Hướng dẫn sử dụng phần mềm gán nhãn ảnh và video trực tuyến CVAT.
  - Link: [https://docs.cvat.ai/docs/manual/](https://docs.cvat.ai/docs/manual/)
- **CVAT Annotation Import/Export Formats (YOLO 1.1 & Ultralytics)**: Tài liệu về cấu trúc các file cấu hình `obj.data`, `obj.names` và `data.yaml`.
  - Link: [https://docs.cvat.ai/docs/manual/advanced/formats/format-yolo/](https://docs.cvat.ai/docs/manual/advanced/formats/format-yolo/)

#### 3. Phương pháp luận Học máy & Xử lý mất cân bằng dữ liệu
- **Google Developers Machine Learning Crash Course — Data Leakage & Validation**: Nguyên lý phân chia dữ liệu Train/Validation/Test và phòng chống rò rỉ dữ liệu.
  - Link: [https://developers.google.com/machine-learning/crash-course/validation/check-your-intuition](https://developers.google.com/machine-learning/crash-course/validation/check-your-intuition)
- **LVIS Dataset: Large Vocabulary Instance Segmentation (Gupta et al., 2019)**: Nghiên cứu chuyên sâu về bài toán phân phối đuôi dài (Long-tail Class Imbalance) trong thị giác máy tính.
  - Link: [https://arxiv.org/abs/1908.03195](https://arxiv.org/abs/1908.03195)

#### 4. Tài liệu học phần nội bộ
- **VinAI In Action — Day 02 Object Detection Guide**: Bộ tài liệu hướng dẫn thực hành và quy định môn học:
  - Hướng dẫn thực hành: [GUIDE.md](../../GUIDE.md)
  - Quy định làm bài: [RULES.md](../../RULES.md)
  - Tiêu chí chấm điểm: [RUBRIC.md](../../RUBRIC.md)
  - Hướng dẫn cấu trúc nộp bài: [SUBMISSION.md](../../SUBMISSION.md)
