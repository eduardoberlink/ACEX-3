import pygame


class Inimigo(pygame.Rect):
    COLOR = (255, 0, 255)  # magenta

    def __init__(self, x, y, size, limit_left, limit_right, speed=8):
        super().__init__(x, y, size, size)
        self.speed = speed
        self.limit_left = limit_left
        self.limit_right = limit_right
        self.start_pos = (x, y)  # para o reset

    def update(self):
        self.x += self.speed
        # Patrulha: inverte a direção ao bater nos limites
        if self.left <= self.limit_left or self.right >= self.limit_right:
            self.speed *= -1

    def reset(self):
        self.topleft = self.start_pos
        self.speed = abs(self.speed)  # volta andando para a direita

    def draw(self, screen):
        # Desenha direto na posição (sem câmera)
        pygame.draw.rect(screen, self.COLOR, self)
