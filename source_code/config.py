# --- KÍCH THƯỚC HỆ THỐNG ---
WIDTH, HEIGHT = 1100, 720  
BOARD_SIZE = 15             # Đạt yêu cầu chuẩn kích thước >= 9x9
CELL_SIZE = 40
BOARD_WIDTH = BOARD_SIZE * CELL_SIZE 

# --- BẢNG MÀU ĐỒ HỌA CYBERPUNK ---
COLOR_BG = (8, 12, 20)          
COLOR_PANEL = (14, 20, 34)       
COLOR_GRID = (25, 38, 60)        
COLOR_NEON_BLUE = (0, 243, 255)  
COLOR_NEON_RED = (255, 0, 85)    
COLOR_TEXT_GREEN = (0, 255, 136) 
WHITE = (240, 244, 255)
GRAY = (100, 115, 140)

# --- TỪ ĐIỂN DỊCH THUẬT (Tuân thủ yêu cầu tối giản ngôn ngữ) ---
TXT = {
    "ENGLISH": {
        "START": "START GAME",
        "TUTORIAL": "TRAINING MODE",
        "LANGUAGE": "LANGUAGE",
        "QUIT_GAME": "QUIT GAME",
        "SELECT_LANG": "SELECT SYSTEM PROGRAM LANGUAGE",
        "SELECT_PROTOCOL": "SELECT SYSTEM PROTOCOL",
        "EASY": "EASY",
        "NORMAL": "NORMAL",
        "HARD": "HARD",
        "BACK": "MAIN MENU",
        "QUIT_MATCH": "QUIT MATCH",
        "LOADING": "INITIALIZING CYBER SYSTEM... PLEASE WAIT",
        "ROBOT_TITLE": "ROBOT BRO 5.0",
        "ROBOT_ACTIVE": "ROBOT CORE ACTIVE",
        "MODE": "PROTOCOL",
        "USER_TURN": "X-TURN: YOUR ACTION",
        "AI_TURN": "O-TURN: AI THINKING...",
        "AI_WIN": "AI VICTORIOUS",
        "PLAYER_WIN": "PLAYER WINS",
        "DRAW": "SYSTEM DRAW",
        "RESTART_MSG": "CLICK BOARD TO RESTART MATCH",
        "SURRENDER": "SURRENDER",
        "TUT_WELCOME": "Yo bro! Welcome to the grid. Line up 4 cells to secure a win. Make your move!",
        "TUT_GOOD": "Whoa! That's a highly logical placement. Keep pushing!",
        "TUT_BAD": "Hmm, not bad, but you could find a deadlier spot. Look closer!",
        "TUT_WIN": "I'm not convinced, let's play another round!",
        "TUT_LOSE": "You need more practice, let's play another round!",
        "TUT_DRAW": "Evenly matched, let's play another round to find the winner!"
    },
    "VIETNAMESE": {
        "START": "BẮT ĐẦU CHƠI",
        "TUTORIAL": "CHẾ ĐỘ TẬP SỰ",
        "LANGUAGE": "NGÔN NGỮ",
        "QUIT_GAME": "THOÁT GAME",
        "SELECT_LANG": "CHỌN NGÔN NGỮ HỆ THỐNG",
        "SELECT_PROTOCOL": "CHỌN CHẾ ĐỘ THỬ NGHIỆM",
        "EASY": "DỄ",          # Tối giản độ khó theo yêu cầu
        "NORMAL": "TRUNG BÌNH",
        "HARD": "KHÓ",
        "BACK": "MENU CHÍNH",
        "QUIT_MATCH": "THOÁT TRẬN",
        "LOADING": "ĐANG KHỞI TẠO HỆ THỐNG...",
        "ROBOT_TITLE": "ROBOT BỒ TÈO 5.0",
        "ROBOT_ACTIVE": "MẠNG NÃO AI SẴN SÀNG",
        "MODE": "CHẾ ĐỘ",
        "USER_TURN": "LƯỢT X: ĐẾN LƯỢT BẠN",
        "AI_TURN": "LƯỢT O: AI ĐANG TÍNH...",
        "AI_WIN": "AI CHIẾN THẮNG",
        "PLAYER_WIN": "BẠN CHIẾN THẮNG",
        "DRAW": "HÒA CỜ",
        "RESTART_MSG": "NHẤP VÀO BÀN CỜ ĐỂ CHƠI VÁN MỚI",
        "SURRENDER": "ĐẦU HÀNG", # Chỉ dịch nút surrender
        "TUT_WELCOME": "Chào bồ tèo! Vào ván chiến liền cho nóng nè. Nhớ luật đánh đủ 4 ô hàng dọc, ngang, chéo là win chặt nha. Đi trước đi bồ tèo!",
        "TUT_GOOD": "Đỉnh chóp luôn bồ tèo ơi! Nước đi này hiểm hóc đấy, tôi bắt đầu thấy áp lực rồi nha!",
        "TUT_BAD": "Nước này hơi hiền nha bồ tèo. Nhìn kỹ thế cờ rộng ra xem có chỗ nào ngon ăn hơn không nào!",
        "TUT_WIN": "Tôi chưa phục, chơi thêm ván nữa nào!",
        "TUT_LOSE": "Bạn cần luyện tập thêm nữa, chơi ván nữa nào!",
        "TUT_DRAW": "Ngang tài ngang sức, chơi thêm ván nữa phân thắng bại nào!"
    }
}