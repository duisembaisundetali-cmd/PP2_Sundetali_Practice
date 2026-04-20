import pygame
import math
import os

class Clock:
    def __init__(self, screen_size):
        self.center = (screen_size[0] // 2, screen_size[1] // 2)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        self.right_hand_img = pygame.image.load(os.path.join(base_dir, "images", "right_hand.png"))
        self.left_hand_img = pygame.image.load(os.path.join(base_dir, "images", "left_hand.png"))
        
    def draw(self, surface, current_time):
        surface.fill((255, 255, 255))
        
        pygame.draw.circle(surface, (200, 200, 200), self.center, 200, 5)
        for i in range(12):
            angle = math.radians(i * 30 - 90)
            x = self.center[0] + math.cos(angle) * 180
            y = self.center[1] + math.sin(angle) * 180
            pygame.draw.circle(surface, (50, 50, 50), (int(x), int(y)), 5)
            
        minutes = current_time.tm_min
        seconds = current_time.tm_sec
        
        minute_angle = -(minutes * 6 + (seconds / 60.0) * 6)
        second_angle = -(seconds * 6)
        
        self._blit_rotated(surface, self.right_hand_img, self.center, minute_angle)
        self._blit_rotated(surface, self.left_hand_img, self.center, second_angle)
        
        pygame.draw.circle(surface, (0, 0, 0), self.center, 10)
        
    def _blit_rotated(self, surface, image, center, angle):
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center=image.get_rect(center=center).center)
        surface.blit(rotated_image, new_rect)