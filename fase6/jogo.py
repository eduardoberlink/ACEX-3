import pygame
from pygame.locals import K_SPACE, K_e, K_r, K_w

from camera.cam import Camera
from config import (BLACK, COR_FUNDO_RESERVA, COR_TELA_MORTE, FPS, LIMITE_QUEDA,
                    SCREEN_HEIGHT, SCREEN_WIDTH, TITULO, WHITE, WORLD_WIDTH, YELLOW)
from nivel import PLAYER_INICIO, PLAYER_TAMANHO, construir_nivel
from personagem.player import Player
from recursos import imagem, repetir_horizontal, superficie_solida

JOGANDO = "jogando"
MORREU = "morreu"
VENCEU = "venceu"


def criar_fundo():
    """Imagem de fundo no tamanho da tela, repetida ao longo do mundo inteiro."""
    bg = imagem("background.jpg", alpha=False)
    if bg:
        bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    else:
        bg = superficie_solida((SCREEN_WIDTH, SCREEN_HEIGHT), COR_FUNDO_RESERVA)
    return repetir_horizontal(bg, WORLD_WIDTH, SCREEN_HEIGHT)


class Jogo:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITULO)
        self.clock = pygame.time.Clock()

        # Fontes criadas uma vez (antes eram recriadas a cada frame)
        self.fonte_morte = pygame.font.SysFont("arial", 20, bold=True, italic=True)
        self.fonte_vitoria = pygame.font.SysFont("arial", 20, bold=True)

        self.fundo = criar_fundo()
        self.nivel = construir_nivel()
        self.player = Player(*PLAYER_INICIO, PLAYER_TAMANHO, WORLD_WIDTH)
        self.camera = Camera(WORLD_WIDTH, SCREEN_WIDTH)
        self.estado = JOGANDO
        self.rodando = True

    def reiniciar(self):
        self.player.reset()
        self.nivel.reset()
        self.estado = JOGANDO

    # ========================
    #       EVENTOS
    # ========================
    def processar_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.rodando = False
            elif event.type == pygame.KEYDOWN:
                self._tecla(event.key)

    def _tecla(self, key):
        if self.estado == JOGANDO:
            if key in (K_SPACE, K_w):
                self.player.jump()
            elif key == K_e:
                self.player.start_dash()
        elif key == K_r:
            self.reiniciar()

    # ========================
    #       LÓGICA
    # ========================
    def atualizar(self):
        if self.estado != JOGANDO:
            return

        self.player.update(self.nivel.plataformas)
        for inimigo in self.nivel.inimigos:
            inimigo.update()
        self.camera.update(self.player)

        if self._jogador_morreu():
            self.estado = MORREU
        elif self.player.colliderect(self.nivel.porta):
            self.estado = VENCEU

    def _jogador_morreu(self):
        caiu = self.player.y > LIMITE_QUEDA
        tocou_perigo = self.player.collidelist(self.nivel.inimigos + self.nivel.espinhos) != -1
        return caiu or tocou_perigo

    # ========================
    #       DESENHO
    # ========================
    def desenhar(self):
        if self.estado == JOGANDO:
            self._desenhar_mundo()
        elif self.estado == MORREU:
            self._tela_mensagem(COR_TELA_MORTE, self.fonte_morte,
                                "VOCÊ MORREU! R para tentar de novo", WHITE)
        else:
            self._tela_mensagem(BLACK, self.fonte_vitoria,
                                "PARABÉNS! VOCÊ ZEROU O JOGO!", YELLOW)
        pygame.display.flip()

    def _desenhar_mundo(self):
        visivel = (self.camera.x, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.screen.blit(self.fundo, (0, 0), visivel)

        n = self.nivel
        for entidade in (*n.plataformas, *n.espinhos, *n.inimigos, n.porta, self.player):
            entidade.draw(self.screen, self.camera)

    def _tela_mensagem(self, cor_fundo, fonte, texto, cor_texto):
        self.screen.fill(cor_fundo)
        render = fonte.render(texto, True, cor_texto)
        pos = (SCREEN_WIDTH // 2 - render.get_width() // 2, SCREEN_HEIGHT // 2)
        self.screen.blit(render, pos)

    # ========================
    #       LOOP
    # ========================
    def executar(self):
        while self.rodando:
            self.processar_eventos()
            self.atualizar()
            self.desenhar()
            self.clock.tick(FPS)
        pygame.quit()
