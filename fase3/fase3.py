import pygame
from pygame.locals import *

from objetos.plataformas import Plataforma
from objetos.porta import Porta
from personagem.player import Player
from inimigos.enemy import Inimigo

pygame.init()

# --- Configurações Fase 3 ---
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Fase 3 - Básico')
clock = pygame.time.Clock()

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
MAGENTA = (255, 0, 255)

# --- Criando o Mundo ---
ground_height = 50

# 1. Chão (Única plataforma desta fase)
chao = Plataforma(0, SCREEN_HEIGHT - ground_height, SCREEN_WIDTH, ground_height, GREEN)

# 2. Saída
final_size = 100
porta_final = Porta(SCREEN_WIDTH - final_size, SCREEN_HEIGHT - ground_height - final_size, final_size)

# 3. Inimigo
enemy_size = 40
limit_door = SCREEN_WIDTH - final_size # Limite direito é a porta
inimigo = Inimigo(
    limit_door - enemy_size,            # Começa perto da porta
    SCREEN_HEIGHT - ground_height - enemy_size, 
    enemy_size, 
    0,                                  # Limite esquerdo
    limit_door,                         # Limite direito
    speed=8
)

# 4. Player
player_size = 50
player = Player(0, 0, player_size, SCREEN_WIDTH)
player.bottomleft = chao.topleft

# --- Estados ---
passou = False
morreu = False

def reiniciar_jogo():
    global passou, morreu
    player.reset()
    inimigo.reset()
    passou = False
    morreu = False

# --- Loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not passou and not morreu:
            if event.type == pygame.KEYDOWN:
                # Pulo Simples
                if (event.key == K_SPACE or event.key == K_w):
                    player.jump()
                # (Nota Didática: Aqui não tem checagem de Dash 'E')
        else:
            if event.type == pygame.KEYDOWN and event.key == K_r:
                reiniciar_jogo()

    if not passou and not morreu:
        # Updates
        # Na fase 3, passamos apenas o objeto 'chao', não uma lista
        player.update(chao) 
        inimigo.update()

        # Colisões
        if player.colliderect(inimigo):
            morreu = True
        
        if player.colliderect(porta_final):
            passou = True

        # Desenho
        screen.fill(BLUE)
        
        chao.draw(screen)
        porta_final.draw(screen)
        inimigo.draw(screen)
        player.draw(screen)

    elif morreu:
        font = pygame.font.SysFont('arial', 20, True, True)
        text = font.render('Você morreu!! Pressione R para repetir', True, WHITE)
        screen.fill(RED)
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT // 2))

    elif passou:
        font = pygame.font.SysFont('arial', 20, True, False)
        text = font.render('Parabéns! Pressione R para Repetir.', True, WHITE)
        screen.fill(BLACK)
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT // 2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()