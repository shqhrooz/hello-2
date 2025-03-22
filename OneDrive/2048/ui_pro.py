import pygame
import time
import os
import sys
from data_handler import *
from game_logic import *

pygame.init() #تنظیمات اولیه pygame 
WINDOW_SIZE = 600
INFO_BAR_HEIGHT = 50
CELL_SIZE = (WINDOW_SIZE - INFO_BAR_HEIGHT) // 4
height = 600
screen = pygame.display.set_mode((height , WINDOW_SIZE))#((CELL_SIZE * 4, WINDOW_SIZE))
pygame.display.set_caption("2048")
icon_path = "icon_path.jpg"
icon_image = pygame.image.load(icon_path)
pygame.display.set_icon(icon_image)
timer = pygame.time.Clock()
fps = 60
FONT_SIZE = 36
FONT = pygame.font.SysFont("Arial" , FONT_SIZE)

music_enabled = True 

TILE_COLORS = {0: (205, 193, 180),
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
    "light text" : (249 , 246 , 242),
    "dark text" :(119 , 110 , 101),
    "other" : (0 , 0 , 0),
    "bg" : (120 , 100 , 90)}





def draw_board(screen, board, tile_colors, start_time, score):
    """رسم صفحه بازی و نوار اطلاعات."""
    pygame.draw.rect(screen , TILE_COLORS["bg"] , [ 0 , 0 , 600 , 600] , 0 , 10 )
    for i in range (4) :
        for j in range(4) :
            value = board [i][j]
            if value > 8 :
                value_color = TILE_COLORS["light text"]
            else : 
                value_color = TILE_COLORS["dark text"]
            color = TILE_COLORS.get(value , TILE_COLORS["other"])

            rect_x = j * CELL_SIZE + 10
            rect_y = i * CELL_SIZE + INFO_BAR_HEIGHT + 10 

            pygame.draw.rect(screen , color , [j * CELL_SIZE + 10 , i * CELL_SIZE + INFO_BAR_HEIGHT + 10,
                                                CELL_SIZE-20 , CELL_SIZE-20] , 0 , 5)
            
            pygame.draw.rect(screen , "black" , [j * CELL_SIZE + 10 , i * CELL_SIZE + INFO_BAR_HEIGHT + 10,
                                                CELL_SIZE-20 , CELL_SIZE-20] , 2 , 5)
            
            # نمایش مقدار خانه (عدد داخل مربع)
            if value != 0:
                font_size = 60 - (4 * len(str(value)))  # تنظیم اندازه فونت بر اساس تعداد ارقام
                font = pygame.font.Font(None, font_size)
                value_text = font.render(str(value), True, value_color)

                # تنظیم متن در مرکز کاشی
                text_rect = value_text.get_rect(center=(rect_x + (CELL_SIZE - 20) // 2, 
                                                        rect_y + (CELL_SIZE - 20) // 2))

                screen.blit(value_text, text_rect)

            elapsed_time = int(time.time() - start_time)
            time_text = FONT.render(f"Time: {elapsed_time}s", True, (255, 255, 255))
            screen.blit(time_text, (10, 10))  # قرار دادن تایمر در گوشه بالای سمت چپ

            score_text = FONT.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_text, (450, 10))  # قرار دادن امتیاز در گوشه بالا سمت راست

    # TODO: پیاده‌سازی تابع برای رسم صفحه بازی

def handle_game_events(board, start_time, data, score):

    """مدیریت رویدادهای بازی."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_game_data(board, start_time, data, score)
            pygame.quit()
            sys.exit() 
        elif event.type == pygame.KEYDOWN :
            if event.key == pygame.K_ESCAPE : # pressing the key esc
                save_game_data(board , start_time , data , score)
                homepage_loop()       
        
    return board, score
    # TODO: پیاده‌سازی تابع برای مدیریت رویدادهای بازی

import json
def save_game_data(board, start_time, data, score):
    """ذخیره اطلاعات بازی."""
    """"ذخیره ی اطلاعات برای بازگشت به صفحه ی اصلی و دوباره زدن دکمه ی ادامه """
    elapsed_time = int(time.time() - start_time) # calculate the time which is passed
    game_state = {
        "board" : board,
        "elapsed_time" : elapsed_time,
        "score" : score
    }
    with open("save_data.json" , "w") as file :
        json.dump(game_state , file)
    
    # TODO: پیاده‌سازی تابع برای ذخیره اطلاعات بازی
    pass

def check_game_status(board, start_time):
    """بررسی وضعیت بازی (برد یا باخت)."""
    # TODO: پیاده‌سازی تابع برای بررسی وضعیت بازی
    pass


def game_loop(board=None):
    """حلقه اصلی بازی."""
    try:
        with open("save_data.json", "r") as file:
            game_state = json.load(file)
            board = game_state["board"]
            elapsed_time = game_state.get("elapsed_time", 0)  # مقدار پیش‌فرض 0 اگر موجود نبود
            score = game_state["score"]

            start_time = time.time() - elapsed_time  # اصلاح start_time
    except FileNotFoundError:
        board = set_board()
        start_time = time.time()
        score = 0

    data = load_data()

    while True:
        draw_board(screen, board, TILE_COLORS, start_time, score)
        pygame.display.update()

        board, score = handle_game_events(board, start_time, data, score)

        status = check_game_status(board, start_time)
 
    # TODO: پیاده‌سازی تابع برای حلقه اصلی بازی

def get_selected_option():
    """تعیین گزینه انتخاب‌شده توسط کاربر از منو."""
    mouse_pos = pygame.mouse.get_pos()
    menu_options = ["New Game","Continue", "Records", "Quit"]
    
    # موقعیت Y هر گزینه منو
    for i, option in enumerate(menu_options):
        option_y = INFO_BAR_HEIGHT + 100 + i * 50  # محاسبه موقعیت Y گزینه
        if (WINDOW_SIZE // 2 - 100 <= mouse_pos[0] <= WINDOW_SIZE // 2 + 100) and \
           (option_y - 25 <= mouse_pos[1] <= option_y + 25):
            return option
    return None

music_enabled = True
def homepage_loop():
    """حلقه اصلی صفحه اصلی بازی."""
    setup_music()

    while True:
        screen.fill((220 , 224 , 245))
        display_title("2048")
        timer.tick(fps)

        display_menu(["New Game","Continue", "Records", "Quit"])
        display_music_status(music_enabled)
        pygame.display.update()

        handle_homepage_events()
    #TODO: پیاده‌سازی تابع برای حلقه صفحه اصلی

def setup_music():
    """تنظیمات موسیقی."""
    global music_enabled
    if music_enabled:
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load("Dmusic.mp3")
            pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.stop()
    # TODO: پیاده‌سازی تابع برای تنظیمات موسیقی
    pass

def draw_button(screen, text, font, color, hover_color, rect, hovered):
    """رسم دکمه با قابلیت hover."""
    if hovered:
        pygame.draw.rect(screen, hover_color, rect)
    else:
        pygame.draw.rect(screen, color, rect)
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)
    # TODO: پیاده‌سازی تابع برای رسم دکمه


def clear_screen():
    """پاک کردن صفحه."""
    # TODO: پیاده‌سازی تابع برای پاک کردن صفحه
    pass

def display_title(title, font_size=72):
    """نمایش عنوان بازی."""
    font = pygame.font.Font(None, font_size)
    text = font.render(title, True, (255 , 204 , 0))
    text_rect = text.get_rect(center=(WINDOW_SIZE // 2, (INFO_BAR_HEIGHT // 2) +40))
    screen.blit(text, text_rect)
    # TODO: پیاده‌سازی تابع برای نمایش عنوان
    

def display_menu(menu_options):
    """نمایش گزینه‌های منو."""
    font = pygame.font.Font(None, 48)
    mouse_x , mouse_y = pygame.mouse.get_pos()

    for i, option in enumerate(menu_options):
        text = font.render(option, True, (255 , 204 , 0))
        text_rect = text.get_rect(center=(height/2 ,INFO_BAR_HEIGHT + 100 + i * 50))
        if text_rect.collidepoint(mouse_x , mouse_y) :
            text = font.render(option , True , (0 , 0 , 250))
        screen.blit(text, text_rect)
    # TODO: پیاده‌سازی تابع برای نمایش منو

def display_music_status(music_enabled):
    """نمایش وضعیت موسیقی."""
    font = pygame.font.Font(None, 48)  # یکسان‌سازی فونت با منو
    button_font = pygame.font.Font(None, 36)  # فونت کوچکتر برای دکمه

    # محاسبه محل دکمه، درست زیر Quit
    quit_y = INFO_BAR_HEIGHT + 100 + 3 * 50  # Quit در موقعیت i=3 است
    music_y = quit_y + 50  # دکمه‌ی موسیقی را 50 پیکسل پایین‌تر قرار می‌دهیم

    # نمایش متن "Music: ON/OFF" در بالای دکمه
    status_text = f"Music: {'ON' if music_enabled else 'OFF'}"
    status_text_render = font.render(status_text, True,(255 , 204 , 0))
    status_text_rect = status_text_render.get_rect(center=(WINDOW_SIZE // 2, music_y + 40))
    screen.blit(status_text_render, status_text_rect)

    return status_text_rect   # برای بررسی کلیک روی دکمه
    # TODO: پیاده‌سازی تابع برای نمایش وضعیت موسیقی

def get_text_rect(text, font, x, y):
    """محاسبه موقعیت متن."""
    # TODO: پیاده‌سازی تابع برای محاسبه موقعیت متن
    pass

def handle_homepage_events():
    """مدیریت رویدادهای کاربر.""" 
    global music_enabled 

    button_rect = display_music_status(music_enabled)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            #handle_menu_selection(get_selected_option())

            # بررسی کلیک روی دکمه موسیقی
            if button_rect.collidepoint(mouse_x, mouse_y):

                music_enabled = not music_enabled
                setup_music()

            handle_menu_selection(get_selected_option())

    # TODO: پیاده‌سازی تابع برای مدیریت رویدادهای صفحه اصلی

def records_loop():
    """حلقه صفحه رکوردها."""
    while True:
        screen.fill((220, 224, 245))  # پس‌زمینه‌ی صفحه رکوردها
        back_button_rect = display_back_button()  # رسم دکمه‌ی "Back"

        pygame.display.update()  # بروزرسانی صفحه

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button_rect.collidepoint(event.pos):  # اگر روی "Back" کلیک شد
                    homepage_loop()  # بازگشت به صفحه اصلی
    # TODO: پیاده‌سازی تابع برای حلقه صفحه رکوردها

def display_records(top_scores):
    """نمایش رکوردها."""
    screen.fill((220, 224, 245))  # پس‌زمینه مشابه صفحه اصلی

    # نمایش دکمه‌ی برگشت
    back_button_rect = display_back_button()

    pygame.display.update()  # بروزرسانی صفحه

    return back_button_rect  # موقعیت دکمه را برمی‌گرداند
    # TODO: پیاده‌سازی تابع برای نمایش رکوردها

def display_back_button() :
    """نمایش دکمه برگشت به خانه و بررسی کلیک روی آن."""

    font = pygame.font.Font(None, 48)
    mouse_x, mouse_y = pygame.mouse.get_pos()  # دریافت موقعیت ماوس

    # تعیین رنگ دکمه (تغییر رنگ هنگام هاور)
    normal_color = (255, 204, 0)  # رنگ عادی
    hover_color = (0, 0, 250)  # رنگ هنگام هاور

    button_rect = pygame.Rect(WINDOW_SIZE // 2 - 50, WINDOW_SIZE // 2 + 100, 100, 50)  # مستطیل دکمه

    # بررسی اگر ماوس روی دکمه باشد، رنگ تغییر کند
    if button_rect.collidepoint(mouse_x, mouse_y):
        color = hover_color
    else:
        color = normal_color

    button_text = font.render("Back", True, color)
    button_text_rect = button_text.get_rect(center=button_rect.center)

    pygame.draw.rect(screen, (50, 50, 50), button_rect, border_radius=10)  # رسم مستطیل دکمه
    screen.blit(button_text, button_text_rect)  # نمایش متن دکمه


    return button_rect  # موقعیت دکمه را برمی‌گرداند
    # TODO: پیاده‌سازی تابع برای نمایش دکمه بازگشت

def handle_records_events():
    """مدیریت رویدادهای صفحه رکوردها (مانند بستن پنجره)."""
    back_button_rect = display_back_button()  # دکمه را نمایش بده و مستطیل آن را بگیر

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if back_button_rect.collidepoint(event.pos):  # بررسی کلیک روی دکمه
                homepage_loop()  # بازگشت به صفحه اصلی
    # TODO: پیاده‌سازی تابع برای مدیریت رویدادهای صفحه رکوردها

def show_message(screen, message):
    """نمایش پیام برد یا باخت روی صفحه."""
    # TODO: پیاده‌سازی تابع برای نمایش پیام
    pass

def handle_menu_selection(selected_option):
    """مدیریت انتخاب گزینه."""
    if selected_option == "New Game":
        if os.path.exists("save_data.json") :
            os.remove("save_data.json")

        game_loop()
    elif selected_option == "Records":
        records_loop()
    elif selected_option == "Quit":
        pygame.quit()
        sys.exit()
    elif selected_option == "Continue" :
        game_loop()
    # TODO: پیاده‌سازی تابع برای مدیریت انتخاب گزینه