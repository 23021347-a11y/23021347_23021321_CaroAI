\# Agent Caro - Phiên bản Học thuật



Một ứng dụng trò chơi caro (5 Tấu) tương tác với trí tuệ nhân tạo, được phát triển cho mục đích học tập và nghiên cứu các thuật toán trò chơi.



\## Tính năng chính



\### Chế độ trò chơi

\- Chế độ Dễ: Sử dụng thuật toán Minimax thuần túy

\- Chế độ Trung bình: Sử dụng Alpha-Beta Pruning

\- Chế độ Khó: Alpha-Beta Pruning kết hợp với heuristic di chuyển thông minh

\- Chế độ Huấn luyện: Chế độ thực hành để người chơi học cách chơi



\### Giao diện

\- Bàn cờ 15x15 theo tiêu chuẩn chơi caro

\- Giao diện phong cách Cyberpunk hiện đại

\- Robot AI tương tác với người chơi thông qua bong bóng đối thoại

\- Hiệu ứng robot thay đổi (bình thường, chiến thắng, thua cuộc)

\- Dòng chữ chạy khi kết thúc ván

\- Hỗ trợ hai ngôn ngữ: Tiếng Anh và Tiếng Việt



\### Tính năng nâng cao

\- Hoàn tác (Undo) nước đi

\- Làm lại (Redo) nước đi

\- Xem telemetry của AI (điểm đánh giá, độ sâu tìm kiếm, số nút duyệt, thời gian thực thi)

\- Đầu hàng trận đấu



\## Cấu trúc dự án



\### main.py

File chính chứa lớp AgentCaro - quản lý giao diện người dùng và luồng trò chơi

\- Xử lý sự kiện chuột từ người chơi

\- Vẽ bàn cờ và các thành phần giao diện

\- Quản lý các trạng thái trò chơi (Menu, Chọn mức độ, Chơi, v.v.)

\- Lưu trữ lịch sử nước đi để hỗ trợ hoàn tác/làm lại



\### ai.py

File chứa lớp AIEngine - xử lý tất cả logic AI

\- Kiểm tra điều kiện kết thúc (4 quân liên tiếp)

\- Đánh giá trạng thái bàn cờ dựa trên các mẫu chiến thuật

\- Lọc nước đi cục bộ để thu hẹp không gian tìm kiếm

\- Các thuật toán:

&#x20; - Pure Minimax: Cho chế độ Dễ, không có cắt tỉa

&#x20; - Alpha-Beta Pruning: Cho chế độ Trung bình và Khó

&#x20; - Move Ordering Heuristic: Sắp xếp nước đi theo độ quan trọng tại chế độ Khó



\### config.py

File cấu hình hệ thống

\- Kích thước cửa sổ: 1100x720 pixels

\- Kích thước bàn cờ: 15x15 ô

\- Bảng màu theo phong cách Cyberpunk

\- Từ điển dịch thuật cho hai ngôn ngữ



\## Yêu cầu hệ thống



\- Python 3.6+

\- Pygame (library vẽ giao diện)

\- Robot images (robot\_normal.png, robot\_win.png, robot\_lose.png)



\## Cách chơi



1\. Mở ứng dụng và chọn "BẮT ĐẦU CHƠI" hoặc "CHẾ ĐỘ TẬP SỰ"

2\. Chọn mức độ khó (Dễ, Trung bình, Khó)

3\. Nhấp vào bàn cờ để đặt quân X

4\. AI sẽ tư duy và đặt quân O

5\. Người chơi thắng khi có 4 quân X liên tiếp (ngang, dọc, chéo)

6\. AI thắng khi có 4 quân O liên tiếp

7\. Ván hòa khi bàn cờ đầy mà không ai thắng



\## Đặc điểm kỹ thuật



\### Chiến lược AI

\- Đánh giá bàn cờ dựa trên các mẫu: 4 quân liên tiếp (OOOO), 3 quân (OOO), 2 quân (OO), v.v.

\- Ưu tiên heuristic: ưa thích các ô gần trung tâm bàn cờ

\- Phát hiện mối nguy hiểm đối phương và ưu tiên phòng ngự



\### Hiệu năng

\- Chế độ Dễ: Minimax độ sâu 2, tối đa 6 nước đi

\- Chế độ Trung bình: Alpha-Beta độ sâu 2, tối đa 12 nước đi

\- Chế độ Khó: Alpha-Beta độ sâu 3 + Move Ordering, tối đa 8 nước đi hàng đầu



\### Hệ thống Telemetry

Hiển thị thông tin chi tiết về mỗi nước đi của AI:

\- Thuật toán sử dụng

\- Nước đi được chọn

\- Điểm đánh giá

\- Độ sâu tìm kiếm

\- Số trạng thái được duyệt

\- Thời gian thực thi



\## Tác giả

* Phạm Văn Tuân vs Nguyễn Thế Phong

Dự án học tập về các thuật toán trò chơi AI (Minimax, Alpha-Beta Pruning)

