"""Carregamento de imagens com cache e imagens reserva.

Cada arquivo é lido do disco uma única vez, mesmo que várias plataformas
ou inimigos usem a mesma imagem.
"""
from functools import lru_cache

import pygame

from config import ASSETS_DIR


@lru_cache(maxsize=None)
def imagem(nome, alpha=True):
    """Carrega assets/<nome>. Retorna None (e avisa no terminal) se falhar."""
    caminho = ASSETS_DIR / nome
    try:
        img = pygame.image.load(str(caminho))
    except (pygame.error, FileNotFoundError) as erro:
        print(f"[recursos] Não foi possível carregar '{caminho}': {erro}")
        return None
    return img.convert_alpha() if alpha else img.convert()


def recorte(nome, area):
    """Recorta um pedaço (x, y, largura, altura) de uma imagem. None se falhar."""
    img = imagem(nome)
    if img is None:
        return None
    try:
        return img.subsurface(area)
    except ValueError as erro:
        print(f"[recursos] Recorte {area} fora de '{nome}': {erro}")
        return None


def superficie_solida(tamanho, cor):
    """Retângulo de uma cor só (usado quando uma imagem não carrega)."""
    surf = pygame.Surface(tamanho, pygame.SRCALPHA)
    surf.fill(cor)
    return surf


def repetir_horizontal(tile, largura, altura, passo=None):
    """Cola o tile lado a lado até preencher `largura`."""
    passo = passo or tile.get_width()
    surf = pygame.Surface((largura, altura), pygame.SRCALPHA)
    for x in range(0, largura, passo):
        surf.blit(tile, (x, 0))
    return surf
