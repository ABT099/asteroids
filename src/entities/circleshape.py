from src.entities.gameobject import GameObject

class CircleShape(GameObject):
    def __init__(self, x, y, radius):
        super().__init__(x, y)
        self.radius = radius

    def draw(self, screen):
        # sub-classes must override
        pass

    def update(self, dt):
        # sub-classes must override
        pass

    def collide(self, other):
        return self.position.distance_to(other.position) < (self.radius + other.radius)