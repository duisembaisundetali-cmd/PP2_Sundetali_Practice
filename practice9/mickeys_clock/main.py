import pygame
import sys
import time
from clock import Clock

def main():
    pygame.init()
    
    screen_size = (600, 600)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Mickey's Clock")
    
    clock_timer = pygame.time.Clock()
    mickey_clock = Clock(screen_size)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        current_time = time.localtime()
        mickey_clock.draw(screen, current_time)
        pygame.display.flip()
        clock_timer.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()