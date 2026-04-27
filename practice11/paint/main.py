import pygame
import math

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Paint Application")
    
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
    
    canvas = pygame.Surface((800, 600))
    canvas.fill(colors['white'])
    
    ui_rect = pygame.Rect(0, 0, 800, 50)
    
    btn_red = pygame.Rect(10, 10, 30, 30)#кнопка красного цвета
    btn_green = pygame.Rect(50, 10, 30, 30)#кнопка зеленого цвета
    btn_blue = pygame.Rect(90, 10, 30, 30)#кнопка синего цвета
    btn_black = pygame.Rect(130, 10, 30, 30)#кнопка черного цвета
    
    btn_brush = pygame.Rect(200, 10, 50, 30)#кнопка кисти
    btn_rect = pygame.Rect(260, 10, 50, 30)#кнопка прямоугольника
    btn_circ = pygame.Rect(320, 10, 50, 30)#кнопка круга
    btn_erase = pygame.Rect(380, 10, 50, 30)#кнопка ластика
    
    btn_sq = pygame.Rect(440, 10, 50, 30)#кнопка квадрата
    btn_rt = pygame.Rect(500, 10, 50, 30)#кнопка прямоугольного треугольника
    btn_et = pygame.Rect(560, 10, 50, 30)#кнопка равностороннего треугольника
    btn_rh = pygame.Rect(620, 10, 50, 30)#кнопка ромба
    
    font = pygame.font.SysFont(None, 22)
    start_pos = None
    
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if y <= 50:
                    if btn_red.collidepoint(x, y): current_color = colors['red']#смена цвета на красный если кликнули по красной кнопке
                    elif btn_green.collidepoint(x, y): current_color = colors['green']
                    elif btn_blue.collidepoint(x, y): current_color = colors['blue']
                    elif btn_black.collidepoint(x, y): current_color = colors['black']
                    elif btn_brush.collidepoint(x, y): mode = 'brush'#смена режима на кисть
                    elif btn_rect.collidepoint(x, y): mode = 'rect'
                    elif btn_circ.collidepoint(x, y): mode = 'circle'
                    elif btn_erase.collidepoint(x, y): mode = 'eraser'
                    elif btn_sq.collidepoint(x, y): mode = 'square'
                    elif btn_rt.collidepoint(x, y): mode = 'rtriangle'
                    elif btn_et.collidepoint(x, y): mode = 'etriangle'
                    elif btn_rh.collidepoint(x, y): mode = 'rhombus'
                else:
                    drawing = True
                    start_pos = event.pos
                    
            if event.type == pygame.MOUSEBUTTONUP:
                if drawing:
                    drawing = False
                    end_pos = event.pos
                    if start_pos and end_pos:
                        if mode == 'rect':#рисуем прямоугольник от начальной до конечной точки
                            r = pygame.Rect(min(start_pos[0], end_pos[0]), min(start_pos[1], end_pos[1]), 
                                            abs(start_pos[0] - end_pos[0]), abs(start_pos[1] - end_pos[1]))
                            pygame.draw.rect(canvas, current_color, r)
                        elif mode == 'circle':#рисуем круг с центром в начальной точке и радиусом до конечной точки
                            radius = int(((start_pos[0] - end_pos[0])**2 + (start_pos[1] - end_pos[1])**2)**0.5)
                            pygame.draw.circle(canvas, current_color, start_pos, radius)
                        elif mode == 'square':#рисуем квадрат от начальной до конечной точки
                            side = max(abs(start_pos[0] - end_pos[0]), abs(start_pos[1] - end_pos[1]))
                            sx = start_pos[0] if end_pos[0] > start_pos[0] else start_pos[0] - side
                            sy = start_pos[1] if end_pos[1] > start_pos[1] else start_pos[1] - side
                            r = pygame.Rect(sx, sy, side, side)
                            pygame.draw.rect(canvas, current_color, r)
                        elif mode == 'rtriangle':#рисуем прямоугольный треугольник от начальной до конечной точки
                            pygame.draw.polygon(canvas, current_color, [start_pos, (start_pos[0], end_pos[1]), end_pos])
                        elif mode == 'etriangle':#рисуем равносторонний треугольник с вершиной в начальной точке и основанием до конечной точки
                            d = ((start_pos[0] - end_pos[0])**2 + (start_pos[1] - end_pos[1])**2)**0.5
                            h = d * (3**0.5) / 2
                            p1 = start_pos
                            p2 = (start_pos[0] - d/2, start_pos[1] + h)
                            p3 = (start_pos[0] + d/2, start_pos[1] + h)
                            pygame.draw.polygon(canvas, current_color, [p1, p2, p3])
                        elif mode == 'rhombus':#рисуем ромб от начальной до конечной точки
                            mx = (start_pos[0] + end_pos[0]) / 2
                            my = (start_pos[1] + end_pos[1]) / 2
                            p1 = (mx, start_pos[1])
                            p2 = (end_pos[0], my)
                            p3 = (mx, end_pos[1])
                            p4 = (start_pos[0], my)
                            pygame.draw.polygon(canvas, current_color, [p1, p2, p3, p4])#рисуем ромб от начальной до конечной точки
                start_pos = None
                
            if event.type == pygame.MOUSEMOTION:#движение мыши
                if drawing:
                    if mode == 'brush':#рисуем круг в текущей позиции мыши для эффекта кисти
                        pygame.draw.circle(canvas, current_color, event.pos, 5)
                    elif mode == 'eraser':#рисуем белый круг для эффекта ластика
                        pygame.draw.circle(canvas, colors['white'], event.pos, 15)

        screen.blit(canvas, (0, 0))
        
        if drawing and start_pos and mode not in ['brush', 'eraser']:#рисуем контур фигуры во время рисования
            mouse_pos = pygame.mouse.get_pos()#получаем позицию мыши
            if mode == 'rect':#рисуем контур прямоугольника во время рисования
                r = pygame.Rect(min(start_pos[0], mouse_pos[0]), min(start_pos[1], mouse_pos[1]), 
                                abs(start_pos[0] - mouse_pos[0]), abs(start_pos[1] - mouse_pos[1]))
                pygame.draw.rect(screen, current_color, r, 2)
            elif mode == 'circle':#рисуем контур круга во время рисования
                radius = int(((start_pos[0] - mouse_pos[0])**2 + (start_pos[1] - mouse_pos[1])**2)**0.5)
                pygame.draw.circle(screen, current_color, start_pos, radius, 2)
            elif mode == 'square':#рисуем контур квадрата во время рисования
                side = max(abs(start_pos[0] - mouse_pos[0]), abs(start_pos[1] - mouse_pos[1]))
                sx = start_pos[0] if mouse_pos[0] > start_pos[0] else start_pos[0] - side
                sy = start_pos[1] if mouse_pos[1] > start_pos[1] else start_pos[1] - side
                r = pygame.Rect(sx, sy, side, side)
                pygame.draw.rect(screen, current_color, r, 2)
            elif mode == 'rtriangle':#рисуем контур прямоугольного треугольника во время рисования
                pygame.draw.polygon(screen, current_color, [start_pos, (start_pos[0], mouse_pos[1]), mouse_pos], 2)
            elif mode == 'etriangle':#рисуем контур равностороннего треугольника во время рисования
                d = ((start_pos[0] - mouse_pos[0])**2 + (start_pos[1] - mouse_pos[1])**2)**0.5
                h = d * (3**0.5) / 2
                p1 = start_pos
                p2 = (start_pos[0] - d/2, start_pos[1] + h)
                p3 = (start_pos[0] + d/2, start_pos[1] + h)
                pygame.draw.polygon(screen, current_color, [p1, p2, p3], 2)
            elif mode == 'rhombus':#рисуем ромб от начальной до конечной точки
                mx = (start_pos[0] + mouse_pos[0]) / 2
                my = (start_pos[1] + mouse_pos[1]) / 2
                p1 = (mx, start_pos[1])
                p2 = (mouse_pos[0], my)
                p3 = (mx, mouse_pos[1])
                p4 = (start_pos[0], my)
                pygame.draw.polygon(screen, current_color, [p1, p2, p3, p4], 2)#рисуем контур ромба во время рисования

        pygame.draw.rect(screen, (200, 200, 200), ui_rect)
        pygame.draw.rect(screen, colors['red'], btn_red)
        pygame.draw.rect(screen, colors['green'], btn_green)
        pygame.draw.rect(screen, colors['blue'], btn_blue)
        pygame.draw.rect(screen, colors['black'], btn_black)
        
        pygame.draw.rect(screen, (0,0,0), btn_red, 2 if current_color != colors['red'] else 4)#обводка для выделения текущего цвета
        
        def draw_btn(rect, text, is_active):#функция для отрисовки кнопок с текстом и выделением активной кнопки
            color = (150, 150, 150) if is_active else (220, 220, 220)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2)
            txt = font.render(text, True, (0, 0, 0))
            screen.blit(txt, (rect.x + 2, rect.y + 6))
            
        draw_btn(btn_brush, "Bsh", mode == 'brush')#рисуем кнопку для кисти с выделением если активна
        draw_btn(btn_rect, "Rect", mode == 'rect')
        draw_btn(btn_circ, "Circ", mode == 'circle')
        draw_btn(btn_erase, "Ers", mode == 'eraser')
        draw_btn(btn_sq, "Squr", mode == 'square')
        draw_btn(btn_rt, "RTri", mode == 'rtriangle')
        draw_btn(btn_et, "ETri", mode == 'etriangle')
        draw_btn(btn_rh, "Rhmb", mode == 'rhombus')

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()