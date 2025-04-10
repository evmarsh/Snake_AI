import pygame

RED = (255, 0, 0)

class Apple:
    def __init__(self, size):
        self.size = size
        self.pos = pygame.math.Vector2()

    def draw(self, surface):
        rect = pygame.Rect(self.pos.x, self.pos.y, self.size, self.size)
        pygame.draw.rect(surface, RED, rect)
    
    def setPosition(self, position: pygame.math.Vector2):
        self.pos = position

    def x(self):
        return self.pos.x
    
    def y(self):
        return self.pos.y