import pygame
import math
from random import choice, randint


# инициализация и настройка pygame
pygame.init()
FPS = 50
clock = pygame.time.Clock()
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)

# массив объектов класса Ball
balls = []

# массив цветов
RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

# счетчики и флаги
score = 0
num_shoots = 0
wait_counter = 0
finished = False


##############################################################################################
class Target:
    def __init__(self, screen, color):
        """
        Конструктор класса Target. Задает параметры по умолчанию для движущейся мишени в виде шарика.
        screen - поверхность для рисования pygame
        color - цвет мишени
        """
        self.live = 1
        self.screen = screen
        self.points = 0
        self.x = randint(600, 780)
        self.y = randint(300, 550)
        self.vx = randint(-10, 10)
        self.vy = randint(-10, 10)
        self.r = randint(2, 50)
        self.color = color

    def new_target_params(self):
        """
        Функция обновления параметров мишени
        """
        self.x = randint(720, 740)
        self.y = randint(450, 500)
        self.vx = randint(-10, 10)
        self.vy = randint(-10, 10)
        self.r = randint(6, 40)

    def draw(self, is_live):
        """
        Функция-отрисовщик движения мишени
        is_live - флажок жизни мишени
        + отрисовка границы области движения шариков
        """
        if is_live:
            if self.x + self.r >= 800:
                self.x = 800 - self.r
                self.vx = -self.vx
            if self.x - self.r <= 500:
                self.x = self.r + 500
                self.vx = -self.vx
            if self.y - self.r <= 0:
                self.y = self.r
                self.vy = -self.vy
            if self.y + self.r >= 550 :
                self.y = 550  - self.r
                self.vy = -self.vy
                
            self.x += int(self.vx)
            self.y -= int(self.vy) - 1

            pygame.draw.circle(
                self.screen,
                self.color,
                (self.x, self.y),
                self.r
            )
        pygame.draw.line(self.screen, GREEN, (500, 800), (500, -200), 2) # граница для целей
        pygame.draw.line(self.screen, BLUE, (0, 0), (1000, 0), 3) # потолок
        pygame.draw.line(self.screen, RED, (0, 60), (1000, 60), 3) # красная линия
        pygame.draw.rect(screen, YELLOW, (0, 551,1000, 200)) # "земля"
        pygame.draw.line(self.screen, BLUE, (0, 598), (1000, 598), 3) # пол


########################################################################################################
class Ball:
    def __init__(self, screen: pygame.Surface, x = 40, y = 450) :
        """
        Конструктор класса Ball. Задает параметры шарика и его движение
        screen - поверхность отрисовки в pygame
        x - положение шарика вдоль горизонтальной оси (по умолчанию равно координате ствола пушки)
        y - положение шарика вдоль веритикальной оси (по умолчанию равно координате ствола пушки)
        """
        self.screen = screen
        self.velocity_loss = 0.25
        self.x = tank.x
        self.y = tank.y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 25
        self.gravity = -9.815 / 20



    def move(self):
        """
        Функция, задающая движение шарика и изменяющая параметры шарика во времени
        """
        self.vy += self.gravity
        if self.x + self.r >= 800:
            self.x = 800 - self.r
            self.vx = -self.vx * 0.5
        if self.x - self.r <= 0:
            self.x = self.r
            self.vx = -self.vx * 0.5
        if self.y - self.r <= 0:
            self.y = self.r
            self.vy = -self.vy * 0.5
        if self.y + self.r >= 600 - 50:
            self.y = 600 - 50 - self.r
            self.vy = -self.vy * 0.5
            self.vx = self.vx - self.velocity_loss * self.vx

        self.x += int(self.vx)
        self.y -= int(self.vy) - 1

        if self.y == 536:
            self.live -= 1
            if self.live <= 0:
                self.color = [0, 255, 255]

    def draw(self):
        """
        Функция-отрисовщик шарика.
        """
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hit_test(self, obj: Target):
        """
        Функция-обработчик попадания шарика по мишени
        obj - объект класса Target
        bool - возвращает bool - попал шарик в цель или нет
        """
        if not self.color == [0, 255, 255]:
            if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + obj.r) ** 2:
                return True
            return False
#################################################################################################
class Tank:
    DEFAULT_GUN_LENGTH = 10 # длина пушки по умолчанию
    tank_speed = 2 # скорость перемещения танка при нажатии клавиш 'A' и 'D'  (из WASD)
    
    def __init__(self, screen, x = 75, y = 492):
        """
        Конструктор класса Gun. Задает параметры пушки по умолчанию
        screen - поверхность отрисовки в pygame
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.fire_power = 10
        self.is_on = 0
        self.angle = 1
        self.color = GREY
        self.length = Tank.DEFAULT_GUN_LENGTH

    def start_shooting(self):
        """
        Поднятие флажка о начале стрельбы
        """
        self.is_on = 1

    def make_bullet(self, event):
        """
        Функция-генератор снаряда в виде шарика. Задает параметры снаряда как объекта класса Ball, вылетевшего из пушки
        event - событие pygame для детектирования положения курсора
        return - объект класса Ball
        """
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.angle = math.atan2((event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))
        new_ball.vx = self.fire_power * math.cos(self.angle)
        new_ball.vy = - self.fire_power * math.sin(self.angle)
        self.is_on = 0
        self.fire_power = 10

        return new_ball

    def aiming(self, event):
        """
        Функция для прицеливания. Задает наклон пушки к горизонту и ее цвет.
        event - событие pygame для детектирования положения компьютерной мыши
        """
        if (event) and (event.pos[1] < self.y) and (event.pos[0] > self.x):
            self.angle = math.atan((event.pos[1] - self.y) / (event.pos[0] - self.x))
        else:
            if event.pos[1] > self.y:
                self.angle = 0
            else:
                self.angle = -1.57

        if self.is_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self, screen):
        x_1 = self.x + self.length * abs(math.cos(self.angle))
        y_1 = self.y + self.length * math.sin(self.angle)
        pygame.draw.polygon(self.screen, self.color, (
            [self.x, self.y], [x_1, y_1],
            [x_1 - Tank.DEFAULT_GUN_LENGTH * math.sin(self.angle), y_1 + Tank.DEFAULT_GUN_LENGTH * math.cos(self.angle)],
            [self.x - Tank.DEFAULT_GUN_LENGTH * math.sin(self.angle), self.y + Tank.DEFAULT_GUN_LENGTH * math.cos(self.angle)]))

    def body(self, screen, r=3.8):
        """
        Функция-отрисовщик ствола пушки
        """
# рисует танк и гусеницы       
        pygame.draw.circle(self.screen, GREY, [self.x+3, self.y+3], 10)
        pygame.draw.circle(self.screen, BLACK, [self.x-13*r, self.y+13*r], 10)
        pygame.draw.circle(self.screen, BLACK, [self.x-13*r+20, self.y+13*r], 10)
        pygame.draw.circle(self.screen, BLACK, [self.x-13*r+40, self.y+13*r], 10)
        pygame.draw.circle(self.screen, BLACK, [self.x-13*r+60, self.y+13*r], 10)
        pygame.draw.circle(self.screen, BLACK, [self.x-13*r+80, self.y+13*r], 10)
        pygame.draw.polygon(self.screen, GREY, (
            [self.x, self.y],
            [self.x+5*r, self.y+5*r],
            [self.x+15*r, self.y+5*r],
            [self.x+10*r, self.y+12*r],
            [self.x-15*r, self.y+12*r],
            [self.x-20*r, self.y+5*r],
            [self.x-13*r, self.y+5*r],
            [self.x-8*r, self.y-1*r],
            [self.x-2*r, self.y-1*r] ))
        
    def power_up(self):
        """
        Функция, задающая мощность пушечного выстрела
        """
        if self.is_on:
            if self.fire_power < 100:
                self.length += 1
                self.fire_power += 1
            self.color = RED
        else:
            self.length = Tank.DEFAULT_GUN_LENGTH
            self.color = GREY
            
    def move_tank(self):
        if (keys[pygame.K_a]) and (self.x>10):
            self.x -= Tank.tank_speed
        elif (keys[pygame.K_d]) and (self.x<300):
            self.x += Tank.tank_speed
'''
class Enemy:
    def __init__(self, screen):
        self.screen = screen
        dy=0
    def draw(self, screen, i):
        traps = [ (screen, [255, 205, 0], (3, 50, 36, 30)),
            (screen, [255, 205, 0], (3+39, 50, 36, 30)),
            (screen, [255, 205, 0], (3+39*2, 50, 36, 30)),
            (screen, [255, 205, 0], (3+39*3, 50, 36, 30)),
            (screen, [255, 205, 0], (3+39*4, 50, 36, 30)),
            (screen, [255, 205, 0], (3+39*5, 50, 36, 30)),
            (screen, [255, 205, 0], (3+39*6, 50, 36, 30)),
            (screen, [255, 205, 0], (3+39*7, 50, 36, 30)),
            (screen, [255, 205, 0], (3+39*8, 50, 36, 30))
            ]
    def warning(i):
        pygame.draw.rect(screen, [200, 0, 0], (3+i*39, 50, 36, 30))
    def bombing(i):
        pygame.draw.circle(self.screen, RED, [self.x-13*r+80, 80+dy], 6)
        pygame.draw.rect(screen, [110, 110, 110], (3+i*39+12, 75, 12, 40))
        dy+=5
        
'''
        
####################################################################################################
###                           ОСНОВНАЯ ЧАСТЬ ПРОГРАММЫ                                           ###
####################################################################################################

# инициализация объектов
tank = Tank(screen)
target1 = Target(screen, RED)
target2 = Target(screen, GREEN)
#enemy = Enemy(screen)

while not finished:
    screen.fill([0, 255, 255])
    clock.tick(FPS)
   
#    if pygame.time.get_ticks()>5000:
#        if clock.get_time()>2000:
#            i = randint(9)
#            enemy.draw(trap[i])
#            enemy.warning(i)
#            fly = True
#            while fly == True:
#                enemy.bombing(i)
         
            
    keys = pygame.key.get_pressed()
    tank.move_tank()
    # обработка шариков
    for b in balls:
        b.draw()
        b.move()
        if b.hit_test(target1) and target1.live:
            score += 0.5
            target1.live = False
            target1.new_target_params()
        if b.hit_test(target2) and target2.live:
            score += 0.5
            target2.live = False
            target2.new_target_params()

    # обработка событий, пушки, мишени и текстового поля
    if target1.live or target2.live or wait_counter >= 100:
        tank.draw(screen)
        tank.body(screen)
        target1.draw(is_live=target1.live)
        target2.draw(is_live=target2.live)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                tank.start_shooting()
            elif event.type == pygame.MOUSEBUTTONUP:
                balls.append(tank.make_bullet(event))
                num_shoots += 1
            elif event.type == pygame.MOUSEMOTION:
                tank.aiming(event)

        tank.power_up()
        if wait_counter >= 100:
            target1.live = True
            target2.live = True
            num_shoots = 0
        wait_counter = 0
    else:
        text_surface = my_font.render("Вы уничтожили цели за " + str(num_shoots) + " выстрелов.", 0, (0, 0, 0))
        screen.blit(text_surface, (150, 250))
        wait_counter += 1

    # отображение очков игрока
    score_surface = my_font.render(str(score), 1, (0, 0, 0))
    screen.blit(score_surface, (10, 10))

    pygame.display.update()

pygame.quit()



























