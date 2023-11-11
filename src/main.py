import pygame
import sys

pygame.init()


WIDTH, HEIGHT = 900, 900
CELL_SIZE = 70
NUM_ROWS, NUM_COLS = 10, 10
FPS = 30

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
LINE_COLOR = (0, 0, 0)
PLAYER_COLORS = [(255, 0, 0), (0, 0, 255)]
TABLE_XY_END = CELL_SIZE * NUM_ROWS + 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill((255, 0, 0))

table = [
            ["XX", "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "XX"],
            ["6C", "5C", "4C", "3C", "2C", "AH", "KH", "QH", "TH", "TS"],
            ["7C", "AS", "2D", "3D", "4D", "5D", "6D", "7D", "9H", "QS"],
            ["8C", "KS", "6C", "5C", "4C", "3C", "2C", "8D", "8H", "KS"],
            ["9C", "QS", "7C", "6H", "5H", "4H", "AH", "9D", "7H", "AS"],
            ["TS", "TS", "8C", "7H", "2H", "3H", "KH", "TD", "6H", "2D"],
            ["QC", "9S", "9C", "8H", "9H", "TH", "QH", "QD", "5H", "3D"],
            ["KC", "8S", "7D", "QC", "KC", "AC", "AD", "KD", "4H", "4D"],
            ["AC", "7S", "6S", "5S", "4S", "3S", "2S", "2H", "3H", "5D"],
            ["XX", "AD", "KD", "QD", "TD", "9D", "8D", "7D", "6D", "XX"]
        ]

def draw_board(board):
    # pygame.draw.line(screen, LINE_COLOR, (10, 10), (650, 10))
    # pygame.draw.line(screen, LINE_COLOR, (10, CELL_SIZE * NUM_ROWS + 10), (650, CELL_SIZE * NUM_ROWS + 10))
    for row in range(NUM_ROWS+1):
        for col in range(NUM_COLS+1):
            pygame.draw.line(screen, LINE_COLOR, (10, row * CELL_SIZE + 10), (TABLE_XY_END , row * CELL_SIZE + 10))
            pygame.draw.line(screen, LINE_COLOR, (row * CELL_SIZE + 10, 10), (row * CELL_SIZE + 10, TABLE_XY_END))
            if row in range(NUM_ROWS) and col in range(NUM_COLS):
                font = pygame.font.Font('freesansbold.ttf', 18)
                string = str(table[row][col])
                if string == "XX":
                    text = font.render(string, True, RED, WHITE)
                else:
                    text = font.render(string, True, BLACK, WHITE)
                screen.blit(text, ((col * CELL_SIZE + CELL_SIZE // 2), (row * CELL_SIZE + CELL_SIZE // 2)))

    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            if board[row][col] != -1:
                color = PLAYER_COLORS[board[row][col]]
                pygame.draw.circle(screen, color, ((col * CELL_SIZE + CELL_SIZE // 2)+10, (row * CELL_SIZE + CELL_SIZE // 2)+10), 20, 0)

def check_win(board, player):
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if all(board[row][col + i] == player for i in range(5)):
                return True

    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS):
            if all(board[row + i][col] == player for i in range(5)):
                return True

    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if all(board[row + i][col + j] == player for i in range(5) for j in range(5)):
                return True

    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if all(board[row - i][col + j] == player for i in range(5) for j in range(5)):
                return True
            
    #Diagonal check!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    return False

clock = pygame.time.Clock()
current_player = 0
board = [[-1 for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = event.pos
            clicked_row = mouseY // CELL_SIZE
            clicked_col = mouseX // CELL_SIZE

            if board[clicked_row][clicked_col] == -1:
                board[clicked_row][clicked_col] = current_player

                if check_win(board, current_player):
                    print(f"Player {current_player + 1} wins!")
                    pygame.quit()
                    sys.exit()

                current_player = (current_player + 1) % 2

    screen.fill(WHITE)
    draw_board(board)

    pygame.display.flip()
    clock.tick(FPS)
