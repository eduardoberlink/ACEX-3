import pygame
from support import carregar_imagem


class Plataforma(pygame.Rect):
    def __init__(self, x, y, width, height, color, textura=None):
        super().__init__(x, y, width, height)
        self.color = color

        # --- atributos usados pelas novas mecânicas ---
        self.parede = False   # True = o jogador pode deslizar/pular nessa parede (item 1)
        self.movel = False    # True = a plataforma se move e carrega o jogador (item 2)
        self.dx = 0           # quanto ela andou neste quadro (só plataformas móveis)
        self.dy = 0

        # Cria uma superfície vazia do tamanho da plataforma para desenhar a textura nela
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)

        # --- TEXTURAS EXTRAS (usadas pela torre) ---
        if textura == "tronco":
            # Tronco de árvore (sprites-ambiente.png) repetido na vertical
            try:
                amb = carregar_imagem("sprites-ambiente.png")
                tronco = amb.subsurface((48, 88, 22, 10))
                tronco = pygame.transform.scale(tronco, (width, 10))
                for j in range(0, height, 10):
                    self.image.blit(tronco, (0, j))
            except Exception:
                self.image.fill((150, 90, 80))

        elif textura == "terra":
            # Tile de terra do tileset.png repetido nas duas direções
            try:
                tileset = carregar_imagem("tileset.png")
                terra = tileset.subsurface((192, 64, 32, 32))
                for i in range(0, width, 32):
                    for j in range(0, height, 32):
                        self.image.blit(terra, (i, j))
            except Exception:
                self.image.fill((100, 60, 70))

        # --- LÓGICA DO CHÃO (VERDE) ---
        elif color == (0, 255, 0):  # Se for o VERDE (Green)
            try:
                tileset = carregar_imagem("tileset.png")
                # Recorta um quadrado de grama do tileset
                tile_grama = tileset.subsurface((68, 184, 27, 7))
                tile_grama = pygame.transform.scale(tile_grama, (height, height))  # Escala para altura do chão

                # Repete a grama lado a lado até preencher a largura
                quantidade = (width // height) + 1
                for i in range(quantidade):
                    self.image.blit(tile_grama, (i * height, 0))
            except Exception:
                self.image.fill(color)  # Se der erro, pinta de verde

        # --- LÓGICA DAS PLATAFORMAS VOADORAS (AMARELO) ---
        elif color == (255, 255, 0):  # Se for AMARELO (Yellow)
            try:
                sprites_amb = carregar_imagem("sprites-ambiente.png")
                # Recorta o galho da árvore (lado direito da imagem)
                galho = sprites_amb.subsurface((155, 28, 21, 7))
                # Estica o galho para ficar do tamanho da plataforma
                self.image = pygame.transform.scale(galho, (width, height))
            except Exception:
                self.image.fill(color)  # Se der erro, pinta de amarelo

        # --- OUTROS CASOS ---
        else:
            self.image.fill(color)

    def draw(self, screen, camera):
        rect_visivel = camera.apply(self)
        screen.blit(self.image, rect_visivel)


# =====================================================
#   ITEM 1 - PAREDE (onde o pulo na parede funciona)
# =====================================================
class Parede(Plataforma):
    """Parede sólida de tronco. Só nas Paredes o jogador desliza e pula (item 1);
    nas plataformas comuns nada muda."""

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, (150, 90, 80), textura="tronco")
        self.parede = True


# =====================================================
#   ITEM 2 - PLATAFORMA MÓVEL
# =====================================================
class PlataformaMovel(Plataforma):
    """Plataforma que anda entre dois limites e leva junto quem está em cima.

    eixo="x": anda de um lado para o outro. limite_a e limite_b são o menor e o
              maior valor de x (posição da borda esquerda).
    eixo="y": anda para cima e para baixo. limite_a e limite_b são o menor e o
              maior valor de y (posição do topo).
    Usa a mesma lógica de patrulha dos inimigos: ao chegar num limite, inverte.
    """

    def __init__(self, x, y, width, height, limite_a, limite_b, velocidade=1, eixo="x"):
        super().__init__(x, y, width, height, (255, 255, 0))  # usa a textura do galho
        self.movel = True
        self.eixo = eixo
        self.limite_a = min(limite_a, limite_b)
        self.limite_b = max(limite_a, limite_b)
        self.vel_base = abs(velocidade)
        self.vel = self.vel_base
        self.start = (x, y)

        # Deixa o galho com um tom azulado: o jogador percebe que essa se move
        self.image = self.image.copy()
        self.image.fill((0, 45, 70, 0), special_flags=pygame.BLEND_RGB_ADD)

    def update(self):
        antes_x, antes_y = self.x, self.y

        if self.eixo == "x":
            self.x += self.vel
            if self.x <= self.limite_a:
                self.x = self.limite_a
                self.vel = self.vel_base
            elif self.x >= self.limite_b:
                self.x = self.limite_b
                self.vel = -self.vel_base
        else:
            self.y += self.vel
            if self.y <= self.limite_a:
                self.y = self.limite_a
                self.vel = self.vel_base
            elif self.y >= self.limite_b:
                self.y = self.limite_b
                self.vel = -self.vel_base

        # O jogador usa isso para ser levado junto
        self.dx = self.x - antes_x
        self.dy = self.y - antes_y

    def reset(self):
        self.x, self.y = self.start
        self.vel = self.vel_base
        self.dx = self.dy = 0
