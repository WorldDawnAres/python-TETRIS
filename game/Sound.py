import pygame
import sys,os

# 初始化pygame
pygame.init()
pygame.mixer.init()

# 设置窗口大小
s_width = 800
s_height = 700

def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# 创建一个窗口
win = pygame.display.set_mode((s_width, s_height))

class sound:
    # 设置音乐播放按钮的尺寸和位置
    button_width = 100
    button_height = 50
    button_x = (20)
    button_y = (20)

    # 设置音乐播放按钮的背景颜色和边框颜色
    button_bg_color = (0, 0, 255)
    button_border_color = (0, 0, 0)

    # 创建一个音乐播放按钮的Surface对象
    button_surface = pygame.Surface((button_width, button_height))

    # 绘制音乐播放按钮的背景
    button_surface.fill(button_bg_color)

    # 设置音乐播放按钮的文本
    button_text = "播放"
    font = pygame.font.Font(get_resource_path("fonts/font1.ttf"), 35)
    text_surface = font.render(button_text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.center = (button_width / 2, button_height / 2)
    button_surface.blit(text_surface, text_rect)

    # 设置音乐播放按钮的可见性
    button_visible = True

    # 创建一个暂停按钮的Surface对象
    pause_button_surface = pygame.Surface((button_width, button_height))

    # 绘制暂停按钮的背景
    pause_button_surface.fill(button_bg_color)

    # 设置暂停按钮的文本
    pause_button_text = "停止"
    pause_font = pygame.font.Font(get_resource_path("fonts/font1.ttf"), 35)
    pause_text_surface = pause_font.render(pause_button_text, True, (255, 255, 255))
    pause_text_rect = pause_text_surface.get_rect()
    pause_text_rect.center = (button_width / 2, button_height / 2)
    pause_button_surface.blit(pause_text_surface, pause_text_rect)

    # 设置暂停按钮的可见性
    pause_button_visible = False

    # 加载音频文件
    pygame.mixer.music.load(get_resource_path("picture/music.mp3"))

def menu_1():
    overlay = pygame.Surface((300, 120))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(128)
    if sound.button_visible:
        win.blit(sound.button_surface, (sound.button_x, sound.button_y))
    if sound.pause_button_visible:
        win.blit(sound.pause_button_surface, (sound.button_x+120, sound.button_y ))