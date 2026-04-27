import pygame
import datetime
import os

class DrawingTools:
    """Класс со всеми инструментами рисования"""
    
    def __init__(self, canvas):
        self.canvas = canvas
        
    def flood_fill(self, x, y, target_color, replacement_color):
        """Flood fill алгоритм"""
        if target_color == replacement_color:
            return
        
        surface = self.canvas
        surface.lock()
        try:
            stack = [(x, y)]
            while stack:
                px, py = stack.pop()
                if px < 0 or px >= surface.get_width() or py < 0 or py >= surface.get_height():
                    continue
                if surface.get_at((px, py)) == target_color:
                    surface.set_at((px, py), replacement_color)
                    stack.append((px + 1, py))
                    stack.append((px - 1, py))
                    stack.append((px, py + 1))
                    stack.append((px, py - 1))
        finally:
            surface.unlock()
    
    def draw_rect(self, start, end, color, thickness):
        """Рисует прямоугольник"""
        r = pygame.Rect(min(start[0], end[0]), min(start[1], end[1]),
                        abs(start[0] - end[0]), abs(start[1] - end[1]))
        pygame.draw.rect(self.canvas, color, r, thickness)
    
    def draw_circle(self, start, end, color, thickness):
        """Рисует круг"""
        radius = int(((start[0] - end[0])**2 + (start[1] - end[1])**2)**0.5)
        pygame.draw.circle(self.canvas, color, start, radius, thickness)
    
    def draw_line(self, start, end, color, thickness):
        """Рисует линию"""
        pygame.draw.line(self.canvas, color, start, end, thickness)
    
    def draw_square(self, start, end, color, thickness):
        """Рисует квадрат"""
        side = max(abs(start[0] - end[0]), abs(start[1] - end[1]))
        sx = start[0] if end[0] > start[0] else start[0] - side
        sy = start[1] if end[1] > start[1] else start[1] - side
        r = pygame.Rect(sx, sy, side, side)
        pygame.draw.rect(self.canvas, color, r, thickness)
    
    def draw_right_triangle(self, start, end, color, thickness):
        """Рисует прямоугольный треугольник"""
        pygame.draw.polygon(self.canvas, color, 
                           [start, (start[0], end[1]), end], thickness)
    
    def draw_equilateral_triangle(self, start, end, color, thickness):
        """Рисует равносторонний треугольник"""
        d = ((start[0] - end[0])**2 + (start[1] - end[1])**2)**0.5
        h = d * (3**0.5) / 2
        p1 = start
        p2 = (start[0] - d/2, start[1] + h)
        p3 = (start[0] + d/2, start[1] + h)
        pygame.draw.polygon(self.canvas, color, [p1, p2, p3], thickness)
    
    def draw_rhombus(self, start, end, color, thickness):
        """Рисует ромб"""
        mx = (start[0] + end[0]) / 2
        my = (start[1] + end[1]) / 2
        p1 = (mx, start[1])
        p2 = (end[0], my)
        p3 = (mx, end[1])
        p4 = (start[0], my)
        pygame.draw.polygon(self.canvas, color, [p1, p2, p3, p4], thickness)
    
    def draw_brush(self, pos, color, size):
        """Рисует кистью (круг)"""
        pygame.draw.circle(self.canvas, color, pos, size)
    
    def draw_pencil(self, last_pos, current_pos, color, size):
        """Рисует карандашом (линия между точками)"""
        pygame.draw.line(self.canvas, color, last_pos, current_pos, size)
    
    def draw_eraser(self, pos, size):
        """Стирает (рисует белым)"""
        pygame.draw.circle(self.canvas, (255, 255, 255), pos, size)
    
    def draw_text(self, text, pos, color, font_size=32):
        """Рисует текст на холсте"""
        font = pygame.font.SysFont(None, font_size)
        text_surface = font.render(text, True, color)
        self.canvas.blit(text_surface, pos)

class SaveManager:
    """Класс для сохранения файлов"""
    
    @staticmethod
    def save_canvas(canvas):
        """Сохраняет холст в файл с timestamp"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"canvas_{timestamp}.png"
        
        # Создаём папку screenshots если её нет
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")
        
        filepath = os.path.join("screenshots", filename)
        pygame.image.save(canvas, filepath)
        print(f"Canvas saved as {filepath}")
        return filepath
    
    @staticmethod
    def save_screenshot(screen, filename="screenshot.png"):
        """Сохраняет скриншот экрана"""
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")
        filepath = os.path.join("screenshots", filename)
        pygame.image.save(screen, filepath)
        return filepath

class PreviewDrawer:
    """Класс для отрисовки предпросмотра фигур при рисовании"""
    
    @staticmethod
    def draw_preview(screen, mode, start_pos, current_pos, color, thickness):
        """Рисует предпросмотр текущей фигуры"""
        if mode == 'line':
            pygame.draw.line(screen, color, start_pos, current_pos, thickness)
        elif mode == 'rect':
            r = pygame.Rect(min(start_pos[0], current_pos[0]), 
                           min(start_pos[1], current_pos[1]),
                           abs(start_pos[0] - current_pos[0]), 
                           abs(start_pos[1] - current_pos[1]))
            pygame.draw.rect(screen, color, r, thickness)
        elif mode == 'circle':
            radius = int(((start_pos[0] - current_pos[0])**2 + 
                         (start_pos[1] - current_pos[1])**2)**0.5)
            pygame.draw.circle(screen, color, start_pos, radius, thickness)
        elif mode == 'square':
            side = max(abs(start_pos[0] - current_pos[0]), 
                      abs(start_pos[1] - current_pos[1]))
            sx = start_pos[0] if current_pos[0] > start_pos[0] else start_pos[0] - side
            sy = start_pos[1] if current_pos[1] > start_pos[1] else start_pos[1] - side
            r = pygame.Rect(sx, sy, side, side)
            pygame.draw.rect(screen, color, r, thickness)
        elif mode == 'rtriangle':
            pygame.draw.polygon(screen, color, 
                               [start_pos, (start_pos[0], current_pos[1]), current_pos], 
                               thickness)
        elif mode == 'etriangle':
            d = ((start_pos[0] - current_pos[0])**2 + 
                 (start_pos[1] - current_pos[1])**2)**0.5
            h = d * (3**0.5) / 2
            p1 = start_pos
            p2 = (start_pos[0] - d/2, start_pos[1] + h)
            p3 = (start_pos[0] + d/2, start_pos[1] + h)
            pygame.draw.polygon(screen, color, [p1, p2, p3], thickness)
        elif mode == 'rhombus':
            mx = (start_pos[0] + current_pos[0]) / 2
            my = (start_pos[1] + current_pos[1]) / 2
            p1 = (mx, start_pos[1])
            p2 = (current_pos[0], my)
            p3 = (mx, current_pos[1])
            p4 = (start_pos[0], my)
            pygame.draw.polygon(screen, color, [p1, p2, p3, p4], thickness)