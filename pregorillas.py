# Text Projectile Game
# Donovan 07/16/23
import math, random, sys, pygame, time

# General setup
pygame.init()
clock = pygame.time.Clock()

# # Setting up the main window
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Pre Gorillas')
game_active = True
base_font = pygame.font.Font(None, 32)
color = pygame.Color('aliceblue')


class Gorilla(pygame.sprite.Sprite):
    def __init__(self, gorillx, gorilly, name):
        self.name = name
        img = pygame.image.load(f'graphics2/{self.name}/weirdPixelMonkey.png')
        self.image = pygame.transform.scale(img, (img.get_width() * 6, img.get_height() * 6))
        self.rect = self.image.get_rect()
        self.rect.midbottom = (gorillx, gorilly)

    def draw(self):
        screen.blit(self.image, self.rect)


#player = Gorilla((random.randint(10, 300)), 310, 'player')
#opponent = Gorilla((random.randint(400, 800)), 310, 'opponent')
player = Gorilla(50, 310, 'player')
opponent = Gorilla(700, 310, 'opponent')


# gorilla_group = pygame.sprite.Group
# gorilla_group.add(player, opponent)

class BombClass(pygame.sprite.Sprite):
    def __init__(self, x, y):
        bimg = pygame.image.load('graphics2/bomb1.png')
        self.px = x
        self.py = y
        self.image = pygame.transform.scale(bimg, (bimg.get_width() * 2, bimg.get_height() * 2))
        self.rect = self.image.get_rect()
        self.rect.center = player.rect.midright

    @staticmethod
    def bombpath(startx, starty, power, angle, time):
        vx = math.cos(angle) * power
        vy = math.sin(angle) * power

        dx = vx * bomb_time
        dy = vy * bomb_time + ((-9.8 * (bomb_time) ** 2) / 2)

        newx = round(dx + startx)
        newy = round(starty - dy)

        return (newx, newy)

    def draw(self):
        screen.blit(self.image, self.rect)


BombObject = BombClass(player.rect.right, player.rect.center[1])

class Building(pygame.sprite.Sprite):
    def __init__(self, x, y):
        buildimg = pygame.image.load('graphics2/bldg.png')
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(buildimg, (buildimg.get_width() * 1/15, buildimg.get_height() * 1/5))
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x,y)

    def draw(self):
        screen.blit(self.image, self.rect)


building1 = Building(400,310)


def findAngle(pos):
    # sX = BombObject.px
    sX = BombObject.rect.x
    # sY = BombObject.py
    sY = BombObject.rect.y
    x_pos = int(pos[0])
    y_pos = int(pos[1])

    #print(sX, x_pos)
    #print(sY, y_pos)


    try:
        angle = math.atan((sY - y_pos) / (sX - x_pos))
    except:
        angle = math.pi / 2

    if y_pos < sY and x_pos > sX:
        angle = abs(angle)
    elif pos[1] < sY and pos[0] < sX:
        angle = math.pi - angle
    elif pos[1] > sY and pos[0] < sX:
        angle = math.pi + abs(angle)
    elif pos[1] > sY and pos[0] > sX:
        angle = (math.pi * 2) - angle

    return angle

def cpuPower():
    #player_x = player.rect.center[0]
    #player_y = player.rect.center[1]
    building_x = building1.rect.topright[0]
    building_y = building1.rect.topleft[1] + 50
    cX = BombObject.rect.x
    cY = BombObject.rect.y
    #cpupower = (((9.8*((cX - player_x) ** 2) ** 0.5)) ** 0.5)
    cpupower = (((9.8 * (350)) + (9.8 * (((cX - building_x) ** 2 + (350) ** 2) ** 0.5))) ** 0.5)
    #print('bomb x bomb y =', cX, cY)
    print('distance between CPU bomb and player =', (cX - player.rect.center[0]))
    print('buliding height =',building1.rect.bottomright[1] - building1.rect.topright[1])

    #print('player rect top =', player.rect.top)
    #print('player rect center =', player.rect.center)

    return cpupower

def cpuAngle():
    cX = BombObject.rect.x
    cY = BombObject.rect.y

    try:
        cpuangle = math.atan((cpuPower() ** 2)/(9.8 * (cX - player.rect.x)))
    except:
        cpuangle = math.pi / 2

    if building1.rect.topleft[1] < cY and building1.rect.topleft[0] > cX:
        cpuangle = abs(cpuangle)
    elif building1.rect.topleft[1] < cY and building1.rect.topleft[0] < cX:
        cpuangle = math.pi - cpuangle
    elif building1.rect.topleft[1] > cY and building1.rect.topleft[0] < cX:
        cpuangle = math.pi + abs(cpuangle)
    elif building1.rect.topleft[1] > cY and building1.rect.topleft[0] > cX:
        cpuangle = (math.pi * 2) - cpuangle
    return cpuangle

def rangefunction(power, angle):
    range = (power ** 2) * (math.sin(2 * angle)) / 9.81
    print('range =', range)
    print('power, angle', power, angle)

def cpurange(power, angle):
    range = (power ** 2) * (math.sin(2 * angle)) / 9.81
    print('range = ',range)
    done = 0
    dx = 0.001
    while not done:
        power_new = power - dx
        range_new = (power_new ** 2) * (math.sin(2 * angle)) / 9.81
        if range_new <= ((player.rect.x - BombObject.rect.x) - 10) and range_new >= ((player.rect.x - BombObject.rect.x) + 10):
            print('new range', range_new)
            done = 1

    return power_new







# Groups
# opp_collision_surf = base_font.render('The opponent has been struck!', True, (111, 196, 169))
#     player_collision_surf = base_font.render('The player has been struck!', True, (111, 196, 169))
# screen.blit(opp_collision_surf, (0, 0))
#         time.sleep(1)
# screen.blit(player_collision_surf, (0, 0))
#         time.sleep(1)

# Background
sky_surface = pygame.image.load('graphics/Sky.png')
ground_surface = pygame.image.load('graphics/ground.png')

# game variables
# initial game state
gorilla_go = 1
# is the bomb in the air? variable
bomb_time = 0
banana = False
power = 0
angle = 0
hrange = 0

def collision_mech():
    opp_collision = pygame.Rect.colliderect(BombObject.rect, opponent.rect)
    player_collision = pygame.Rect.colliderect(BombObject.rect, player.rect)
    building_collision = pygame.Rect.colliderect(BombObject.rect, building1.rect)

    global banana, bomb_time, gorilla_go
    if opp_collision:
        banana = False
        bomb_time = 0
        gorilla_go = 3
        print('oppcollision', opp_collision)


    if player_collision:
        banana = False
        bomb_time = 0
        gorilla_go = 1
        print('playercollision', player_collision)

    if building_collision:
        banana = False
        bomb_time = 0
        gorilla_go = 1
        print('buildingcolission', building_collision)


# Game Loop
while True:

    if banana:
        if BombObject.rect.bottom < 300 and BombObject.rect.right < 800 and BombObject.rect.left > 0:
            bomb_time += 1 / 60
            po = BombClass.bombpath(x, y, power, angle, bomb_time)
            # BombObject.px = po[0]
            # BombObject.py = po[1]
            BombObject.rect.x = po[0]
            BombObject.rect.y = po[1]
            if bomb_time >= 15:
                banana = False
                gorilla_go = 1
                bomb_time = 0
            if BombObject.rect.bottom >= 300 or BombObject.rect.top < -200:
                banana = False
                gorilla_go += 1
                bomb_time = 0

        else:
            banana = False
            bomb_time = 0
            # BombObject.py = 310
            BombObject.rect.y = 280


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if banana == False and gorilla_go == 1:
                x = player.rect.right
                y = player.rect.center[1]
                pos = pygame.mouse.get_pos()
                banana = True
                power = math.sqrt((line[1][1] - line[0][1]) ** 2 + (line[1][0] - line[0][0]) ** 2)
                angle = findAngle(pos)
                gorilla_go = 2
                #print('player angle, power', angle, power)
                print(rangefunction(power, angle))
            # if banana == False and gorilla_go == 3:
                # x = opponent.rect.left - 35
                # y = opponent.rect.center[1]
                # banana = True
                # power = random.randint(50,100)
                # angle = random.uniform(1.57, 3.14)
                # gorilla_go = 2
                # print(angle, power)


    line = [(BombObject.rect.right, BombObject.rect.top), pygame.mouse.get_pos()]



    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        player.draw()
        opponent.draw()
        building1.draw()



    if gorilla_go == 1:
        #BombObject.px = player.rect.right
        #BombObject.py = player.rect.center[1]
        BombObject.rect.x = player.rect.right
        BombObject.rect.y = player.rect.center[1]
        BombObject.draw()
        text_surface1 = base_font.render('Click to fire.', True, (111, 196, 169))
        screen.blit(text_surface1, (0, 0))
        pygame.draw.line(screen, (255, 255, 255), line[0], line[1])



    if gorilla_go == 2:
        BombObject.draw()
        collision_mech()


    if gorilla_go == 3:
        BombObject.rect.x = opponent.rect.left - 35
        BombObject.rect.y = opponent.rect.center[1]
        x = opponent.rect.left - 35
        y = opponent.rect.center[1]
        banana = True
        power = cpuPower()
        angle = cpuAngle()
        time.sleep(1.5)
        gorilla_go = 2
        #print('cpu angle, power', angle, power)
        print(rangefunction(power, angle))
        text_surface3 = base_font.render('Your Opponent Is Firing.', True, (111, 196, 169))
        screen.blit(text_surface3, (0, 0))
        BombObject.draw()



    pygame.display.update()
    clock.tick(60)
