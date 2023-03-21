import pygame
import random
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.bird import Bird

class ObstacleManager:
    def __init__(self):
        self.obstacles = []

    def update(self, game):
        self.image_obstacles = [Cactus(), Bird()]
        if len(self.obstacles) == 0:
            self.obstacles.append(self.image_obstacles[random.randint(0,1)])
        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                if not game.player.has_power_up:
                    game.playing = False
                    game.death_count += 1 
                    break
                else:  
                    self.obstacles.remove(obstacle)
    
    def reset_obstacles(self):
        self.obstacles = []
    
    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)
