import pygame
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
    
    btn_red = pygame.Rect(10, 10, 30, 30)
    btn_green = pygame.Rect(50, 10, 30, 30)
    btn_blue = pygame.Rect(90, 10, 30, 30)
    btn_black = pygame.Rect(130, 10, 30, 30)
    
    btn_brush = pygame.Rect(200, 10, 60, 30)
    btn_rect = pygame.Rect(270, 10, 60, 30)
    btn_circ = pygame.Rect(340, 10, 60, 30)
    btn_erase = pygame.Rect(410, 10, 60, 30)
    
    font = pygame.font.SysFont(None, 24)
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
                    if btn_red.collidepoint(x, y): current_color = colors['red']
                    elif btn_green.collidepoint(x, y): current_color = colors['green']
                    elif btn_blue.collidepoint(x, y): current_color = colors['blue']
                    elif btn_black.collidepoint(x, y): current_color = colors['black']
                    elif btn_brush.collidepoint(x, y): mode = 'brush'
                    elif btn_rect.collidepoint(x, y): mode = 'rect'
                    elif btn_circ.collidepoint(x, y): mode = 'circle'
                    elif btn_erase.collidepoint(x, y): mode = 'eraser'
                else:
                    drawing = True
                    start_pos = event.pos
                    
            if event.type == pygame.MOUSEBUTTONUP:
                if drawing:
                    drawing = False
                    end_pos = event.pos
                    if start_pos and end_pos:
                        if mode == 'rect':
                            r = pygame.Rect(min(start_pos[0], end_pos[0]), min(start_pos[1], end_pos[1]), 
                                            abs(start_pos[0] - end_pos[0]), abs(start_pos[1] - end_pos[1]))
                            pygame.draw.rect(canvas, current_color, r)
                        elif mode == 'circle':
                            radius = int(((start_pos[0] - end_pos[0])**2 + (start_pos[1] - end_pos[1])**2)**0.5)
                            pygame.draw.circle(canvas, current_color, start_pos, radius)
                start_pos = None
                
            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    if mode == 'brush':
                        pygame.draw.circle(canvas, current_color, event.pos, 5)
                    elif mode == 'eraser':
                        pygame.draw.circle(canvas, colors['white'], event.pos, 15)

        screen.blit(canvas, (0, 0))
        
        if drawing and start_pos and mode in ['rect', 'circle']:
            mouse_pos = pygame.mouse.get_pos()
            if mode == 'rect':
                r = pygame.Rect(min(start_pos[0], mouse_pos[0]), min(start_pos[1], mouse_pos[1]), 
                                abs(start_pos[0] - mouse_pos[0]), abs(start_pos[1] - mouse_pos[1]))
                pygame.draw.rect(screen, current_color, r, 2)
            elif mode == 'circle':
                radius = int(((start_pos[0] - mouse_pos[0])**2 + (start_pos[1] - mouse_pos[1])**2)**0.5)
                pygame.draw.circle(screen, current_color, start_pos, radius, 2)

        pygame.draw.rect(screen, (200, 200, 200), ui_rect)
        pygame.draw.rect(screen, colors['red'], btn_red)
        pygame.draw.rect(screen, colors['green'], btn_green)
        pygame.draw.rect(screen, colors['blue'], btn_blue)
        pygame.draw.rect(screen, colors['black'], btn_black)
        
        pygame.draw.rect(screen, (0,0,0), btn_red, 2 if current_color != colors['red'] else 4)
        
        def draw_btn(rect, text, is_active):
            color = (150, 150, 150) if is_active else (220, 220, 220)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2)
            txt = font.render(text, True, (0, 0, 0))
            screen.blit(txt, (rect.x + 5, rect.y + 5))
            
        draw_btn(btn_brush, "Brush", mode == 'brush')
        draw_btn(btn_rect, "Rect", mode == 'rect')
        draw_btn(btn_circ, "Circ", mode == 'circle')
        draw_btn(btn_erase, "Erase", mode == 'eraser')

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()