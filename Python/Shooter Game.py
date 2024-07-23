import pygame
from sys import exit
import math
import random
import pyautogui

size = pyautogui.size()

end_game = False

WIDTH, HEIGHT = size

levels = {
    1: {"enemy_number": 15, "width": WIDTH, "height": HEIGHT},
    2: {"enemy_number": 20, "width": WIDTH - 50, "height": HEIGHT - 50},
    3: {"enemy_number": 25, "width": WIDTH - 100, "height": HEIGHT - 100},
    4: {"enemy_number": 30, "width": WIDTH - 150, "height": HEIGHT - 150},
    5: {"enemy_number": 35, "width": WIDTH - 200, "height": HEIGHT - 200},
    6: {"enemy_number": 40, "width": WIDTH - 250, "height": HEIGHT - 250},
    7: {"enemy_number": 45, "width": WIDTH - 300, "height": HEIGHT - 300},
    8: {"enemy_number": 50, "width": WIDTH - 350, "height": HEIGHT - 350},
    9: {"enemy_number": 55, "width": WIDTH - 400, "height": HEIGHT - 400},
    10: {"enemy_number": 60, "width": WIDTH - 450, "height": HEIGHT - 450},
    11: {"enemy_number": 65, "width": WIDTH - 500, "height": HEIGHT - 500},
    12: {"enemy_number": 70, "width": WIDTH - 550, "height": HEIGHT - 550},
    13: {"enemy_number": 75, "width": WIDTH - 600, "height": HEIGHT - 600},
    14: {"enemy_number": 80, "width": WIDTH - 650, "height": HEIGHT - 650},
    15: {"enemy_number": 85, "width": WIDTH - 700, "height": HEIGHT - 700},
    16: {"enemy_number": 90, "width": WIDTH - 750, "height": HEIGHT - 750},
    17: {"enemy_number": 95, "width": WIDTH - 800, "height": HEIGHT - 800},
    18: {"enemy_number": 100, "width": WIDTH - 850, "height": HEIGHT - 850},
    19: {"enemy_number": 105, "width": WIDTH - 870, "height": HEIGHT - 870},
    20: {"enemy_number": 110, "width": WIDTH - 900, "height": HEIGHT - 900},
}

level = 1

SPEED = 1.5

player_x, player_y = WIDTH // 2, HEIGHT // 2

player_health = 150

projectile_lst = []

enemy_lst = []

particle_lst = []

should_shirink = []

goingup = False
goingdown = False
goingright = False
goingleft = False

gameover = False


class Projectile:
    def __init__(self, x, y, speed, angle, size, r, g, b):
        self.x = x
        self.y = y
        self.speed = speed
        self.angle = angle
        self.size = size
        self.r = r
        self.g = g
        self.b = b
        self.shade = 255

    def update(self):

        self.x += self.speed * math.cos(self.angle) * 1.5
        self.y += self.speed * math.sin(self.angle) * 1.5

    def shirink(self):
        self.size -= 1

    def draw(self, screen):
        pygame.draw.circle(screen, pygame.Color(
            self.r, self.g, self.b, self.shade), (self.x, self.y), self.size)


def health_bar(player_health):
    global gameover
    global end_game
    if player_health <= 0:
        gameover = True
        player_health = 0
        end_game = True
    health_surface = pygame.Surface((player_health, 30))
    health_surface.fill("green")
    health_rect = health_surface.get_rect(topleft=(WIDTH - 200, 30))
    screen.blit(health_surface, health_rect)
    border = pygame.draw.rect(
        screen, "white", pygame.Rect(WIDTH - 200, 30, 150, 30), 2, 0)


def shirink(object):
    if object.size < 100:
        for _ in range(int(object.size * 3)):
            x = object.x
            y = object.y
            speed = random.uniform(0, 3)
            angle = random.uniform(-3, 3)
            size = random.uniform(0, 2)
            project = Projectile(x, y, speed, angle, size,
                                 object.r, object.g, object.b)
            particle_lst.append(project)


def calculate():
    global player_x, player_y
    mouse_x, mouse_y = pygame.mouse.get_pos()
    return math.atan2(mouse_y - player_y, mouse_x - player_x)


def create_enemy():

    lst = ["x", "y"]
    choice = random.choice(lst)
    number = random.randint(1, 2)
    x = random.randint(-50, WIDTH + 50)
    y = random.randint(-50, HEIGHT + 50)

    if choice == "x" and number == 1:
        x = -50
    elif choice == "x" and number == 2:
        x = WIDTH + 50
    elif choice == "y" and number == 1:
        y = -50
    elif choice == "y" and number == 2:
        y = HEIGHT + 50

    global player_x, player_y

    angle = math.atan2(player_y - y,  player_x - x)

    speed = SPEED - 1

    size = random.randint(10, 30)
    if size > 20:
        speed = random.uniform(0.2, 0.7)

    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    enemy = Projectile(x, y, speed, angle, size, r, g, b)
    enemy_lst.append(enemy)


def move():
    global goingup
    global goingdown
    global goingright
    global goingleft
    global player_x
    global player_y
    count = 0
    for i in [goingup, goingdown, goingright, goingleft]:
        if i == True:
            count += 1
    if count == 2:
        if goingup and goingright:
            player_x += SPEED
            player_y -= SPEED
        if goingup and goingleft:
            player_x -= SPEED
            player_y -= SPEED
        if goingdown and goingright:
            player_x += SPEED
            player_y += SPEED
        if goingdown and goingleft:
            player_x -= SPEED
            player_y += SPEED
    if count == 1:
        if goingup:
            player_y -= (2*(SPEED**2))**0.5
        if goingdown:
            player_y += (2*(SPEED**2))**0.5
        if goingright:
            player_x += (2*(SPEED**2))**0.5
        if goingleft:
            player_x -= (2*(SPEED**2))**0.5


def collide(projectile, enemy):
    projectile = pygame.Rect(projectile.x - projectile.size, projectile.y -
                             projectile.size, projectile.size*2, projectile.size*2)
    enemy = pygame.Rect(enemy.x - enemy.size, enemy.y -
                        enemy.size, enemy.size*2, enemy.size*2)
    if projectile.colliderect(enemy):
        return True
    else:
        return False


def draw():
    # caculating the angle of the enemy
    for enemy in enemy_lst:
        enemy.angle = math.atan2(player_y - enemy.y,  player_x - enemy.x)
    global enemy_count
    global count_score
    pygame.draw.circle(screen, "white", (player_x, player_y), 15)

    # Particle draw
    for pro in particle_lst:
        pro.update()
        pro.speed *= 0.985
        if pro.shade <= 5:
            particle_lst.remove(pro)
        pro.shade -= 1
        if pro.r > 1:
            pro.r -= 1
        if pro.g > 1:
            pro.g -= 1
        if pro.b > 1:
            pro.b -= 1
        pro.draw(screen)

    for enemy in should_shirink:
        if enemy[0].size > enemy[1] and enemy[0].size >= 15:
            enemy[0].size -= 0.5

    for pro in projectile_lst:
        for enemy in enemy_lst:
            if collide(pro, enemy):
                shirink(enemy)
                if enemy.size <= 20:
                    enemy_lst.remove(enemy)
                    # enemy_count -= 1
                    count_score -= 1
                else:
                    should_shirink.append([enemy, enemy.size/2])
                projectile_lst.remove(pro)
                break

    for projectile in projectile_lst:
        if projectile.x < -100 or projectile.x > WIDTH + 100 or projectile.y < -100 or projectile.y > HEIGHT + 100:
            projectile_lst.remove(projectile)
        if not gameover:
            projectile.update()
        projectile.draw(screen)

    for enemy in enemy_lst:
        if enemy.x < -100 or enemy.x > WIDTH + 100 or enemy.y < -100 or enemy.y > HEIGHT + 100:
            enemy_lst.remove(enemy)
        if not gameover:
            enemy.update()
        enemy.draw(screen)

    score_text = score.render(f"Enemy : {count_score}", True, "white")
    screen.blit(score_text, (20, 20))

    health_bar(player_health)


def check():
    global player_health, player_x, player_y, gameover, end_game

    if player_x - 10 > WIDTH or player_x + 10 < 0 or player_y - 10 > HEIGHT or player_y + 10 < 0:
        gameover = True
        end_game = True
    for enemy in enemy_lst:
        enemy = pygame.Rect(enemy.x - enemy.size, enemy.y -
                            enemy.size, enemy.size*1.5, enemy.size*1.5)
        player = pygame.Rect(player_x - 15, player_y - 15, 25, 25)
        if enemy.colliderect(player):
            player_health -= 1
            break


def reset():
    global gameover, projectile_lst, enemy_lst, particle_lst, player_health, player_y, player_x, count_score, enemy_count, level

    gameover = False
    projectile_lst = []
    enemy_lst = []
    particle_lst = []
    player_x, player_y = WIDTH // 2, HEIGHT // 2
    enemy_count += 5
    count_score = levels[level]["enemy_number"]


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
clock = pygame.time.Clock()

level_text1 = pygame.font.Font(None, 50)

level_text = level_text1.render(f"level {level}", True, "white")
level_text_rect = level_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))

restart = pygame.font.Font(None, 30)
restart_text = restart.render("(space) to restart", True, "white")

win = pygame.font.Font(None, 30)
win_text = win.render("YOU WON", True, "white")

enemy_count = 25
count_score = levels[level]["enemy_number"]
score = pygame.font.Font(None, 20)

changing = True

counter = 0

ischeck = False

while True:
    pygame.display.set_caption(f" FPS : {round(clock.get_fps())} Shooter")
    if count_score == 0:
        if level == 20:
            win_rect = win_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            screen.fill("black")
            screen.blit(win_text, win_rect)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
            pygame.display.update()
            clock.tick(120)
            continue
        ischeck = True
        gameover = True
        counter = 0
        changing = True
        if WIDTH == levels[level + 1]["width"] and HEIGHT == levels[level + 1]["height"]:
            level += 1
            enemy_count += 4
            reset()
            changing = False
        else:
            if WIDTH >= levels[level + 1]["width"]:
                WIDTH -= 1
            if HEIGHT >= levels[level + 1]["height"]:
                HEIGHT -= 1
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                goingup = True
            if event.key == pygame.K_s:
                goingdown = True
            if event.key == pygame.K_d:
                goingright = True
            if event.key == pygame.K_a:
                goingleft = True
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            if event.key == pygame.K_SPACE and gameover and end_game:
                while WIDTH < levels[1]["width"] and HEIGHT < levels[1]["height"]:
                    WIDTH += 1
                    HEIGHT += 1
                    screen = pygame.display.set_mode(
                        (WIDTH, HEIGHT), pygame.RESIZABLE)

                level = 1
                reset()
                end_game = False
                player_health = 150

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                goingup = False
            if event.key == pygame.K_s:
                goingdown = False
            if event.key == pygame.K_d:
                goingright = False
            if event.key == pygame.K_a:
                goingleft = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            radius = calculate()
            projectile = Projectile(
                player_x, player_y, SPEED+1.5, radius, 5, 255, 255, 255)
            projectile_lst.append(projectile)

    if changing:
        if level == 1:
            level_text = level_text1.render(f"level {level}", True, "white")
            level_text_rect = level_text.get_rect(
                center=(WIDTH / 2, HEIGHT / 2))
        if ischeck:
            level_text = level_text1.render(
                f"level {level + 1}", True, "white")
            level_text_rect = level_text.get_rect(
                center=(WIDTH / 2, HEIGHT / 2))

        screen.blit(level_text, level_text_rect)
        if counter == 360:
            changing = False
            gameover = False
    else:
        sscreen = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        sscreen_rect = sscreen.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        if not gameover:
            check()
            move()
            if counter % 4 == 0 and len(enemy_lst) < enemy_count and len(enemy_lst) < count_score:
                create_enemy()
            if counter % 600 == 0:
                enemy_count += 5
        draw()

        if end_game:
            restart_text_rect = restart_text.get_rect(
                center=(WIDTH / 2, HEIGHT / 2))
            screen.blit(restart_text, restart_text_rect)

        sscreen.fill((0, 0, 0, 30))
        screen.blit(sscreen, sscreen_rect)

    counter += 1

    pygame.display.update()
    clock.tick(120)
