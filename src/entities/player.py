import os
import pygame
from src.entities.circleshape import CircleShape
from src.game.constants import (
    MARGIN, PLAYER_RADIUS, PLAYER_SHOOT_COOLDOWN, PLAYER_SPEED, PLAYER_TURN_SPEED
)
from src.entities.shot import Shot

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        size = int(self.radius * 8) 
        
        loaded_image = pygame.image.load(os.path.join("assets", "spaceship.png")).convert_alpha()
        scaled_image = pygame.transform.scale(loaded_image, (size, size))
        self.original_image = pygame.transform.rotate(scaled_image, -90)

        self.image = self.original_image
        self.rect = self.image.get_rect(center=self.position)


        self.rotation = 0
        self.shot_cooldown = 0
        self.lives = 3
   
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
        screen.blit(self.image, self.rect)
        heart_spacing = 25
        base_y = MARGIN + 10 + self.radius
        for i in range(self.lives):
            self.draw_heart(screen, MARGIN + 10 + (i * heart_spacing), base_y)
            
    def update(self, dt):
        if self.shot_cooldown > 0:
            self.shot_cooldown -= dt
       
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rotation += PLAYER_TURN_SPEED * dt
        if keys[pygame.K_d]:
            self.rotation -= PLAYER_TURN_SPEED * dt
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
            
        self.image = pygame.transform.rotate(self.original_image, self.rotation)
        self.rect = self.image.get_rect(center=self.position)

        self.wrap_around_screen()
        
    def move(self, dt):
        forward = pygame.math.Vector2(0, -1).rotate(-self.rotation)
        self.position += forward * PLAYER_SPEED * dt
        
    def shoot(self):
        if self.shot_cooldown <= 0:
            self.shot_cooldown = PLAYER_SHOOT_COOLDOWN
            forward = pygame.math.Vector2(0, -1).rotate(-self.rotation)
            
            # Calculate the nose position. It's the center of the ship,
            # plus a small offset in the forward direction. The offset is
            # roughly half the height of the ship's image.
            nose_position = self.position + forward * (self.rect.height / 2)
            Shot(nose_position, self.rotation)
            
    def respawn(self):
        self.position = pygame.Vector2(pygame.display.get_surface().get_size()) / 2
        self.rotation = 0
        self.shot_cooldown = 0
        
    def kill(self):
        if self.lives > 0:
            self.lives -= 1
            
    def could_respawn(self):
        return self.lives > 0