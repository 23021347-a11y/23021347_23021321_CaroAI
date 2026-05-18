import time
from config import BOARD_SIZE

class AIEngine:
    def __init__(self):
        self.states_counted = 0 # Đếm tổng số trạng thái đã duyệt phục vụ báo cáo

    def check_terminal(self, board):
        # Kiểm tra điều kiện dừng: Tìm chuỗi đúng 4 quân liên tiếp để kết thúc trận đấu
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if board[r][c] != '.':
                    p = board[r][c]
                    for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:
                        if all(0 <= r+i*dr < BOARD_SIZE and 0 <= c+i*dc < BOARD_SIZE and board[r+i*dr][c+i*dc] == p for i in range(4)):
                            return p 
        if all(board[r][c] != '.' for r in range(BOARD_SIZE) for c in range(BOARD_SIZE)):
            return "DRAW"
        return None

    def evaluate_line(self, line):
        # Hàm đánh giá trọng số điểm cho các trạng thái chưa kết thúc theo yêu cầu đề bài
        score = 0
        s = "".join(line)
        if "OOOO" in s: score += 500000        # Máy có 4 quân: Điểm cực lớn công phá
        if "XXXX" in s: score -= 400000        # Người có 4 quân: Điểm âm nặng
        if ".OOO." in s: score += 10000        # Máy có 3 quân thoáng rộng: Điểm cao công kích
        if ".XXX." in s: score -= 25000        # Người có 3 quân: Điểm phạt âm lớn để ưu tiên chặn đứng
        if "OOO." in s or ".OOO" in s: score += 2000
        if "XXX." in s or ".XXX" in s: score -= 6000
        if ".OO." in s: score += 400           # Máy có 2 quân liên tiếp
        if ".XX." in s: score -= 800           # Người chơi có 2 quân liên tiếp
        return score

    def evaluate_board(self, board):
        # Quét tổng điểm toàn diện bàn cờ theo mọi hướng Dọc/Ngang/Chéo chéo
        total_score = 0
        for i in range(BOARD_SIZE):
            total_score += self.evaluate_line(board[i])
            total_score += self.evaluate_line([board[j][i] for j in range(BOARD_SIZE)])
        for d in range(-BOARD_SIZE + 1, BOARD_SIZE):
            total_score += self.evaluate_line([board[i][i+d] for i in range(BOARD_SIZE) if 0 <= i+d < BOARD_SIZE])
            total_score += self.evaluate_line([board[i][BOARD_SIZE-1-i+d] for i in range(BOARD_SIZE) if 0 <= BOARD_SIZE-1-i+d < BOARD_SIZE])
        return total_score

    def get_local_moves(self, board, prioritize_heuristics):
        # Cải tiến hiệu năng: Chỉ quét các ô trống phát sinh trong phạm vi gần các quân đã đánh
        moves = set()
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if board[r][c] != '.':
                    for dr in range(-1, 2):
                        for dc in range(-1, 2):
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and board[nr][nc] == '.':
                                moves.add((nr, nc))
        if not moves: return [(BOARD_SIZE//2, BOARD_SIZE//2)]
        
        move_list = list(moves)
        # LEVEL HARD CẢI TIẾN: Sắp xếp các nước đi ưu tiên gần tâm bàn cờ trước để ép Alpha-Beta cắt nhánh cực đại
        if prioritize_heuristics:
            move_list.sort(key=lambda m: (m[0] - BOARD_SIZE//2)**2 + (m[1] - BOARD_SIZE//2)**2)
            return move_list[:8] # Giới hạn nhánh hẹp tính sâu mượt mà không lag
        
        return move_list[:12]

    # --- LEVEL EASY: MINIMAX THUẦN TÚY GIỚI HẠN ĐỘ SÂU ---
    def pure_minimax(self, board, depth, is_maximizing):
        self.states_counted += 1
        term = self.check_terminal(board)
        if term == 'O': return 1000000
        if term == 'X': return -1000000
        if term == "DRAW": return 0
        if depth == 0: return self.evaluate_board(board)
            
        valid_moves = self.get_local_moves(board, False)
        if is_maximizing:
            max_eval = -float('inf')
            for r, c in valid_moves:
                board[r][c] = 'O'
                max_eval = max(max_eval, self.pure_minimax(board, depth - 1, False))
                board[r][c] = '.'
            return max_eval
        else:
            min_eval = float('inf')
            for r, c in valid_moves:
                board[r][c] = 'X'
                min_eval = min(min_eval, self.pure_minimax(board, depth - 1, True))
                board[r][c] = '.'
            return min_eval

    # --- LEVEL NORMAL & HARD: THUẬT TOÁN ALPHA-BETA PRUNING CẮT NHÁNH THÔNG MINH ---
    def alpha_beta(self, board, depth, alpha, beta, is_maximizing, advanced_sort):
        self.states_counted += 1
        term = self.check_terminal(board)
        if term == 'O': return 1000000
        if term == 'X': return -1000000
        if term == "DRAW": return 0
        if depth == 0: return self.evaluate_board(board)
            
        valid_moves = self.get_local_moves(board, advanced_sort)
        if is_maximizing:
            max_eval = -float('inf')
            for r, c in valid_moves:
                board[r][c] = 'O'
                ev = self.alpha_beta(board, depth - 1, alpha, beta, False, advanced_sort)
                board[r][c] = '.'
                max_eval = max(max_eval, ev)
                alpha = max(alpha, ev)
                if beta <= alpha: break # Cắt nhánh Beta (Khách quan hóa dữ liệu thực nghiệm)
            return max_eval
        else:
            min_eval = float('inf')
            for r, c in valid_moves:
                board[r][c] = 'X'
                ev = self.alpha_beta(board, depth - 1, alpha, beta, True, advanced_sort)
                board[r][c] = '.'
                min_eval = min(min_eval, ev)
                beta = min(beta, ev)
                if beta <= alpha: break # Cắt nhánh Alpha
            return min_eval

    def get_best_move(self, board, difficulty):
        t_start = time.time()
        self.states_counted = 0
        
        # Phân phối độ sâu cấu trúc theo độ khó phân tầng học thuật
        if difficulty == "EASY":
            depth_setting = 2
            algo_label = "Pure Minimax"
        elif difficulty == "NORMAL":
            depth_setting = 2     # Đồng độ sâu với Easy để làm bảng đối chứng thực nghiệm trong báo cáo
            algo_label = "Alpha-Beta"
        else:
            depth_setting = 3     # Level Hard tăng độ sâu kết hợp Heuristic sắp xếp nhánh cờ chuyên sâu
            algo_label = "Alpha-Beta (Heuristics)"

        valid_moves = self.get_local_moves(board, prioritize_heuristics=(difficulty == "HARD"))
        if not valid_moves: return None, {}

        best_val = -float('inf')
        chosen = valid_moves[0]
        
        for r, c in valid_moves:
            board[r][c] = 'O'
            if difficulty == "EASY":
                val = self.pure_minimax(board, depth_setting - 1, False)
            elif difficulty == "NORMAL":
                val = self.alpha_beta(board, depth_setting - 1, -float('inf'), float('inf'), False, False)
            else:
                val = self.alpha_beta(board, depth_setting - 1, -float('inf'), float('inf'), False, True)
            board[r][c] = '.'
            
            if val > best_val:
                best_val = val
                chosen = (r, c)
                
        telemetry = {
            "move": f"({chosen[0]},{chosen[1]})",
            "eval_score": best_val,
            "search_depth": depth_setting,
            "states_explored": self.states_counted,
            "execution_time": round(time.time() - t_start, 4),
            "algo_used": algo_label
        }
        return chosen, telemetry