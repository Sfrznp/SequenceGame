import pygame
import sys
import random

pygame.init()

display_info = pygame.display.Info()
window_w = display_info.current_w
window_h = display_info.current_h
# screen = pygame.display.set_mode((window_w, window_h))
screen = pygame.display.set_mode((980, 960))
screen.fill((255, 0, 0))

AI_ENABLED = 1

CELL_SIZE = window_w // 25
NUM_ROWS, NUM_COLS = 10, 10
FPS = 30

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
LINE_COLOR = (0, 0, 0)
BLUE = (0, 0, 255)
PLAYER_COLORS = [(255, 0, 0), (0, 0, 255)]
TABLE_XY_START = 10
TABLE_XY_END = CELL_SIZE * NUM_ROWS + 10


UNASSIGNED = -1
FREE_SPACE = -2

table = [
    ["XX", "2♠", "3♠", "4♠", "5♠", "6♠", "7♠", "8♠", "9♠", "XX"],
    ["6♣", "5♣", "4♣", "3♣", "2♣", "A♥", "K♥", "Q♥", "T♥", "T♠"],
    ["7♣", "A♠", "2♦", "3♦", "4♦", "5♦", "6♦", "7♦", "9♥", "Q♠"],
    ["8♣", "K♠", "6♣", "5♣", "4♣", "3♣", "2♣", "8♦", "8♥", "K♠"],
    ["9♣", "Q♠", "7♣", "6♥", "5♥", "4♥", "A♥", "9♦", "7♥", "A♠"],
    ["T♠", "T♠", "8♣", "7♥", "2♥", "3♥", "K♥", "T♦", "6♥", "2♦"],
    ["Q♣", "9♠", "9♣", "8♥", "9♥", "T♥", "Q♥", "Q♦", "5♥", "3♦"],
    ["K♣", "8♠", "7♦", "Q♣", "K♣", "A♣", "A♦", "K♦", "4♥", "4♦"],
    ["A♣", "7♠", "6♠", "5♠", "4♠", "3♠", "2♠", "2♥", "3♥", "5♦"],
    ["XX", "A♦", "K♦", "Q♦", "T♦", "9♦", "8♦", "7♦", "6♦", "XX"]
]

cards = ["2♠", "3♠", "4♠", "5♠", "6♠", "7♠", "8♠", "9♠", "6♣", "5♣", "4♣", "3♣", "2♣", "A♥", "K♥", "Q♥", "T♥", "T♠",
    "7♣", "A♠", "2♦", "3♦", "4♦", "5♦", "6♦", "7♦", "9♥", "Q♠", "8♣", "K♠", "6♣", "5♣", "4♣", "3♣", "2♣", "8♦", "8♥",
    "K♠", "9♣", "Q♠", "7♣", "6♥", "5♥", "4♥", "A♥", "9♦", "7♥", "A♠", "T♠", "T♠", "8♣", "7♥", "2♥", "3♥", "K♥", "T♦",
    "6♥", "2♦", "Q♣", "9♠", "9♣", "8♥", "9♥", "T♥", "Q♥", "Q♦", "5♥", "3♦", "K♣", "8♠", "7♦", "Q♣", "K♣", "A♣", "A♦",
    "K♦", "4♥", "4♦", "A♣", "7♠", "6♠", "5♠", "4♠", "3♠", "2♠", "2♥", "3♥", "5♦", "A♦", "K♦", "Q♦", "T♦", "9♦", "8♦",
    "7♦", "6♦"]


def suit_color(card):
    if card[1] in ['♣', '♠']:
        return BLACK
    elif card[1] in ['♦', '♥']:
        return RED
    return BLACK

def draw_board(board, player, win):
    for row in range(NUM_ROWS + 1):
        for col in range(NUM_COLS + 1):
            pygame.draw.line(screen, LINE_COLOR, (TABLE_XY_START, row * CELL_SIZE + 10), (TABLE_XY_END, row * CELL_SIZE + 10))
            pygame.draw.line(screen, LINE_COLOR, (row * CELL_SIZE + 10, TABLE_XY_START), (row * CELL_SIZE + 10, TABLE_XY_END))
            if row in range(NUM_ROWS) and col in range(NUM_COLS):
                font = pygame.font.Font('seguisym.ttf', 18)
                string = str(table[row][col])
                if string == "XX":
                    text = font.render(string, True, GREEN, WHITE)
                else:
                    text = font.render(string, True, suit_color(string), WHITE)
                screen.blit(text, ((col * CELL_SIZE + CELL_SIZE // 2), (row * CELL_SIZE + CELL_SIZE // 2)))

    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            if board[row][col] not in [UNASSIGNED, FREE_SPACE]:
                color = PLAYER_COLORS[board[row][col]]
                pygame.draw.circle(screen, color,
                                   ((col * CELL_SIZE + CELL_SIZE // 2) + 10, (row * CELL_SIZE + CELL_SIZE // 2) + 10),
                                   25, 10)
            # Outline for valid moves 
            # if table[row][col] in player1_hand and current_player == 0 and board[row][col] == UNASSIGNED:
            if table[row][col] in player1_hand and board[row][col] == UNASSIGNED:
                color = PLAYER_COLORS[0]
                pygame.draw.rect(screen, color ,pygame.Rect(col * CELL_SIZE + 11, row * CELL_SIZE + 11, CELL_SIZE - 1, CELL_SIZE - 1), 3)
            if table[row][col] in player2_hand and board[row][col] == UNASSIGNED:
                color = PLAYER_COLORS[1]
                pygame.draw.rect(screen, color ,pygame.Rect(col * CELL_SIZE + 11, row * CELL_SIZE + 11, CELL_SIZE - 1, CELL_SIZE - 1), 3)

            
    font = pygame.font.Font('seguisym.ttf', 18)


    # Display player 1 hand at the top
    for i, card in enumerate(player1_hand):
        text = font.render('Player 1 hand: ', True, RED, WHITE)
        screen.blit(text, (TABLE_XY_START , TABLE_XY_END + 70))
        text = font.render(card, True, suit_color(card), WHITE)
        screen.blit(text, (TABLE_XY_START + 50 * i, TABLE_XY_END + 100))

    # Display player 2 hand at the bottom
    for i, card in enumerate(player2_hand):
        text = font.render('Player 2 hand: ', True, BLUE, WHITE)
        screen.blit(text, (TABLE_XY_START, TABLE_XY_END + 130))
        text = font.render(card, True, suit_color(card), WHITE)
        screen.blit(text, (TABLE_XY_START + 50 * i, TABLE_XY_END + 160))

    # Display remaining cards in 4 columns on the right side
    font = pygame.font.Font('seguisym.ttf', 18)
    num_columns = 4
    column_width = 50  # Width of each column
    card_height = 25  # Height of each card in the table

    
    text = font.render(f'Available cards ({len(cards)}): ', True, BLACK, WHITE)
    screen.blit(text, (TABLE_XY_END + 10, TABLE_XY_START))

    table_x_start = TABLE_XY_END + 10  # Starting x-coordinate
    table_y_start = TABLE_XY_START + card_height # Starting y-coordinate
    for i, card in enumerate(cards):
        column = i % num_columns
        row = i // num_columns
        x = table_x_start + column * column_width
        y = table_y_start + row * card_height

        text = font.render(card, True, suit_color(card), WHITE)
        screen.blit(text, (x, y))

    if win:
        text = font.render(f"Player {player + 1} wins!", True, PLAYER_COLORS[player], WHITE)
    else:
        text = font.render(f"Player {player + 1} turn!", True, PLAYER_COLORS[player], WHITE)
    
    screen.blit(text, (TABLE_XY_START + CELL_SIZE * 4, TABLE_XY_END + 20))
    
def restart_display(player, win):    
    font = pygame.font.Font('seguisym.ttf', 18)

    if win:
        text = font.render(f"Player {player + 1} wins!", True, PLAYER_COLORS[player], WHITE)
    else:
        text = font.render(f"Player {player + 1} turn!", True, PLAYER_COLORS[player], WHITE)
    
    screen.blit(text, (TABLE_XY_START + CELL_SIZE * 4, TABLE_XY_END + 20))

def distribute_cards():
    p1_hand = random.sample(cards, 5)
    p2_hand = random.sample(cards, 5)
    return p1_hand, p2_hand
    
win_num_tokens = 5

def check_win(board, player):
    # Horizontal Check
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS - (win_num_tokens-1)):
            if all(board[row][col + i] in [player, FREE_SPACE] for i in range(win_num_tokens)):
                return True
    # Vertical Check
    for row in range(NUM_ROWS - (win_num_tokens-1)):
        for col in range(NUM_COLS):
            if all(board[row + i][col] in [player, FREE_SPACE] for i in range(win_num_tokens)):
                return True

    # Down-Right Diagonal Check
    for row in range(NUM_ROWS - (win_num_tokens-1)):
        for col in range(NUM_COLS - (win_num_tokens-1)):
            if all(board[row + i][col + i] in [player, FREE_SPACE] for i in range(win_num_tokens)):
                return True

    # Up-Right Diagonal Check
    for row in range(4, NUM_ROWS):
        for col in range(NUM_COLS - (win_num_tokens-1)):
            if all(board[row - i][col + i] in [player, FREE_SPACE] for i in range(win_num_tokens)):
                return True

    return False

def game_over(baord):
    if check_win(board, 0) or check_win(board, 1):
        return 1
    return 0
    

'''
Minimax Functions
'''
def evaluate(board):
    # This function evaluates the current state of the board.
    # You can customize it based on your game's rules.
    # For simplicity, this example only checks for wins.
    if check_win(board, 0):  # Check if player 1 wins
        return -10
    elif check_win(board, 1):  # Check if player 2 wins => AI Agent
        return 10
    else:
        return 0  # The game is still ongoing

def minimax(board, depth, is_maximizing_player, alpha, beta):

    if depth == 0 or game_over(board):
        return evaluate(board)

    if is_maximizing_player:
        max_eval = float('-inf')
        for move in legal_moves(board, player2_hand):

            # Simulate a Player 2's move

            print("Simulating Player 2's Move:")
            print("Depth = ", depth)
            print("Player 2's Hand:", player2_hand)
            print("Move:",table[move[0]][move[1]], move[0], move[1] )

            board[move[0]][move[1]] = 0  
            player2_hand.remove(table[move[0]][move[1]])

            print("Player 2's Hand:", player2_hand)
            print("Move:",table[move[0]][move[1]], move[0], move[1] )
            print("=    =   =   =   =   =   =   =   =   =   =   =   ")
            evaluation = minimax(board, depth - 1, False, alpha, beta)
            
            # Undo Move
            player2_hand.append(table[move[0]][move[1]])
            board[move[0]][move[1]] = UNASSIGNED

            max_eval = max(max_eval, evaluation)
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in legal_moves(board, player1_hand):
            # Simulating a Player 1's move

            print("Simulating Player 1's Move:")
            print("Depth = ", depth)
            print("Player 1's Hand:", player1_hand)
            print("Move:",table[move[0]][move[1]], move[0], move[1] )

            board[move[0]][move[1]] = 0  
            player1_hand.remove(table[move[0]][move[1]])
            evaluation = minimax(board, depth - 1, True, alpha, beta)

            print("Player 1's Hand:", player1_hand)
            print("Move:",table[move[0]][move[1]], move[0], move[1] )
            print("=    =   =   =   =   =   =   =   =   =   =   =   ")

            # Undo Move
            board[move[0]][move[1]] = UNASSIGNED  
            player1_hand.append(table[move[0]][move[1]])

            min_eval = min(min_eval, evaluation)
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        return min_eval


def legal_moves(board, player_hand):
    moves = []
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            if table[row][col] in player_hand and board[row][col] == UNASSIGNED:
                moves.append((row, col))
    return moves

def find_best_move(board, depth):
    best_score = float('-inf')
    best_move = (-1, -1)

    print('========================================================================')

    for move in legal_moves(board,player2_hand):

        score = minimax(board, depth - 1, True, float('-inf'), float('inf'))
        # score = 1

        if score > best_score:
            best_score = score
            best_move = move

    return best_move

'''
Initializing the game state
'''

clock = pygame.time.Clock()
current_player = 0
board = [[UNASSIGNED for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

# Marking the corner squares as FREE_SPACE, as they belong to both teams.
board[0][0] = board[NUM_ROWS - 1][0] = board[0][NUM_COLS - 1] = board[NUM_ROWS - 1][NUM_COLS - 1] = FREE_SPACE

# Initialize the player hands
player1_hand, player2_hand = [], []

# Call the distribute function
player1_hand, player2_hand = distribute_cards()

# Remove the distributed cards from the deck
for card in player1_hand:
    cards.remove(card)
for card in player2_hand:
    cards.remove(card)


while True:
    for event in pygame.event.get():
        player_made_move = False
        win = False

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = event.pos
            clicked_row = mouseY // CELL_SIZE
            clicked_col = mouseX // CELL_SIZE

            if (clicked_row < NUM_ROWS and clicked_col < NUM_COLS) and board[clicked_row][clicked_col] == UNASSIGNED:

                clicked_cell_value = table[clicked_row][clicked_col]

                # Check if the clicked cell's value is in the current player's hand
                if current_player == 0 and clicked_cell_value in player1_hand:
                    print("Player 1's hand: ", player1_hand)
                    print("Player 1 played: ", clicked_cell_value)

                    board[clicked_row][clicked_col] = current_player
                    player1_hand.remove(clicked_cell_value)

                    # Dealing a card to the player
                    if len(cards) != 0:
                        new_card = random.sample(cards, 1)[0]
                        player1_hand.append(new_card)
                        cards.remove(new_card)
                    player_made_move = True
                    
                #  Will never get to this if AI_ENABLED is set to 1
                elif current_player == 1 and clicked_cell_value in player2_hand: 
                    print("Player 2's hand: ", player2_hand)
                    print("Player 2 played: ", clicked_cell_value)

                    board[clicked_row][clicked_col] = current_player
                    player2_hand.remove(clicked_cell_value)

                    # Dealing a card to the player
                    if len(cards) != 0:
                        new_card = random.sample(cards, 1)[0]
                        player2_hand.append(new_card)
                        cards.remove(new_card)
                    player_made_move = True


                if check_win(board, current_player):
                    print(f"Player {current_player + 1} wins!")
                    win = True
                    pygame.quit()
                    sys.exit()
                

                if player_made_move:
                    current_player = (current_player + 1) % 2


                # Logic flows to this if condition after player 1's turn if AI_ENABLED is set to 1
                if current_player == 1 and player_made_move and AI_ENABLED:
                    ai_row, ai_col = find_best_move(board, 4)
                    board[ai_row][ai_col] = current_player

                    print("AI's Hand: ", player2_hand)
                    print("AI played: ", table[ai_row][ai_col])
                    player_made_move = True

                    player2_hand.remove(table[ai_row][ai_col])

                    # Dealing a card to the player
                    if len(cards) != 0:
                        new_card = random.sample(cards, 1)[0]
                        player2_hand.append(new_card)
                        cards.remove(new_card)
                    player_made_move = True

                    if check_win(board, current_player):
                        print("AI wins!")
                        pygame.quit()
                        sys.exit()

                    if player_made_move:
                        current_player = (current_player + 1) % 2

    screen.fill(WHITE)
    draw_board(board, current_player, win)

    pygame.display.flip()
    clock.tick(FPS)
