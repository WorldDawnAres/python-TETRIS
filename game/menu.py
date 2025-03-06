import pygame,sqlite3,os,random,sys
from game import Sound

pygame.font.init()

s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 30 height per block
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

font_1="fonts/font1.ttf"

def user_1():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    row = c.fetchall()
    c.close()
    conn.close()
    return row[0][1]

# SHAPE FORMATS

S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape


class Piece(object):  # *
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


def create_grid(locked_pos={}):  # *
    grid = [[(0,0,0) for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_pos:
                c = locked_pos[(j,i)]
                grid[i][j] = c
    return grid


def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True

    return False


def get_shape():
    return Piece(5, 0, random.choice(shapes))


def draw_text_middle(surface,text,color):
    font = pygame.font.Font(get_resource_path(font_1),50)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width /2 - (label.get_width()/2), top_left_y + play_height/2 - label.get_height()/2))


def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid)):
        pygame.draw.line(surface, (128,128,128), (sx, sy + i*block_size), (sx+play_width, sy+ i*block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (sx + j*block_size, sy),(sx + j*block_size, sy + play_height))


def clear_rows(grid, locked):

    inc = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0,0,0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j,i)]
                except:
                    continue

    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)

    return inc


def draw_next_shape(shape, surface):
    font = pygame.font.Font(get_resource_path(font_1), 30)
    label = font.render('下一个是', 1, (255,0,255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*block_size, sy + i*block_size, block_size, block_size), 0)

    surface.blit(label, (sx + 10, sy - 30))


def update_score(nscore):
    score = max_score()

    with open('scores.txt', 'w') as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))


def max_score():
    file_path = 'scores.txt'
    if os.path.exists(file_path):
      with open(file_path, 'r') as f:
          lines = f.readlines()
          if lines:
              score = lines[0].strip()
          else:
              score = 0
    else:
      with open(file_path, 'x') as f:
          score = 0

    return score


def draw_window(surface, grid, score=0, last_score = 0):
    background_image = pygame.image.load(get_resource_path("picture/background2.jpg"))
    for x in range(0, s_width, background_image.get_width()):
        for y in range(0, s_height, background_image.get_height()):
            win.blit(background_image, (x, y))
    pygame.font.init()
    font = pygame.font.Font(get_resource_path(font_1), 50)
    label = font.render("俄罗斯方块", 1, (255, 0, 255))
    surface.blit(background_image, (0, 0))
    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))
    Sound.menu_1()
    # current score
    font = pygame.font.Font(get_resource_path(font_1), 25)
    label = font.render('本局分数: ' + str(score), 1, (255,0,0))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100

    surface.blit(label, (sx + 20, sy + 160))
    # last score
    label = font.render('历史最高分: ' + str(last_score), 1, (225,0,0))
    win.blit(label,(10,100))
    font = pygame.font.Font(get_resource_path(font_1), 25)
    label = font.render('用户名 ' + str(user_1()), 1, (225,0,0))
    win.blit(label,(10,70))

    font = pygame.font.Font(get_resource_path(font_1), 15)
    label = font.render("游戏的规则和操作方法", 1, (255,255,0))
    win.blit(label,(10,135))
    font = pygame.font.Font(get_resource_path(font_1), 15)
    label = font.render("游戏的目标是移动、旋转和摆放游戏", 1, (255,255,0))
    win.blit(label,(10,150))
    font = pygame.font.Font(get_resource_path(font_1), 15)
    label = font.render("自动输出的各种方块,使之排列成完", 1, (255,255,0))
    win.blit(label,(10,165))
    font = pygame.font.Font(get_resource_path(font_1), 15)
    label = font.render("整的一行或多行并且消除得分。", 1, (255,255,0))
    win.blit(label,(10,180))
    font = pygame.font.Font(get_resource_path(font_1), 15)
    label = font.render("游戏的规则和操作方法", 1, (255,255,0))
    win.blit(label,(10,195))
    font = pygame.font.Font(get_resource_path(font_1), 15)
    label = font.render("左键：方块向左移动一格", 1, (0,0,255))
    win.blit(label,(10,210))
    font = pygame.font.Font(get_resource_path(font_1), 15)
    label = font.render("右键：方块向右移动一格", 1, (0,0,255))
    win.blit(label,(10,225))
    font = pygame.font.Font(get_resource_path(font_1), 15)
    label = font.render("上键: 方块顺时针旋转90度", 1, (0,0,255))
    win.blit(label,(10,240))
    font = pygame.font.Font(get_resource_path(font_1), 15)
    label = font.render("下键：方块向下移动一格", 1, (0,0,255))
    win.blit(label,(10,255))
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)

    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)

    draw_grid(surface, grid)

def main2(win):  # *
    last_score = max_score()
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0
    score = 0

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()
            
        if level_time/1000 > 5:
            level_time = 0
            if level_time > 0.12:
                level_time -= 0.005

        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # 检查鼠标点击事件的位置
                pos = pygame.mouse.get_pos()
                if Sound.sound.button_visible and Sound.sound.button_x < pos[0] < Sound.sound.button_x + Sound.sound.button_width and Sound.sound.button_y < pos[1] < Sound.sound.button_y + Sound.sound.button_height:
                # 播放音乐
                    pygame.mixer.music.play(-1)
                    Sound.sound.button_visible = False
                    Sound.sound.pause_button_visible = True
                elif Sound.sound.pause_button_visible and Sound.sound.button_x + 120 < pos[0] < Sound.sound.button_x + 120 + Sound.sound.button_width and Sound.sound.button_y < pos[1] < Sound.sound.button_y + Sound.sound.button_height:
                    # 暂停音乐
                    pygame.mixer.music.pause()
                    Sound.sound.button_visible = True
                    Sound.sound.pause_button_visible = False 
              
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation -= 1

        shape_pos = convert_shape_format(current_piece)
        

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10

        draw_window(win, grid, score, last_score)
        draw_next_shape(next_piece, win)
        pygame.display.update()
        
        if check_lost(locked_positions):
            draw_text_middle(win, "游戏结束",(255,255,255))
            pygame.display.update()
            pygame.time.delay(3000)
            run = False
            update_score(score)
            
        
def main_menu(win):  # *
    main2(win)

win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption("俄罗斯方块")