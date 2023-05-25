
import pygame
import random

pygame.init()

# initial set up
WIDTH = 800
HEIGHT = 500
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('2048 by Ramazan')
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 24)

# 2048 game color library
colors = {0: (204, 192, 179),
          2: (238, 228, 218),
          4: (237, 224, 200),
          8: (242, 177, 121),
          16: (245, 149, 99),
          32: (246, 124, 95),
          64: (246, 94, 59),
          128: (237, 207, 114),
          256: (237, 204, 97),
          512: (237, 200, 80),
          1024: (237, 197, 63),
          2048: (237, 194, 46),
          'light text': (249, 246, 242),
          'dark text': (119, 110, 101),
          'other': (0, 0, 0),
          'bg': (187, 173, 160)}

# game variables initialize
tales_number = 6
board_values = [[0 for _ in range(6)] for _ in range(6)]
game_over = False
spawn_new = True
init_count = 0
direction = ''
score = 0
file = open('Maximum_score.txt', 'r')
init_high = int(file.readline())
file.close()
high_score = init_high
bot = False
directions = ['UP','DOWN','LEFT','RIGHT']


#class of buttons

class Button:
    def __init__(self, txt, pos):
        self.text = txt
        self.pos = pos
        self.button = pygame.rect.Rect((self.pos[0], self.pos[1]), (260, 40))

    def draw(self):
        pygame.draw.rect(screen, 'light gray', self.button, 0, 5)
        pygame.draw.rect(screen, 'dark gray', [self.pos[0], self.pos[1], 260, 40], 5, 5)
        text2 = font.render(self.text, True, 'black')
        screen.blit(text2, (self.pos[0] + 15, self.pos[1] + 7))

    def check_clicked(self):
        if self.button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return True
        else:
            return False



# draw game over and restart text
def draw_over():
    pygame.draw.rect(screen, 'black', [50, 50, 300, 100], 0, 10)
    game_over_text1 = font.render('Game Over', True, 'white')
    game_over_text2 = font.render('Press Enter to Restart', True, 'white')
    screen.blit(game_over_text1, (130, 65))
    screen.blit(game_over_text2, (70, 105))


# take your turn based on direction
def take_turn(direc, board):
    global tales_number
    global score
    merged = [[False for _ in range(10)] for _ in range(10)]
    if direc == 'UP':
        for i in range(tales_number):
            for j in range(tales_number):
                shift = 0
                if i > 0:
                    for q in range(i):
                        if board[q][j] == 0:
                            shift += 1
                    if shift > 0:
                        board[i - shift][j] = board[i][j]
                        board[i][j] = 0
                    if board[i - shift - 1][j] == board[i - shift][j] and not merged[i - shift][j] \
                            and not merged[i - shift - 1][j]:
                        board[i - shift - 1][j] *= 2
                        score += board[i - shift - 1][j]
                        board[i - shift][j] = 0
                        merged[i - shift - 1][j] = True

    elif direc == 'DOWN':
        for i in range(tales_number-1):
            for j in range(tales_number):
                shift = 0
                for q in range(i + 1):
                    if board[tales_number -1 - q][j] == 0:
                        shift += 1
                if shift > 0:
                    board[tales_number - 2 - i + shift][j] = board[tales_number -2 - i][j]
                    board[tales_number -2 - i][j] = 0
                if tales_number -1  - i + shift <= tales_number - 1:
                    if board[tales_number -2 - i + shift][j] == board[tales_number -1 - i + shift][j] and not merged[tales_number -1 - i + shift][j] \
                            and not merged[tales_number -2 - i + shift][j]:
                        board[tales_number -1 - i + shift][j] *= 2
                        score += board[tales_number -1 - i + shift][j]
                        board[tales_number -2  - i + shift][j] = 0
                        merged[tales_number -1 - i + shift][j] = True

    elif direc == 'LEFT':
        for i in range(tales_number):
            for j in range(tales_number):
                shift = 0
                for q in range(j):
                    if board[i][q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][j - shift] = board[i][j]
                    board[i][j] = 0
                if board[i][j - shift] == board[i][j - shift - 1] and not merged[i][j - shift - 1] \
                        and not merged[i][j - shift]:
                    board[i][j - shift - 1] *= 2
                    score += board[i][j - shift - 1]
                    board[i][j - shift] = 0
                    merged[i][j - shift - 1] = True

    elif direc == 'RIGHT':
        for i in range(tales_number):
            for j in range(tales_number):
                shift = 0
                for q in range(j):
                    if board[i][tales_number -1 - q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][tales_number -1 - j + shift] = board[i][tales_number -1 - j]
                    board[i][tales_number -1 - j] = 0
                if tales_number - j + shift <= tales_number -1:
                    if board[i][tales_number - j + shift] == board[i][tales_number -1 - j + shift] and not merged[i][tales_number - j + shift] \
                            and not merged[i][tales_number -1 - j + shift]:
                        board[i][tales_number - j + shift] *= 2
                        score += board[i][tales_number - j + shift]
                        board[i][tales_number -1 - j + shift] = 0
                        merged[i][tales_number - j + shift] = True
    return board


# spawn in new pieces randomly when turns start
def new_pieces(board):
    global tales_number
    count = 0
    full = False
    while any(0 in row for row in board ) and count < 1:
        row = random.randint(0, tales_number -1)
        col = random.randint(0, tales_number -1)
        if board[row][col] == 0:
            count += 1
            if random.randint(1, 10) == 10:
                board[row][col] = 4
            else:
                board[row][col] = 2
    if count < 1:
        full = True
    return board, full


# draw background for the board
def draw_board():
    global tales_number
    global bot
    pygame.draw.rect(screen, colors['bg'], [0, 0, 450, 450], 0, 10)
    score_text = font.render(f'Score: {score}', True, 'black')
    high_score_text = font.render(f'High Score: {high_score}', True, 'black')
    screen.blit(score_text, (450, 410))
    screen.blit(high_score_text, (450, 450))
    button1 = Button('4*4', (450, 20))
    button1.draw()
    button2 = Button('5*5', (450, 70))
    button2.draw()
    button3 = Button('6*6', (450, 120))
    button3.draw()
    button4 = Button('BOT', (450, 170))
    button4.draw()
    button5 = Button('Shut down BOT', (450, 220))
    button5.draw()

    if button1.check_clicked():
        tales_number = 4
    if button2.check_clicked():
        tales_number = 5
    if button3.check_clicked():
        tales_number = 6
    if button4.check_clicked():
        bot = True
    if button5.check_clicked():
        bot = False
    pass


# draw tiles for game
def draw_pieces(board):
    global tales_number
    tales_size = 300/tales_number
    tt= 20+(tales_size/2)
    for i in range(tales_number):
        for j in range(tales_number):
            value = board[i][j]
            if value > 8:
                value_color = colors['light text']
            else:
                value_color = colors['dark text']
            if value <= 2048:
                color = colors[value]
            else:
                color = colors['other']
            pygame.draw.rect(screen, color, [j * (20+tales_size) +20 , i *(tales_size+20) + 20, tales_size, tales_size], 0, 5)
            if value > 0:
                value_len = len(str(value))
                font = pygame.font.Font('freesansbold.ttf', 48 - (5 * value_len))
                value_text = font.render(str(value), True, value_color)
                text_rect = value_text.get_rect(center=(j * (tales_size+20) +tt , i * (tales_size+20)+tt))
                screen.blit(value_text, text_rect)


# main game loop
run = True
while run:
    timer.tick(fps)
    screen.fill('gray')
    draw_board()
    draw_pieces(board_values)
    if spawn_new or init_count < 2:
        board_values, game_over = new_pieces(board_values)
        spawn_new = False
        init_count += 1
    if direction != '' and not bot:
        board_values = take_turn(direction, board_values)
        direction = ''
        spawn_new = True
    if bot:
            direction = random.choice(directions)
            board_values = take_turn(direction, board_values)
            direction = ''
            spawn_new = True
    if game_over:
        draw_over()
        if high_score > init_high:
            file = open('Maximum_score.txt', 'w')
            file.write(f'{high_score}')
            file.close()
            init_high = high_score

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                direction = 'UP'
            elif event.key == pygame.K_DOWN:
                direction = 'DOWN'
            elif event.key == pygame.K_LEFT:
                direction = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                direction = 'RIGHT'
            elif event.key == pygame.K_RETURN:
                 board_values = [[0 for _ in range(6)] for _ in range(6)]
                 spawn_new = True
                 init_count = 0
                 score = 0
                 direction = ''
                 game_over = False

    if score > high_score:
        high_score = score

    pygame.display.flip()
pygame.quit()
