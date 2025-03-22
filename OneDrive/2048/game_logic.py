import random

def set_board(size = 4):
    """ایجاد صفحه بازی با اندازه مشخص و پر کردن دو خانه اول."""
    # بخش زیر خانه های صفحات را ایجاد می کند
    board = [ [0 for _ in range(size)] for _ in range(size)]
    fill_board(board)
    fill_board(board)
    return board
    # TODO: پیاده‌سازی تابع برای ایجاد صفحه بازی
    pass

def fill_board(board):
    """پر کردن خانه‌های خالی"""
    #این قسمت به صورت تصادفی بین دو و چهار یک عدد در یک خانه قرار داده و خانه را پر می کند
    empty_cells = [(i,j) for i in range(len(board)) for j in range(len(board)) if board[i][j] == 0 ]

    if empty_cells :
        i , j = random.choice(empty_cells)
        board[i][j] = 2 if random.random() < 0.9 else 4 # احتمال 90 درصد برای 2  و 10 درصد برای 4
    # TODO: پیاده‌سازی تابع برای پر کردن خانه‌های خالی
    pass




def move_left(board, score):
    """حرکت دادن کل صفحه به چپ."""
    # TODO: پیاده‌سازی تابع برای حرکت به چپ
    pass

def move_right(board, score):
    """حرکت دادن کل صفحه به راست."""
    # TODO: پیاده‌سازی تابع برای حرکت به راست
    pass

def move_up(board, score):
    """حرکت دادن کل صفحه به بالا."""
    # TODO: پیاده‌سازی تابع برای حرکت به بالا
    pass

def move_down(board, score):
    """حرکت دادن کل صفحه به پایین."""
    # TODO: پیاده‌سازی تابع برای حرکت به پایین
    pass

def board_completed(board):
    """بررسی پر شدن صفحه."""
    # TODO: پیاده‌سازی تابع برای بررسی پر شدن صفحه
    pass

def any_move(board):
    """بررسی می‌کند که آیا حرکت ممکن است یا نه."""
    # TODO: پیاده‌سازی تابع برای بررسی امکان حرکت بیشتر
    pass

def win(board):
    """بررسی برد (آیا 2048 در صفحه هست؟)"""
    # TODO: پیاده‌سازی تابع برای بررسی برد
    pass