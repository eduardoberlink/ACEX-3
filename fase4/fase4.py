import pygame
from pygame.locals import *

# Importa as classes da pasta Fase_04
from objetos.plataformas import Plataforma
from objetos.porta import Porta
from personagem.player import Player
from inimigos.enemy import Inimigo

pygame.init()

# --- Configurações da Fase 4 ---
# Tela Grande, fixa
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Fase 4')
clock = pygame.time.Clock()

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)

# --- Criando o Mundo ---

# 1. Chão e Plataformas
ground_height = 50
# Lista para passar para o player checar colisão
objetos_colisao = []

# Chão
chao = Plataforma(0, SCREEN_HEIGHT - ground_height, SCREEN_WIDTH, ground_height, GREEN)
objetos_colisao.append(chao)

# Plataformas (Posições originais da Fase 4)
plat_coords = [
    (150, SCREEN_HEIGHT - ground_height - 100, 200, 20),
    (400, SCREEN_HEIGHT - ground_height - 200, 150, 20),
    (650, SCREEN_HEIGHT - ground_height - 300, 200, 20)
]
for (x, y, w, h) in plat_coords:
    p = Plataforma(x, y, w, h, YELLOW)
    objetos_colisao.append(p)

# 2. Saída
final_size = 100
porta_final = Porta(SCREEN_WIDTH - final_size, SCREEN_HEIGHT - ground_height - final_size, final_size)

# 3. Inimigo
enemy_size = 40
# Limites da patrulha (Começo da tela até antes da porta)
borda_dir = 600
limite_porta= SCREEN_WIDTH - final_size
inimigo = Inimigo(borda_dir, 
                  SCREEN_HEIGHT - ground_height - enemy_size, 
                  enemy_size, 
                  0,
                  limite_porta, 
                  speed=0)

# 4. Player
player_size = 50
player = Player(0, 0, player_size, SCREEN_WIDTH)
player.bottomleft = chao.topleft # Posiciona no chão

# --- Variáveis de Controle ---
passou = False
morreu = False

def reiniciar_jogo():
    global passou, morreu
    # Reset do player
    player.reset()
    # Reset do inimigo
    inimigo.reset()
    
    passou = False
    morreu = False

# --- Loop Principal ---
running = True
while running:
    # 1. Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not passou and not morreu:
            if event.type == pygame.KEYDOWN:
                if (event.key == K_SPACE or event.key == K_w):
                    player.jump()
                if event.key == K_e:
                    player.start_dash()
        else:
            if event.type == pygame.KEYDOWN and event.key == K_r:
                reiniciar_jogo()

    # 2. Lógica de Jogo
    if not passou and not morreu:
        player.update(objetos_colisao)
        inimigo.update()

        if player.colliderect(inimigo):
            morreu = True
        
        if player.colliderect(porta_final):
            passou = True

        # 3. Desenho (Render)
        screen.fill(BLUE) # Fundo azul simples
        
        # Desenha tudo diretamente (sem câmera)
        for obj in objetos_colisao:
            obj.draw(screen)
            
        porta_final.draw(screen)
        inimigo.draw(screen)
        player.draw(screen)

    # 4. Telas de Game Over / Vitoria
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
    clock.tick(65)

pygame.quit()