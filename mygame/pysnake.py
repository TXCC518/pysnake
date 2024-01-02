from mygame import MyGame
from apple import Apple
from snake import Snake
from setting import *


class PySnake(MyGame):
    """贪吃蛇游戏"""

    def __init__(self):
        super(PySnake, self).__init__(game_name=GAME_NAME, icon=ICON, screen_size=SCREEN_SIZE,
                                      display_mode=DISPLAY_MODE, loop_speed=LOOP_SPEED,
                                      font_name=FONT_NAME, font_size=FONT_SIZE)
        # 绘制背景
        self.prepare_background()
        # 创建对象
        self.apple_counter = 0  # 苹果数量
        self.snake = Snake(self)  # 蛇
        self.apple = Apple(self)  # 苹果
        # 绑定按键
        self.add_key_binding(KEY_EXIT, self.quit)
        self.add_key_binding(KEY_UP, self.snake.turn, direction=UP)
        self.add_key_binding(KEY_DOWN, self.snake.turn, direction=DOWN)
        self.add_key_binding(KEY_LEFT, self.snake.turn, direction=LEFT)
        self.add_key_binding(KEY_RIGHT, self.snake.turn, direction=RIGHT)
        self.add_key_binding(KEY_RESTART, self.restart)
        # 添加绘图函数，绘制文字函数
        self.add_draw_action(self.draw_score)

    def prepare_background(self):
        """绘制背景"""
        self.background.fill(BACKGROUND_COLOR)
        # 画方格线
        for _ in range(CELL_SIZE, SCREEN_WIDTH, CELL_SIZE):
            self.draw.line(self.background, GRID_COLOR, (_, 0), (_, SCREEN_HEIGHT))
        for _ in range(CELL_SIZE, SCREEN_HEIGHT, CELL_SIZE):
            self.draw.line(self.background, GRID_COLOR, (0, _), (SCREEN_WIDTH, _))

    def restart(self):
        # 重新生成蛇
        if not self.snake.alive:
            # 苹果数量为0，重新绘制苹果
            self.apple_counter = 0
            self.apple.drop()
            # 蛇的重生
            self.snake.respawn()
            self.running = True

    def draw_score(self):
        """绘制文字"""
        text = 'Apple %d ' % self.apple_counter
        self.draw_text(text, (0, 0), (255, 255, 33))
        # GAME OVER
        if not self.snake.alive:
            self.draw_text(' GAME OVER ', (SCREEN_WIDTH / 2 - 54, SCREEN_HEIGHT / 2 - 10), (255, 33, 33), WHITE)
            self.draw_text(' press R to restart ', (SCREEN_WIDTH / 2 - 85, SCREEN_HEIGHT / 2 + 20), GREY, DARK_GREY)
        # GAME PAUSED
        if not self.running and self.snake.alive:
            self.draw_text(' GAME PAUSED ', (SCREEN_WIDTH / 2 - 55, SCREEN_HEIGHT / 2 - 10), LIGHT_GREY, DARK_GREY)


if __name__ == '__main__':
    PySnake().run()
