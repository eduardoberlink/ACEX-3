"""Fase 5 - Câmera

Novidades: mundo maior que a tela, câmera que segue o jogador,
imagem de fundo e configurações separadas em config.py.
Controles: A/D andar, W/Espaço pular (2x), E dash, W na parede escala, R repetir.
"""
import pygame
from pygame.locals import K_SPACE, K_e, K_r, K_w, KEYDOWN, QUIT

from camera.cam import Camera
from config import (ASSETS_DIR, BLACK, FPS, GREEN, GROUND_H, RED, SCREEN_HEIGHT,
                    SCREEN_WIDTH, TITULO, WHITE, WORLD_WIDTH, YELLOW)
from inimigos.enemy import Inimigo
from objetos.plataformas import Plataforma
from objetos.porta import Porta
from personagem.player import Player

# --- Mapa ---
CHAO_Y = SCREEN_HEIGHT - GROUND_H
PLATAFORMAS = [  # (x, y, largura, altura)
    (80, CHAO_Y - 60, 100, 15),
    (260, CHAO_Y - 120, 120, 15),
    (450, CHAO_Y - 80, 100, 15),
]
PORTA_X, PORTA_TAMANHO = 560, 30
INIMIGO_X, INIMIGO_TAMANHO = 300, 25   # começa no meio
INIMIGO_LIMITE_ESQ = 100
PLAYER_X, PLAYER_TAMANHO = 50, 25

# --- Estados ---
JOGANDO, MORREU, VENCEU = "jogando", "morreu", "venceu"


def carregar_fundo():
    """Fundo esticado para a largura do mundo (preto se a imagem não carregar)."""
    caminho = ASSETS_DIR / "background.jpg"
    try:
        img = pygame.image.load(str(caminho)).convert()
        return pygame.transform.scale(img, (WORLD_WIDTH, SCREEN_HEIGHT))
    except (pygame.error, FileNotFoundError) as erro:
        print(f"Erro ao carregar o fundo '{caminho}': {erro}")
        fundo = pygame.Surface((WORLD_WIDTH, SCREEN_HEIGHT))
        fundo.fill(BLACK)
        return fundo


def desenhar_mensagem(screen, fonte, texto, cor_texto, cor_fundo):
    screen.fill(cor_fundo)
    render = fonte.render(texto, True, cor_texto)
    screen.blit(render, (SCREEN_WIDTH // 2 - render.get_width() // 2, SCREEN_HEIGHT // 2))


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITULO)
    clock = pygame.time.Clock()
    fonte_morte = pygame.font.SysFont("arial", 20, bold=True, italic=True)
    fonte_vitoria = pygame.font.SysFont("arial", 20, bold=True)
    fundo = carregar_fundo()

    # --- Mundo ---
    chao = Plataforma(0, CHAO_Y, WORLD_WIDTH, GROUND_H, GREEN)
    plataformas = [chao] + [Plataforma(*d, YELLOW) for d in PLATAFORMAS]
    porta = Porta(PORTA_X, CHAO_Y - PORTA_TAMANHO, PORTA_TAMANHO)
    inimigo = Inimigo(INIMIGO_X, CHAO_Y - INIMIGO_TAMANHO, INIMIGO_TAMANHO,
                      limit_left=INIMIGO_LIMITE_ESQ, limit_right=porta.left - 20)
    player = Player(PLAYER_X, CHAO_Y - PLAYER_TAMANHO, PLAYER_TAMANHO, WORLD_WIDTH)
    camera = Camera(WORLD_WIDTH, SCREEN_WIDTH)

    estado = JOGANDO
    running = True
    while running:
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

        if estado == JOGANDO:
            # --- Atualizações ---
            player.update(plataformas)
            inimigo.update()
            camera.update(player)

            if player.colliderect(inimigo):
                estado = MORREU
            elif player.colliderect(porta):
                estado = VENCEU

            # --- Desenho: só o pedaço do fundo que a câmera vê ---
            screen.blit(fundo, (0, 0), (camera.x, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            for obj in (*plataformas, porta, inimigo, player):
                obj.draw(screen, camera)
        elif estado == MORREU:
            desenhar_mensagem(screen, fonte_morte, "Você morreu!! Pressione R para repetir", WHITE, RED)
        else:
            desenhar_mensagem(screen, fonte_vitoria, "Parabéns! Pressione R para Repetir.", WHITE, BLACK)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
