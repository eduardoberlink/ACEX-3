"""Fase 2 - Plataformas

Novidade: uma LISTA de plataformas e colisão por todos os lados.
Controles: A/D andar, W/Espaço pular, R repetir.
"""
import pygame
from pygame.locals import K_SPACE, K_r, K_w, KEYDOWN, QUIT

from objetos.plataformas import Plataforma
from objetos.porta import Porta
from personagem.player import Player

# --- Configurações ---
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
FPS = 60

GROUND_H = 50
PORTA_TAMANHO = 80
PLAYER_TAMANHO = 50

# --- Cores ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)

# --- Mapa ---
# O chão fica em y=550 e o pulo alcança uns 120px: os degraus sobem de 100 em 100.
DEGRAUS = [  # (x, y, largura, altura)
    (200, 450, 150, 20),  # degrau 1
    (450, 350, 150, 20),  # degrau 2
    (700, 250, 150, 20),  # degrau 3
    (400, 150, 200, 20),  # degrau 4 (o mais alto, com a porta)
]


def desenhar_mensagem(screen, fonte, texto, cor_texto, cor_fundo):
    screen.fill(cor_fundo)
    render = fonte.render(texto, True, cor_texto)
    screen.blit(render, (SCREEN_WIDTH // 2 - render.get_width() // 2, SCREEN_HEIGHT // 2))


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Fase 2 - Plataformas")
    clock = pygame.time.Clock()
    fonte = pygame.font.SysFont("arial", 20, bold=True)

    # --- Mundo ---
    chao = Plataforma(0, SCREEN_HEIGHT - GROUND_H, SCREEN_WIDTH, GROUND_H, GREEN)
    plataformas = [chao] + [Plataforma(*d, YELLOW) for d in DEGRAUS]

    # A porta fica em cima do último degrau
    topo = plataformas[-1]
    porta = Porta(topo.x + 50, topo.top - PORTA_TAMANHO, PORTA_TAMANHO)

    # O jogador começa em pé no canto esquerdo do chão
    player = Player(0, chao.top - PLAYER_TAMANHO, PLAYER_TAMANHO, SCREEN_WIDTH)

    passou = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if not passou and event.key in (K_SPACE, K_w):
                    player.jump()
                elif passou and event.key == K_r:
                    player.reset()
                    passou = False

        if not passou:
            player.update(plataformas)
            passou = player.colliderect(porta)

            screen.fill(BLUE)
            for plat in plataformas:
                plat.draw(screen)
            porta.draw(screen)
            player.draw(screen)
        else:
            desenhar_mensagem(screen, fonte, "Parabéns! Pressione R para Repetir.", WHITE, BLACK)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
