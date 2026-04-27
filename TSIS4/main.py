import pygame
import sys
from config import *
from game import Game
from db import Database
from settings_manager import SettingsManager

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.font = font
        self.is_hovered = False
    
    def draw(self, screen):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False

class ColorPicker:
    def __init__(self, x, y, colors):
        self.x = x
        self.y = y
        self.colors = colors
        self.selected = 0
        self.rects = []
        
        for i, color in enumerate(colors):
            rect = pygame.Rect(x + i * 35, y, 30, 30)
            self.rects.append((rect, color))
    
    def draw(self, screen):
        for i, (rect, color) in enumerate(self.rects):
            pygame.draw.rect(screen, color, rect)
            if i == self.selected:
                pygame.draw.rect(screen, WHITE, rect, 3)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i, (rect, _) in enumerate(self.rects):
                if rect.collidepoint(event.pos):
                    self.selected = i
                    return self.colors[i]
        return None

class GameScreens:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        
        self.font_title = pygame.font.Font(None, 72)
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        self.db = Database()
        self.settings_manager = SettingsManager()
        self.username = ""
        self.input_text = ""
        
        self.available_colors = [
            (0, 255, 0), (255, 0, 0), (0, 0, 255),
            (255, 255, 0), (255, 0, 255)
        ]
    
    def draw_text_input(self, text, x, y, width):
        input_rect = pygame.Rect(x, y, width, 40)
        pygame.draw.rect(self.screen, WHITE, input_rect, 2)
        
        text_surface = self.font_medium.render(text, True, WHITE)
        self.screen.blit(text_surface, (x + 5, y + 8))
        
        return input_rect
    
    def username_entry_screen(self):
        self.username = ""
        self.input_text = ""
        
        while True:
            self.screen.fill(BLACK)
            
            title = self.font_title.render("SNAKE GAME", True, WHITE)
            title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 100))
            self.screen.blit(title, title_rect)
            
            instruction = self.font_medium.render("Enter your username:", True, WHITE)
            instruction_rect = instruction.get_rect(center=(WINDOW_WIDTH//2, 200))
            self.screen.blit(instruction, instruction_rect)
            
            input_rect = self.draw_text_input(self.input_text, WINDOW_WIDTH//2 - 150, 250, 300)
            
            if self.input_text.strip():
                continue_btn = Button(WINDOW_WIDTH//2 - 100, 350, 200, 50, 
                                     "PLAY", BLUE, LIGHT_BLUE, self.font_medium)
                continue_btn.draw(self.screen)
                
                for event in pygame.event.get():
                    if continue_btn.handle_event(event):
                        self.username = self.input_text.strip()
                        return
                    self.handle_input_events(event, input_rect)
            else:
                for event in pygame.event.get():
                    self.handle_input_events(event, input_rect)
            
            pygame.display.flip()
            self.clock.tick(30)
    
    def handle_input_events(self, event, input_rect):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and self.input_text.strip():
                self.username = self.input_text.strip()
                return
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            else:
                if len(self.input_text) < 20 and event.unicode.isprintable():
                    self.input_text += event.unicode
    
    def main_menu(self):
        buttons = [
            Button(WINDOW_WIDTH//2 - 100, 200, 200, 50, "PLAY", BLUE, LIGHT_BLUE, self.font_large),
            Button(WINDOW_WIDTH//2 - 100, 280, 200, 50, "LEADERBOARD", BLUE, LIGHT_BLUE, self.font_large),
            Button(WINDOW_WIDTH//2 - 100, 360, 200, 50, "SETTINGS", BLUE, LIGHT_BLUE, self.font_large),
            Button(WINDOW_WIDTH//2 - 100, 440, 200, 50, "QUIT", RED, (255, 100, 100), self.font_large)
        ]
        
        while True:
            self.screen.fill(BLACK)
            
            title = self.font_title.render("SNAKE GAME", True, WHITE)
            title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 100))
            self.screen.blit(title, title_rect)
            
            username_text = self.font_medium.render(f"Player: {self.username}", True, WHITE)
            username_rect = username_text.get_rect(center=(WINDOW_WIDTH//2, 150))
            self.screen.blit(username_text, username_rect)
            
            for button in buttons:
                button.draw(self.screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                
                if buttons[0].handle_event(event):
                    return "play"
                elif buttons[1].handle_event(event):
                    return "leaderboard"
                elif buttons[2].handle_event(event):
                    return "settings"
                elif buttons[3].handle_event(event):
                    return "quit"
            
            pygame.display.flip()
            self.clock.tick(30)
    
    def leaderboard_screen(self):
        top_scores = self.db.get_top_scores()
        
        back_button = Button(WINDOW_WIDTH//2 - 100, 500, 200, 50, 
                            "BACK", BLUE, LIGHT_BLUE, self.font_medium)
        
        while True:
            self.screen.fill(BLACK)
            
            title = self.font_large.render("TOP 10 SCORES", True, WHITE)
            title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 50))
            self.screen.blit(title, title_rect)
            
            headers = ["Rank", "Username", "Score", "Level", "Date"]
            x_positions = [50, 150, 350, 480, 580]
            for i, header in enumerate(headers):
                header_text = self.font_small.render(header, True, WHITE)
                self.screen.blit(header_text, (x_positions[i], 100))
            
            y_offset = 130
            for i, score in enumerate(top_scores[:10]):
                username, score_val, level, played_at = score
                date_str = played_at.strftime("%Y-%m-%d")
                
                row_data = [str(i+1), username[:15], str(score_val), str(level), date_str]
                for j, data in enumerate(row_data):
                    score_text = self.font_small.render(data, True, WHITE)
                    self.screen.blit(score_text, (x_positions[j], y_offset))
                
                y_offset += 30
                if y_offset > 450:
                    break
            
            back_button.draw(self.screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if back_button.handle_event(event):
                    return "menu"
            
            pygame.display.flip()
            self.clock.tick(30)
    
    def settings_screen(self):
        current_settings = self.settings_manager.settings.copy()
        
        grid_button = Button(400, 150, 150, 40, 
                            f"Grid: {'ON' if current_settings['grid_overlay'] else 'OFF'}",
                            BLUE, LIGHT_BLUE, self.font_small)
        
        sound_button = Button(400, 210, 150, 40,
                             f"Sound: {'ON' if current_settings['sound'] else 'OFF'}",
                             BLUE, LIGHT_BLUE, self.font_small)
        
        color_picker = ColorPicker(400, 280, self.available_colors)
        current_color = tuple(current_settings['snake_color'])
        if current_color in self.available_colors:
            color_picker.selected = self.available_colors.index(current_color)
        
        save_button = Button(WINDOW_WIDTH//2 - 100, 500, 200, 50,
                            "SAVE & BACK", GREEN, LIGHT_BLUE, self.font_medium)
        
        while True:
            self.screen.fill(BLACK)
            
            title = self.font_large.render("SETTINGS", True, WHITE)
            title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 50))
            self.screen.blit(title, title_rect)
            
            grid_label = self.font_medium.render("Grid Overlay:", True, WHITE)
            self.screen.blit(grid_label, (250, 155))
            
            sound_label = self.font_medium.render("Sound Effects:", True, WHITE)
            self.screen.blit(sound_label, (250, 215))
            
            color_label = self.font_medium.render("Snake Color:", True, WHITE)
            self.screen.blit(color_label, (250, 285))
            
            grid_button.draw(self.screen)
            sound_button.draw(self.screen)
            color_picker.draw(self.screen)
            save_button.draw(self.screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                
                if grid_button.handle_event(event):
                    current_settings['grid_overlay'] = not current_settings['grid_overlay']
                    grid_button.text = f"Grid: {'ON' if current_settings['grid_overlay'] else 'OFF'}"
                
                if sound_button.handle_event(event):
                    current_settings['sound'] = not current_settings['sound']
                    sound_button.text = f"Sound: {'ON' if current_settings['sound'] else 'OFF'}"
                
                selected_color = color_picker.handle_event(event)
                if selected_color:
                    current_settings['snake_color'] = list(selected_color)
                
                if save_button.handle_event(event):
                    self.settings_manager.update(current_settings)
                    return "menu"
            
            pygame.display.flip()
            self.clock.tick(30)
    
    def game_over_screen(self, score, level_reached):
        personal_best = self.db.get_personal_best(self.username)
        
        retry_button = Button(WINDOW_WIDTH//2 - 220, 400, 180, 50,
                             "RETRY", BLUE, LIGHT_BLUE, self.font_medium)
        menu_button = Button(WINDOW_WIDTH//2 + 40, 400, 180, 50,
                            "MAIN MENU", BLUE, LIGHT_BLUE, self.font_medium)
        
        while True:
            self.screen.fill(BLACK)
            
            game_over_text = self.font_large.render("GAME OVER!", True, RED)
            game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH//2, 100))
            self.screen.blit(game_over_text, game_over_rect)
            
            score_text = self.font_medium.render(f"Final Score: {score}", True, WHITE)
            score_rect = score_text.get_rect(center=(WINDOW_WIDTH//2, 200))
            self.screen.blit(score_text, score_rect)
            
            level_text = self.font_medium.render(f"Level Reached: {level_reached}", True, WHITE)
            level_rect = level_text.get_rect(center=(WINDOW_WIDTH//2, 250))
            self.screen.blit(level_text, level_rect)
            
            best_text = self.font_medium.render(f"Personal Best: {personal_best}", True, WHITE)
            best_rect = best_text.get_rect(center=(WINDOW_WIDTH//2, 300))
            self.screen.blit(best_text, best_rect)
            
            retry_button.draw(self.screen)
            menu_button.draw(self.screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if retry_button.handle_event(event):
                    return "retry"
                if menu_button.handle_event(event):
                    return "menu"
            
            pygame.display.flip()
            self.clock.tick(30)
    
    def run(self):
        # First, get username
        self.username_entry_screen()
        
        while True:
            action = self.main_menu()
            
            if action == "play":
                game = Game(self.db, self.settings_manager, self.username)
                result = game.run()
                if result == "game_over":
                    game_over_result = self.game_over_screen(game.score, game.level)
                    if game_over_result == "retry":
                        continue
                    elif game_over_result == "menu":
                        continue
                    elif game_over_result == "quit":
                        break
                elif result == "quit":
                    break
            
            elif action == "leaderboard":
                self.leaderboard_screen()
            
            elif action == "settings":
                self.settings_screen()
            
            elif action == "quit":
                break
        
        self.db.close()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    screens = GameScreens()
    screens.run()