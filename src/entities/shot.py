import pygame
from src.entities.circleshape import CircleShape
from src.game.constants import PLAYER_SHOT_SPEED, SCREEN_HEIGHT, SCREEN_WIDTH, SHOT_RADIUS

class Shot(CircleShape):
    def __init__(self, position, rotation):
        super().__init__(position.x, position.y, SHOT_RADIUS)
        
        self.velocity = pygame.math.Vector2(0, -1).rotate(-rotation) * PLAYER_SHOT_SPEED

    def draw(self, screen):
        pygame.draw.circle(screen, "yellow", self.position, self.radius)

    def update(self, dt):
        self.position += self.velocity * dt
        
        if self.position.x + self.radius < 0 or \
           self.position.x - self.radius > SCREEN_WIDTH or \
           self.position.y + self.radius < 0 or \
           self.position.y - self.radius > SCREEN_HEIGHT:
            self.kill()