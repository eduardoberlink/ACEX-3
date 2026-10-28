"""Configurações da Fase 5 (primeira fase com câmera e imagens)."""
from pathlib import Path

# Caminho calculado a partir deste arquivo: o jogo roda de qualquer pasta
ASSETS_DIR = Path(__file__).resolve().parent / "assets"

# --- Tela ---
TITULO = "Fase 5 - Modularizada"
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 360
FPS = 65

# --- Mundo ---
WORLD_WIDTH = int(SCREEN_WIDTH * 1.4)  # o fundo é 40% mais largo que a tela
GROUND_H = 30

# --- Cores ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
