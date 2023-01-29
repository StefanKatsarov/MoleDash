import random
import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 400, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
VEL = 3

SCORE_FONT = pygame.font.SysFont('comicsans', 20)

pygame.display.set_caption('Mole hunter')

mole = pygame.image.load("mole_png.png").convert_alpha()
mole = pygame.transform.scale(mole, (70, 70))

carrot = pygame.image.load('carrot.png').convert_alpha()
carrot = pygame.transform.scale(carrot, (40, 40))
carrot_rect = carrot.get_rect()

TERRAIN = pygame.image.load('terrain_og.jpg').convert_alpha()
TERRAIN_HEIGHT = TERRAIN.get_height()
bg_rect = TERRAIN.get_rect()

tiles = 3
CARROT_SPAWN = pygame.USEREVENT + 1
CARROT_EATEN = pygame.USEREVENT + 2
pygame.time.set_timer(CARROT_SPAWN, 1500)
carrots = []


def carrots_movement(carrots, player):
    if carrots:
        for carr in carrots:
            carr.y += VEL
            if player.colliderect(carr):
                carrots.remove(carr)
                pygame.event.post(pygame.event.Event(CARROT_EATEN))

            screen.blit(carrot, carr)
        return carrots
    else:
        return []


def draw_window(player, scroll, carrots, score):
    for i in range(0, tiles):
        screen.blit(TERRAIN, (0, i * TERRAIN_HEIGHT + scroll))
    score_to_draw = SCORE_FONT.render('Score: ' + str(score), True, 'black')
    screen.blit(score_to_draw, (160, 15))
    screen.blit(mole, (player.x, player.y))
    carrots = carrots_movement(carrots, player)
    pygame.display.update()


def mole_movement(keys_pressed, player):
    if keys_pressed[pygame.K_a] and player.x > 0:  # LEFT
        player.x -= VEL
    if keys_pressed[pygame.K_w] and player.y > 0:  # UP
        player.y -= VEL
    if keys_pressed[pygame.K_s] and player.y <= HEIGHT - 70:  # DOWN
        player.y += VEL
    if keys_pressed[pygame.K_d] and player.x <= WIDTH - 70:  # RIGHT
        player.x += VEL


def main():
    player = pygame.Rect(100, 300, mole.get_width(), mole.get_height())
    clock = pygame.time.Clock()
    run = True
    scroll = 0
    score = 0
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == CARROT_SPAWN:
                carrots.append(carrot.get_rect(midtop=(random.randint(0, WIDTH), 0)))
            if event.type == CARROT_EATEN:
                score += 1
        keys_pressed = pygame.key.get_pressed()
        mole_movement(keys_pressed, player)
        draw_window(player, scroll, carrots, score)

        scroll -= 3
        if abs(scroll) > TERRAIN_HEIGHT:
            scroll = 0

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
