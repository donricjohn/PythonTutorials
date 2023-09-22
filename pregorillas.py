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


player = Gorilla((random.randint(10, 300)), 310, 'player')
opponent = Gorilla((random.randint(400, 800)), 310, 'opponent')


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


def findAngle(pos):
    # sX = BombObject.px
    sX = BombObject.rect.x
    # sY = BombObject.py
    sY = BombObject.rect.y
    x_pos = int(pos[0])
    y_pos = int(pos[1])

    print(sX)
    print(sY)

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

    global banana, bomb_time, gorilla_go
    if opp_collision:
        banana = False
        bomb_time = 0
        gorilla_go = 3

    if player_collision:
        banana = False
        bomb_time = 0
        gorilla_go = 1


# Game Loop
while True:

    if banana and gorilla_go == 2:
        if BombObject.rect.bottom < 300 and BombObject.rect.right <800 and BombObject.rect.left > 0:
            bomb_time += 1 / 60
            po = BombClass.bombpath(x, y, power, angle, bomb_time)
            # BombObject.px = po[0]
            # BombObject.py = po[1]
            BombObject.rect.x = po[0]
            BombObject.rect.y = po[1]
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
            if banana == False and gorilla_go == 3:
                x = opponent.rect.left
                y = opponent.rect.center[1]
                pos = pygame.mouse.get_pos()
                banana = True
                power = 3
                angle = findAngle(pos)
                gorilla_go = 2
    line = [(BombObject.rect.right, BombObject.rect.top), pygame.mouse.get_pos()]



    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        player.draw()
        opponent.draw()

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
        BombObject.rect.x = opponent.rect.left
        BombObject.rect.y = opponent.rect.center[1]
        text_surface3 = base_font.render('Your Opponent Is Firing.', True, (111, 196, 169))
        screen.blit(text_surface3, (0, 0))
        BombObject.draw()


    pygame.display.update()
    clock.tick(60)
