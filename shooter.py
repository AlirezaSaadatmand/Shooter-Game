import pygame
from sys import exit
import math
import random
import pyautogui

size = pyautogui.size()

WIDTH  , HEIGHT = size

SPEED = 1.5

player_x , player_y = WIDTH // 2 , HEIGHT // 2

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
    def __init__(self , x , y , speed , angle , side , size , r , g , b):
        self.x = x
        self.y = y
        self.speed = speed
        self.angle = angle
        self.side = side
        self.size = size
        self.r = r
        self.g = g 
        self.b = b
        self.shade = 255
    def update(self):
        if self.side == "left":
            self.x -= self.speed * math.cos(self.angle) * 1.5
            self.y -= self.speed * math.sin(self.angle) * 1.5
        if self.side == "right":
            self.x += self.speed * math.cos(self.angle) * 1.5
            self.y += self.speed * math.sin(self.angle) * 1.5            
    
    def shirink(self):
        self.size -= 1
    
    def draw(self , screen):
        pygame.draw.circle(screen, pygame.Color(self.r , self.g , self.b , self.shade) , (self.x , self.y), self.size)

def health_bar(player_health):
    global gameover
    if player_health <= 0:
        gameover = True
        player_health = 0
    health_surface = pygame.Surface( (player_health , 30) )
    health_surface.fill("green")
    health_rect = health_surface.get_rect(topleft = (WIDTH - 200 , 30))
    screen.blit(health_surface , health_rect)
    border = pygame.draw.rect(screen, "white", pygame.Rect(WIDTH - 200 , 30 , 150 , 30) , 2  , 0)

def shirink(object):
    for _ in range(int(object.size *3)):
        x = object.x
        y = object.y
        speed = random.uniform(0 , 3)
        angle = random.uniform(-1.5 , 1.5)
        side = random.choice(["left" , "right"])
        size = random.uniform(0  , 2)
        project = Projectile(x , y , speed , angle , side , size , object.r , object.g , object.b)
        particle_lst.append(project)

def calculate():

    x_dir = 0
    y_dir = 0
    side = ''
    global player_x , player_y
    mouse_x , mouse_y = pygame.mouse.get_pos()

    if mouse_x > player_x and mouse_y < player_y:
        x_dir = mouse_x - player_x
        y_dir = -abs(mouse_y - player_y)
        side = "right"
    if mouse_x < player_x and mouse_y < player_y:
        x_dir = -abs(mouse_x - player_x)
        y_dir = -abs(mouse_y - player_y)
        side = "left"
    if mouse_x < player_x and mouse_y > player_y:
        x_dir = -abs(mouse_x - player_x)
        y_dir = mouse_y - player_y
        side = "left"
    if mouse_x > player_x and mouse_y > player_y:
        x_dir = mouse_x - player_x
        y_dir = mouse_y - player_y
        side = "right"
    if x_dir == 0:
        x_dir = 1
    return math.radians(math.atan(y_dir / x_dir)*(180 / math.pi)) , side

def create_enemy():
    
    lst = ["x" , "y"]
    choice = random.choice(lst)
    number = random.randint(1 , 2)
    x = random.randint(-50 , WIDTH + 50)
    y = random.randint(-50 , HEIGHT + 50)
    
    if choice == "x" and number == 1 : x = -50
    elif choice == "x" and number == 2 : x = WIDTH + 50
    elif choice == "y" and number == 1 : y = -50
    elif choice == "y" and number == 2 : y = HEIGHT + 50
    
    x_dir = 1
    y_dir = 1
    side = ''
    global player_x , player_y

    if player_x > x and player_y < y:
        x_dir = player_x - x
        y_dir = -abs(player_y - y)
        side = "right"
    if player_x < x and player_y < y:
        x_dir = -abs(player_x - x)
        y_dir = -abs(player_y - y)
        side = "left"
    if player_x < x and player_y > y:
        x_dir = -abs(player_x - x)
        y_dir = player_y - y
        side = "left"
    if player_x > x and player_y > y:
        x_dir = player_x - x
        y_dir = player_y - y
        side = "right"
    angle = math.radians(math.atan(y_dir / x_dir)*(180 / math.pi))
    
    speed = SPEED -1
    size = random.randint(10 , 30)
    if size > 20 :
        speed = random.uniform(0.2 , 0.7)

    r = random.randint(0 , 255)
    g = random.randint(0 , 255)
    b = random.randint(0 , 255)
    
    enemy = Projectile(x , y , speed , angle , side , size , r , g , b)
    enemy_lst.append(enemy)
    
def move():
    global goingup
    global goingdown
    global goingright
    global goingleft
    global player_x
    global player_y
    count = 0
    for i in [goingup , goingdown , goingright , goingleft]:
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

def collide(projectile , enemy):
    projectile = pygame.Rect(projectile.x - projectile.size , projectile.y - projectile.size ,projectile.size*2 , projectile.size*2)
    enemy = pygame.Rect(enemy.x - enemy.size, enemy.y - enemy.size , enemy.size*2 , enemy.size*2)
    if projectile.colliderect(enemy):
        return True
    else:
        return False

def draw():
    global enemy_count
    global count_score
    pygame.draw.circle(screen, "white", (player_x , player_y), 15)
    
    for pro in particle_lst:
        pro.update()
        pro.speed *= 0.985
        if pro.shade <= 5 :
            particle_lst.remove(pro)
        pro.shade -= 1
        if pro.r > 1:
            pro.r -= 1
        if pro.g > 1:
            pro.g -= 1
        if pro.b > 1:
            pro.b -= 1
        pro.draw(screen)
    
    for enemy  in should_shirink:
        if enemy[0].size > enemy[1] and enemy[0].size >= 15:
            enemy[0].size -= 0.5
    
    for pro in projectile_lst:
        for enemy in enemy_lst:
            if collide(pro , enemy) :
                count_score += 100
                shirink(enemy)
                if enemy.size <=20:
                    enemy_lst.remove(enemy)
                    enemy_count -= 1
                else:
                    should_shirink.append([enemy ,enemy.size/2])
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

    score_text = score.render(f"Score : {count_score}" , True , "white")
    screen.blit(score_text , (20 , 20))
    
    health_bar(player_health)

def check():
    global player_health
    global player_x
    global player_y
    global gameover
    for enemy in enemy_lst:
        enemy = pygame.Rect(enemy.x - enemy.size, enemy.y - enemy.size , enemy.size*1.5 , enemy.size*1.5)
        player = pygame.Rect(player_x - 15 , player_y - 15 , 25 , 25)
        if enemy.colliderect(player):
            
            player_health -= 1
            break

pygame.init()
screen = pygame.display.set_mode( (WIDTH , HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Shooter")
clock = pygame.time.Clock()

enemy_count = 15
count_score = 0
score = pygame.font.Font(None , 20)

counter = 0
while True:
    sscreen = pygame.Surface( (WIDTH , HEIGHT) , pygame.SRCALPHA )
    sscreen_rect = sscreen.get_rect(center = (WIDTH / 2 , HEIGHT / 2))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                goingup = True
            if event.key == pygame.K_s :
                goingdown = True
            if event.key == pygame.K_d :
                goingright = True
            if event.key == pygame.K_a :
                goingleft = True
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            if event.key == pygame.K_SPACE and gameover:
                gameover = False
                projectile_lst = []
                enemy_lst = []
                particle_lst = []
                player_x , player_y = WIDTH // 2 , HEIGHT // 2
                count_score = 0
                enemy_count = 15
                player_health = 150
                          
        if event.type  == pygame.KEYUP:
            if event.key == pygame.K_w:
                goingup = False
            if event.key == pygame.K_s:
                goingdown = False
            if event.key == pygame.K_d:
                goingright = False
            if event.key == pygame.K_a:
                goingleft = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            radius , side = calculate()
            projectile = Projectile(player_x , player_y , SPEED+1.5 , radius , side , 5 , 255 , 255 , 255)
            projectile_lst.append(projectile)
    if not gameover:
        check()
        move()
        if counter % 4 == 0 and len(enemy_lst) < enemy_count:
            create_enemy()
        counter += 1
        if counter % 600 == 0:
            enemy_count += 5
    draw()
    sscreen.fill((0 , 0 , 0, 30))
    screen.blit(sscreen , sscreen_rect)
    
    pygame.display.update()
    clock.tick(120)