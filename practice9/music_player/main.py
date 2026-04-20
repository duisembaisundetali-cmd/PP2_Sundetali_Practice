import pygame
import sys
import os
import glob
from player import MusicPlayer

def main():
    pygame.init()
    screen = pygame.display.set_mode((500, 300))
    pygame.display.set_caption("Music Player")
    font = pygame.font.SysFont(None, 36)
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    track_dir = os.path.join(base_dir, "music", "sample_tracks")
    track_files = sorted(glob.glob(os.path.join(track_dir, "*.wav")))
    
    player = MusicPlayer(track_files)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    player.play()
                elif event.key == pygame.K_s:
                    player.stop()
                elif event.key == pygame.K_n:
                    player.next_track()
                elif event.key == pygame.K_b:
                    player.prev_track()
                elif event.key == pygame.K_q:
                    running = False
                    
        screen.fill((30, 30, 30))
        
        info_text = player.get_info()
        text_surface = font.render(info_text, True, (255, 255, 255))
        screen.blit(text_surface, (20, 130))
        
        ctrl_text = font.render("P:Play S:Stop N:Next B:Prev Q:Quit", True, (150, 150, 150))
        screen.blit(ctrl_text, (20, 250))
        
        pygame.display.flip()
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()