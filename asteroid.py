import pygame
import random
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "gray", self.position, self.radius)

    def update(self, dt):
        self.position += self.velocity * dt

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