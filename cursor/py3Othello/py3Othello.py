import pygame
import sys

# 初期設定
pygame.init()
SCREEN_SIZE = 640
BOARD_SIZE = 8
CELL_SIZE = SCREEN_SIZE // BOARD_SIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
GRID_COLOR = (0, 0, 0)

class Othello:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
        pygame.display.set_caption("オセロ")
        self.board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = BLACK
        self.initialize_board()

    def initialize_board(self):
        """初期配置を設定"""
        center = BOARD_SIZE // 2
        self.board[center-1][center-1] = WHITE
        self.board[center-1][center] = BLACK
        self.board[center][center-1] = BLACK
        self.board[center][center] = WHITE

    def draw_board(self):
        """ボードを描画"""
        self.screen.fill(GREEN)
        # グリッド線を描画
        for i in range(BOARD_SIZE + 1):
            pygame.draw.line(self.screen, GRID_COLOR, 
                           (i * CELL_SIZE, 0), 
                           (i * CELL_SIZE, SCREEN_SIZE))
            pygame.draw.line(self.screen, GRID_COLOR, 
                           (0, i * CELL_SIZE), 
                           (SCREEN_SIZE, i * CELL_SIZE))
        
        # 石を描画
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board[row][col]:
                    center = (col * CELL_SIZE + CELL_SIZE // 2,
                            row * CELL_SIZE + CELL_SIZE // 2)
                    pygame.draw.circle(self.screen, self.board[row][col],
                                     center, CELL_SIZE // 2 - 4)

    def get_valid_moves(self):
        """有効な手を取得"""
        valid_moves = []
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.is_valid_move(row, col):
                    valid_moves.append((row, col))
        return valid_moves

    def is_valid_move(self, row, col):
        """指定位置が有効な手かどうかを判定"""
        if self.board[row][col] is not None:
            return False

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0),
                     (1, 1), (-1, -1), (1, -1), (-1, 1)]

        for dr, dc in directions:
            if self.would_flip(row, col, dr, dc):
                return True
        return False

    def would_flip(self, row, col, dr, dc):
        """指定方向に石を裏返せるかを判定"""
        r, c = row + dr, col + dc
        if not (0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE):
            return False
        if self.board[r][c] != self.get_opponent_color():
            return False

        r, c = r + dr, c + dc
        while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
            if self.board[r][c] is None:
                return False
            if self.board[r][c] == self.current_player:
                return True
            r, c = r + dr, c + dc
        return False

    def make_move(self, row, col):
        """石を置いて裏返す"""
        if not self.is_valid_move(row, col):
            return False

        self.board[row][col] = self.current_player
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0),
                     (1, 1), (-1, -1), (1, -1), (-1, 1)]

        for dr, dc in directions:
            if self.would_flip(row, col, dr, dc):
                r, c = row + dr, col + dc
                while self.board[r][c] == self.get_opponent_color():
                    self.board[r][c] = self.current_player
                    r, c = r + dr, c + dc

        self.current_player = self.get_opponent_color()
        return True

    def get_opponent_color(self):
        """相手の色を取得"""
        return WHITE if self.current_player == BLACK else BLACK

    def run(self):
        """ゲームループ"""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    col = x // CELL_SIZE
                    row = y // CELL_SIZE
                    if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
                        self.make_move(row, col)

                    # パスの処理
                    if not self.get_valid_moves():
                        self.current_player = self.get_opponent_color()
                        if not self.get_valid_moves():  # 両者パスでゲーム終了
                            print("ゲーム終了")
                            pygame.quit()
                            sys.exit()

            self.draw_board()
            pygame.display.flip()

if __name__ == "__main__":
    game = Othello()
    game.run()
