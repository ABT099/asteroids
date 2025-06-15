import os
import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = []
        for i in range(1, 6): 
            try:
                path = os.path.join("assets", "explosions", f"exp{i}.png")
                img = pygame.image.load(path).convert_alpha()
                self.images.append(pygame.transform.scale(img, (100, 100)))
            except pygame.error:
                print(f"Warning: Could not load explosion image: {path}")
                pass
        self.index = 0
        self.image = self.images[self.index] if self.images else pygame.Surface((0,0)) 
        self.rect = self.image.get_rect(center=(x, y))
        self.animation_speed_ms = 75 
        self.last_update_time = pygame.time.get_ticks()

    def update(self, dt=None):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time > self.animation_speed_ms:
            self.last_update_time = current_time
            self.index += 1
            if self.index >= len(self.images):
                self.kill()
                return
            self.image = self.images[self.index]
            self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self, screen):
        screen.blit(self.image, self.rect)