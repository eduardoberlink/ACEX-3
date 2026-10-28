import pygame

PRETO = (0, 0, 0)


class Porta(pygame.Rect):
    """Saída da fase: um quadrado preto de lado `size`."""

    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        self.color = PRETO

    def draw(self, screen, camera):
        pygame.draw.rect(screen, self.color, camera.apply(self))
