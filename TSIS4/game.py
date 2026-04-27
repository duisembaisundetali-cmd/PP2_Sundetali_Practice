import pygame
import random
from config import *

class Food:
    def __init__(self, x, y, food_type="normal"):
        self.x = x
        self.y = y
        self.food_type = food_type
        self.spawn_time = pygame.time.get_ticks()
        
        if food_type == "normal":
            self.color = RED
            self.points = 1
            self.lifetime = None
        elif food_type == "golden":
            self.color = YELLOW
            self.points = 5
            self.lifetime = 5000
        elif food_type == "poison":
            self.color = DARK_RED
            self.points = -2
            self.lifetime = None
    
    def is_expired(self):
        if self.lifetime:
            return pygame.time.get_ticks() - self.spawn_time > self.lifetime
        return False

class PowerUp:
    def __init__(self, x, y, power_type):
        self.x = x
        self.y = y
        self.power_type = power_type
        self.spawn_time = pygame.time.get_ticks()
        
        if power_type == "speed":
            self.color = BLUE
            self.duration = 5000
        elif power_type == "slow":
            self.color = PURPLE
            self.duration = 5000
        elif power_type == "shield":
            self.color = ORANGE
            self.duration = None
    
    def is_expired(self):
        return pygame.time.get_ticks() - self.spawn_time > 8000

class Snake:
    def __init__(self, x, y, color):
        self.body = [[x, y]]
        self.direction = "RIGHT"
        self.change_to = self.direction
        self.color = color
        self.grow_flag = False
        self.shield_active = False
        self.shield_end_time = 0
    
    def move(self):
        self.direction = self.change_to
        
        if self.direction == "RIGHT":
            self.body.insert(0, [self.body[0][0] + 1, self.body[0][1]])
        elif self.direction == "LEFT":
            self.body.insert(0, [self.body[0][0] - 1, self.body[0][1]])
        elif self.direction == "UP":
            self.body.insert(0, [self.body[0][0], self.body[0][1] - 1])
        elif self.direction == "DOWN":
            self.body.insert(0, [self.body[0][0], self.body[0][1] + 1])
        
        if not self.grow_flag:
            self.body.pop()
        else:
            self.grow_flag = False
    
    def grow(self):
        self.grow_flag = True
    
    def shorten(self):
        if len(self.body) > 2:
            self.body.pop()
            self.body.pop()
            return True
        return False
    
    def check_collision(self, walls=None):
        head = self.body[0]
        
        if head[0] < 0 or head[0] >= GRID_SIZE or head[1] < 0 or head[1] >= GRID_SIZE:
            if self.shield_active:
                return False
            return True
        
        if head in self.body[1:]:
            if self.shield_active:
                return False
            return True
        
        if walls and head in walls:
            if self.shield_active:
                return False
            return True
        
        return False
    
    def activate_shield(self, duration):
        self.shield_active = True
        self.shield_end_time = pygame.time.get_ticks() + duration
    
    def update_shield(self):
        if self.shield_active and pygame.time.get_ticks() > self.shield_end_time:
            self.shield_active = False

class Game:
    def __init__(self, db, settings_manager, username):
        self.db = db
        self.settings_manager = settings_manager
        self.username = username
        
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game - Advanced")
        self.clock = pygame.time.Clock()
        
        self.font_small = pygame.font.Font(None, 24)
        self.font_medium = pygame.font.Font(None, 36)
        
        self.reset_game()
        self.personal_best = self.db.get_personal_best(username)
    
    def reset_game(self):
        snake_color = self.settings_manager.get("snake_color")
        self.snake = Snake(GRID_SIZE//2, GRID_SIZE//2, snake_color)
        
        self.score = 0
        self.level = 1
        self.foods_eaten_for_level = 0
        self.speed = FPS
        self.running = True
        
        self.foods = []
        self.powerups = []
        self.active_powerup = False
        self.walls = []
        
        self.speed_boost_end = 0
        self.slow_motion_end = 0
        
        self.spawn_food()
        
        if self.level >= 3:
            self.generate_obstacles()
    
    def spawn_food(self):
        available_positions = self.get_available_positions()
        if not available_positions:
            return
        
        rand = random.random()
        if rand < 0.7:
            food_type = "normal"
        elif rand < 0.85:
            food_type = "golden"
        else:
            food_type = "poison"
        
        x, y = random.choice(available_positions)
        self.foods.append(Food(x, y, food_type))
    
    def spawn_powerup(self):
        if self.active_powerup:
            return
        
        available_positions = self.get_available_positions()
        if not available_positions:
            return
        
        power_type = random.choice(["speed", "slow", "shield"])
        x, y = random.choice(available_positions)
        self.powerups.append(PowerUp(x, y, power_type))
        self.active_powerup = True
    
    def get_available_positions(self):
        occupied = set(tuple(pos) for pos in self.snake.body)
        occupied.update((food.x, food.y) for food in self.foods)
        occupied.update(tuple(wall) for wall in self.walls)
        
        available = []
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                if (x, y) not in occupied:
                    available.append((x, y))
        return available
    
    def generate_obstacles(self):
        self.walls = []
        num_obstacles = min(self.level * 2, 20)
        
        safe_zone = []
        head = self.snake.body[0]
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                x, y = head[0] + dx, head[1] + dy
                if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
                    safe_zone.append((x, y))
        
        available = self.get_available_positions()
        available = [pos for pos in available if pos not in safe_zone]
        
        for _ in range(num_obstacles):
            if available:
                wall_pos = random.choice(available)
                self.walls.append(list(wall_pos))
                available.remove(wall_pos)
    
    def apply_powerup(self, powerup):
        current_time = pygame.time.get_ticks()
        
        if powerup.power_type == "speed":
            self.speed_boost_end = current_time + powerup.duration
        elif powerup.power_type == "slow":
            self.slow_motion_end = current_time + powerup.duration
        elif powerup.power_type == "shield":
            self.snake.activate_shield(10000)
    
    def get_current_speed(self):
        base_speed = FPS + (self.level - 1) * 2
        current_time = pygame.time.get_ticks()
        
        if current_time < self.speed_boost_end:
            return min(base_speed + 5, 30)
        elif current_time < self.slow_motion_end:
            return max(base_speed - 3, 5)
        return base_speed
    
    def update(self):
        self.snake.update_shield()
        self.snake.move()
        
        if self.snake.check_collision(self.walls):
            self.game_over()
            return
        
        head = self.snake.body[0]
        
        # Check food collisions
        for food in self.foods[:]:
            if head[0] == food.x and head[1] == food.y:
                if food.food_type == "poison":
                    if not self.snake.shorten():
                        self.game_over()
                        return
                else:
                    self.score += food.points
                    self.foods_eaten_for_level += 1
                    self.snake.grow()
                
                self.foods.remove(food)
                self.spawn_food()
                
                if self.foods_eaten_for_level >= self.level * 3:
                    self.level_up()
                break
        
        # Check power-up collisions
        for powerup in self.powerups[:]:
            if head[0] == powerup.x and head[1] == powerup.y:
                self.apply_powerup(powerup)
                self.powerups.remove(powerup)
                self.active_powerup = False
        
        # Remove expired items
        for powerup in self.powerups[:]:
            if powerup.is_expired():
                self.powerups.remove(powerup)
                self.active_powerup = False
        
        for food in self.foods[:]:
            if food.is_expired():
                self.foods.remove(food)
                self.spawn_food()
        
        # Spawn power-up
        if not self.active_powerup and random.random() < 0.01:
            self.spawn_powerup()
    
    def level_up(self):
        self.level += 1
        self.foods_eaten_for_level = 0
        self.spawn_food()
        
        if self.level >= 3:
            self.generate_obstacles()
    
    def game_over(self):
        self.db.save_game_result(self.username, self.score, self.level)
        self.running = False
    
    def draw_grid(self):
        if self.settings_manager.get("grid_overlay"):
            for x in range(0, WINDOW_WIDTH, CELL_SIZE):
                pygame.draw.line(self.screen, GRAY, (x, 0), (x, WINDOW_HEIGHT))
            for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
                pygame.draw.line(self.screen, GRAY, (0, y), (WINDOW_WIDTH, y))
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw obstacles
        for wall in self.walls:
            pygame.draw.rect(self.screen, GRAY, 
                           (wall[0]*CELL_SIZE, wall[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        # Draw foods
        for food in self.foods:
            pygame.draw.rect(self.screen, food.color,
                           (food.x*CELL_SIZE, food.y*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        # Draw power-ups
        for powerup in self.powerups:
            pygame.draw.rect(self.screen, powerup.color,
                           (powerup.x*CELL_SIZE, powerup.y*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        # Draw snake
        for segment in self.snake.body:
            pygame.draw.rect(self.screen, self.snake.color,
                           (segment[0]*CELL_SIZE, segment[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        # Draw shield effect
        if self.snake.shield_active:
            pygame.draw.circle(self.screen, ORANGE,
                             (self.snake.body[0][0]*CELL_SIZE + CELL_SIZE//2,
                              self.snake.body[0][1]*CELL_SIZE + CELL_SIZE//2),
                             CELL_SIZE//2, 3)
        
        self.draw_grid()
        
        # Draw UI
        score_text = self.font_small.render(f"Score: {self.score}", True, WHITE)
        level_text = self.font_small.render(f"Level: {self.level}", True, WHITE)
        best_text = self.font_small.render(f"Best: {self.personal_best}", True, WHITE)
        
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (10, 35))
        self.screen.blit(best_text, (10, 60))
        
        # Draw active power-ups
        y_offset = 90
        current_time = pygame.time.get_ticks()
        if current_time < self.speed_boost_end:
            time_left = (self.speed_boost_end - current_time) // 1000
            text = self.font_small.render(f"Speed Boost: {time_left}s", True, BLUE)
            self.screen.blit(text, (10, y_offset))
        elif current_time < self.slow_motion_end:
            time_left = (self.slow_motion_end - current_time) // 1000
            text = self.font_small.render(f"Slow Motion: {time_left}s", True, PURPLE)
            self.screen.blit(text, (10, y_offset))
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return "quit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.snake.direction != "DOWN":
                        self.snake.change_to = "UP"
                    elif event.key == pygame.K_DOWN and self.snake.direction != "UP":
                        self.snake.change_to = "DOWN"
                    elif event.key == pygame.K_LEFT and self.snake.direction != "RIGHT":
                        self.snake.change_to = "LEFT"
                    elif event.key == pygame.K_RIGHT and self.snake.direction != "LEFT":
                        self.snake.change_to = "RIGHT"
            
            self.update()
            self.draw()
            self.clock.tick(self.get_current_speed())
        
        return "game_over"