import pygame
from pygame.locals import *

from objetos.plataformas import Plataforma
from objetos.porta import Porta
from personagem.player import Player

pygame.init()

# --- Configurações Fase 2 (Tela Menor) ---
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600  # <--- Altura ajustada
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Fase 2 - Plataformas ')
clock = pygame.time.Clock()

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)

# --- Criando o Mundo ---
ground_height = 50
objetos_colisao = []

# 1. Chão (Agora fica na posição Y = 550)
chao = Plataforma(0, SCREEN_HEIGHT - ground_height, SCREEN_WIDTH, ground_height, GREEN)
objetos_colisao.append(chao)

# 2. Plataformas Voadoras (Recalculadas para caber em 600px)
# O chão está em y=550. O pulo alcança uns 120px de altura.
# Vamos subir de 100 em 100 pixels.
plataformas_coords = [
    (200, 450, 150, 20),  # Degrau 1
    (450, 350, 150, 20),  # Degrau 2
    (700, 250, 150, 20),  # Degrau 3
    (400, 150, 200, 20)   # Degrau 4 (O mais alto)
]

for (x, y, w, h) in plataformas_coords:
    p = Plataforma(x, y, w, h, YELLOW)
    objetos_colisao.append(p)

# 3. Saída
# Coloca a porta em cima da última plataforma (Degrau 4)
final_size = 80
ultima_plat = objetos_colisao[-1] 
porta_final = Porta(ultima_plat.x + 50, ultima_plat.top - final_size, final_size)

# 4. Player
player_size = 50
player = Player(0, 0, player_size, SCREEN_WIDTH)
player.bottomleft = chao.topleft

# --- Estados ---
passou = False

def reiniciar_jogo():
    global passou
    player.reset()
    passou = False

# --- Loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not passou:
            if event.type == pygame.KEYDOWN:
                if (event.key == K_SPACE or event.key == K_w):
                    player.jump()
        else:
            if event.type == pygame.KEYDOWN and event.key == K_r:
                reiniciar_jogo()

    if not passou:
        # Update
        player.update(objetos_colisao)

        # Colisão com Porta
        if player.colliderect(porta_final):
            passou = True

        # Desenho
        screen.fill(BLUE)
        
        for obj in objetos_colisao:
            obj.draw(screen)
            
        porta_final.draw(screen)
        player.draw(screen)

    elif passou:
        font = pygame.font.SysFont('arial', 20, True, False)
        text = font.render('Parabéns! Pressione R para Repetir.', True, WHITE)
        screen.fill(BLACK)
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT // 2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()