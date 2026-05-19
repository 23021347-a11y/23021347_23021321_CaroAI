# Agent Caro - Phiên bản Học thuật

Một ứng dụng trò chơi caro (5 Tấu) tương tác với trí tuệ nhân tạo, được phát triển cho mục đích học tập và nghiên cứu các thuật toán trò chơi.

## Tính năng chính

### Chế độ trò chơi
- Chế độ Dễ: Sử dụng thuật toán Minimax thuần túy
- Chế độ Trung bình: Sử dụng Alpha-Beta Pruning
- Chế độ Khó: Alpha-Beta Pruning kết hợp với heuristic di chuyển thông minh
- Chế độ Huấn luyện: Chế độ thực hành để người chơi học cách chơi

### Giao diện
- Bàn cờ 15x15 theo tiêu chuẩn chơi caro
- Giao diện phong cách Cyberpunk hiện đại
- Robot AI tương tác với người chơi thông qua bong bóng đối thoại
- Hiệu ứng robot thay đổi (bình thường, chiến thắng, thua cuộc)
- Dòng chữ chạy khi kết thúc ván
- Hỗ trợ hai ngôn ngữ: Tiếng Anh và Tiếng Việt

### Tính năng nâng cao
- Hoàn tác (Undo) nước đi
- Làm lại (Redo) nước đi
- Xem telemetry của AI (điểm đánh giá, độ sâu tìm kiếm, số nút duyệt, thời gian thực thi)
- Đầu hàng trận đấu

---

## Cấu trúc dự án

### main.py
File chính chứa lớp AgentCaro - quản lý giao diện người dùng và luồng trò chơi
- Xử lý sự kiện chuột từ người chơi: Tiếp nhận tọa độ click, ánh xạ chính xác vị trí pixel trên màn hình thành chỉ số dòng/cột tương ứng trong ma trận bàn cờ.
- Vẽ bàn cờ và các thành phần giao diện: Thiết lập vòng lặp render đồ họa Pygame để vẽ lưới ô cờ, các biểu tượng X/O phát sáng Neon, bảng thông số kỹ thuật thời gian thực và bong bóng hội thoại cho Robot.
- Quản lý các trạng thái trò chơi (Menu, Chọn mức độ, Chơi, v.v.): Vận hành một sơ đồ chuyển dịch trạng thái (Finite State Machine) tuần tự từ màn hình Loading ban đầu sang các bảng cấu hình hệ thống.
- Lưu trữ lịch sử nước đi để hỗ trợ hoàn tác/làm lại: Sử dụng cấu trúc dữ liệu mảng hoặc ngăn xếp để ghi lại ảnh chụp trạng thái (Snapshot) bàn cờ sau mỗi lượt đi, hỗ trợ duyệt ngược/xuôi lịch sử trận đấu một cách đồng bộ.

### ai.py
File chứa lớp AIEngine - xử lý tất cả logic AI dựa trên nền tảng toán học cây quyết định:
- Kiểm tra điều kiện kết thúc (4 quân liên tiếp): Thực hiện thuật toán quét ma trận cục bộ theo 4 hướng hình học (Ngang, Dọc, Chéo xuôi, Chéo ngược) bao quanh nước đi vừa hạ để xác định trạng thái kết thúc (Terminal State) ngay khi đạt chuỗi quân liên tiếp.
- Đánh giá trạng thái bàn cờ dựa trên các mẫu chiến thuật: Kích hoạt hàm lượng giá Heuristic tĩnh tại các nút lá để chấm điểm cho cấu hình hiện tại thông qua cơ chế so khớp mẫu chuỗi cờ tiềm năng (Pattern Matching).
- Lọc nước đi cục bộ để thu hẹp không gian tìm kiếm: Triển khai hàm `get_local_moves` nhằm giới hạn các ô trống tiềm năng trong bán kính lân cận 2 ô xung quanh các quân cờ hiện có, giúp hạ hệ số nhánh lý thuyết xuống mức tối thiểu, ngăn ngừa bùng nổ tổ hợp trạng thái.
- Các thuật toán:
  - **Pure Minimax:** Cho chế độ Dễ, duyệt cây đệ quy theo chiều sâu (DFS) đến giới hạn độ sâu được thiết lập. Tại tầng MAX, AI chọn giá trị lớn nhất từ các con truyền lên, tại tầng MIN (lượt người chơi), AI giả định người chơi chọn giá trị nhỏ nhất để triệt tiêu điểm của Máy. Thuật toán này không có cơ chế cắt tỉa nên bắt buộc phải duyệt cạn toàn bộ nhánh cây.
  * **Alpha-Beta Pruning:** Cho chế độ Trung bình và Khó. Hoạt động dựa trên nguyên lý duy trì hai tham số biên rào chắn: $\alpha$ (giá trị tối thiểu nút MAX chắc chắn đạt được) và $\beta$ (giá trị tối đa nút MIN cho phép MAX đạt được). Trong quá trình duyệt đệ quy, nếu tại một nút MIN xuất hiện nhánh con trả về giá trị $v \le \alpha$, thuật toán lập tức chặt đứt (ngừng duyệt) các con còn lại vì tầng MAX phía trên sẽ không bao giờ chọn lối đi này. Tương tự, tại nút MAX nếu gặp giá trị $v \ge \beta$, nhánh đó bị hủy bỏ ngay (Cắt nhánh khi $\alpha \ge \beta$).
  * **Move Ordering Heuristic:** Sắp xếp nước đi theo độ quan trọng tại chế độ Khó. Toàn bộ danh sách ô trống sau khi lọc cục bộ sẽ được tính điểm tĩnh sơ bộ và sắp xếp giảm dần theo sức mạnh. Thuật toán Alpha-Beta sẽ ưu tiên duyệt các ô mạnh nhất đứng đầu danh sách này, giúp thắt chặt rào chắn $\alpha$ và $\beta$ ngay từ những bước đầu tiên, đạt hiệu suất cắt nhánh lý tưởng nhất.

### config.py
File cấu hình hệ thống
- Kích thước cửa sổ: 1100x720 pixels
- Kích thước bàn cờ: 15x15 ô
- Bảng màu theo phong cách Cyberpunk
- Từ điển dịch thuật cho hai ngôn ngữ

---

## Yêu cầu hệ thống

- Python 3.6+
- Pygame (library vẽ giao diện)
- Robot images (robot_normal.png, robot_win.png, robot_lose.png)

---

## Cách chơi

1. Mở ứng dụng và chọn "BẮT ĐẦU CHƠI" hoặc "CHẾ ĐỘ TẬP SỰ"
2. Chọn mức độ khó (Dễ, Trung bình, Khó)
3. Nhấp vào bàn cờ để đặt quân X
4. AI sẽ tư duy và đặt quân O
5. Người chơi thắng khi có 4 quân X liên tiếp (ngang, dọc, chéo)
6. AI thắng khi có 4 quân O liên tiếp
7. Ván hòa khi bàn cờ đầy mà không ai thắng

---

## Đặc điểm kỹ thuật

### Chiến lược AI
- **Nguyên lý Đánh giá mẫu thế cờ:** Do không gian bài toán cờ Caro là vô hạn, AI sử dụng hàm lượng giá để ước lượng điểm số tại độ sâu giới hạn. Hàm số quét ma trận theo 4 hướng và tính tổng hiệu số điểm: $E(s) = \sum \text{Score}_{\text{AI}} - \sum \text{Score}_{\text{Player}}$.
- **Trọng số Tấn công (Quân O của AI):** Cộng điểm thưởng rất cao và lũy tiến mạnh mẽ cho các cấu hình mẫu mang tính chủ động như: 4 quân liên tiếp (`OOOO` -> $+100,000$ điểm), chuỗi 3 quân thoáng hai đầu (`.OOO.` -> $+5,000$ điểm), hoặc chuỗi 2 quân thoáng phát triển (`.OO.` -> $+100$ điểm).
- **Trọng số Phòng ngự (Chặn Quân X của Người):** Phát hiện sớm các cấu hình nguy hiểm của đối phương để gán điểm phạt cực nặng, cưỡng ép AI phải chọn nước đi cản phá: Chuỗi 4 quân của người (`XXXX` -> $-80,000$ điểm, bắt buộc chặn), chuỗi 3 quân thoáng (`.XXX.` -> $-4,000$ điểm).
- **Ưu tiên heuristic:** Ưa thích các ô gần trung tâm bàn cờ. Các ô nằm càng gần tâm ma trận ($7, 7$) sẽ được cộng thêm điểm thưởng tĩnh nhỏ vì khu vực trung tâm sở hữu số lượng đường thẳng và đường chéo hình học nhiều nhất để thiết lập thế trận tấn công.
- **Phát hiện mối nguy hiểm đối phương và ưu tiên phòng ngự:** AI liên tục thực hiện cơ chế cân bằng động giữa hai thái cực Tấn công và Phòng thủ. Nếu đối phương có chuỗi quân mở rải rác, trọng số phòng ngự sẽ tự động nhân hệ số cao để ép AI từ bỏ ý định xây dựng chuỗi quân mình mà chuyển hẳn sang chế độ đánh chặn an toàn.

### Hiệu năng
- **Chế độ Dễ:** Minimax độ sâu 2, tối đa 6 nước đi. Do thuật toán phải duyệt cạn tổ hợp $O(b^d)$ nhánh trạng thái, hệ thống chủ động ép chặt hệ số nhánh $b = 6$ (chỉ lấy 6 ô trống có điểm tĩnh cao nhất) nhằm khống chế tổng số nút duyệt không vượt quá giới hạn gây trễ luồng đồ họa.
- **Chế độ Trung bình:** Alpha-Beta độ sâu 2, tối đa 12 nước đi. Nhờ tích hợp nguyên lý cắt tỉa biên $\alpha / \beta$ loại bỏ các nhánh cây vô ích, độ phức tạp thuật toán được giảm thiểu tối đa. Hệ thống có thể mở rộng hệ số nhánh lên $b = 12$ giúp AI tính toán bao quát hơn mà số nút duyệt thực tế vẫn thấp hơn duyệt cạn.
- **Chế độ Khó:** Alpha-Beta độ sâu 3 + Move Ordering, tối đa 8 nước đi hàng đầu. Bằng việc sắp xếp các nước đi tối ưu lên đầu danh sách duyệt, điều kiện cắt nhánh $\alpha \ge \beta$ được kích hoạt cực kỳ sớm ở các tầng trên cùng của cây. Hệ năng toán học tiệm cận mức lý tưởng $O(b^{d/2})$, cho phép nâng giới hạn độ sâu lên $depth = 3$ và xử lý 8 nhánh con mạnh nhất mà vẫn duy trì tốc độ phản hồi tính toán mượt mà dưới vài chục mili-giây.

### Hệ thống Telemetry
Hiển thị thông tin chi tiết về mỗi nước đi của AI để phục vụ mục đích kiểm định thực nghiệm và minh chứng cho lý thuyết toán học:
- Thuật toán sử dụng: Ghi nhận chính xác nhãn giải thuật đang chạy (`Pure Minimax`, `Alpha-Beta` hoặc `Alpha-Beta (Heuristics)`).
- Nước đi được chọn: Tọa độ ma trận dạng `(Hàng, Cột)` của nước đi tối ưu nhất được bốc tách tại nút gốc.
- Điểm đánh giá: Giá trị điểm số thực tế trả về từ hàm lượng giá tĩnh tại các nút lá của nhánh cây được chọn.
- Độ sâu tìm kiếm: Thể hiện mức giới hạn thám hiểm cây quyết định hiện tại ($depth = 2$ hoặc $depth = 3$).
- Số trạng thái được duyệt: Biến đếm tích lũy số nút thực tế đã mở rộng trong bộ nhớ. (Số liệu chứng minh cơ chế cắt nhánh Alpha-Beta giảm được từ 3 đến 5 lần số nút duyệt so với Minimax thuần túy trên cùng một cấu hình thế cờ).
- Thời gian thực thi: Khoảng thời gian hiệu dụng tính bằng mili-giây (ms) đo đạc từ lúc giải thuật bắt đầu xây dựng cây cho đến khi đưa ra quyết định cuối cùng.

---

## Tác giả

* Phạm Văn Tuân vs Nguyễn Thế Phong
* Dự án học tập về các thuật toán trò chơi AI (Minimax, Alpha-Beta Pruning)