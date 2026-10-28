"""Configurações gerais do jogo (tela, mundo, cores e caminhos)."""
from pathlib import Path

# Caminhos calculados a partir deste arquivo: o jogo roda de qualquer pasta.
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"

# --- Tela ---
TITULO = "Fase 6"
SCREEN_WIDTH = 640   # resolução "retro" herdada da Fase 5
SCREEN_HEIGHT = 360
FPS = 60

# --- Mundo ---
WORLD_WIDTH = 5000
GROUND_H = 30                          # altura do chão
CHAO_Y = SCREEN_HEIGHT - GROUND_H      # topo do chão
LIMITE_QUEDA = SCREEN_HEIGHT + 100     # abaixo disso o jogador morreu

# --- Cores ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
COR_FUNDO_RESERVA = (20, 20, 40)
COR_TELA_MORTE = (100, 0, 0)
