"""Fase 4 - Habilidades

Novidades: plataformas + inimigo juntos, pulo duplo, dash e escalada.
Controles: A/D andar, W/Espaço pular (2x), E dash, W na parede escala, R repetir.
"""
import pygame
from pygame.locals import K_SPACE, K_e, K_r, K_w, KEYDOWN, QUIT

from inimigos.enemy import Inimigo
from objetos.plataformas import Plataforma
from objetos.porta import Porta
from personagem.player import Player

# --- Configurações ---
# Tela grande e fixa (ainda sem câmera)
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
FPS = 65

GROUND_H = 50
PORTA_TAMANHO = 100
PLAYER_TAMANHO = 50
INIMIGO_TAMANHO = 40
INIMIGO_X = 600
INIMIGO_VELOCIDADE = 0  # com 0 o inimigo fica parado

# --- Cores ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)

# --- Mapa ---
CHAO_Y = SCREEN_HEIGHT - GROUND_H
PLATAFORMAS = [  # (x, y, largura, altura)
    (150, CHAO_Y - 100, 200, 20),
    (400, CHAO_Y - 200, 150, 20),
    (650, CHAO_Y - 300, 200, 20),
]

# --- Estados ---
JOGANDO, MORREU, VENCEU = "jogando", "morreu", "venceu"


def desenhar_mensagem(screen, fonte, texto, cor_texto, cor_fundo):
    screen.fill(cor_fundo)
    render = fonte.render(texto, True, cor_texto)
    screen.blit(render, (SCREEN_WIDTH // 2 - render.get_width() // 2, SCREEN_HEIGHT // 2))


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Fase 4")
    clock = pygame.time.Clock()
    fonte_morte = pygame.font.SysFont("arial", 20, bold=True, italic=True)
    fonte_vitoria = pygame.font.SysFont("arial", 20, bold=True)

    # --- Mundo ---
    chao = Plataforma(0, CHAO_Y, SCREEN_WIDTH, GROUND_H, GREEN)
    plataformas = [chao] + [Plataforma(*d, YELLOW) for d in PLATAFORMAS]

    porta = Porta(SCREEN_WIDTH - PORTA_TAMANHO, CHAO_Y - PORTA_TAMANHO, PORTA_TAMANHO)

    # Patrulha do começo da tela até a porta
    inimigo = Inimigo(
        INIMIGO_X, CHAO_Y - INIMIGO_TAMANHO, INIMIGO_TAMANHO,
        limit_left=0, limit_right=porta.left, speed=INIMIGO_VELOCIDADE,
    )

    player = Player(0, CHAO_Y - PLAYER_TAMANHO, PLAYER_TAMANHO, SCREEN_WIDTH)

    estado = JOGANDO
    running = True
    while running:
        # 1. Eventos
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if estado == JOGANDO:
                    if event.key in (K_SPACE, K_w):
                        player.jump()
                    elif event.key == K_e:
                        player.start_dash()
                elif event.key == K_r:
                    player.reset()
                    inimigo.reset()
                    estado = JOGANDO

        # 2. Lógica e desenho
        if estado == JOGANDO:
            player.update(plataformas)
            inimigo.update()

            if player.colliderect(inimigo):
                estado = MORREU
            elif player.colliderect(porta):
                estado = VENCEU

            # Desenha tudo direto na tela (sem câmera)
            screen.fill(BLUE)
            for plat in plataformas:
                plat.draw(screen)
            porta.draw(screen)
            inimigo.draw(screen)
            player.draw(screen)
        elif estado == MORREU:
            desenhar_mensagem(screen, fonte_morte, "Você morreu!! Pressione R para repetir", WHITE, RED)
        else:
            desenhar_mensagem(screen, fonte_vitoria, "Parabéns! Pressione R para Repetir.", WHITE, BLACK)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
