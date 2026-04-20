import pygame

class Ball:
    def __init__(self, x, y, radius, color, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = speed
        
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)
        
    def move(self, dx, dy, screen_width, screen_height):
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        if new_x - self.radius >= 0 and new_x + self.radius <= screen_width:
            self.x = new_x
        if new_y - self.radius >= 0 and new_y + self.radius <= screen_height:
            self.y = new_y