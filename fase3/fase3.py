"""Fase 3 - Inimigo

Novidade: um inimigo que patrulha e um estado de "morreu".
(Nota didática: a física volta a ser só o chão, sem plataformas e sem dash.)
Controles: A/D andar, W/Espaço pular, R repetir.
"""
import pygame
from pygame.locals import K_SPACE, K_r, K_w, KEYDOWN, QUIT

from inimigos.enemy import Inimigo
from objetos.plataformas import Plataforma
from objetos.porta import Porta
from personagem.player import Player

# --- Configurações ---
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
FPS = 60

GROUND_H = 50
PORTA_TAMANHO = 100
PLAYER_TAMANHO = 50
INIMIGO_TAMANHO = 40
INIMIGO_VELOCIDADE = 8

# --- Cores ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)

# --- Estados ---
JOGANDO, MORREU, VENCEU = "jogando", "morreu", "venceu"


def desenhar_mensagem(screen, fonte, texto, cor_texto, cor_fundo):
    screen.fill(cor_fundo)
    render = fonte.render(texto, True, cor_texto)
    screen.blit(render, (SCREEN_WIDTH // 2 - render.get_width() // 2, SCREEN_HEIGHT // 2))


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Fase 3 - Básico")
    clock = pygame.time.Clock()
    fonte_morte = pygame.font.SysFont("arial", 20, bold=True, italic=True)
    fonte_vitoria = pygame.font.SysFont("arial", 20, bold=True)

    # --- Mundo ---
    chao = Plataforma(0, SCREEN_HEIGHT - GROUND_H, SCREEN_WIDTH, GROUND_H, GREEN)  # única plataforma
    porta = Porta(SCREEN_WIDTH - PORTA_TAMANHO, chao.top - PORTA_TAMANHO, PORTA_TAMANHO)

    # O inimigo patrulha do canto esquerdo até a porta, começando perto dela
    inimigo = Inimigo(
        porta.left - INIMIGO_TAMANHO, chao.top - INIMIGO_TAMANHO, INIMIGO_TAMANHO,
        limit_left=0, limit_right=porta.left, speed=INIMIGO_VELOCIDADE,
    )

    player = Player(0, chao.top - PLAYER_TAMANHO, PLAYER_TAMANHO, SCREEN_WIDTH)

    estado = JOGANDO
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if estado == JOGANDO and event.key in (K_SPACE, K_w):
                    player.jump()  # pulo simples (ainda não existe dash)
                elif estado != JOGANDO and event.key == K_r:
                    player.reset()
                    inimigo.reset()
                    estado = JOGANDO

        if estado == JOGANDO:
            player.update(chao)  # nesta fase passamos só o chão, não uma lista
            inimigo.update()

            if player.colliderect(inimigo):
                estado = MORREU
            elif player.colliderect(porta):
                estado = VENCEU

            screen.fill(BLUE)
            chao.draw(screen)
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
