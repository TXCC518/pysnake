import sys

from setting import *


class MyGame:
    """pygame模板类"""

    def __init__(self, **kwargs):
        """初始化

            可选参数：
                game_name       游戏名称
                icon            图标文件名
                screen_size     画面大小
                display_mode    显示模式
                loop_speed      主循环速度
                font_name       字体文件名
                font_size       字体大小
        """
        # pygame初始化
        pygame.init()
        # 音效初始化
        pygame.mixer.init()
        self.game_name = kwargs.get('game_name')  # 游戏名称
        pygame.display.set_caption(self.game_name)
        self.screen_size = kwargs.get('screen_size')  # 游戏窗口尺寸
        self.screen_width, self.screen_height = self.screen_size
        self.display_mode = kwargs.get('display_mode')  # 游戏模式
        self.icon = kwargs.get('icon') or None  # 游戏图标
        self.icon and pygame.display.set_icon(pygame.image.load(self.icon))  # 加载游戏图标
        self.screen = pygame.display.set_mode(self.screen_size, self.display_mode)  # 加载游戏窗口
        self.loop_speed = kwargs.get('loop_speed')  # 主循环速度
        self.font_name = kwargs.get('font_name')  # 字体
        self.font_size = kwargs.get('font_size')
        self.font = pygame.font.Font(self.font_name, self.font_size)  # 加载字体文件
        self.clock = pygame.time.Clock()  # 加载游戏时间
        self.now = 0  # 游戏运行时间
        self.background = pygame.Surface(self.screen_size)  # 背景，方格线
        self.key_bindings = {}
        self.add_key_binding(KEY_PAUSE, self.pause)  # 按键与函数绑定字典
        self.game_actions = {}  # 游戏数据更新动作
        self.draw_actions = [self.draw_background]  # 画面更新动作列表
        self.running = True  # 控制游戏暂停、开始
        self.draw = pygame.draw

    def run(self):
        """主循环"""
        while True:
            self.now = pygame.time.get_ticks()  # 获取游戏运行时间
            self.process_events()  # 按键绑定函数
            if self.running:  # 如果游戏运行中，更新游戏数据
                self.update_gamedata()
            self.update_display()  # 更新游戏画面
            self.clock.tick(self.loop_speed)  # 游戏主循环速度

    def pause(self):
        """按键p暂停游戏"""
        self.running = not self.running  # 暂停变为运行， 运行变为暂停
        if self.running:  # 从暂停变为运行，修改下次游戏数据更新的时间
            for name, action in self.game_actions.items():
                if action['next_time']:
                    action['next_time'] = self.now + action['interval']

    def process_events(self):
        """事件处理"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 关闭游戏窗口
                self.quit()
            elif event.type == pygame.KEYDOWN:  # 游戏中按键按下执行函数
                action, kwargs = self.key_bindings.get(event.key, (None, None))
                action(**kwargs) if kwargs else action() if action else None

    def update_gamedata(self):
        """更新游戏数据"""
        for action in self.game_actions.values():
            if not action['next_time']:  # 第一次运行游戏
                action['run']()
            elif self.now >= action['next_time']:  # 是否到更新游戏数据的时间
                action['next_time'] += action['interval']
                action['run']()

    def update_display(self):
        """更新画面显示"""
        for action in self.draw_actions:
            action()
        pygame.display.flip()

    def draw_background(self):
        """绘制背景"""
        self.screen.blit(self.background, (0, 0))

    def add_key_binding(self, key, action, **kwargs):
        """增加按键绑定"""
        self.key_bindings[key] = action, kwargs

    # 更新动作若有次序要求，用字典保存不合适
    def add_game_action(self, name, action, interval=0):
        """添加游戏数据更新动作"""
        next_time = self.now + interval if interval else None
        self.game_actions[name] = dict(run=action, interval=interval, next_time=next_time)

    def add_draw_action(self, action):
        """添加更新游戏画面函数"""
        self.draw_actions.append(action)

    def draw_text(self, text, loc, color, bgcolor=None):
        """在游戏窗口中绘制游戏信息"""
        if bgcolor:
            surface = self.font.render(text, True, color, bgcolor)
        else:
            surface = self.font.render(text, True, color)
        self.screen.blit(surface, loc)

    def draw_cell(self, xy, size, color1, color2=None):
        """绘制蛇身体和头部、苹果"""
        x, y = xy
        rect = pygame.Rect(x * size, y * size, size, size)
        self.screen.fill(color1, rect)
        if color2:
            self.screen.fill(color2, rect.inflate(-4, -4))

    def quit(self):
        """退出游戏"""
        pygame.quit()
        sys.exit(0)
