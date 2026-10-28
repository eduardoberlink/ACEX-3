from config import RED
from objetos.entidade import Entidade
from recursos import recorte, repetir_horizontal, superficie_solida

ALTURA_HITBOX = 25
ALTURA_IMAGEM = 26
PASSO = 16                        # distância entre um espinho e o próximo
RECORTE_ESPINHO = (64, 105, 23, 12)  # em tileset.png


class Espinho(Entidade):
    def __init__(self, x, y, width):
        super().__init__(x, y, width, ALTURA_HITBOX)

        tile = recorte("tileset.png", RECORTE_ESPINHO)
        if tile:
            self.image = repetir_horizontal(tile, width, ALTURA_IMAGEM, passo=PASSO)
        else:
            self.image = superficie_solida((width, ALTURA_IMAGEM), RED)
