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

right_shovel = pygame.image.load('shovel_300.png').convert_alpha()
left_shovel = pygame.transform.rotate(right_shovel, 180)

TERRAIN = pygame.image.load('terrain_og.jpg').convert_alpha()
TERRAIN_HEIGHT = TERRAIN.get_height()
bg_rect = TERRAIN.get_rect()
background_mole = pygame.image.load('full_game_over.png').convert_alpha()

tiles = 3

# Custom events
CARROT_SPAWN = pygame.USEREVENT + 1
CARROT_EATEN = pygame.USEREVENT + 2
SHOVEL_SPAWN = pygame.USEREVENT + 3


# Custom events spawn intervals
pygame.time.set_timer(CARROT_SPAWN, 1500)
pygame.time.set_timer(SHOVEL_SPAWN, 3000)


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


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type_of_shovel):
        super().__init__()
        if type_of_shovel == 'right':
            self.image = right_shovel
            self.rect = right_shovel.get_rect(midbottom=(WIDTH, 0))
        elif type_of_shovel == 'left':
            self.image = left_shovel
            self.rect = left_shovel.get_rect(midbottom=(0, 0))

    def update(self):
        self.rect.y += VEL
        self.destroy()

    def destroy(self):
        if self.rect.y >= HEIGHT + 100:
            self.kill()


def collision_sprite(score):
    if pygame.sprite.spritecollide(player.sprite, veggies, True):
        score += 1
    return score


def endgame():
    if pygame.sprite.spritecollide(player.sprite, shovels, True):
        veggies.empty()
        shovels.empty()
        return False
    return True


player = pygame.sprite.GroupSingle()
player.add(Player())

veggies = pygame.sprite.Group()
shovels = pygame.sprite.Group()


def draw_window(scroll, score):
    for i in range(0, tiles):
        screen.blit(TERRAIN, (0, i * TERRAIN_HEIGHT + scroll))
    score_to_draw = SCORE_FONT.render('Score: ' + str(score), True, 'black')
    screen.blit(score_to_draw, (160, 15))
    player.draw(screen)
    veggies.draw(screen)
    shovels.draw(screen)
    pygame.display.update()


def main():
    clock = pygame.time.Clock()
    run = True
    scroll = 0
    score = 0
    game_active = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if game_active:
                if event.type == CARROT_SPAWN:
                    veggies.add(Vegetables())
                if event.type == SHOVEL_SPAWN:
                    shovels.add(Obstacle(random.choice(['right', 'left'])))
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_active = True
        if game_active:
            draw_window(scroll, score)

            player.update()
            veggies.update()
            shovels.update()

            game_active = endgame()
            score = collision_sprite(score)

            scroll -= 3
            if abs(scroll) > TERRAIN_HEIGHT:
                scroll = 0
        else:
            screen.blit(background_mole, (0, 0))
            score = 0
            player.sprite.rect = mole.get_rect(midbottom=(WIDTH // 2, HEIGHT))
            pygame.display.update()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
