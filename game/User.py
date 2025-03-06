import pygame,sqlite3,os,hashlib,sys
from game import menu
pygame.init()
screen_width = 800
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("游戏登录")
def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
logo=pygame.image.load(get_resource_path("picture/icon.jpg"))
pygame.display.set_icon(logo)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

font = pygame.font.Font(get_resource_path("fonts/font1.ttf"), 32)

# 定义用户管理类
class UserManagement:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_users_table()

    def create_users_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                username TEXT UNIQUE NOT NULL,
                                password TEXT NOT NULL,
                                score INTEGER NOT NULL)''')
        self.conn.commit()

    def register(self, username, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.cursor.execute("INSERT INTO users (username, password, score) VALUES (?, ?, 0)", (username, hashed_password))
        self.conn.commit()

    def login(self, username, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_password))
        user = self.cursor.fetchone()
        return user

    def update_score(self, username, score):
        self.cursor.execute("UPDATE users SET score=? WHERE username=?", (score, username))
        self.conn.commit()

    def get_score(self, username):
        self.cursor.execute("SELECT score FROM users WHERE username=?", (username,))
        score = self.cursor.fetchone()
        return score[0]

    def close(self):
        self.conn.close()

    def get_user_data():
        user = user_management.login(username,password)
        return user   


# 初始化用户管理实例
user_management = UserManagement("users.db")

# 定义用户名和密码字符串
username = ""
password = ""

# 定义当前激活的输入框，0表示用户名，1表示密码
active_input = 0

# 定义提示信息
message = ""

# 定义主循环
def User():
    global username, password, active_input, message
    running = True
    while running:
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 如果用户点击了用户名输入框
                if username_rect.collidepoint(event.pos):
                    active_input = 0
                # 如果用户点击了密码输入框
                elif password_rect.collidepoint(event.pos):
                    active_input = 1
                # 如果用户点击了登录按钮
                elif login_rect.collidepoint(event.pos):
                    # 验证用户名和密码是否正确
                    user = user_management.login(username, password)
                    if not user: 
                        message = "请输入用户名或密码！"
                    elif user:
                        message = "登录成功！"
                        menu.main_menu(screen)
                        running =False
                    else:
                        message = "用户名或密码错误，请重试！"
                # 如果用户点击了注册按钮
                elif register_rect.collidepoint(event.pos):
                    # 尝试将用户名和密码存入数据库
                    try:
                        user_management.register(username, password)
                        message = "注册成功！"
                        # 清空用户名和密码
                        username = ""
                        password = ""
                    except sqlite3.IntegrityError:
                        message = "用户名已存在，请更换！"
                    except sqlite3.Error as e:
                        message = f"数据库错误：{e}"
            if event.type == pygame.KEYDOWN:
                # 如果用户按下了退格键
                if event.key == pygame.K_BACKSPACE:
                    # 删除最后一个字符
                    if active_input == 0:
                        username = username[:-1]
                    elif active_input == 1:
                        password = password[:-1]
                else:
                    # 获取用户输入的字符
                    char = event.unicode
                    # 追加到相应的字符串中
                    if active_input == 0:
                        username += char
                    elif active_input == 1:
                        password += char

        # 清除屏幕
        screen.fill(WHITE)
        background = pygame.image.load(get_resource_path("picture/background1.jpg"))
        background = pygame.transform.smoothscale(background, screen.get_size())
        screen.blit(background, (0, 0))

        # 绘制文本
        text = font.render("游戏登录", True, (255,0,255))
        screen.blit(text, (screen_width / 2 - text.get_width() / 2, 200))
        # 绘制用户名输入框
        username_rect = pygame.Rect(300, 250, 200, 45)
        pygame.draw.rect(screen, BLACK, username_rect)
        username_text = font.render(username, True, WHITE)
        screen.blit(username_text, (username_rect.x + 5, username_rect.y + 5))

        # 绘制密码输入框
        password_rect = pygame.Rect(300, 300, 200, 45)
        pygame.draw.rect(screen, BLACK, password_rect)
        password_text = font.render("*" * len(password), True, WHITE)
        screen.blit(password_text, (password_rect.x + 5, password_rect.y + 5))

        # 绘制光标
        cursor_color = WHITE if active_input == 0 else BLACK
        cursor_x = username_rect.x + 5 + username_text.get_width() if active_input == 0 else password_rect.x + 5 + password_text.get_width()
        cursor_y = username_rect.y + 5 if active_input == 0 else password_rect.y + 5
        cursor_height = username_text.get_height() if active_input == 0 else password_text.get_height()
        pygame.draw.line(screen, cursor_color, (cursor_x, cursor_y), (cursor_x, cursor_y + cursor_height))

        # 绘制登录按钮
        login_rect = pygame.Rect(300, 350, 80, 40)
        pygame.draw.rect(screen, BLUE, login_rect)
        login_text = font.render("登录", True, WHITE)
        screen.blit(login_text, (login_rect.x + 5, login_rect.y + 5))

        # 绘制注册按钮
        register_rect = pygame.Rect(420, 350, 80, 40)
        pygame.draw.rect(screen, RED, register_rect)
        register_text = font.render("注册", True, WHITE)
        screen.blit(register_text, (register_rect.x + 5, register_rect.y + 5))

        # 绘制提示信息
        message_text = font.render(message, True, RED)
        screen.blit(message_text, (screen_width / 2 - message_text.get_width() / 2, 450))

        # 更新屏幕显示
        pygame.display.flip()