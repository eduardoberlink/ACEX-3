import pygame
from pygame.locals import *

# Importando Módulos da Fase 5 + O novo Espinho
from camera.cam import Camera
from objetos.plataformas import Plataforma
from objetos.porta import Porta
from objetos.espinho import Espinho
from personagem.player import Player
from inimigos.enemy import Inimigo

pygame.init()

# --- Configurações Tela ---
SCREEN_WIDTH = 640  # Mantemos a resolução "Retro" da Fase 5
SCREEN_HEIGHT = 360
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Fase 6')
clock = pygame.time.Clock()

# --- Assets ---
try:
    bg_original = pygame.image.load('fase6/assets/background.jpg').convert()
    # 1. Redimensiona a imagem para o tamanho exato da TELA (fica com a proporção bonita)
    bg_screen_sized = pygame.transform.scale(bg_original, (SCREEN_WIDTH, SCREEN_HEIGHT))
except:
    # Se der erro, cria um quadrado preto
    bg_screen_sized = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    bg_screen_sized.fill((20, 20, 40))

# 2. MUNDO GIGANTE (5000 pixels de largura)
WORLD_WIDTH = 5000

# 3. Criamos uma superfície vazia gigante
bg_extended = pygame.Surface((WORLD_WIDTH, SCREEN_HEIGHT))

# 4. Desenhamos a imagem repetida (lado a lado) até preencher tudo
# Calculamos quantas vezes a imagem cabe no mundo
tiles = (WORLD_WIDTH // SCREEN_WIDTH) + 1 

for i in range(tiles):
    # Colamos a imagem na posição 0, depois 640, depois 1280...
    bg_extended.blit(bg_screen_sized, (i * SCREEN_WIDTH, 0))
# --- Cores ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# --- CONSTRUINDO O NÍVEL ---
ground_h = 30
objs_colisao = [] # Chão e Plataformas
objs_morte = []   # Espinhos
inimigos = []     # Lista de inimigos

# ==========================================
# SETOR 1: O AQUECIMENTO (0 a 1000px)
# ==========================================
# Chão inicial
objs_colisao.append(Plataforma(0, SCREEN_HEIGHT - ground_h, 800, ground_h, GREEN))

# Escadinha simples
objs_colisao.append(Plataforma(300, 250, 100, 15, YELLOW))
objs_colisao.append(Plataforma(500, 200, 100, 15, YELLOW))

# Primeiro Inimigo (Tutorial de combate)
inimigos.append(Inimigo(600, SCREEN_HEIGHT - ground_h - 35, 35, 500, 750, speed=2))

# ==========================================
# SETOR 2: O LAGO DE ESPINHOS (1000px a 2000px)
# ==========================================
# Aqui não tem chão, só plataformas voadoras e espinhos embaixo
# Espinho gigante no chão (se cair, morre)
objs_morte.append(Espinho(800, SCREEN_HEIGHT - 10, 1200)) # Do pixel 800 ao 2000

# Parkour
coords_setor2 = [
    (900, 250, 80, 15),
    (1100, 220, 80, 15),
    (1250, 280, 80, 15), # Pulo baixo
    (1400, 200, 100, 15), # Plataforma pequena (difícil)
    (1600, 180, 50, 15),
    (1800, 250, 100, 15) # Descanso
]
for (x, y, w, h) in coords_setor2:
    objs_colisao.append(Plataforma(x, y, w, h, YELLOW))

# Inimigo voando/patrulhando em uma plataforma
inimigos.append(Inimigo(1800, 250 - 25, 25, 1800, 1900, speed=1))

# ==========================================
# SETOR 3: A TORRE (2000px a 3500px)
# ==========================================
# O chão volta, mas com inimigos rápidos
objs_colisao.append(Plataforma(2000, SCREEN_HEIGHT - ground_h, 1500, ground_h, GREEN))

# Dois inimigos rápidos no chão
inimigos.append(Inimigo(2200, SCREEN_HEIGHT - ground_h - 25, 25, 2100, 2500, speed=5))
inimigos.append(Inimigo(2800, SCREEN_HEIGHT - ground_h - 25, 25, 2600, 3000, speed=3))

# Obstáculos aéreos (precisa usar pulo duplo)
objs_colisao.append(Plataforma(2400, 200, 600, 15, YELLOW))
objs_morte.append(Espinho(2400, 210, 600)) # Espinho EM CIMA da plataforma! Cuidado!

# ==========================================
# SETOR 4: RETA FINAL (3500px a 5000px)d
# ==========================================
# Plataformas móveis simuladas (distantes) exigindo DASH
objs_colisao.append(Plataforma(3600, 250, 80, 15, YELLOW))
objs_colisao.append(Plataforma(3850, 250, 80, 15, YELLOW)) # Pulo longo (Dash necessário)
objs_colisao.append(Plataforma(4100, 250, 80, 15, YELLOW))

# Chão final seguro
objs_colisao.append(Plataforma(4300, SCREEN_HEIGHT - ground_h, 700, ground_h, GREEN))

# O Guardião Final (Inimigo muito rápido na porta)
inimigos.append(Inimigo(4500, SCREEN_HEIGHT - ground_h - 50, 50, 4300, 4800, speed=9))

# A Porta
porta_final = Porta(4900, SCREEN_HEIGHT - ground_h - 40, 40)

# ==========================================
# SETUP DO JOGADOR E CÂMERA
# ==========================================
player = Player(50, SCREEN_HEIGHT - 100, 35, WORLD_WIDTH)
camera = Camera(WORLD_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH)

# --- Estados ---
passou = False
morreu = False

def reiniciar_jogo():
    global passou, morreu
    player.reset()
    # Reinicia todos os inimigos
    for ini in inimigos:
        ini.reset()
    passou = False
    morreu = False

# --- LOOP PRINCIPAL ---
running = True
while running:
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

    if not passou and not morreu:
        # --- UPDATES ---
        player.update(objs_colisao)
        
        for ini in inimigos:
            ini.update()
            
        camera.update(player)

        # --- CHECAGEM DE MORTES ---
        # 1. Caiu no buraco (Y muito alto)
        if player.y > SCREEN_HEIGHT + 100:
            morreu = True
            
        # 2. Tocou em inimigo
        if player.colliderect(inimigos[0]): # Verifica colisão com qualquer inimigo da lista
             pass # Lógica feita abaixo no loop for
        
        for ini in inimigos:
            if player.colliderect(ini):
                morreu = True

        # 3. Tocou em espinhos
        for espinho in objs_morte:
            if player.colliderect(espinho):
                morreu = True

        # --- VITÓRIA ---
        if player.colliderect(porta_final):
            passou = True

        # --- DESENHO ---
        # Background com paralaxe simples (câmera movendo o fundo)
        screen.blit(bg_extended, (0, 0), (camera.x, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

        for obj in objs_colisao:
            obj.draw(screen, camera)
            
        for esp in objs_morte:
            esp.draw(screen, camera)
            
        for ini in inimigos:
            ini.draw(screen, camera)
            
        porta_final.draw(screen, camera)
        player.draw(screen, camera)

    elif morreu:
        font = pygame.font.SysFont('arial', 20, True, True)
        # Fundo vermelho translúcido
        screen.fill((100, 0, 0)) 
        text = font.render('VOCÊ MORREU! R para tentar de novo', True, WHITE)
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT // 2))

    elif passou:
        font = pygame.font.SysFont('arial', 20, True, False)
        screen.fill(BLACK)
        text = font.render('PARABÉNS! VOCÊ ZEROU O JOGO!', True, YELLOW)
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT // 2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()