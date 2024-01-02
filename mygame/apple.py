
from setting import *
from random import randint

class Apple:
    """苹果类"""
    def __init__(self, game):
        self.game = game
        # 苹果的位置
        self.x = self.y = 0
        # 加入绘制苹果的函数
        self.game.add_draw_action(self.draw)
        self.drop()

    def drop(self):
        # 临时变量，生成苹果不在蛇里面
        snake = self.game.snake.body + [self.game.snake.head]
        while True:
            (x, y) = randint(0, COLUMNS-1), randint(0, ROWS-1)
            # 保证苹果的位置没有蛇的身体和头
            if (x, y) not in snake:
                self.x, self.y = x, y
                break

    def draw(self):
        # 根据苹果位置绘制苹果
        self.game.draw_cell((self.x, self.y), CELL_SIZE, APPLE_COLOR_SKIN, APPLE_COLOR_BODY)