from setting import *


class Snake:
    """贪吃蛇"""

    def __init__(self, game):
        self.game = game
        # 撞击音效
        self.sound_hit = pygame.mixer.Sound('resources/hit.wav')
        # 吃东西音效
        self.sound_eat = pygame.mixer.Sound('resources/eat.wav')
        self.game.add_draw_action(self.draw)
        self.respawn()  # 生成一条新的蛇

    def draw(self):
        # 蛇存活和死亡有不同的颜色
        skin_color = SNAKE_COLOR_SKIN if self.alive else SNAKE_COLOR_SKIN_DEAD
        body_color = SNAKE_COLOR_BODY if self.alive else SNAKE_COLOR_BODY_DEAD
        head_color = SNAKE_COLOR_HEAD if self.alive else SNAKE_COLOR_HEAD_DEAD
        # 生成身体
        for cell in self.body:
            self.game.draw_cell(cell, CELL_SIZE, skin_color, body_color)
        # 生成蛇头
        self.game.draw_cell(self.head, CELL_SIZE, skin_color, head_color)

    # 按指定按钮改变方向
    def turn(self, **kwargs):
        if self.direction in [LEFT, RIGHT] and \
                kwargs['direction'] in [UP, DOWN] or \
                self.direction in [UP, DOWN] and \
                kwargs['direction'] in [LEFT, RIGHT]:
            self.new_direction = kwargs['direction']

    # 判断下一个位置，并做出相对应的动作
    def move(self):
        if self.alive:
            # 改变方向
            self.direction = self.new_direction
            # 判断下一个位置的物体
            x, y = meeting = (self.head[0] + self.direction[0],
                              self.head[1] + self.direction[1])
            # 判断下一个位置是否是墙壁或者自己的身体
            if meeting in self.body or x not in range(COLUMNS) \
                    or y not in range(ROWS):
                self.die()
                return

            # 判断有没有吃苹果，吃了就不截断尾巴
            if meeting == (self.game.apple.x, self.game.apple.y):
                self.sound_eat.play()
                self.game.apple.drop()
                self.game.apple_counter += 1
                self.speed += 0.5
            else:
                self.body.pop()
            # 蛇头变成了身体
            self.body = [self.head] + self.body
            # 蛇头移动到新位置
            self.head = meeting

    # 设置蛇的移动速度
    def set_speed(self, speed):
        self._speed = speed
        interval = 1000 / self._speed
        self.game.add_game_action('snake.move', self.move, interval)

    def get_speed(self):
        return self._speed

    # self.speed发生改变，就改变蛇的移动速度
    speed = property(get_speed, set_speed)

    # 蛇死亡后身体和头部发生的变化
    def die(self):
        self.sound_hit.play()
        self.alive = False

    # 蛇的重生
    def respawn(self):
        """重生"""
        self.head = (SNAKE_X, SNAKE_Y)  # 头部
        self.body = [(-1, -1)] * SNAKE_BODY_LENGTH  # 身体
        self.direction = SNAKE_DIRECTION  # 方向
        self.new_direction = SNAKE_DIRECTION
        self.speed = SNAKE_SPEED  # 速度
        self.alive = True  # 是否存活
