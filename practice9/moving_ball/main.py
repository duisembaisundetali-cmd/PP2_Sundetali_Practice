import pygame
import sys
from ball import Ball

def main():
    pygame.init()
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Moving Ball")
    
    ball = Ball(screen_width // 2, screen_height // 2, 25, (255, 0, 0), 20)
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    ball.move(0, -1, screen_width, screen_height)
                elif event.key == pygame.K_DOWN:
                    ball.move(0, 1, screen_width, screen_height)
                elif event.key == pygame.K_LEFT:
                    ball.move(-1, 0, screen_width, screen_height)
                elif event.key == pygame.K_RIGHT:
                    ball.move(1, 0, screen_width, screen_height)

        screen.fill((255, 255, 255))
        ball.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()