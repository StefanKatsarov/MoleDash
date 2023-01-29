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

shovel = pygame.image.load('shovel.png').convert_alpha()
right_shovel = pygame.transform.scale(shovel, (300, 300))
left_shovel = pygame.transform.rotate(right_shovel, 180)

TERRAIN = pygame.image.load('terrain_og.jpg').convert_alpha()
TERRAIN_HEIGHT = TERRAIN.get_height()
bg_rect = TERRAIN.get_rect()

tiles = 3

# Custom events
CARROT_SPAWN = pygame.USEREVENT + 1
CARROT_EATEN = pygame.USEREVENT + 2
RIGHT_SHOVEL_SPAWN = pygame.USEREVENT + 3
LEFT_SHOVEL_SPAWN = pygame.USEREVENT + 4

# Custom events spawn intervals
pygame.time.set_timer(CARROT_SPAWN, 1500)
pygame.time.set_timer(RIGHT_SHOVEL_SPAWN, 3000)
pygame.time.set_timer(LEFT_SHOVEL_SPAWN, 5500)

left_shovels = []
right_shovels = []


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = mole
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, HEIGHT))

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.rect.y > 0:  # UP
            self.rect.y -= VEL
        if keys[pygame.K_s] and self.rect.y <= HEIGHT - 70:  # DOWN
            self.rect.y += VEL
        if keys[pygame.K_a] and self.rect.x > 0:  # LEFT
            self.rect.x -= VEL
        if keys[pygame.K_d] and self.rect.x <= WIDTH - 70:  # RIGHT
            self.rect.x += VEL

    def update(self):
        self.player_input()


class Vegetables(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = carrot
        self.rect = self.image.get_rect(midtop=(random.randint(0, WIDTH), 0))

    def update(self):
        self.rect.y += VEL
        self.destroy()

    def destroy(self):
        if self.rect.y >= HEIGHT + 100:
            self.kill()


def collision_sprite(score):
    if pygame.sprite.spritecollide(play.sprite, veggies, True):
        score += 1
    return score


play = pygame.sprite.GroupSingle()
play.add(Player())

veggies = pygame.sprite.Group()


def shovels_movement(right_shovels, left_shovels):
    if right_shovels:
        for shov in right_shovels:
            shov.y += VEL

            screen.blit(right_shovel, shov)
    if left_shovels:
        for shov in left_shovels:
            shov.y += VEL

            screen.blit(left_shovel, shov)

    return right_shovels, left_shovels


def draw_window(scroll, score, right_shovels, left_shovels):
    for i in range(0, tiles):
        screen.blit(TERRAIN, (0, i * TERRAIN_HEIGHT + scroll))
    score_to_draw = SCORE_FONT.render('Score: ' + str(score), True, 'black')
    screen.blit(score_to_draw, (160, 15))
    right_shovels, left_shovels = shovels_movement(right_shovels, left_shovels)
    play.draw(screen)
    veggies.draw(screen)
    pygame.display.update()


def main():
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
                veggies.add(Vegetables())
            if event.type == RIGHT_SHOVEL_SPAWN:
                right_shovels.append((right_shovel.get_rect(midbottom=(WIDTH, 0))))
            if event.type == LEFT_SHOVEL_SPAWN:
                left_shovels.append((right_shovel.get_rect(midbottom=(0, 0))))
        draw_window(scroll, score, right_shovels, left_shovels)
        play.update()
        veggies.update()
        score = collision_sprite(score)

        scroll -= 3
        if abs(scroll) > TERRAIN_HEIGHT:
            scroll = 0

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
