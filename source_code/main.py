import pygame
import time
import sys

# Khởi tạo liên kết dữ liệu mô-đun nội bộ
from config import *
from ai import AIEngine

class AgentCaro:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("AGENT CARO - ACADEMIC EDITION")
        
        self.font_name = "Times New Roman"
        self.font_title = pygame.font.SysFont(self.font_name, 75, bold=True)
        self.font_large = pygame.font.SysFont(self.font_name, 44, bold=True)
        self.font_medium = pygame.font.SysFont(self.font_name, 22, bold=True)
        self.font_tut = pygame.font.SysFont(self.font_name, 19, bold=False)
        self.font_small = pygame.font.SysFont(self.font_name, 17, bold=False)
        self.font_bold_small = pygame.font.SysFont(self.font_name, 18, bold=True)
        
        self.state = "LOADING"
        self.start_time = time.time()
        self.board = [['.' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.difficulty = "EASY"
        self.turn = "USER"  
        self.game_over = False
        self.winner = None
        self.marquee_x = WIDTH
        self.language = "ENGLISH"
        self.tut_bubble_text = ""
        self.history = []       
        self.redo_stack = []    
        
        self.ai_core = AIEngine()
        self.telemetry = {"move": "N/A", "eval_score": 0, "search_depth": 0, "states_explored": 0, "execution_time": 0.0, "algo_used": "Minimax"}

        try:
            self.img_normal = pygame.transform.scale(pygame.image.load("robot_normal.png"), (140, 140))
            self.img_win = pygame.transform.scale(pygame.image.load("robot_win.png"), (140, 140))
            self.img_lose = pygame.transform.scale(pygame.image.load("robot_lose.png"), (140, 140))
        except:
            self.img_normal = self.img_win = self.img_lose = None

        self.robot_img = self.img_normal

    def get_txt(self, key):
        return TXT[self.language][key]

    def reset_game(self):
        self.board = [['.' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.turn = "USER"
        self.game_over = False
        self.winner = None
        self.marquee_x = WIDTH
        self.history.clear()
        self.redo_stack.clear()
        self.robot_img = self.img_normal
        self.tut_bubble_text = self.get_txt("TUT_WELCOME")
        self.telemetry = {"move": "N/A", "eval_score": 0, "search_depth": 0, "states_explored": 0, "execution_time": 0.0, "algo_used": "Minimax"}

    def draw_text(self, text, font, color, x, y, center=True):
        img = font.render(text, True, color)
        if center: self.screen.blit(img, img.get_rect(center=(x, y)))
        else: self.screen.blit(img, (x, y))

    def draw_button(self, text, x, y, w, h, base_color, mouse_pos):
        rect = pygame.Rect(x, y, w, h)
        is_hover = rect.collidepoint(mouse_pos)
        pygame.draw.rect(self.screen, (22, 38, 68) if is_hover else COLOR_PANEL, rect, border_radius=8)
        pygame.draw.rect(self.screen, base_color if is_hover else COLOR_GRID, rect, width=2, border_radius=8)
        self.draw_text(text, self.font_medium, base_color if is_hover else WHITE, x + w//2, y + h//2)
        return rect

    def draw_wrapped_text(self, text, font, color, rect, line_spacing=4):
        words = text.split(' ')
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + " " + word if current_line else word
            if font.size(test_line)[0] < rect.width: current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        if current_line: lines.append(current_line)
        y = rect.y
        for line in lines:
            self.draw_text(line, font, color, rect.x, y, center=False)
            y += font.size(line)[1] + line_spacing

    def draw_robot_cloud_bubble(self, x, y, w, h):
        pygame.draw.rect(self.screen, (18, 26, 46), (x, y, w, h), border_radius=12)
        pygame.draw.rect(self.screen, COLOR_NEON_BLUE, (x, y, w, h), width=2, border_radius=12)
        pts = [(x + 40, y + h), (x + 25, y + h + 15), (x + 55, y + h)]
        pygame.draw.polygon(self.screen, (18, 26, 46), pts)
        pygame.draw.line(self.screen, COLOR_NEON_BLUE, pts[0], pts[1], 2)
        pygame.draw.line(self.screen, COLOR_NEON_BLUE, pts[1], pts[2], 2)

    def screen_loading(self):
        self.screen.fill(COLOR_BG)
        elapsed = time.time() - self.start_time
        progress = min(1.0, elapsed / 1.5) 
        self.draw_text(self.get_txt("LOADING"), self.font_large, COLOR_NEON_BLUE, WIDTH//2, HEIGHT//2 - 40)
        bar_w = 600
        pygame.draw.rect(self.screen, COLOR_GRID, (WIDTH//2 - bar_w//2, HEIGHT//2 + 30, bar_w, 12), border_radius=4)
        pygame.draw.rect(self.screen, COLOR_TEXT_GREEN, (WIDTH//2 - bar_w//2, HEIGHT//2 + 30, int(bar_w * progress), 12), border_radius=4)
        if progress >= 1.0: self.state = "MENU"

    def screen_menu(self, mouse_pos):
        self.screen.fill(COLOR_BG)
        pygame.draw.line(self.screen, COLOR_GRID, (0, 150), (WIDTH, 150), 2)
        pygame.draw.line(self.screen, COLOR_GRID, (0, 620), (WIDTH, 620), 2)
        self.draw_text("AGENT CARO", self.font_title, WHITE, WIDTH//2, 210)
        b_start = self.draw_button(self.get_txt("START"), WIDTH//2 - 150, 320, 300, 50, COLOR_NEON_BLUE, mouse_pos)
        b_tutor = self.draw_button(self.get_txt("TUTORIAL"), WIDTH//2 - 150, 390, 300, 50, COLOR_TEXT_GREEN, mouse_pos)
        b_lang  = self.draw_button(self.get_txt("LANGUAGE"), WIDTH//2 - 150, 460, 300, 50, (255, 165, 0), mouse_pos)
        b_quit  = self.draw_button(self.get_txt("QUIT_GAME"), WIDTH//2 - 150, 530, 300, 50, COLOR_NEON_RED, mouse_pos)
        return b_start, b_tutor, b_lang, b_quit

    def screen_language_select(self, mouse_pos):
        self.screen.fill(COLOR_BG)
        self.draw_text(self.get_txt("SELECT_LANG"), self.font_large, WHITE, WIDTH//2, 200)
        b_en = self.draw_button("ENGLISH", WIDTH//2 - 150, 320, 300, 55, COLOR_NEON_BLUE, mouse_pos)
        b_vi = self.draw_button("TIẾNG VIỆT", WIDTH//2 - 150, 400, 300, 55, COLOR_TEXT_GREEN, mouse_pos)
        b_back = self.draw_button(self.get_txt("BACK"), WIDTH//2 - 150, 520, 300, 50, GRAY, mouse_pos)
        return b_en, b_vi, b_back

    def screen_difficulty(self, mouse_pos):
        self.screen.fill(COLOR_BG)
        self.draw_text(self.get_txt("SELECT_PROTOCOL"), self.font_large, WHITE, WIDTH//2, 180)
        b1 = self.draw_button(self.get_txt("EASY"), WIDTH//2 - 150, 300, 300, 55, COLOR_TEXT_GREEN, mouse_pos)
        b2 = self.draw_button(self.get_txt("NORMAL"), WIDTH//2 - 150, 380, 300, 55, COLOR_NEON_BLUE, mouse_pos)
        b3 = self.draw_button(self.get_txt("HARD"), WIDTH//2 - 150, 460, 300, 55, COLOR_NEON_RED, mouse_pos)
        b_back = self.draw_button(self.get_txt("BACK"), WIDTH//2 - 150, 550, 300, 50, GRAY, mouse_pos)
        return b1, b2, b3, b_back

    def screen_playing(self, mouse_pos):
        self.screen.fill(COLOR_BG)
        offset_x, offset_y = 40, 40
        
        # Thiết kế vẽ Ma trận lưới cờ
        pygame.draw.rect(self.screen, COLOR_GRID, (offset_x - 4, offset_y - 4, BOARD_WIDTH + 8, BOARD_WIDTH + 8), width=2, border_radius=4)
        pygame.draw.rect(self.screen, (10, 14, 25), (offset_x, offset_y, BOARD_WIDTH, BOARD_WIDTH))
        for i in range(BOARD_SIZE + 1):
            pygame.draw.line(self.screen, COLOR_GRID, (offset_x + i*CELL_SIZE, offset_y), (offset_x + i*CELL_SIZE, offset_y + BOARD_WIDTH), 1)
            pygame.draw.line(self.screen, COLOR_GRID, (offset_x, offset_y + i*CELL_SIZE), (offset_x + BOARD_WIDTH, offset_y + i*CELL_SIZE), 1)
            
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                cx, cy = offset_x + c * CELL_SIZE + CELL_SIZE // 2, offset_y + r * CELL_SIZE + CELL_SIZE // 2
                if self.board[r][c] == 'X':
                    pygame.draw.line(self.screen, COLOR_NEON_BLUE, (cx - 10, cy - 10), (cx + 10, cy + 10), 4)
                    pygame.draw.line(self.screen, COLOR_NEON_BLUE, (cx + 10, cy - 10), (cx - 10, cy + 10), 4)
                elif self.board[r][c] == 'O':
                    pygame.draw.circle(self.screen, COLOR_NEON_RED, (cx, cy), 12, 4)

        # --- PANEL ĐIỀU KHIỂN BÊN PHẢI ---
        sb_x = BOARD_WIDTH + 80 
        pygame.draw.rect(self.screen, COLOR_PANEL, (sb_x, 0, WIDTH - sb_x, HEIGHT))
        pygame.draw.line(self.screen, COLOR_GRID, (sb_x, 0), (sb_x, HEIGHT), 2)
        self.draw_text(self.get_txt("ROBOT_TITLE"), self.font_medium, COLOR_TEXT_GREEN, sb_x + 160, 25)
        
        self.draw_robot_cloud_bubble(sb_x + 20, 55, 300, 105)
        self.draw_wrapped_text(self.tut_bubble_text, self.font_tut, WHITE, pygame.Rect(sb_x + 35, 65, 270, 85))
        
        r_y = 180
        if self.robot_img and not self.game_over: self.screen.blit(self.robot_img, (sb_x + 95, r_y))
        else:
            pygame.draw.rect(self.screen, COLOR_BG, (sb_x + 95, r_y, 130, 130), border_radius=15)
            pygame.draw.rect(self.screen, COLOR_GRID, (sb_x + 95, r_y, 130, 130), width=2, border_radius=15)
        self.draw_text(self.get_txt("ROBOT_ACTIVE"), self.font_small, COLOR_TEXT_GREEN, sb_x + 160, r_y + 145)
        
        pygame.draw.line(self.screen, COLOR_GRID, (sb_x + 20, 350), (WIDTH - 20, 350), 1)
        self.draw_text(f"{self.get_txt('MODE')}: {self.get_txt(self.difficulty) if self.state=='PLAYING' else self.get_txt('TUTORIAL')}", self.font_bold_small, WHITE, sb_x + 25, 360, center=False)
        status = self.get_txt("USER_TURN") if self.turn == "USER" else self.get_txt("AI_TURN")
        if self.game_over: status = self.get_txt(self.winner)
        self.draw_text(status, self.font_bold_small, COLOR_NEON_BLUE if self.turn == "USER" else COLOR_NEON_RED, sb_x + 25, 385, center=False)
        pygame.draw.line(self.screen, COLOR_GRID, (sb_x + 20, 410), (WIDTH - 20, 410), 1)

        # --- BẢNG SỐ LIỆU ĐO LƯỜNG THỰC NGHIỆM ACADEMIC (Yêu cầu đề bài) ---
        t_y = 420
        self.draw_text("AI ACADEMIC TELEMETRY:", self.font_bold_small, COLOR_NEON_BLUE, sb_x + 25, t_y, center=False)
        self.draw_text(f"- Algorithm: {self.telemetry['algo_used']}", self.font_small, WHITE, sb_x + 30, t_y + 22, center=False)
        self.draw_text(f"- Chosen Move: {self.telemetry['move']}", self.font_small, WHITE, sb_x + 30, t_y + 42, center=False)
        self.draw_text(f"- Eval Score: {self.telemetry['eval_score']}", self.font_small, WHITE, sb_x + 30, t_y + 62, center=False)
        self.draw_text(f"- Search Depth: {self.telemetry['search_depth']}", self.font_small, WHITE, sb_x + 30, t_y + 82, center=False)
        self.draw_text(f"- States Explored: {self.telemetry['states_explored']}", self.font_small, COLOR_TEXT_GREEN, sb_x + 30, t_y + 102, center=False)
        self.draw_text(f"- Execution Time: {self.telemetry['execution_time']}s", self.font_small, COLOR_NEON_RED, sb_x + 30, t_y + 122, center=False)
        pygame.draw.line(self.screen, COLOR_GRID, (sb_x + 20, 560), (WIDTH - 20, 560), 1)

        # Các nút giữ nguyên chữ tiếng Anh, riêng surrender dịch theo yêu cầu
        btn_undo = self.draw_button("UNDO", sb_x + 20, 575, 140, 40, COLOR_NEON_BLUE, mouse_pos)
        btn_redo = self.draw_button("REDO", sb_x + 180, 575, 140, 40, COLOR_TEXT_GREEN, mouse_pos)
        btn_surr = self.draw_button(self.get_txt("SURRENDER"), sb_x + 20, 625, 300, 40, (255, 140, 0), mouse_pos)
        btn_back = self.draw_button(self.get_txt("BACK") if self.state == "TUTORIAL_PLAYING" else self.get_txt("QUIT_MATCH"), sb_x + 20, 673, 300, 40, COLOR_NEON_RED, mouse_pos)
        
        # --- THIẾT KẾ BĂNG RÔN CHỮ CHẠY VÀ ROBOT Ở CHÍNH GIỮA MÀN HÌNH ---
        if self.game_over:
            s_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            s_overlay.fill((0, 0, 0, 195)) 
            self.screen.blit(s_overlay, (0, 0))
            
            b_height = 240
            pygame.draw.rect(self.screen, COLOR_PANEL, (0, HEIGHT//2 - b_height//2, WIDTH, b_height))
            pygame.draw.line(self.screen, COLOR_NEON_BLUE, (0, HEIGHT//2 - b_height//2), (WIDTH, HEIGHT//2 - b_height//2), 3)
            pygame.draw.line(self.screen, COLOR_NEON_BLUE, (0, HEIGHT//2 + b_height//2), (WIDTH, HEIGHT//2 + b_height//2), 3)
            
            # Khóa Robot nằm chuẩn mực ở vị trí chính giữa màn hình theo yêu cầu mới
            if self.robot_img: self.screen.blit(self.robot_img, (WIDTH//2 - 70, HEIGHT//2 - 105))
                
            self.marquee_x -= 5 
            marquee_string = f"<< {self.get_txt(self.winner)} !! {self.get_txt('RESTART_MSG')} >>"
            self.draw_text(marquee_string, self.font_title, COLOR_NEON_RED if "AI" in self.winner else COLOR_TEXT_GREEN, self.marquee_x, HEIGHT//2 + 60)
            if self.marquee_x < -1300: self.marquee_x = WIDTH + 100
                
        return btn_undo, btn_redo, btn_surr, btn_back

    def run(self):
        clock = pygame.time.Clock()
        while True:
            mouse_pos = pygame.mouse.get_pos()
            
            if (self.state in ["PLAYING", "TUTORIAL_PLAYING"]) and self.turn == "AI" and not self.game_over:
                self.screen_playing(mouse_pos)
                pygame.display.flip()
                
                chosen, telemetry_data = self.ai_core.get_best_move(self.board, self.difficulty if self.state=="PLAYING" else "EASY")
                if chosen:
                    r, c = chosen
                    self.board[r][c] = 'O'
                    self.telemetry = telemetry_data
                    
                    term = self.ai_core.check_terminal(self.board)
                    if term == 'O':
                        self.game_over = True; self.winner = "AI_WIN"
                        self.tut_bubble_text = self.get_txt("TUT_LOSE")
                        self.robot_img = self.img_win
                    elif term == "DRAW":
                        self.game_over = True; self.winner = "DRAW"
                        self.tut_bubble_text = self.get_txt("TUT_DRAW")
                        self.robot_img = self.img_normal
                    else: self.turn = "USER"
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.state == "MENU":
                        b_s, b_t, b_l, b_q = self.screen_menu(mouse_pos)
                        if b_s.collidepoint(mouse_pos): self.state = "DIFFICULTY"
                        elif b_t.collidepoint(mouse_pos): self.state = "TUTORIAL_PLAYING"; self.reset_game()
                        elif b_l.collidepoint(mouse_pos): self.state = "LANGUAGE"
                        elif b_q.collidepoint(mouse_pos): pygame.quit(); sys.exit()
                    elif self.state == "LANGUAGE":
                        b_en, b_vi, b_back = self.screen_language_select(mouse_pos)
                        if b_en.collidepoint(mouse_pos): self.language = "ENGLISH"; self.state = "MENU"
                        elif b_vi.collidepoint(mouse_pos): self.language = "VIETNAMESE"; self.state = "MENU"
                        elif b_back.collidepoint(mouse_pos): self.state = "MENU"
                    elif self.state == "DIFFICULTY":
                        d1, d2, d3, d_b = self.screen_difficulty(mouse_pos)
                        if d1.collidepoint(mouse_pos): self.difficulty = "EASY"; self.reset_game(); self.state = "PLAYING"
                        elif d2.collidepoint(mouse_pos): self.difficulty = "NORMAL"; self.reset_game(); self.state = "PLAYING"
                        elif d3.collidepoint(mouse_pos): self.difficulty = "HARD"; self.reset_game(); self.state = "PLAYING"
                        elif d_b.collidepoint(mouse_pos): self.state = "MENU"
                    elif self.state in ["PLAYING", "TUTORIAL_PLAYING"]:
                        b_undo, b_redo, b_surr, b_back = self.screen_playing(mouse_pos)
                        if b_back.collidepoint(mouse_pos): self.state = "MENU" if self.state == "TUTORIAL_PLAYING" else "DIFFICULTY"
                        elif b_undo.collidepoint(mouse_pos) and len(self.history) > 0:
                            self.redo_stack.append(([row[:] for row in self.board], self.tut_bubble_text, self.robot_img, self.telemetry.copy()))
                            self.board, self.tut_bubble_text, self.robot_img, self.telemetry = self.history.pop()
                            self.game_over = False; self.turn = "USER"
                        elif b_redo.collidepoint(mouse_pos) and len(self.redo_stack) > 0:
                            self.history.append(([row[:] for row in self.board], self.tut_bubble_text, self.robot_img, self.telemetry.copy()))
                            self.board, self.tut_bubble_text, self.robot_img, self.telemetry = self.redo_stack.pop()
                            term = self.ai_core.check_terminal(self.board)
                            if term: self.game_over = True; self.winner = "PLAYER_WIN" if term == 'X' else ("AI_WIN" if term == 'O' else "DRAW")
                        elif b_surr.collidepoint(mouse_pos) and not self.game_over:
                            self.game_over = True; self.winner = "AI_WIN"
                            self.tut_bubble_text = self.get_txt("TUT_LOSE"); self.robot_img = self.img_win
                        elif self.game_over: self.reset_game()
                        elif self.turn == "USER":
                            x, y = event.pos
                            if 40 <= x < 40 + BOARD_WIDTH and 40 <= y < 40 + BOARD_WIDTH:
                                c, r = (x - 40) // CELL_SIZE, (y - 40) // CELL_SIZE
                                if self.board[r][c] == '.':
                                    self.history.append(([row[:] for row in self.board], self.tut_bubble_text, self.robot_img, self.telemetry.copy()))
                                    self.redo_stack.clear()
                                    self.board[r][c] = 'X'
                                    
                                    self.tut_bubble_text = self.get_txt("TUT_GOOD") if self.ai_core.evaluate_board(self.board) <= -800 else self.get_txt("TUT_BAD")
                                    term = self.ai_core.check_terminal(self.board)
                                    if term == 'X':
                                        self.game_over = True; self.winner = "PLAYER_WIN"
                                        self.tut_bubble_text = self.get_txt("TUT_WIN"); self.robot_img = self.img_lose
                                    elif term == "DRAW":
                                        self.game_over = True; self.winner = "DRAW"; self.robot_img = self.img_normal
                                    else: self.turn = "AI"

            if self.state == "LOADING": self.screen_loading()
            elif self.state == "MENU": self.screen_menu(mouse_pos)
            elif self.state == "LANGUAGE": self.screen_language_select(mouse_pos)
            elif self.state == "DIFFICULTY": self.screen_difficulty(mouse_pos)
            elif self.state in ["PLAYING", "TUTORIAL_PLAYING"]: self.screen_playing(mouse_pos)

            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    AgentCaro().run()