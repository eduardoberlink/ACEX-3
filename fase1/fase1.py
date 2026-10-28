"""Fase 1 - Introdução

Conceitos: loop do jogo, gravidade, pulo e colisão com o chão.
Controles: A/D andar, W/Espaço pular, R repetir.
"""
import pygame
from pygame.locals import K_SPACE, K_r, K_w, KEYDOWN, QUIT

from objetos.plataformas import Plataforma
from objetos.porta import Porta
from personagem.player import Player

# --- Configurações ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

GROUND_H = 50
PORTA_TAMANHO = 100
PLAYER_TAMANHO = 50

# --- Cores ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)


def desenhar_mensagem(screen, fonte, texto, cor_texto, cor_fundo):
    screen.fill(cor_fundo)
    render = fonte.render(texto, True, cor_texto)
    screen.blit(render, (SCREEN_WIDTH // 2 - render.get_width() // 2, SCREEN_HEIGHT // 2))


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Fase 1 - Introdução")
    clock = pygame.time.Clock()
    fonte = pygame.font.SysFont("arial", 20, bold=True)

    # --- Mundo ---
    chao = Plataforma(0, SCREEN_HEIGHT - GROUND_H, SCREEN_WIDTH, GROUND_H, GREEN)
    porta = Porta(SCREEN_WIDTH - PORTA_TAMANHO, chao.top - PORTA_TAMANHO, PORTA_TAMANHO)
    # O jogador começa no meio da tela, caindo do topo (y = 0)
    player = Player(SCREEN_WIDTH // 2 - PLAYER_TAMANHO // 2, 0, PLAYER_TAMANHO, SCREEN_WIDTH)

    passou = False
    running = True
    while running:
        # 1. Eventos (teclas apertadas uma vez)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if not passou and event.key in (K_SPACE, K_w):
                    player.jump()
                elif passou and event.key == K_r:
                    player.reset()
                    passou = False

        # 2. Lógica e desenho
        if not passou:
            player.update(chao)
            passou = player.colliderect(porta)

            screen.fill(BLUE)
            chao.draw(screen)
            porta.draw(screen)
            player.draw(screen)
        else:
            desenhar_mensagem(screen, fonte, "Parabéns, passou de fase!! Pressione R para Repetir.",
                              WHITE, BLACK)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
