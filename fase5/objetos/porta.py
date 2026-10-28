import pygame

class Porta(pygame.Rect):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        self.color = (0, 0, 0) # Preto

    def draw(self, screen, camera):
        rect_visivel = camera.apply(self)
        pygame.draw.rect(screen, self.color, rect_visivel)