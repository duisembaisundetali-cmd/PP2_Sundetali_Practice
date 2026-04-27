import pygame
import sys
from pygame.locals import *
from tools import DrawingTools, SaveManager, PreviewDrawer

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 650))
    pygame.display.set_caption("Paint Application - Extended Edition")
    
    # Цвета
    colors = {
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255),
        'black': (0, 0, 0),
        'white': (255, 255, 255)
    }
    
    current_color = colors['black']
    mode = 'brush'
    drawing = False
    brush_size = 5
    
    # Размеры кисти
    brush_sizes = {1: 2, 2: 5, 3: 10}
    
    # Создаём холст (600x600, так как сверху 50px под UI)
    canvas_width = 800
    canvas_height = 600
    canvas = pygame.Surface((canvas_width, canvas_height))
    canvas.fill(colors['white'])
    
    tools = DrawingTools(canvas)
    preview = PreviewDrawer()
    
    # UI элементы
    ui_rect = pygame.Rect(0, 0, 800, 50)
    
    # ВАЖНО: Все кнопки в верхней части (y от 10 до 50)
    btn_red = pygame.Rect(10, 10, 30, 30)
    btn_green = pygame.Rect(50, 10, 30, 30)
    btn_blue = pygame.Rect(90, 10, 30, 30)
    btn_black = pygame.Rect(130, 10, 30, 30)
    
    btn_brush = pygame.Rect(200, 10, 50, 30)
    btn_pencil = pygame.Rect(260, 10, 50, 30)
    btn_line = pygame.Rect(320, 10, 50, 30)
    btn_rect = pygame.Rect(380, 10, 50, 30)
    btn_circ = pygame.Rect(440, 10, 50, 30)
    btn_erase = pygame.Rect(500, 10, 50, 30)
    btn_fill = pygame.Rect(560, 10, 50, 30)
    btn_text = pygame.Rect(620, 10, 50, 30)
    
    # Вторая строка кнопок (y = 55)
    second_row_y = 55
    btn_sq = pygame.Rect(200, second_row_y, 50, 30)
    btn_rt = pygame.Rect(260, second_row_y, 50, 30)
    btn_et = pygame.Rect(320, second_row_y, 50, 30)
    btn_rh = pygame.Rect(380, second_row_y, 50, 30)
    
    btn_small = pygame.Rect(500, second_row_y, 40, 30)
    btn_medium = pygame.Rect(550, second_row_y, 50, 30)
    btn_large = pygame.Rect(610, second_row_y, 40, 30)
    
    # Область холста (y = 95, потому что 50 + 45 = 95)
    canvas_offset_y = 95
    
    font = pygame.font.SysFont(None, 22)
    
    start_pos = None
    last_pos = None
    text_input_active = False
    text_input_str = ""
    text_input_pos = None
    
    clock = pygame.time.Clock()
    running = True
    
    def get_canvas_pos(screen_pos):
        """Преобразует координаты экрана в координаты холста"""
        x, y = screen_pos
        return (x, y - canvas_offset_y)
    
    def draw_ui():
        """Отрисовка интерфейса"""
        # Фон верхней панели
        pygame.draw.rect(screen, (200, 200, 200), (0, 0, 800, 50))
        pygame.draw.rect(screen, (180, 180, 180), (0, 50, 800, 45))
        
        # Цветные кнопки
        pygame.draw.rect(screen, colors['red'], btn_red)
        pygame.draw.rect(screen, colors['green'], btn_green)
        pygame.draw.rect(screen, colors['blue'], btn_blue)
        pygame.draw.rect(screen, colors['black'], btn_black)
        
        # Обводка текущего цвета
        if current_color == colors['red']:
            pygame.draw.rect(screen, (0,0,0), btn_red, 4)
        elif current_color == colors['green']:
            pygame.draw.rect(screen, (0,0,0), btn_green, 4)
        elif current_color == colors['blue']:
            pygame.draw.rect(screen, (0,0,0), btn_blue, 4)
        elif current_color == colors['black']:
            pygame.draw.rect(screen, (0,0,0), btn_black, 4)
        else:
            pygame.draw.rect(screen, (0,0,0), btn_red, 2)
            pygame.draw.rect(screen, (0,0,0), btn_green, 2)
            pygame.draw.rect(screen, (0,0,0), btn_blue, 2)
            pygame.draw.rect(screen, (0,0,0), btn_black, 2)
        
        def draw_btn(rect, text, is_active):
            color = (100, 100, 100) if is_active else (220, 220, 220)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2)
            txt = font.render(text, True, (0, 0, 0))
            screen.blit(txt, (rect.x + 2, rect.y + 6))
        
        # Кнопки инструментов (верхний ряд)
        draw_btn(btn_brush, "Brush", mode == 'brush')
        draw_btn(btn_pencil, "Pencil", mode == 'pencil')
        draw_btn(btn_line, "Line", mode == 'line')
        draw_btn(btn_rect, "Rect", mode == 'rect')
        draw_btn(btn_circ, "Circ", mode == 'circle')
        draw_btn(btn_erase, "Erase", mode == 'eraser')
        draw_btn(btn_fill, "Fill", mode == 'fill')
        draw_btn(btn_text, "Text", mode == 'text')
        
        # Кнопки фигур (второй ряд)
        draw_btn(btn_sq, "Sqr", mode == 'square')
        draw_btn(btn_rt, "RTri", mode == 'rtriangle')
        draw_btn(btn_et, "ETri", mode == 'etriangle')
        draw_btn(btn_rh, "Rhmb", mode == 'rhombus')
        
        # Кнопки размера кисти
        small_color = (150, 150, 150) if brush_size == brush_sizes[1] else (220, 220, 220)
        medium_color = (150, 150, 150) if brush_size == brush_sizes[2] else (220, 220, 220)
        large_color = (150, 150, 150) if brush_size == brush_sizes[3] else (220, 220, 220)
        
        pygame.draw.rect(screen, small_color, btn_small)
        pygame.draw.rect(screen, medium_color, btn_medium)
        pygame.draw.rect(screen, large_color, btn_large)
        pygame.draw.rect(screen, (0, 0, 0), btn_small, 2)
        pygame.draw.rect(screen, (0, 0, 0), btn_medium, 2)
        pygame.draw.rect(screen, (0, 0, 0), btn_large, 2)
        
        small_txt = font.render("S", True, (0, 0, 0))
        medium_txt = font.render("M", True, (0, 0, 0))
        large_txt = font.render("L", True, (0, 0, 0))
        
        screen.blit(small_txt, (btn_small.x + 12, btn_small.y + 6))
        screen.blit(medium_txt, (btn_medium.x + 12, btn_medium.y + 6))
        screen.blit(large_txt, (btn_large.x + 12, btn_large.y + 6))
        
        # Информация
        size_text = font.render(f"Size: {brush_size}", True, (0, 0, 0))
        screen.blit(size_text, (680, second_row_y + 8))
        instruct_text = font.render("Ctrl+S: Save | 1,2,3: Size", True, (0, 0, 0))
        screen.blit(instruct_text, (10, second_row_y + 8))
        
        # Рамка вокруг холста
        pygame.draw.rect(screen, (100, 100, 100), (0, canvas_offset_y - 2, 800, canvas_height + 4), 2)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Горячие клавиши
            if event.type == pygame.KEYDOWN:
                if event.mod & pygame.KMOD_CTRL and event.key == pygame.K_s:
                    SaveManager.save_canvas(canvas)
                
                if event.key in brush_sizes:
                    brush_size = brush_sizes[event.key]
                
                # Ввод текста
                if text_input_active:
                    if event.key == pygame.K_RETURN:
                        if text_input_str and text_input_pos:
                            # Текст сохраняется на холст
                            font_text = pygame.font.SysFont(None, 24)
                            text_surface = font_text.render(text_input_str, True, current_color)
                            canvas.blit(text_surface, text_input_pos)
                        text_input_active = False
                        text_input_str = ""
                        text_input_pos = None
                    elif event.key == pygame.K_ESCAPE:
                        text_input_active = False
                        text_input_str = ""
                        text_input_pos = None
                    elif event.key == pygame.K_BACKSPACE:
                        text_input_str = text_input_str[:-1]
                    else:
                        text_input_str += event.unicode
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                
                # Определяем, кликнули ли по UI (выше области холста)
                if y < canvas_offset_y:
                    # Обработка кнопок (просто проверяем все кнопки)
                    if btn_red.collidepoint(x, y): current_color = colors['red']
                    elif btn_green.collidepoint(x, y): current_color = colors['green']
                    elif btn_blue.collidepoint(x, y): current_color = colors['blue']
                    elif btn_black.collidepoint(x, y): current_color = colors['black']
                    elif btn_brush.collidepoint(x, y): mode = 'brush'
                    elif btn_pencil.collidepoint(x, y): mode = 'pencil'
                    elif btn_line.collidepoint(x, y): mode = 'line'
                    elif btn_rect.collidepoint(x, y): mode = 'rect'
                    elif btn_circ.collidepoint(x, y): mode = 'circle'
                    elif btn_erase.collidepoint(x, y): mode = 'eraser'
                    elif btn_fill.collidepoint(x, y): mode = 'fill'
                    elif btn_text.collidepoint(x, y): mode = 'text'
                    elif btn_sq.collidepoint(x, y): mode = 'square'
                    elif btn_rt.collidepoint(x, y): mode = 'rtriangle'
                    elif btn_et.collidepoint(x, y): mode = 'etriangle'
                    elif btn_rh.collidepoint(x, y): mode = 'rhombus'
                    elif btn_small.collidepoint(x, y): brush_size = brush_sizes[1]
                    elif btn_medium.collidepoint(x, y): brush_size = brush_sizes[2]
                    elif btn_large.collidepoint(x, y): brush_size = brush_sizes[3]
                else:
                    # Клик по холсту - преобразуем координаты!
                    canvas_x, canvas_y = get_canvas_pos(event.pos)
                    
                    # Проверяем, что клик в пределах холста
                    if 0 <= canvas_x < canvas_width and 0 <= canvas_y < canvas_height:
                        if mode == 'fill':
                            target_color = canvas.get_at((canvas_x, canvas_y))
                            tools.flood_fill(canvas_x, canvas_y, target_color, current_color)
                        elif mode == 'text':
                            text_input_active = True
                            text_input_str = ""
                            text_input_pos = (canvas_x, canvas_y)
                        else:
                            drawing = True
                            start_pos = (canvas_x, canvas_y)
                            if mode == 'pencil':
                                last_pos = (canvas_x, canvas_y)
            
            if event.type == pygame.MOUSEBUTTONUP:
                if drawing and start_pos:
                    drawing = False
                    
                    if mode in ['rect', 'circle', 'line', 'square', 'rtriangle', 'etriangle', 'rhombus']:
                        # Конечная позиция в координатах холста
                        canvas_x, canvas_y = get_canvas_pos(event.pos)
                        end_pos = (canvas_x, canvas_y)
                        
                        if start_pos and end_pos:
                            if mode == 'rect':
                                tools.draw_rect(start_pos, end_pos, current_color, brush_size)
                            elif mode == 'circle':
                                tools.draw_circle(start_pos, end_pos, current_color, brush_size)
                            elif mode == 'line':
                                tools.draw_line(start_pos, end_pos, current_color, brush_size)
                            elif mode == 'square':
                                tools.draw_square(start_pos, end_pos, current_color, brush_size)
                            elif mode == 'rtriangle':
                                tools.draw_right_triangle(start_pos, end_pos, current_color, brush_size)
                            elif mode == 'etriangle':
                                tools.draw_equilateral_triangle(start_pos, end_pos, current_color, brush_size)
                            elif mode == 'rhombus':
                                tools.draw_rhombus(start_pos, end_pos, current_color, brush_size)
                    
                    start_pos = None
                    last_pos = None
            
            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    canvas_x, canvas_y = get_canvas_pos(event.pos)
                    
                    if 0 <= canvas_x < canvas_width and 0 <= canvas_y < canvas_height:
                        if mode == 'brush':
                            tools.draw_brush((canvas_x, canvas_y), current_color, brush_size)
                        elif mode == 'pencil' and last_pos:
                            tools.draw_pencil(last_pos, (canvas_x, canvas_y), current_color, brush_size)
                            last_pos = (canvas_x, canvas_y)
                        elif mode == 'eraser':
                            tools.draw_eraser((canvas_x, canvas_y), brush_size)
        
        # Отрисовка
        screen.fill((240, 240, 240))
        
        # Рисуем холст на экране со смещением
        screen.blit(canvas, (0, canvas_offset_y))
        
        # Предпросмотр фигур (в координатах экрана)
        if drawing and start_pos and mode in ['rect', 'circle', 'line', 'square', 'rtriangle', 'etriangle', 'rhombus']:
            # Преобразуем текущую позицию мыши в координаты холста
            current_canvas_pos = get_canvas_pos(pygame.mouse.get_pos())
            # Преобразуем начальную позицию в координаты экрана для отрисовки предпросмотра
            start_screen = (start_pos[0], start_pos[1] + canvas_offset_y)
            current_screen = (current_canvas_pos[0], current_canvas_pos[1] + canvas_offset_y)
            preview.draw_preview(screen, mode, start_screen, current_screen, current_color, brush_size)
        
        # Предпросмотр текста
        if text_input_active and text_input_pos:
            preview_font = pygame.font.SysFont(None, 24)
            text_surface = preview_font.render(text_input_str + "|", True, current_color)
            # Рисуем текст на экране, а не на холсте
            screen.blit(text_surface, (text_input_pos[0], text_input_pos[1] + canvas_offset_y))
        
        draw_ui()
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()