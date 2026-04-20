import pygame
import sys
import random
from pygame.locals import *

pygame.init()

WIDTH = 400
HEIGHT = 600
SPEED = 5
COINS_COLLECTED = 0

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")
clock = pygame.time.Clock()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 80))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, WIDTH-40), 0)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > HEIGHT:
            self.rect.top = 0
            self.rect.center = (random.randint(40, WIDTH-40), 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.image, YELLOW, (15, 15), 15)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, WIDTH-40), -50)
        
    def move(self):
        self.rect.move_ip(0, 3) 
        if self.rect.top > HEIGHT:
            self.rect.top = -50
            self.rect.center = (random.randint(40, WIDTH-40), -50)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 80))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 100)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

P1 = Player()
E1 = Enemy()
C1 = Coin()

enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.fill(WHITE)
    
    pygame.draw.rect(DISPLAYSURF, BLACK, (WIDTH//4, 0, 2, HEIGHT))
    pygame.draw.rect(DISPLAYSURF, BLACK, (WIDTH//2, 0, 2, HEIGHT))
    pygame.draw.rect(DISPLAYSURF, BLACK, (WIDTH*3//4, 0, 2, HEIGHT))

    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)

    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.draw.rect(DISPLAYSURF, RED, (0, HEIGHT//2-50, WIDTH, 100))
        DISPLAYSURF.blit(game_over, (30, HEIGHT//2-30))
        pygame.display.update()
        import time
        time.sleep(2)
        pygame.quit()
        sys.exit()

    collected = pygame.sprite.spritecollide(P1, coins, False)
    if collected:
        COINS_COLLECTED += 1
        C1.rect.top = -50
        C1.rect.center = (random.randint(40, WIDTH-40), -50)

    score_text = font_small.render(f"Coins: {COINS_COLLECTED}", True, BLACK)
    DISPLAYSURF.blit(score_text, (WIDTH - 120, 10))

    pygame.display.update()
    clock.tick(60)