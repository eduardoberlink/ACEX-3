import pygame
from pygame.locals import *
# Assumindo que support.py está acessível:
from support import import_cut_graphics 
# Importe a classe base da sua Plataforma/Espinho:
from objetos.plataformas import Plataforma 
from objetos.espinho import Espinho 

# --- CARREGAR E CORTAR O TILESET UMA VEZ ---
# TILE_SIZE: Definir o tamanho do tile (pode estar em settings.py)
TILE_SIZE = 32 # Valor típico para tiles

# Lista de superfícies cortadas do tileset.png
TILES = import_cut_graphics('tileset.png', TILE_SIZE)

# Identificadores para os tiles:
# TILE_CHAO: O tile que você quer usar para o chão e plataformas (ex: o primeiro tile)
TILE_CHAO = TILES[0] 
# TILE_ESPINHO: O tile que você quer usar para os espinhos (ex: o tile vermelho/de perigo)
# Você precisará contar qual é o índice do tile vermelho no seu tileset.png
TILE_ESPINHO = TILES[5] # Exemplo: assume que o espinho está no índice 5 (linha 0, coluna 5)


# --- NOVA CLASSE DE PLATAFORMA TEXTURIZADA ---
class TexturedTile(Plataforma): # Herda da sua classe Plataforma
    def __init__(self, x, y, width, height, tile_surface):
        super().__init__(x, y, width, height, (0, 0, 0)) # Chama o construtor da Plataforma, cor preta temporária
        
        self.tile_surface = tile_surface
        self.width = width
        self.height = height

    def draw(self, screen, camera):
        rect_visivel = camera.apply(self)
        
        # Desenha o tile repetidamente para cobrir toda a área da plataforma
        for i in range(0, self.width, TILE_SIZE):
            for j in range(0, self.height, TILE_SIZE):
                # Calcular a posição do tile atual (x + i, y + j)
                tile_rect = pygame.Rect(self.x + i, self.y + j, TILE_SIZE, TILE_SIZE)
                
                # Aplica a câmera e desenha
                final_rect = camera.apply(tile_rect)
                screen.blit(self.tile_surface, final_rect)


# --- NOVA CLASSE DE ESPINHO TEXTURIZADO ---
class TexturedSpike(Espinho): # Herda da sua classe Espinho
    def __init__(self, x, y, width, height, tile_surface):
        super().__init__(x, y, width) # Chama o construtor do Espinho
        
        self.tile_surface = tile_surface
        self.width = width
        self.height = height

    def draw(self, screen, camera):
        # O Espinho provavelmente só usa a altura (SCREEN_HEIGHT - 10)
        # Vamos desenhar o tile de espinho por toda a largura
        for i in range(0, self.width, TILE_SIZE):
            # Posiciona o tile de espinho
            tile_rect = pygame.Rect(self.x + i, self.y, TILE_SIZE, TILE_SIZE)
            
            # Aplica a câmera e desenha
            final_rect = camera.apply(tile_rect)
            screen.blit(self.tile_surface, final_rect)