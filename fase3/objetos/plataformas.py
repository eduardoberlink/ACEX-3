import pygame

class Plataforma(pygame.Rect):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height)
        self.color = color

    def draw(self, screen):
        # Desenha direto na tela
        pygame.draw.rect(screen, self.color, self)