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
user_text = ''
input_rect = pygame.Rect(0,30,140,28)
color = pygame.Color('aliceblue')
current_time = 0
bomb_time = 0
class Gorilla(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        monkey1 = pygame.image.load('graphics2/weirdPixelMonkey1.png')
        self.image = pygame.transform.scale(monkey1, (monkey1.get_width() * 6, monkey1.get_height() * 6))
        self.rect = self.image.get_rect(midbottom = (random.randint(10,300),310))



class Opponent(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        monkey = pygame.image.load('graphics2/weirdPixelMonkey.png')
        self.image = pygame.transform.scale(monkey, (monkey.get_width() * 6, monkey.get_height() * 6))
        self.rect = self.image.get_rect(midbottom = (random.randint(400,600),310))


class Bomb(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('graphics2/bomb1.png')
        self.rect = self.image.get_rect()

    def update(self):
        if gorilla_go == 3:
            self.rect.x = 10 + (power) * math.cos(theta) * bomb_time
            self.rect.y = 300 + 0.5 * 9.81 * pow(bomb_time, 2) - (power) * math.sin(theta) * bomb_time
        

# def collision_sprite():
#     if pygame.sprite.spritecollide(bomb.sprite,gorilla_group,False):
#         gorilla_group.empty()
#         return False
#     else: return True

# Groups

bomb = pygame.sprite.GroupSingle()
bomb.add(Bomb())

player = pygame.sprite.GroupSingle()
player.add(Gorilla())

opponent = pygame.sprite.GroupSingle()
opponent.add(Opponent())

# Background
sky_surface = pygame.image.load('graphics/Sky.png')
ground_surface = pygame.image.load('graphics/ground.png')

# game variables
gorilla_go = 1


# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
            else:
                user_text += event.unicode
            if event.key == pygame.K_RETURN and gorilla_go == 1:
                power = int(user_text)
                user_text = ''
                gorilla_go = 2

            if event.key == pygame.K_UP and gorilla_go == 2:
                theta = int(user_text)
                theta = math.radians(theta)
                print(theta)
                gorilla_go = 3
                user_text = ''
                bomb_time = (pygame.time.get_ticks() / 1000) - current_time



    if game_active:
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        player.draw(screen)
        opponent.draw(screen)

    current_time = (pygame.time.get_ticks() / 1000)


    if gorilla_go == 1:
        text_surface = base_font.render('Choose your power from 0-10. Press Return to confirm.',True,(111,196,169))
        screen.blit(text_surface,(0,0))
        pygame.draw.rect(screen,color,input_rect,2)
        text_surface_2 = base_font.render(user_text,True,(111,196,169))
        screen.blit(text_surface_2,(input_rect.x + 5,input_rect.y + 5))
        input_rect.w = text_surface_2.get_width() + 10

    if gorilla_go == 2:
        text_surface = base_font.render('Choose an angle from 0-90 degrees. Press Up Arrow to confirm.', True, (111, 196, 169))
        screen.blit(text_surface, (0, 0))
        pygame.draw.rect(screen, color, input_rect, 2)
        text_surface_2 = base_font.render(user_text, True, (111, 196, 169))
        screen.blit(text_surface_2, (input_rect.x + 5, input_rect.y + 5))
        input_rect.w = text_surface_2.get_width() + 10

    if gorilla_go == 3:
        bomb.draw(screen)
        bomb.update()


    pygame.display.update()
    clock.tick(60)



# Game Rectangles

# while True:
#     # Handling input
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()

    # Draw the Rectangles
    # screen.fill(bg_color)
    # pygame.draw.rect(screen, light_grey, player)
    # pygame.draw.rect(screen,light_grey, opponent)
    # pygame.draw.rect(screen, light_grey, ground)
    # pygame.draw.aaline(screen,light_grey, (screen_width/2,0), (screen_width/2, screen_height))

    # Update Window
    # pygame.display.flip()
    # clock.tick(60)



# theta = input("Player 1, choose an angle from 0-90 degrees")
# theta = int(theta)
# theta = math.radians(theta)
# print(theta)
# power = input("Player 1, choose your power from 0-10")
# power = int(power)
#
# projectile_range = ((2 * (power ** 2) * math.sin(2 * theta) ) // 9.81) + player_1_pos
# print("your projectile landed at",projectile_range,"meters")
#
# if projectile_range == player_2_pos:
#     print("BOOM! you hit!")
# else:
#     print("aw, you missed")
#
# theta = input("Player 2, choose an angle from 0-90 degrees")
# theta = int(theta)
# theta = math.radians(theta)
#
# power = input("Player 1, choose your power from 0-10")
# power = int(power)
#
# projectile_range = -((2 * (power ** 2) * math.sin(2 * theta) ) // 9.81) + player_2_pos
# print("your projectile landed at",projectile_range,"meters")
#
# if projectile_range == player_1_pos:
#     print("BOOM! you hit!")
# else:
#     print("aw, you missed")