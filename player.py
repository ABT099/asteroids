import pygame
from circleshape import CircleShape
from constants import MARGIN, PLAYER_RADIUS, PLAYER_SHOOT_COOLDOWN, PLAYER_SHOT_SPEED, PLAYER_SPEED, PLAYER_TURN_SPEED
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_cooldown = 0
        self.lives = 3
    
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw_heart(self, screen, x, y):
        size = 20
        
        pygame.draw.circle(screen, "red", (x - size//4, y), size//4)
        pygame.draw.circle(screen, "red", (x + size//4, y), size//4)
        
        points = [
            (x - size//2, y + size//8),
            (x + size//2, y + size//8),
            (x, y + size//2)
        ]
        pygame.draw.polygon(screen, "red", points)
    
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle())
        heart_spacing = 25
        base_y = MARGIN + 10 + self.radius
        for i in range(self.lives):
            self.draw_heart(screen, MARGIN + 10 + (i * heart_spacing), base_y)

    def update(self, dt):
        if self.shot_cooldown > 0:
            self.shot_cooldown -= dt
        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(dt * -1)

        if keys[pygame.K_d]:
            self.rotate(dt)

        if keys[pygame.K_w]:
            self.move(dt)

        if keys[pygame.K_s]:
            self.move(dt * -1)

        if keys[pygame.K_SPACE]:
            self.shoot()

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def shoot(self):
        if self.shot_cooldown <= 0:
            self.shot_cooldown = PLAYER_SHOOT_COOLDOWN
            shot = Shot(self.position.x, self.position.y)
            shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOT_SPEED

    def respawn(self):
        self.position = pygame.Vector2(pygame.display.get_surface().get_size()) / 2
        self.rotation = 0
        self.shot_cooldown = 0

    def kill(self):
        if self.lives > 0:
            self.lives -= 1

    def could_respawn(self):
        return self.lives > 0
