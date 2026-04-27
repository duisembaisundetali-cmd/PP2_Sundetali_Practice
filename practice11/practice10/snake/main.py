import pygame, sys, random
from pygame.locals import *

pygame.init()

CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
WIDTH = CELL_SIZE * GRID_WIDTH
HEIGHT = CELL_SIZE * GRID_HEIGHT

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Verdana", 18)

class Snake:
    def __init__(self):
        self.body = [(10, 10), (9, 10), (8, 10)]
        self.direction = (1, 0)
        self.grow = False
        
    def update(self):
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        
        self.body.insert(0, new_head)
        
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
            
    def draw(self, surface):
        for segment in self.body:
            rect = pygame.Rect(segment[0]*CELL_SIZE, segment[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, GREEN, rect)

class Food:
    def __init__(self, snake_body):
        self.position = (0,0)
        self.randomize_position(snake_body)
        
    def randomize_position(self, snake_body):
        while True:
            pos = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
            if pos not in snake_body:
                self.position = pos
                break
                
    def draw(self, surface):
        rect = pygame.Rect(self.position[0]*CELL_SIZE, self.position[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(surface, RED, rect)

def main():
    snake = Snake()
    food = Food(snake.body)
    
    score = 0
    level = 1
    base_fps = 8
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_UP and snake.direction != (0, 1):
                    snake.direction = (0, -1)
                elif event.key == K_DOWN and snake.direction != (0, -1):
                    snake.direction = (0, 1)
                elif event.key == K_LEFT and snake.direction != (1, 0):
                    snake.direction = (-1, 0)
                elif event.key == K_RIGHT and snake.direction != (-1, 0):
                    snake.direction = (1, 0)
                    
        snake.update()
        
        head_x, head_y = snake.body[0]
        if head_x < 0 or head_x >= GRID_WIDTH or head_y < 0 or head_y >= GRID_HEIGHT:
            print(f"Game Over! You hit a wall. Score: {score}")
            pygame.quit()
            sys.exit()
            
        if snake.body[0] in snake.body[1:]:
            print(f"Game Over! You hit yourself. Score: {score}")
            pygame.quit()
            sys.exit()
            
        if snake.body[0] == food.position:
            snake.grow = True
            score += 10
            food.randomize_position(snake.body)
            
            if score % 30 == 0:
                level += 1
                base_fps += 2
                
        DISPLAYSURF.fill(BLACK)
        snake.draw(DISPLAYSURF)
        food.draw(DISPLAYSURF)
        
        score_txt = font.render(f"Score: {score}", True, WHITE)
        level_txt = font.render(f"Level: {level}", True, WHITE)
        DISPLAYSURF.blit(score_txt, (10, 10))
        DISPLAYSURF.blit(level_txt, (10, 30))
        
        pygame.display.update()
        clock.tick(base_fps)

if __name__ == "__main__":
    main()