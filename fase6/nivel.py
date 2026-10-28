"""Desenho do nível da Fase 6, escrito como dados.

Para mudar o mapa, basta editar as listas abaixo.
"""
from dataclasses import dataclass

from config import CHAO_Y, GROUND_H, SCREEN_HEIGHT
from inimigos.enemy import Inimigo
from objetos.espinho import Espinho
from objetos.plataformas import CHAO, GALHO, Plataforma
from objetos.porta import Porta

GALHO_H = 15

# (x, y, largura, altura, tipo)
PLATAFORMAS = [
    # --- SETOR 1: O AQUECIMENTO (0 a 1000px) ---
    (0, CHAO_Y, 800, GROUND_H, CHAO),
    (300, 250, 100, GALHO_H, GALHO),          # escadinha
    (500, 200, 100, GALHO_H, GALHO),

    # --- SETOR 2: O LAGO DE ESPINHOS (1000 a 2000px) - sem chão ---
    (900, 250, 80, GALHO_H, GALHO),
    (1100, 220, 80, GALHO_H, GALHO),
    (1250, 280, 80, GALHO_H, GALHO),          # pulo baixo
    (1400, 200, 100, GALHO_H, GALHO),         # plataforma pequena (difícil)
    (1600, 180, 50, GALHO_H, GALHO),
    (1800, 250, 100, GALHO_H, GALHO),         # descanso

    # --- SETOR 3: A TORRE (2000 a 3500px) ---
    (2000, CHAO_Y, 1500, GROUND_H, CHAO),
    (2400, 200, 600, GALHO_H, GALHO),         # obstáculo aéreo (pulo duplo)

    # --- SETOR 4: RETA FINAL (3500 a 5000px) - exige DASH ---
    (3600, 250, 80, GALHO_H, GALHO),
    (3850, 250, 80, GALHO_H, GALHO),          # pulo longo
    (4100, 250, 80, GALHO_H, GALHO),
    (4300, CHAO_Y, 700, GROUND_H, CHAO),      # chão final seguro
]

# (x, y, largura)
ESPINHOS = [
    (800, SCREEN_HEIGHT - 10, 1200),          # lago de espinhos do setor 2
    (2400, 210, 600),                         # espinhos EM CIMA da plataforma do setor 3
]

# (x, y_da_superficie, tamanho, limite_esq, limite_dir, velocidade)
# O inimigo é posicionado em cima da superfície: y = superfície - tamanho
INIMIGOS = [
    (600, CHAO_Y, 35, 500, 750, 2),           # tutorial de combate
    (1800, 250, 25, 1800, 1900, 1),           # patrulhando a plataforma de descanso
    (2200, CHAO_Y, 25, 2100, 2500, 5),        # rápidos do setor 3
    (2800, CHAO_Y, 25, 2600, 3000, 3),
    (4500, CHAO_Y, 50, 4300, 4800, 9),        # o guardião final
]

PORTA = (4900, CHAO_Y - 40, 40)               # (x, y, tamanho)

PLAYER_INICIO = (50, SCREEN_HEIGHT - 100)
PLAYER_TAMANHO = 35


@dataclass
class Nivel:
    plataformas: list
    espinhos: list
    inimigos: list
    porta: Porta

    def reset(self):
        for inimigo in self.inimigos:
            inimigo.reset()


def construir_nivel():
    return Nivel(
        plataformas=[Plataforma(*dados) for dados in PLATAFORMAS],
        espinhos=[Espinho(*dados) for dados in ESPINHOS],
        inimigos=[
            Inimigo(x, sup - tam, tam, esq, dir_, speed=vel)
            for (x, sup, tam, esq, dir_, vel) in INIMIGOS
        ],
        porta=Porta(*PORTA),
    )
