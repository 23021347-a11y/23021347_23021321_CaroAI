import time
from config import BOARD_SIZE

class AIEngine:
    def __init__(self):
        self.states_counted = 0  # Đếm số trạng thái phục vụ telemetry báo cáo

    def check_terminal(self, board):
        """
        Kiểm tra điều kiện kết thúc (Chuỗi đúng 4 quân liên tiếp).
        Đã tối ưu hóa loại bỏ hàm lồng để đạt tốc độ xử lý tối đa.
        """
        # Quét nhanh 4 hướng bằng indexing trực tiếp
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                p = board[r][c]
                if p == '.':
                    continue
                
                # Hướng Ngang (Horizontal)
                if c + 3 < BOARD_SIZE and board[r][c+1] == p and board[r][c+2] == p and board[r][c+3] == p:
                    return p
                # Hướng Dọc (Vertical)
                if r + 3 < BOARD_SIZE and board[r+1][c] == p and board[r+2][c] == p and board[r+3][c] == p:
                    return p
                # Hướng Chéo Xuống (Diagonal Down-Right)
                if r + 3 < BOARD_SIZE and c + 3 < BOARD_SIZE and board[r+1][c+1] == p and board[r+2][c+2] == p and board[r+3][c+3] == p:
                    return p
                # Hướng Chéo Lên (Diagonal Down-Left)
                if r + 3 < BOARD_SIZE and c - 3 >= 0 and board[r+1][c-1] == p and board[r+2][c-2] == p and board[r+3][c-3] == p:
                    return p

        # Kiểm tra trạng thái Hòa (Bàn cờ không còn ô trống)
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if board[r][c] == '.':
                    return None
        return "DRAW"

    def evaluate_line(self, s):
        """ Nhận đầu vào là một chuỗi ký tự s đã được nối sẵn để tăng tốc độ khớp mẫu """
        score = 0
        if "OOOO" in s: score += 500000        # Máy thắng
        if "XXXX" in s: score -= 400000        # Người thắng
        if ".OOO." in s: score += 10000        # 3 quân thoáng hai đầu
        if ".XXX." in s: score -= 25000        # Chặn người chơi có 3 quân thoáng 
        if "OOO." in s or ".OOO" in s: score += 2000
        if "XXX." in s or ".XXX" in s: score -= 6000
        if ".OO." in s: score += 400
        if ".XX." in s: score -= 800
        return score

    def evaluate_board(self, board):
        """ Đánh giá toàn cục diện diện tích bàn cờ """
        total_score = 0
        
        # 1. Hàng ngang
        for r in range(BOARD_SIZE):
            total_score += self.evaluate_line("".join(board[r]))
        
        # 2. Hàng dọc
        for c in range(BOARD_SIZE):
            total_score += self.evaluate_line("".join(board[r][c] for r in range(BOARD_SIZE)))
            
        # 3. Hai đường chéo song song
        for d in range(-BOARD_SIZE + 1, BOARD_SIZE):
            diag1 = "".join(board[i][i+d] for i in range(BOARD_SIZE) if 0 <= i+d < BOARD_SIZE)
            total_score += self.evaluate_line(diag1)
            
            diag2 = "".join(board[i][BOARD_SIZE-1-i+d] for i in range(BOARD_SIZE) if 0 <= BOARD_SIZE-1-i+d < BOARD_SIZE)
            total_score += self.evaluate_line(diag2)
            
        return total_score

    def score_move_heuristic(self, board, r, c):
        """
        Hàm định lượng giá trị chiến thuật cục bộ của một ô trống (Chỉ dùng cho chế độ HARD).
        Giúp định hình các nước đi nguy hiểm để Alpha-Beta ưu tiên duyệt trước.
        """
        score = 0
        center = BOARD_SIZE // 2
        # Ưu tiên nhẹ các vị trí gần trung tâm bàn cờ mở rộng thế trận
        score += (center - abs(r - center)) + (center - abs(c - center))
        
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            o_count, x_count = 0, 0
            
            # Quét tiến
            for step in range(1, 4):
                nr, nc = r + step * dr, c + step * dc
                if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
                    if board[nr][nc] == 'O': o_count += 1
                    elif board[nr][nc] == 'X': x_count += 1
                    else: break
                else: break
                
            # Quét lùi
            for step in range(1, 4):
                nr, nc = r - step * dr, c - step * dc
                if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
                    if board[nr][nc] == 'O': o_count += 1
                    elif board[nr][nc] == 'X': x_count += 1
                    else: break
                else: break
            
            # Đánh trọng số điểm thông minh cho việc gom nhánh
            if o_count >= 3: score += 10000  # Cơ hội tự quyết định thắng lợi
            if x_count >= 3: score += 8000   # Bắt buộc phải phòng ngự chặn đối phương
            if o_count == 2: score += 500    # Xây dựng thế công công kích
            if x_count == 2: score += 400    # Đánh chặn từ xa
            
        return score

    def get_local_moves(self, board, difficulty):
        """ Lọc vùng nước đi cục bộ xung quanh các quân cờ hiện tại để thu hẹp không gian tìm kiếm """
        moves = set()
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if board[r][c] != '.':
                    for dr in (-1, 0, 1):
                        for dc in (-1, 0, 1):
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and board[nr][nc] == '.':
                                moves.add((nr, nc))
                                
        if not moves: 
            return [(BOARD_SIZE // 2, BOARD_SIZE // 2)]
        
        move_list = list(moves)
        
        # --- PHÂN CẤP CẤU TRÚC PHÂN NHÁNH ---
        if difficulty == "EASY":
            # Chế độ dễ: Hạn chế tối đa số nhánh vì Minimax thuần không thể tự cắt tỉa
            return move_list[:6]
        elif difficulty == "NORMAL":
            # Chế độ trung bình: Alpha-Beta xử lý tốt hơn, cho phép lấy nhiều nước tự nhiên hơn
            return move_list[:12]
        else:
            # Chế độ KHÓ: Định hình nước đi bằng Heuristic chuyên sâu rồi mới cắt lát lấy 8 nhánh chất lượng tốt nhất
            scored_moves = []
            for r, c in move_list:
                score = self.score_move_heuristic(board, r, c)
                scored_moves.append((score, (r, c)))
            scored_moves.sort(key=lambda x: x[0], reverse=True)
            return [m[1] for m in scored_moves[:8]]

    # --- CHẾ ĐỘ EASY: MINIMAX THUẦN TÚY KHÔNG CẮT NHÁNH ---
    def pure_minimax(self, board, depth, is_maximizing):
        self.states_counted += 1
        term = self.check_terminal(board)
        if term == 'O': return 1000000
        if term == 'X': return -1000000
        if term == "DRAW": return 0
        if depth == 0: return self.evaluate_board(board)
            
        valid_moves = self.get_local_moves(board, "EASY")
        if is_maximizing:
            max_eval = -float('inf')
            for r, c in valid_moves:
                board[r][c] = 'O'
                ev = self.pure_minimax(board, depth - 1, False)
                board[r][c] = '.'
                if ev > max_eval: max_eval = ev
            return max_eval
        else:
            min_eval = float('inf')
            for r, c in valid_moves:
                board[r][c] = 'X'
                ev = self.pure_minimax(board, depth - 1, True)
                board[r][c] = '.'
                if ev < min_eval: min_eval = ev
            return min_eval

    # --- CHẾ ĐỘ NORMAL & HARD: NÂNG CẤP ALPHA-BETA PRUNING ---
    def alpha_beta(self, board, depth, alpha, beta, is_maximizing, difficulty):
        self.states_counted += 1
        term = self.check_terminal(board)
        if term == 'O': return 1000000
        if term == 'X': return -1000000
        if term == "DRAW": return 0
        if depth == 0: return self.evaluate_board(board)
            
        valid_moves = self.get_local_moves(board, difficulty)
        if is_maximizing:
            max_eval = -float('inf')
            for r, c in valid_moves:
                board[r][c] = 'O'
                ev = self.alpha_beta(board, depth - 1, alpha, beta, False, difficulty)
                board[r][c] = '.'
                if ev > max_eval: max_eval = ev
                if alpha < ev: alpha = ev
                if beta <= alpha: break  # Cắt nhánh Beta
            return max_eval
        else:
            min_eval = float('inf')
            for r, c in valid_moves:
                board[r][c] = 'X'
                ev = self.alpha_beta(board, depth - 1, alpha, beta, True, difficulty)
                board[r][c] = '.'
                if ev < min_eval: min_eval = ev
                if beta > ev: beta = ev
                if beta <= alpha: break  # Cắt nhánh Alpha
            return min_eval

    def get_best_move(self, board, difficulty):
        t_start = time.time()
        self.states_counted = 0
        
        # Thiết lập độ sâu và nhãn giải thuật theo quy định học thuật
        if difficulty == "EASY":
            depth_setting = 2
            algo_label = "Pure Minimax"
        elif difficulty == "NORMAL":
            depth_setting = 2     # Độ sâu tương đương để làm mốc đối chứng kiểm định thực nghiệm số nút duyệt
            algo_label = "Alpha-Beta"
        else:
            depth_setting = 3     # Tăng độ sâu kết hợp Heuristic Move-Ordering cho cấp độ khó nhằn nhất
            algo_label = "Alpha-Beta (Heuristics)"

        valid_moves = self.get_local_moves(board, difficulty)
        if not valid_moves: 
            return None, {}

        best_val = -float('inf')
        chosen = valid_moves[0]
        
        for r, c in valid_moves:
            board[r][c] = 'O'
            if difficulty == "EASY":
                val = self.pure_minimax(board, depth_setting - 1, False)
            else:
                val = self.alpha_beta(board, depth_setting - 1, -float('inf'), float('inf'), False, difficulty)
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