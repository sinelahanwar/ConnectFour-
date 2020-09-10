import sys as sys
import numpy as np
import pygame as pygame
import math

# constants
ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 0
AI = 1

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def print_board(board):
    print(np.flip(board, 0))     #reverseorderofelementsinarray


def winning_move(board, piece):
    # horizonal
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and \
               board[r][c+1] == piece and \
               board[r][c+2] == piece and \
               board[r][c+3] == piece:
                return True
    # vertical
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and \
               board[r+1][c] == piece and \
               board[r+2][c] == piece and \
               board[r+3][c] == piece:
                return True
    # positive slope diagonal
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and \
               board[r+1][c+1] == piece and \
               board[r+2][c+2] == piece and \
               board[r+3][c+3] == piece:
                return True
    # negative slope diagonal
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and \
               board[r-1][c+1] == piece and \
               board[r-2][c+2] == piece and \
               board[r-3][c+3] == piece:
                return True


def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen,
                             BLUE,
                             (c*SQUARE_SIZE,
                              r*SQUARE_SIZE+SQUARE_SIZE,
                              SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen,
                               BLACK,
                               (int(c*SQUARE_SIZE+SQUARE_SIZE/2),
                                int(r*SQUARE_SIZE+SQUARE_SIZE+SQUARE_SIZE/2)),
                               RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen,
                                   RED,
                                   (int(c*SQUARE_SIZE+SQUARE_SIZE/2),
                                    height - int(r*SQUARE_SIZE+SQUARE_SIZE/2)),
                                   RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen,
                                   YELLOW,
                                   (int(c*SQUARE_SIZE+SQUARE_SIZE/2),
                                    height - int(r*SQUARE_SIZE+SQUARE_SIZE/2)),
                                   RADIUS)
    pygame.display.update()


pygame.init()
SQUARE_SIZE = 100
RADIUS = int(SQUARE_SIZE/2 - 5)
width = COLUMN_COUNT * SQUARE_SIZE
height = (ROW_COUNT + 1) * SQUARE_SIZE

size = (width, height)

screen = pygame.display.set_mode(size)

board = create_board()
game_over = False
turn = 0

draw_board(board)
pygame.display.update()
myfont = pygame.font.SysFont("inconsolata", 75)


while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen,
                                   RED, (posx, int(SQUARE_SIZE/2)), RADIUS)
            else:
                pygame.draw.circle(screen,
                                   YELLOW, (posx, int(SQUARE_SIZE/2)), RADIUS)
            pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # askplayer1forinput
            if turn == PLAYER:
                # col = int(input("Player 1 Make Your Selection (0-6):"))
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARE_SIZE))
                # print(col)
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)
                    # print_board(board)
                    if winning_move(board, 1):
                        pygame.draw.rect(screen,
                                         BLACK, (0, 0, width, SQUARE_SIZE))
                        label = myfont.render("Player 1 Wins!", 1, RED)
                        screen.blit(label, (40, 10))
                        game_over = True
                    else:
                        pygame.draw.circle(screen,
                                           YELLOW,
                                           (posx, int(SQUARE_SIZE/2)), RADIUS)
  # player2
            else:
              # col = int(input("Player 2 Make Your Selection (0-6):"))
              posx = event.pos[0] col = int(math.floor(posx/SQUARE_SIZE))
              # print(col)
              if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)
                    # print_board(board)
                    if winning_move(board, 2):
                        pygame.draw.rect(screen,
                                         BLACK, (0, 0, width, SQUARE_SIZE))
                        label = myfont.render("Player 2 Wins!", 1, YELLOW)
                        screen.blit(label, (40, 10))
                        game_over = True
                    else:
                        pygame.draw.circle(screen,
                                           RED, (posx, int(SQUARE_SIZE/2)),
                                           RADIUS)
            draw_board(board)
            turn += 1
            turn = turn % 2

            if game_over:
                pygame.time.wait(3000)
                pygame.quit()

