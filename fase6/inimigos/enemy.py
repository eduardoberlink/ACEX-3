import pygame

from config import MAGENTA
from objetos.entidade import Entidade
from recursos import imagem, superficie_solida


class Inimigo(Entidade):
    """Capivara que patrulha entre limit_left e limit_right."""

    def __init__(self, x, y, size, limit_left, limit_right, speed=3):
        super().__init__(x, y, size, size)

        self.base_speed = speed
        self.speed = speed
        self.limit_left = limit_left
        self.limit_right = limit_right
        self.start_pos = (x, y)

        img = imagem("capivara-corrompida.png")
        if img:
            esquerda = pygame.transform.scale(img, (size, size))
        else:
            esquerda = superficie_solida((size, size), MAGENTA)

        # O sprite original olha para a esquerda; o espelhado é calculado uma vez só
        self.sprites = {-1: esquerda, 1: pygame.transform.flip(esquerda, True, False)}
        self._atualizar_sprite()

    def _atualizar_sprite(self):
        self.image = self.sprites[1 if self.speed > 0 else -1]

    def update(self):
        self.x += self.speed

        # Patrulha: inverte ao chegar num dos limites
        if self.left <= self.limit_left and self.speed < 0:
            self.speed *= -1
        elif self.right >= self.limit_right and self.speed > 0:
            self.speed *= -1

        self._atualizar_sprite()

    def reset(self):
        self.topleft = self.start_pos
        self.speed = abs(self.base_speed)
        self._atualizar_sprite()
