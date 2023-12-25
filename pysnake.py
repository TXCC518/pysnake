import sys
import pygame

pygame.init()   # pygame初始化
pygame.display.set_caption('pysnake')   # 更改游戏窗口标题

game_clock = pygame.time.Clock()
game_speed = 120     # 每秒刷新60帧
game_screen_width, game_screen_height = 640, 480    # 游戏画面宽、高
game_screen = pygame.display.set_mode((game_screen_width, game_screen_height))  # 绘制游戏窗口
game_running = True
game_bgcolor = 0, 0, 0   # 背景色
game_linecolor = 33, 33, 33 # 方格线
square_color = 33, 255, 33  # 小方块颜色
square_color2 = 33, 192, 33  # 小方块颜色

CELL_SIZE = 20  # 最小单元格
square_rect = pygame.Rect(0, 0, CELL_SIZE, CELL_SIZE)   # 小方块的信息，位置、尺寸大小
UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)    # 上下左右方向
square_direction = RIGHT    # 移动的方向
square_turn = RIGHT     # 临时遍历，准备改变的方向

while game_running:
    # 用户控制
    for event in pygame.event.get():    # 循环在游戏窗口中执行的事件
        if event.type == pygame.QUIT:   # 关闭窗口，退出循环
            game_running = False
        elif event.type == pygame.KEYDOWN:  # 发生了键盘按下事件
            # 按键上下左右移动，改变移动方向
            if event.key == pygame.K_UP:
                square_turn = UP
            elif event.key == pygame.K_DOWN:
                square_turn = DOWN
            elif event.key == pygame.K_LEFT:
                square_turn = LEFT
            elif event.key == pygame.K_RIGHT:
                square_turn = RIGHT
    # 更新数据
    # 保证小方块在方格线中移动
    if square_rect.x % CELL_SIZE == 0 and square_rect.y % CELL_SIZE == 0:
        square_direction = square_turn
    square_rect = square_rect.move(square_direction)
    if square_rect.left < 0:
        square_rect.left = 0
    elif square_rect.right > game_screen_width:
        square_rect.right = game_screen_width
    if square_rect.top < 0:
        square_rect.top = 0
    elif square_rect.bottom > game_screen_height:
        square_rect.bottom = game_screen_height
    # 更新画面
    game_screen.fill(game_bgcolor)  # 填充背景色
    # 画方格线
    for i in range(CELL_SIZE, game_screen_width, CELL_SIZE):
        pygame.draw.line(game_screen, game_linecolor, (i, 0), (i, game_screen_height))
    for i in range(CELL_SIZE, game_screen_height, CELL_SIZE):
        pygame.draw.line(game_screen, game_linecolor, (0, i), (game_screen_width, i))

    # 在游戏窗口中画小方块
    # pygame.draw.rect()：在游戏窗口画矩形，（游戏窗口，矩形颜色，(x轴位置, y轴位置, 长, 宽)）
    game_screen.fill(square_color, square_rect)
    game_screen.fill(square_color2, square_rect.inflate(-4, -4))

    pygame.display.flip()   # 绘制游戏窗口
    game_clock.tick(game_speed)     # 控制每秒钟循环60次

pygame.quit()
sys.exit(0)