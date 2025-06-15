import os
import pygame
import random
from src.entities.circleshape import CircleShape
from src.game.constants import ASTEROID_MIN_RADIUS, ASTEROID_SPEED
    
class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        size = int(self.radius * 1.5 * 2)
        self.image = pygame.transform.scale(pygame.image.load(os.path.join("assets", "asteroid.png")).convert_alpha(), (size, size))
        self.rect = self.image.get_rect(center=self.position)

        self.velocity = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)) * ASTEROID_SPEED


    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, dt):
        self.position += self.velocity * dt
        self.rect.center = self.position
        self.wrap_around_screen()

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        
        angle = random.uniform(20, 50)

        vec1 = self.velocity.rotate(angle)
        vec2 = self.velocity.rotate(-angle)

        new_radius = self.radius / 2

        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid1.velocity = vec1 * 1.2

        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2.velocity = vec2 * 1.2