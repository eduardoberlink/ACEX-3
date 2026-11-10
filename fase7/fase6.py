import pygame
from pygame.locals import *

from support import caminho_asset
from camera.cam import Camera
from objetos.plataformas import Plataforma, PlataformaMovel, Parede
from objetos.porta import Porta
from objetos.espinho import Espinho
from objetos.checkpoint import Checkpoint
from objetos.itens import Chave, Acai, Gema
from personagem.player import Player, INVENCIVEL_FRAMES
from inimigos.enemy import Inimigo
from interface.hud import desenhar_hud, desenhar_tela_derrota, desenhar_tela_vitoria, texto

# --- Configurações Tela ---
SCREEN_WIDTH = 640  # Mantemos a resolução "Retro" da Fase 5
SCREEN_HEIGHT = 360

# MUNDO GIGANTE (5000 pixels de largura)
WORLD_WIDTH = 5000

# --- Cores ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

VIDAS_INICIAIS = 3   # Item 12
ground_h = 30
CHAO_Y = SCREEN_HEIGHT - ground_h   # altura do topo do chão (330)


def construir_fundo():
    """Fundo do jogo: a imagem repetida lado a lado até cobrir o mundo inteiro."""
    try:
        bg_original = pygame.image.load(caminho_asset('background.jpg')).convert()
        # Redimensiona a imagem para o tamanho exato da TELA
        bg_screen_sized = pygame.transform.scale(bg_original, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except Exception:
        # Se der erro, cria um quadrado escuro
        bg_screen_sized = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        bg_screen_sized.fill((20, 20, 40))

    bg_extended = pygame.Surface((WORLD_WIDTH, SCREEN_HEIGHT))
    tiles = (WORLD_WIDTH // SCREEN_WIDTH) + 1
    for i in range(tiles):
        bg_extended.blit(bg_screen_sized, (i * SCREEN_WIDTH, 0))
    return bg_extended


def gema_em(cx, cy):
    """Cria uma gema com o CENTRO em (cx, cy)."""
    return Gema(cx - 8, cy - 8)


class Jogo:
    def __init__(self, screen):
        self.screen = screen
        self.bg = construir_fundo()
        self.camera = Camera(WORLD_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH)
        self.fonte = pygame.font.SysFont('arial', 14, True)
        self.fonte_dica = pygame.font.SysFont('arial', 13, True)
        self.fonte_grande = pygame.font.SysFont('arial', 22, True)

        # Recordes da sessão (item 13: incentiva repetir a fase)
        self.melhor_tempo = None
        self.melhor_gemas = 0

        self.reiniciar()

    # ==========================================
    #   CONSTRUINDO O NÍVEL
    # ==========================================
    def construir_nivel(self):
        self.objs_colisao = []   # Chão, plataformas e paredes
        self.moveis = []         # Plataformas móveis (também estão em objs_colisao)
        self.objs_morte = []     # Espinhos
        self.inimigos = []
        self.checkpoints = []
        self.gemas = []
        self.dicas = []          # textos de ajuda escritos no cenário: (x, y, texto)

        # ==========================================
        # SETOR 1: O AQUECIMENTO (0 a 1000px)
        # ==========================================
        # Chão inicial
        self.objs_colisao.append(Plataforma(0, CHAO_Y, 800, ground_h, GREEN))

        # Escadinha simples
        self.objs_colisao.append(Plataforma(300, 250, 100, 15, YELLOW))
        self.objs_colisao.append(Plataforma(500, 200, 100, 15, YELLOW))

        # Primeiro Inimigo (Tutorial de combate: aperte F ou pule em cima dele)
        self.inimigos.append(Inimigo(600, CHAO_Y - 35, 35, 500, 750, speed=2))

        self.gemas.append(gema_em(545, 85))   # exige o pulo duplo a partir da plataforma
        self.dicas.append((30, 100, "A/D mover   W/Espaço pular (segure = mais alto)   E dash   F purificar"))
        self.dicas.append((395, 150, "Capivara corrompida! Aperte F ou pule em cima dela"))

        # ==========================================
        # SETOR 2: O LAGO DE ESPINHOS (1000px a 2000px)
        # ==========================================
        # Espinho gigante no chão (se cair, perde uma vida)
        self.objs_morte.append(Espinho(800, SCREEN_HEIGHT - 10, 1200))  # Do pixel 800 ao 2000

        # Parkour
        coords_setor2 = [
            (900, 250, 80, 15),
            (1100, 220, 80, 15),
            (1250, 280, 80, 15),   # Pulo baixo
            (1400, 200, 100, 15),  # Plataforma pequena (difícil)
            (1600, 180, 50, 15),
            (1800, 250, 100, 15),  # Descanso
        ]
        for (x, y, w, h) in coords_setor2:
            self.objs_colisao.append(Plataforma(x, y, w, h, YELLOW))

        # Inimigo patrulhando em uma plataforma
        self.inimigos.append(Inimigo(1800, 250 - 25, 25, 1800, 1900, speed=1))

        self.gemas.append(gema_em(1212, 296))   # arriscada: no vão entre duas plataformas, perto dos espinhos
        self.gemas.append(gema_em(1450, 80))    # pulo duplo a partir da plataforma de 100px
        self.gemas.append(gema_em(1625, 70))    # pulo duplo a partir da plataforma de 50px

        # ==========================================
        # SETOR 3: A TORRE (2000px a 3500px)
        # ==========================================
        # O chão volta, mas com inimigos rápidos
        self.objs_colisao.append(Plataforma(2000, CHAO_Y, 1500, ground_h, GREEN))
        self.checkpoints.append(Checkpoint(2030, CHAO_Y))          # Item 11: começo do setor 3

        # Dois inimigos rápidos no chão
        self.inimigos.append(Inimigo(2200, CHAO_Y - 25, 25, 2100, 2500, speed=5))
        self.inimigos.append(Inimigo(2800, CHAO_Y - 25, 25, 2600, 3000, speed=3))

        # Obstáculos aéreos (precisa usar pulo duplo)
        self.objs_colisao.append(Plataforma(2400, 200, 600, 15, YELLOW))
        self.objs_morte.append(Espinho(2400, 210, 600))  # Espinho embaixo da plataforma! Cuidado!

        # --- A TORRE (itens 1, 3 e 4) ---
        # A base fica no alto (topo em y=190): sem ajuda, o pulo duplo (128px) não chega lá.
        # É preciso purificar a capivara da torre e subir nela como degrau (item 3).
        self.inimigos.append(Inimigo(3160, CHAO_Y - 35, 35, 3150, 3240, speed=2))
        self.objs_colisao.append(Plataforma(3246, 190, 172, 16, YELLOW))      # base da torre

        # Poço de paredes paralelas (item 1). A parede da esquerda deixa uma porta embaixo
        # (y 140 a 190) para entrar; a parede da direita termina no topo (y=40) e vira a
        # área secreta. Do chão do poço até lá são 150px: o pulo duplo (128px) não chega,
        # só subindo de parede em parede.
        self.objs_colisao.append(Parede(3270, 20, 24, 120))   # parede esquerda
        self.objs_colisao.append(Parede(3370, 40, 24, 150))   # parede direita

        # Área secreta no topo da torre: a chave (item 4) e uma gema
        self.objs_colisao.append(Plataforma(3394, 40, 90, 15, YELLOW))
        self.chave = Chave(3430, 16)
        self.gemas.append(gema_em(3332, 110))   # dentro do poço
        self.gemas.append(gema_em(3466, 20))    # na área secreta

        self.dicas.append((2880, 128, "Purifique a capivara e use-a de degrau!"))
        self.dicas.append((3090, 70, "Pule de parede em parede!"))

        # ==========================================
        # SETOR 4: RETA FINAL (3500px a 5000px)
        # ==========================================
        self.checkpoints.append(Checkpoint(3468, CHAO_Y))          # Item 11: começo do setor 4 (logo onde se desce da torre)

        # Item 5: tigela de açaí logo no começo (8s de velocidade + pulo extra)
        self.acai = Acai(3430, CHAO_Y - 24)

        # Atalho por cima: a primeira plataforma só é alcançável com o 3º pulo do açaí
        atalho = [
            (3530, 160, 70), (3660, 145, 70), (3790, 130, 70),
            (3920, 140, 70), (4050, 150, 70), (4180, 165, 70),
        ]
        for (x, y, w) in atalho:
            self.objs_colisao.append(Plataforma(x, y, w, 15, YELLOW))
        self.gemas.append(gema_em(4215, 130))   # recompensa do atalho

        # Item 2: plataformas móveis no lugar das 3 plataformas fixas
        mov = [
            PlataformaMovel(3550, 250, 80, 15, 3540, 3640, velocidade=1, eixo="x"),
            PlataformaMovel(3790, 250, 80, 15, 195, 280, velocidade=1, eixo="y"),
            PlataformaMovel(3970, 250, 80, 15, 3960, 4100, velocidade=2, eixo="x"),
        ]
        for m in mov:
            self.moveis.append(m)
            self.objs_colisao.append(m)
        self.gemas.append(gema_em(3925, 272))   # arriscada: sobre o buraco

        # Chão final seguro
        self.objs_colisao.append(Plataforma(4300, CHAO_Y, 700, ground_h, GREEN))

        # O Guardião Final (inimigo muito rápido): precisa de 3 purificações
        self.inimigos.append(Inimigo(4500, CHAO_Y - 50, 50, 4300, 4800, speed=9, vida=3))

        # A Porta (agora trancada: precisa da chave da torre)
        self.porta_final = Porta(4900, CHAO_Y - 40, 40)

    # ==========================================
    #   (RE)INICIAR O JOGO
    # ==========================================
    def reiniciar(self):
        self.construir_nivel()
        self.player = Player(50, CHAO_Y - 35, 35, WORLD_WIDTH)
        self.camera.update(self.player)

        self.estado = "jogando"        # "jogando", "derrota" ou "vitoria"
        self.vidas_max = VIDAS_INICIAIS
        self.vidas = VIDAS_INICIAIS
        self.tem_chave = False
        self.gemas_coletadas = 0
        self.checkpoint_pos = self.player.start_pos
        self.quadros = 0               # cronômetro (60 quadros = 1 segundo)
        self.mensagem = ""
        self.mensagem_timer = 0

    def mostrar_mensagem(self, msg, frames=150):
        self.mensagem = msg
        self.mensagem_timer = frames

    # ==========================================
    #   REGRAS DO JOGO
    # ==========================================
    def perder_vida(self, empurrao=0, renascer=False):
        """Tira uma vida. Dano de inimigo empurra o jogador; espinho/buraco leva ao checkpoint."""
        self.vidas -= 1
        if self.vidas <= 0:
            self.estado = "derrota"
            return

        if renascer:
            self.player.reset(self.checkpoint_pos)
            self.player.invencivel = INVENCIVEL_FRAMES
            self.acai.reset()          # o açaí volta, para dar para tentar o atalho de novo
            self.camera.update(self.player)
        else:
            self.player.levar_dano(empurrao)

    def empurrar_para_fora(self, ini):
        """Se uma capivara acabou de virar bloco em cima do jogador, tira o jogador de dentro dela."""
        p = self.player
        if p.colliderect(ini):
            if p.centerx < ini.centerx:
                p.right = ini.left
            else:
                p.left = ini.right
            p.sincronizar_posicao()

    def verificar_golpe(self):
        """ITEM 3 - o golpe (F) purifica as capivaras que estiverem na área à frente do jogador."""
        golpe = self.player.hitbox_ataque
        if golpe is None:
            return
        for ini in self.inimigos:
            if ini.purificado or id(ini) in self.player.ja_atingidos:
                continue
            if golpe.colliderect(ini):
                self.player.ja_atingidos.add(id(ini))
                if ini.receber_purificacao() and ini.purificado:
                    self.empurrar_para_fora(ini)

    def verificar_itens(self):
        p = self.player
        for g in self.gemas:
            if not g.coletado and p.colliderect(g):
                g.coletado = True
                self.gemas_coletadas += 1

        if not self.chave.coletado and p.colliderect(self.chave):
            self.chave.coletado = True
            self.tem_chave = True
            self.porta_final.destrancar()
            self.mostrar_mensagem("Pegou a chave! A porta final foi destrancada.")

        if not self.acai.coletado and p.colliderect(self.acai):
            self.acai.coletado = True
            p.ativar_acai()
            self.mostrar_mensagem("Açaí! Mais velocidade e um pulo extra por 8s.", 120)

    def verificar_checkpoints(self):
        for c in self.checkpoints:
            if not c.ativo and self.player.colliderect(c):
                c.ativar()
                self.checkpoint_pos = c.respawn_pos
                self.mostrar_mensagem("Checkpoint!", 90)

    def verificar_inimigos(self):
        p = self.player
        for ini in self.inimigos:
            if ini.purificado or not p.colliderect(ini):
                continue

            # ITEM 10 - cair por cima purifica e faz o jogador quicar (recupera o dash)
            pisada = p.vel_y > 0 and p.bottom_anterior <= ini.top + 8
            if pisada:
                p.bottom = ini.top
                p.sincronizar_posicao()
                ini.receber_purificacao()
                p.quicar()
            # ITEM 12 - contato lateral: perde uma vida (se não estiver invencível)
            elif p.invencivel == 0:
                lado = 1 if p.centerx >= ini.centerx else -1
                self.perder_vida(empurrao=lado)
                return

    def verificar_perigos(self):
        p = self.player
        # 1. Caiu no buraco (Y muito alto)
        if p.y > SCREEN_HEIGHT + 100:
            self.perder_vida(renascer=True)
            return
        # 3. Tocou em espinhos
        for espinho in self.objs_morte:
            if p.colliderect(espinho):
                self.perder_vida(renascer=True)
                return

    def verificar_porta(self):
        if self.player.colliderect(self.porta_final):
            if self.porta_final.trancada:
                if self.mensagem_timer == 0:
                    self.mostrar_mensagem("Porta trancada! A chave está no alto da torre.", 120)
            else:
                self.estado = "vitoria"
                if self.melhor_tempo is None or self.quadros < self.melhor_tempo:
                    self.melhor_tempo = self.quadros
                self.melhor_gemas = max(self.melhor_gemas, self.gemas_coletadas)

    # ==========================================
    #   UM QUADRO DO JOGO
    # ==========================================
    def atualizar(self, keys=None):
        if self.estado != "jogando":
            return

        self.quadros += 1
        if self.mensagem_timer > 0:
            self.mensagem_timer -= 1

        # --- UPDATES ---
        for m in self.moveis:
            m.update()

        # capivaras purificadas viram plataformas (item 3)
        solidos = self.objs_colisao + [i for i in self.inimigos if i.purificado]
        self.player.update(solidos, keys)

        for ini in self.inimigos:
            ini.update()
        for c in self.checkpoints:
            c.update()
        for item in self.gemas + [self.chave, self.acai]:
            item.update()

        self.camera.update(self.player)

        # --- REGRAS ---
        self.verificar_golpe()
        self.verificar_itens()
        self.verificar_checkpoints()
        self.verificar_inimigos()
        if self.estado == "jogando":
            self.verificar_perigos()
        if self.estado == "jogando":
            self.verificar_porta()

    # ==========================================
    #   DESENHO
    # ==========================================
    def desenhar(self):
        screen = self.screen

        if self.estado == "derrota":
            desenhar_tela_derrota(screen, self, self.fonte_grande, self.fonte)
            return
        if self.estado == "vitoria":
            desenhar_tela_vitoria(screen, self, self.fonte_grande, self.fonte)
            return

        # Background com paralaxe simples (câmera movendo o fundo)
        screen.blit(self.bg, (0, 0), (self.camera.x, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

        for (x, y, msg) in self.dicas:
            texto(screen, self.fonte_dica, msg, (x - self.camera.x, y), (255, 255, 255))

        for obj in self.objs_colisao:
            obj.draw(screen, self.camera)

        for esp in self.objs_morte:
            esp.draw(screen, self.camera)

        for c in self.checkpoints:
            c.draw(screen, self.camera)

        self.porta_final.draw(screen, self.camera)

        for item in self.gemas + [self.chave, self.acai]:
            item.draw(screen, self.camera)

        for ini in self.inimigos:
            ini.draw(screen, self.camera)

        self.player.draw(screen, self.camera)
        desenhar_hud(screen, self, self.fonte)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Fase 6')
    clock = pygame.time.Clock()

    jogo = Jogo(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if jogo.estado == "jogando":
                    if event.key == K_SPACE or event.key == K_w:
                        jogo.player.jump()
                    elif event.key == K_e:
                        jogo.player.start_dash()
                    elif event.key == K_f:
                        jogo.player.atacar()
                elif event.key == K_r:
                    jogo.reiniciar()

        jogo.atualizar()
        jogo.desenhar()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
