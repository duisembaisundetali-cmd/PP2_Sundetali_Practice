import pygame
import sys
from racer import RacerGame
from ui import UIManager
from persistence import PersistenceManager

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("TSIS 3 - Advanced Racer Game")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Load settings
        self.settings = PersistenceManager.load_settings()
        
        # Initialize UI
        self.ui_manager = UIManager(self.screen, self.settings)
        
        # Game state
        self.current_screen = "menu"
        self.player_name = ""
        self.game_instance = None
        self.final_score = 0
        self.final_distance = 0
        self.final_coins = 0
        
    def run(self):
        while self.running:
            # Обрабатываем события постоянно
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
            
            if self.current_screen == "menu":
                self.menu_screen()
            elif self.current_screen == "game":
                self.game_screen()
            elif self.current_screen == "leaderboard":
                self.leaderboard_screen()
            elif self.current_screen == "settings":
                self.settings_screen()
            elif self.current_screen == "game_over":
                self.game_over_screen()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()
    
    def menu_screen(self):
        action = self.ui_manager.draw_main_menu()
        
        if action == "play":
            self.player_name = self.ui_manager.get_player_name()
            if self.player_name:
                self.game_instance = RacerGame(self.screen, self.settings, self.player_name)
                self.current_screen = "game"
        elif action == "leaderboard":
            self.current_screen = "leaderboard"
        elif action == "settings":
            self.current_screen = "settings"
        elif action == "quit":
            self.running = False
    
    def game_screen(self):
        if self.game_instance:
            result = self.game_instance.run()
            if result:
                self.final_score, self.final_distance, self.final_coins = result
                PersistenceManager.save_score(self.player_name, self.final_score, self.final_distance)
                self.current_screen = "game_over"
    
    def leaderboard_screen(self):
        action = self.ui_manager.draw_leaderboard_screen()
        if action == "back":
            self.current_screen = "menu"
    
    def settings_screen(self):
        action, new_settings = self.ui_manager.draw_settings_screen(self.settings)
        
        if action == "save":
            self.settings = new_settings
            PersistenceManager.save_settings(self.settings)
            if self.game_instance:
                self.game_instance.update_settings(self.settings)
            self.current_screen = "menu"
        elif action == "back":
            self.current_screen = "menu"
    
    def game_over_screen(self):
        action = self.ui_manager.draw_game_over_screen(self.final_score, self.final_distance, self.final_coins)
        
        if action == "retry":
            self.game_instance = RacerGame(self.screen, self.settings, self.player_name)
            self.current_screen = "game"
        elif action == "menu":
            self.current_screen = "menu"

if __name__ == "__main__":
    game = Game()
    game.run()