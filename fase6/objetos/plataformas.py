import pygame

from config import GREEN, YELLOW
from objetos.entidade import Entidade
from recursos import recorte, repetir_horizontal, superficie_solida

# Tipos de plataforma
CHAO = "chao"    # grama do tileset, repetida
GALHO = "galho"  # galho de árvore esticado

RECORTE_GRAMA = (68, 184, 27, 7)    # em tileset.png
RECORTE_GALHO = (155, 28, 21, 7)    # em sprites-ambiente.png


class Plataforma(Entidade):
    def __init__(self, x, y, width, height, tipo=GALHO):
        super().__init__(x, y, width, height)
        self.tipo = tipo
        self.image = self._criar_imagem(tipo, width, height)

    @staticmethod
    def _criar_imagem(tipo, width, height):
        if tipo == CHAO:
            grama = recorte("tileset.png", RECORTE_GRAMA)
            if grama:
                grama = pygame.transform.scale(grama, (height, height))
                return repetir_horizontal(grama, width, height, passo=height)
            return superficie_solida((width, height), GREEN)

        galho = recorte("sprites-ambiente.png", RECORTE_GALHO)
        if galho:
            return pygame.transform.scale(galho, (width, height))
        return superficie_solida((width, height), YELLOW)
