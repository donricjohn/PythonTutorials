# Text Projectile Game
# Donovan 07/16/23
import math, random, sys, pygame

# General setup
pygame.init()
clock = pygame.time.Clock()

# # Setting up the main window
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Pre Gorillas')
game_active = True
base_font = pygame.font.Font(None,32)
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


player = Gorilla((random.randint(10,300)), 310, 'player')
opponent = Gorilla((random.randint(400,800)), 310, 'opponent')


class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y):
        bimg = pygame.image.load('graphics2/bomb1.png')
        self.image = pygame.transform.scale(bimg, (bimg.get_width() * 2, bimg.get_height() * 2))
        self.rect = self.image.get_rect()
        self.rect.center = player.rect.midright

    @staticmethod
    def bombpath(startx, starty, power, angle, time):
        vx = math.cos(angle) * power
        vy = math.sin(angle) * power

        dx = vx * bomb_time
        dy = vy * bomb_time + ((-9.8 * (bomb_time)**2)/2)

        newx = round(dx + startx)
        newy = round(starty - dy)

        return(newx,newy)

    def draw(self):
        screen.blit(self.image, self.rect)


bomb = Bomb(player.rect.right,player.rect.center)

# def collision_sprite():
#     if pygame.sprite.spritecollide(bomb.sprite,gorilla_group,False):
#         gorilla_group.empty()
#         return False
#     else: return True


def findAngle(pos):
    sX = bomb.x
    sY = bomb.y
    try:
        angle = math.atan((sY - pos[1]) / (sX - pos[0]))
    except:
        angle = math.pi/2

    if pos[1] < sY and pos[0] > sX:
        angle = abs(angle)
    elif pos[1] < sY and pos[0] < sX:
        angle = math.pi - angle
    elif pos[1] > sY and pos[0] < sX:
        angle = math.pi + abs(angle)
    elif pos[1] > sY and pos[0] > sX:
        angle = (math.pi * 2) - angle

    return angle

# Groups



# Background
sky_surface = pygame.image.load('graphics/Sky.png')
ground_surface = pygame.image.load('graphics/ground.png')

# game variables
# initial game state
gorilla_go = 1
# is the bomb in the air? variable
banana = False
bomb_time = 0
power = 0
angle = 0

# Game Loop
while True:

    if banana:
        if bomb.rect.bottom < 300:
            bomb_time += 1/60
            po = Bomb.bombpath(x,y,power,angle,bomb_time)
            bomb.x = po[0]
            bomb.y = po[1]
        else:
            banana = False
            bomb.y = 310

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if banana == False:
                banana = True
                x = player.rect.right
                y = player.rect.center
                bomb_time = 0
                power = math.sqrt((line[1][1] - line[0][1])**2 + (line[1][0] - line[0][0])**2)/8
                angle = findAngle(pos)

    pos = pygame.mouse.get_pos()
    line = [(bomb.rect.right, bomb.rect.top), pos]

    if game_active:
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        player.draw()
        opponent.draw()



    if gorilla_go == 1:
        bomb.x = player.rect.right
        bomb.y = player.rect.center
        bomb.draw()
        text_surface = base_font.render('Click to fire.',True,(111,196,169))
        screen.blit(text_surface,(0,0))
        pygame.draw.line(screen, (255,255,255), line[0], line[1])






    pygame.display.update()
    clock.tick(60)





