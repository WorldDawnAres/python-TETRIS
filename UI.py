import pygame,sys,os
from game import User
pygame.init()
screen_width = 800
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("俄罗斯方块")
def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
def menu():
    background_image = pygame.image.load(get_resource_path("picture/background.jpg"))
    background_image= pygame.transform.scale(background_image,(screen_width,screen_height))
    logo_image = pygame.image.load(get_resource_path("picture/icon.jpg"))
    screen.blit(background_image, (0, 0))  # 绘制背景图像

    # 绘制Logo图像
    logo_x = (screen_width - logo_image.get_width()) // 2
    logo_y = 100
    screen.blit(logo_image, (logo_x, logo_y))
    pygame.display.update()
    # 绘制"开始游戏"文字
    font = pygame.font.Font(get_resource_path("fonts/font1.ttf"), 48)
    text = font.render("开始游戏", True, (0, 0, 255))
    text_rect = text.get_rect(center=(screen_width // 2, 400))
    screen.blit(text, text_rect)
    pygame.display.flip()
    running = True  
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if text_rect.collidepoint(mouse_pos):
                    User.User()
                    running = False
    pygame.quit()
menu()