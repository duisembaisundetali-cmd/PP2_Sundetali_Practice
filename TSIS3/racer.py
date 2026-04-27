import pygame
import random
from enum import Enum

class GameState(Enum):
    RUNNING = 1
    GAME_OVER = 2

class PowerUpType(Enum):
    NITRO = 1
    SHIELD = 2
    REPAIR = 3

class PowerUp:
    def __init__(self, x, y, power_type):
        self.x = x
        self.y = y
        self.type = power_type
        self.width = 30
        self.height = 30
        self.collected = False
        self.lifetime = 300
        self.age = 0
    
    def update(self):
        self.age += 1
        return self.age < self.lifetime
    
    def draw(self, screen):
        if self.age % 10 < 5:
            colors = {
                PowerUpType.NITRO: (255, 100, 0),
                PowerUpType.SHIELD: (0, 100, 255),
                PowerUpType.REPAIR: (0, 255, 100)
            }
            color = colors.get(self.type, (255, 255, 255))
            pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))
            pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height), 2)

class Obstacle:
    def __init__(self, x, y, obs_type):
        self.x = x
        self.y = y
        self.type = obs_type
        self.width = 40
        self.height = 40
    
    def draw(self, screen):
        if self.type == 'barrier':
            pygame.draw.rect(screen, (139, 69, 19), (self.x, self.y, self.width, self.height))
            pygame.draw.line(screen, (255, 0, 0), (self.x, self.y), (self.x + self.width, self.y + self.height), 3)
        elif self.type == 'oil':
            pygame.draw.ellipse(screen, (50, 50, 50), (self.x, self.y, self.width, self.height))
        elif self.type == 'pothole':
            pygame.draw.rect(screen, (80, 80, 80), (self.x, self.y, self.width, self.height))

class TrafficCar:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 60
        self.speed = speed
    
    def update(self):
        self.y += self.speed
    
    def draw(self, screen):
        pygame.draw.rect(screen, (200, 0, 0), (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, (100, 100, 100), (self.x + 5, self.y + 5, self.width - 10, 10))

class Coin:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        self.width = 30
        self.height = 30
    
    def draw(self, screen):
        colors = {10: (255, 215, 0), 20: (0, 255, 0), 50: (255, 165, 0)}
        pygame.draw.rect(screen, colors.get(self.value, (255, 215, 0)), (self.x, self.y, self.width, self.height))
        font = pygame.font.Font(None, 20)
        text = font.render(str(self.value), True, (0, 0, 0))
        screen.blit(text, (self.x + 10, self.y + 10))

class RacerGame:
    def __init__(self, screen, settings, player_name):
        self.screen = screen
        self.settings = settings
        self.player_name = player_name
        self.clock = pygame.time.Clock()
        
        # Game state
        self.state = GameState.RUNNING
        self.score = 0
        self.distance = 0
        self.coins_collected = 0
        self.active_powerup = None
        self.powerup_timer = 0
        self.shield_active = False
        
        # Lane system (4 lanes)
        self.lanes = [180, 300, 420, 540]
        self.lane_index = 1
        self.player_x = self.lanes[self.lane_index] - 20
        self.player_y = 500
        self.player_width = 40
        self.player_height = 60
        self.base_speed = 5
        self.current_speed = self.base_speed
        self.speed_multiplier = 1.0
        self.nitro_timer = 0
        
        # Difficulty settings - FIXED
        difficulty = settings.get('difficulty', 'Medium')
        self.difficulty_settings = {
            'Easy': {'spawn_rate': 0.015, 'traffic_speed': 3, 'obstacle_rate': 0.008, 'powerup_rate': 0.003},
            'Medium': {'spawn_rate': 0.025, 'traffic_speed': 4, 'obstacle_rate': 0.015, 'powerup_rate': 0.005},
            'Hard': {'spawn_rate': 0.04, 'traffic_speed': 6, 'obstacle_rate': 0.025, 'powerup_rate': 0.008}
        }.get(difficulty, {'spawn_rate': 0.025, 'traffic_speed': 4, 'obstacle_rate': 0.015, 'powerup_rate': 0.005})
        
        # Game objects
        self.coins = []
        self.powerups = []
        self.obstacles = []
        self.traffic = []
        
        # Car color
        self.car_color = self.settings.get('car_color', (0, 255, 0))
        
    def update_settings(self, settings):
        self.settings = settings
        self.car_color = settings.get('car_color', (0, 255, 0))
        difficulty = settings.get('difficulty', 'Medium')
        self.difficulty_settings = {
            'Easy': {'spawn_rate': 0.015, 'traffic_speed': 3, 'obstacle_rate': 0.008, 'powerup_rate': 0.003},
            'Medium': {'spawn_rate': 0.025, 'traffic_speed': 4, 'obstacle_rate': 0.015, 'powerup_rate': 0.005},
            'Hard': {'spawn_rate': 0.04, 'traffic_speed': 6, 'obstacle_rate': 0.025, 'powerup_rate': 0.008}
        }.get(difficulty, {'spawn_rate': 0.025, 'traffic_speed': 4, 'obstacle_rate': 0.015, 'powerup_rate': 0.005})
    
    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.lane_index > 0:
            self.lane_index -= 1
            self.player_x = self.lanes[self.lane_index] - 20
            pygame.time.wait(50)
        if keys[pygame.K_RIGHT] and self.lane_index < len(self.lanes) - 1:
            self.lane_index += 1
            self.player_x = self.lanes[self.lane_index] - 20
            pygame.time.wait(50)
    
    def spawn_coin(self):
        if random.random() < 0.02:
            lane = random.choice(self.lanes)
            x = lane - 15
            y = -30
            value = random.choices([10, 20, 50], weights=[0.7, 0.2, 0.1])[0]
            self.coins.append(Coin(x, y, value))
    
    def spawn_powerup(self):
        if random.random() < self.difficulty_settings['powerup_rate']:
            lane = random.choice(self.lanes)
            x = lane - 15
            y = -30
            power_type = random.choice([PowerUpType.NITRO, PowerUpType.SHIELD, PowerUpType.REPAIR])
            self.powerups.append(PowerUp(x, y, power_type))
    
    def spawn_obstacle(self):
        if random.random() < self.difficulty_settings['obstacle_rate']:
            lane = random.choice(self.lanes)
            x = lane - 20
            y = -40
            obstacle_type = random.choice(['barrier', 'oil', 'pothole'])
            self.obstacles.append(Obstacle(x, y, obstacle_type))
    
    def spawn_traffic(self):
        if random.random() < self.difficulty_settings['spawn_rate']:
            lane = random.choice(self.lanes)
            x = lane - 20
            y = -60
            speed = self.difficulty_settings['traffic_speed'] + random.uniform(-0.5, 0.5)
            self.traffic.append(TrafficCar(x, y, speed))
    
    def update_objects(self):
        # Update coins
        for coin in self.coins[:]:
            coin.y += self.current_speed
            if coin.y > 600:
                self.coins.remove(coin)
        
        # Update powerups
        for powerup in self.powerups[:]:
            if not powerup.update():
                self.powerups.remove(powerup)
            else:
                powerup.y += self.current_speed
                if powerup.y > 600:
                    self.powerups.remove(powerup)
        
        # Update obstacles
        for obstacle in self.obstacles[:]:
            obstacle.y += self.current_speed
            if obstacle.y > 600:
                self.obstacles.remove(obstacle)
        
        # Update traffic
        for traffic in self.traffic[:]:
            traffic.update()
            if traffic.y > 600:
                self.traffic.remove(traffic)
    
    def check_collisions(self):
        player_rect = pygame.Rect(self.player_x, self.player_y, self.player_width, self.player_height)
        
        # Coin collisions
        for coin in self.coins[:]:
            coin_rect = pygame.Rect(coin.x, coin.y, coin.width, coin.height)
            if player_rect.colliderect(coin_rect):
                self.coins_collected += coin.value
                self.score += coin.value
                self.coins.remove(coin)
                # Difficulty scaling - increase speed
                self.current_speed = min(self.base_speed + (self.coins_collected // 15), 14)
        
        # Power-up collisions
        for powerup in self.powerups[:]:
            powerup_rect = pygame.Rect(powerup.x, powerup.y, powerup.width, powerup.height)
            if player_rect.colliderect(powerup_rect):
                self.activate_powerup(powerup.type)
                self.powerups.remove(powerup)
        
        # Obstacle collisions
        for obstacle in self.obstacles[:]:
            obstacle_rect = pygame.Rect(obstacle.x, obstacle.y, obstacle.width, obstacle.height)
            if player_rect.colliderect(obstacle_rect):
                if self.shield_active:
                    self.shield_active = False
                    self.active_powerup = None
                    self.obstacles.remove(obstacle)
                elif self.active_powerup == PowerUpType.REPAIR:
                    self.active_powerup = None
                    self.obstacles.remove(obstacle)
                    self.score += 50
                else:
                    self.state = GameState.GAME_OVER
                    return
        
        # Traffic collisions
        for traffic in self.traffic[:]:
            traffic_rect = pygame.Rect(traffic.x, traffic.y, traffic.width, traffic.height)
            if player_rect.colliderect(traffic_rect):
                if self.shield_active:
                    self.shield_active = False
                    self.active_powerup = None
                    self.traffic.remove(traffic)
                else:
                    self.state = GameState.GAME_OVER
                    return
    
    def activate_powerup(self, power_type):
        if power_type == PowerUpType.NITRO:
            self.nitro_timer = 180
            self.speed_multiplier = 1.8
            self.active_powerup = power_type
            self.powerup_timer = 180
        elif power_type == PowerUpType.SHIELD:
            self.shield_active = True
            self.active_powerup = power_type
            self.powerup_timer = 300
        elif power_type == PowerUpType.REPAIR:
            if self.obstacles:
                self.obstacles.pop(0)
            self.score += 100
            self.active_powerup = power_type
            self.powerup_timer = 1
    
    def update_powerups(self):
        if self.nitro_timer > 0:
            self.nitro_timer -= 1
            if self.nitro_timer == 0:
                self.speed_multiplier = 1.0
                if self.active_powerup == PowerUpType.NITRO:
                    self.active_powerup = None
        
        if self.powerup_timer > 0 and self.active_powerup != PowerUpType.NITRO:
            self.powerup_timer -= 1
            if self.powerup_timer == 0:
                if self.active_powerup == PowerUpType.SHIELD:
                    self.shield_active = False
                self.active_powerup = None
        
        self.current_speed = (self.base_speed + (self.coins_collected // 15)) * self.speed_multiplier
        self.current_speed = min(self.current_speed, 18)
    
    def update_distance(self):
        self.distance += int(self.current_speed)
        self.score += int(self.current_speed / 10)
    
    def draw_road(self):
        # Road background
        pygame.draw.rect(self.screen, (40, 40, 40), (120, 0, 560, 600))
        
        # Lane markings
        for i in range(1, 4):
            x = 120 + i * 140
            for y in range(0, 600, 40):
                pygame.draw.rect(self.screen, (255, 255, 255), (x - 2, y, 4, 25))
        
        # Road edges
        pygame.draw.line(self.screen, (255, 255, 0), (120, 0), (120, 600), 5)
        pygame.draw.line(self.screen, (255, 255, 0), (680, 0), (680, 600), 5)
    
    def draw_player(self):
        pygame.draw.rect(self.screen, self.car_color, (self.player_x, self.player_y, self.player_width, self.player_height))
        pygame.draw.rect(self.screen, (100, 100, 100), (self.player_x + 5, self.player_y + 5, self.player_width - 10, 10))
        pygame.draw.rect(self.screen, (50, 50, 50), (self.player_x + 5, self.player_y + 50, self.player_width - 10, 5))
        
        if self.shield_active:
            pygame.draw.circle(self.screen, (0, 255, 255), (self.player_x + 20, self.player_y + 30), 30, 3)
    
    def draw_powerup_status(self):
        if self.active_powerup:
            y_offset = 100
            font = pygame.font.Font(None, 24)
            
            if self.active_powerup == PowerUpType.NITRO:
                text = f"NITRO: {self.nitro_timer // 60}s"
                color = (255, 100, 0)
            elif self.active_powerup == PowerUpType.SHIELD:
                text = f"SHIELD: {self.powerup_timer // 60}s"
                color = (0, 100, 255)
            else:
                text = "REPAIR READY"
                color = (0, 255, 100)
            
            text_surface = font.render(text, True, color)
            self.screen.blit(text_surface, (10, y_offset))
    
    def draw_score(self):
        font = pygame.font.Font(None, 32)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        coins_text = font.render(f"Coins: {self.coins_collected}", True, (255, 215, 0))
        distance_text = font.render(f"Distance: {self.distance}m", True, (255, 255, 255))
        speed_text = font.render(f"Speed: {int(self.current_speed * 8)}km/h", True, (255, 255, 255))
        
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(coins_text, (10, 45))
        self.screen.blit(distance_text, (10, 80))
        self.screen.blit(speed_text, (10, 115))
    
    def draw(self):
        self.screen.fill((0, 0, 0))
        self.draw_road()
        
        for coin in self.coins:
            coin.draw(self.screen)
        
        for powerup in self.powerups:
            powerup.draw(self.screen)
        
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
        
        for traffic in self.traffic:
            traffic.draw(self.screen)
        
        self.draw_player()
        self.draw_score()
        self.draw_powerup_status()
        
        pygame.display.flip()
    
    def run(self):
        while self.state == GameState.RUNNING:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
            
            self.handle_input()
            self.spawn_coin()
            self.spawn_powerup()
            self.spawn_obstacle()
            self.spawn_traffic()
            self.update_objects()
            self.check_collisions()
            self.update_powerups()
            self.update_distance()
            self.draw()
            self.clock.tick(60)
        
        return (self.score, self.distance, self.coins_collected)