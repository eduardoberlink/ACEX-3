import pygame
from pygame.locals import *

# Importando nossos novos módulos
from camera.cam import Camera
from objetos.plataformas import Plataforma
from objetos.porta import Porta
from personagem.player import Player
from inimigos.enemy import Inimigo

pygame.init()

# --- Configurações da Tela ---
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 360
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Fase 5 - Modularizada')
clock = pygame.time.Clock()

# --- Cores ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# --- Carregamento de Assets ---
# Mantemos isso aqui para passar a imagem para o loop de desenho
try:
    background_img_original = pygame.image.load('fase6/assets/background.jpg').convert()
    background_width = int(SCREEN_WIDTH * 1.4)
    background_extended = pygame.transform.scale(background_img_original, (background_width, SCREEN_HEIGHT))
except pygame.error as e:
    print(f"Erro ao carregar background: {e}")
    background_width = int(SCREEN_WIDTH * 1.4)
    background_extended = pygame.Surface((background_width, SCREEN_HEIGHT))
    background_extended.fill(BLACK)

# --- Setup do Nível ---
ground_height = 30
# Lista de objetos que colidem (Chão + Plataformas)
objetos_colisao = []

# 1. Chão
chao = Plataforma(0, SCREEN_HEIGHT - ground_height, background_width, ground_height, GREEN)
objetos_colisao.append(chao)

# 2. Plataformas Flutuantes
plats_coords = [
    (80, SCREEN_HEIGHT - ground_height - 60, 100, 15),
    (260, SCREEN_HEIGHT - ground_height - 120, 120, 15),
    (450, SCREEN_HEIGHT - ground_height - 80, 100, 15)
]
for (x, y, w, h) in plats_coords:
    p = Plataforma(x, y, w, h, YELLOW)
    objetos_colisao.append(p)

# 3. Saída (Porta)
final_size = 30
porta_final = Porta(560, chao.top - final_size, final_size)

# 4. Inimigo
enemy_size = 25
borda_esquerda = 100
borda_direita = porta_final.left - 20
# Inicia no meio (300)
inimigo = Inimigo(300, chao.top - enemy_size, enemy_size, borda_esquerda, borda_direita)

# 5. Jogador
player_size = 25
player = Player(50, chao.top - player_size, player_size, background_width)

# 6. Câmera
camera = Camera(background_width, SCREEN_HEIGHT, SCREEN_WIDTH)

# --- Estados do Jogo ---
passou = False
morreu = False

def reiniciar_jogo():
    global passou, morreu
    player.reset()
    inimigo.reset()
    passou = False
    morreu = False

# --- Loop Principal ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not passou and not morreu:
            if event.type == pygame.KEYDOWN:
                # Pulo
                if (event.key == K_SPACE or event.key == K_w):
                    player.jump()
                # Dash
                if event.key == K_e:
                    player.start_dash()
        else:
            # Reiniciar se morreu ou ganhou
            if event.type == pygame.KEYDOWN and event.key == K_r:
                reiniciar_jogo()

    if not passou and not morreu:
        # --- Atualizações (Updates) ---
        player.update(objetos_colisao)
        inimigo.update()
        camera.update(player)

        # --- Colisões de Jogo ---
        if player.colliderect(inimigo):
            morreu = True
        
        if player.colliderect(porta_final):
            passou = True

        # --- Desenho (Draw) ---
        # 1. Background (com parallax simples da camera)
        screen.blit(background_extended, (0, 0), (camera.x, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

        # 2. Objetos
        for obj in objetos_colisao:
            obj.draw(screen, camera)
        
        porta_final.draw(screen, camera)
        inimigo.draw(screen, camera)
        player.draw(screen, camera)

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