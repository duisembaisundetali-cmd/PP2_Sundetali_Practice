import pygame
from persistence import PersistenceManager

class UIManager:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        self.font_tiny = pygame.font.Font(None, 24)
    
    def draw_button(self, text, x, y, width, height, color=(100, 100, 100), hover_color=(150, 150, 150)):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        button_rect = pygame.Rect(x, y, width, height)
        
        if button_rect.collidepoint(mouse):
            pygame.draw.rect(self.screen, hover_color, button_rect)
            if click[0]:
                return True
        else:
            pygame.draw.rect(self.screen, color, button_rect)
        
        pygame.draw.rect(self.screen, (255, 255, 255), button_rect, 3)
        
        text_surface = self.font_small.render(text, True, (255, 255, 255))
        text_x = x + (width - text_surface.get_width()) // 2
        text_y = y + (height - text_surface.get_height()) // 2
        self.screen.blit(text_surface, (text_x, text_y))
        
        return False
    
    def draw_main_menu(self):
        self.screen.fill((0, 0, 0))
        
        title = self.font_large.render("TSIS 3", True, (255, 215, 0))
        title2 = self.font_medium.render("RACER GAME", True, (255, 255, 255))
        title_x = (800 - title.get_width()) // 2
        title2_x = (800 - title2.get_width()) // 2
        self.screen.blit(title, (title_x, 80))
        self.screen.blit(title2, (title2_x, 160))
        
        # Draw decorative road
        pygame.draw.rect(self.screen, (40, 40, 40), (200, 220, 400, 10))
        pygame.draw.rect(self.screen, (255, 255, 0), (200, 220, 400, 2))
        
        buttons = [
            ("PLAY", 300, 280, 200, 50, (0, 100, 0)),
            ("LEADERBOARD", 300, 350, 200, 50, (0, 0, 100)),
            ("SETTINGS", 300, 420, 200, 50, (100, 100, 0)),
            ("QUIT", 300, 490, 200, 50, (100, 0, 0))
        ]
        
        for text, x, y, width, height, color in buttons:
            if self.draw_button(text, x, y, width, height, color):
                return text.lower()
        
        return None
    
    def get_player_name(self):
        name = ""
        input_active = True
        
        while input_active:
            self.screen.fill((0, 0, 0))
            
            title = self.font_medium.render("ENTER YOUR NAME", True, (255, 215, 0))
            title_x = (800 - title.get_width()) // 2
            self.screen.blit(title, (title_x, 150))
            
            subtitle = self.font_small.render("(Max 15 characters)", True, (200, 200, 200))
            sub_x = (800 - subtitle.get_width()) // 2
            self.screen.blit(subtitle, (sub_x, 210))
            
            # Input box
            input_rect = pygame.Rect(250, 280, 300, 50)
            pygame.draw.rect(self.screen, (50, 50, 50), input_rect)
            pygame.draw.rect(self.screen, (255, 215, 0), input_rect, 3)
            
            name_surface = self.font_medium.render(name, True, (255, 255, 255))
            self.screen.blit(name_surface, (260, 290))
            
            # Buttons
            if self.draw_button("START", 300, 380, 200, 50, (0, 100, 0)):
                if name.strip():
                    return name.strip()
            
            if self.draw_button("BACK", 300, 450, 200, 50, (100, 0, 0)):
                return None
            
            pygame.display.flip()
            
            # Обрабатываем события
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and name.strip():
                        return name.strip()
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        return None
                    else:
                        if len(name) < 15 and event.unicode.isprintable():
                            name += event.unicode
    
    def draw_leaderboard_screen(self):
        self.screen.fill((0, 0, 0))
        
        title = self.font_medium.render("LEADERBOARD", True, (255, 215, 0))
        title_x = (800 - title.get_width()) // 2
        self.screen.blit(title, (title_x, 50))
        
        scores = PersistenceManager.load_leaderboard()
        
        # Headers
        headers = ["#", "NAME", "SCORE", "DISTANCE"]
        header_x = [80, 180, 480, 620]
        
        for i, header in enumerate(headers):
            header_surface = self.font_small.render(header, True, (255, 215, 0))
            self.screen.blit(header_surface, (header_x[i], 120))
        
        # Separator line
        pygame.draw.line(self.screen, (255, 255, 255), (60, 155), (740, 155), 2)
        
        # Scores
        y = 175
        for i, score in enumerate(scores[:10]):
            rank = i + 1
            name = score['name'][:15]
            score_value = score['score']
            distance = score['distance']
            
            if rank == 1:
                color = (255, 215, 0)
            elif rank == 2:
                color = (192, 192, 192)
            elif rank == 3:
                color = (205, 127, 50)
            else:
                color = (255, 255, 255)
            
            rank_surface = self.font_small.render(str(rank), True, color)
            name_surface = self.font_small.render(name, True, color)
            score_surface = self.font_small.render(str(score_value), True, color)
            distance_surface = self.font_small.render(str(distance), True, color)
            
            self.screen.blit(rank_surface, (95, y))
            self.screen.blit(name_surface, (180, y))
            self.screen.blit(score_surface, (490, y))
            self.screen.blit(distance_surface, (630, y))
            
            y += 35
            if y > 500:
                break
        
        # Back button
        if self.draw_button("BACK", 300, 520, 200, 50, (100, 0, 0)):
            return "back"
        
        return None
    
    def draw_settings_screen(self, settings):
        self.screen.fill((0, 0, 0))
        
        title = self.font_medium.render("SETTINGS", True, (255, 215, 0))
        title_x = (800 - title.get_width()) // 2
        self.screen.blit(title, (title_x, 50))
        
        # Sound toggle
        sound_enabled = settings['sound']
        sound_text = self.font_small.render(f"SOUND EFFECTS: {'ON' if sound_enabled else 'OFF'}", True, (255, 255, 255))
        self.screen.blit(sound_text, (150, 150))
        
        if self.draw_button("TOGGLE", 500, 135, 120, 40, (100, 100, 100)):
            settings['sound'] = not settings['sound']
        
        # Difficulty
        difficulty = settings['difficulty']
        diff_text = self.font_small.render("DIFFICULTY:", True, (255, 255, 255))
        self.screen.blit(diff_text, (150, 230))
        
        difficulties = ["Easy", "Medium", "Hard"]
        for i, diff in enumerate(difficulties):
            x = 400 + i * 110
            color = (0, 100, 0) if diff == difficulty else (100, 100, 100)
            if self.draw_button(diff, x, 215, 90, 40, color):
                settings['difficulty'] = diff
        
        # Car color
        color_text = self.font_small.render("CAR COLOR:", True, (255, 255, 255))
        self.screen.blit(color_text, (150, 310))
        
        colors = [
            ((0, 255, 0), "GREEN"),
            ((255, 0, 0), "RED"),
            ((0, 0, 255), "BLUE"),
            ((255, 255, 0), "YELLOW")
        ]
        
        for i, (color, name) in enumerate(colors):
            x = 350 + i * 100
            btn_color = color if settings['car_color'] == color else (100, 100, 100)
            if self.draw_button(name, x, 295, 80, 40, btn_color):
                settings['car_color'] = color
        
        # Save and Back
        if self.draw_button("SAVE", 250, 420, 120, 50, (0, 100, 0)):
            return "save", settings
        
        if self.draw_button("BACK", 430, 420, 120, 50, (100, 0, 0)):
            return "back", settings
        
        return None, settings
    
    def draw_game_over_screen(self, score, distance, coins):
        self.screen.fill((0, 0, 0))
        
        title = self.font_large.render("GAME OVER", True, (255, 0, 0))
        title_x = (800 - title.get_width()) // 2
        self.screen.blit(title, (title_x, 80))
        
        # Stats panel
        panel_rect = pygame.Rect(200, 180, 400, 200)
        pygame.draw.rect(self.screen, (30, 30, 30), panel_rect)
        pygame.draw.rect(self.screen, (255, 215, 0), panel_rect, 3)
        
        score_text = self.font_medium.render(f"SCORE: {score}", True, (255, 215, 0))
        distance_text = self.font_small.render(f"DISTANCE: {distance}m", True, (255, 255, 255))
        coins_text = self.font_small.render(f"COINS: {coins}", True, (255, 215, 0))
        
        score_x = (800 - score_text.get_width()) // 2
        distance_x = (800 - distance_text.get_width()) // 2
        coins_x = (800 - coins_text.get_width()) // 2
        
        self.screen.blit(score_text, (score_x, 210))
        self.screen.blit(distance_text, (distance_x, 270))
        self.screen.blit(coins_text, (coins_x, 320))
        
        # Buttons
        if self.draw_button("RETRY", 230, 430, 150, 50, (0, 100, 0)):
            return "retry"
        
        if self.draw_button("MAIN MENU", 420, 430, 150, 50, (100, 0, 0)):
            return "menu"
        
        return None