import math
import pygame
from pygame.locals import *
from support import carregar_imagem

# ==========================================================
#   CONSTANTES DE "SENSAÇÃO" DO JOGO (mexa aqui para ajustar)
# ==========================================================
GRAVIDADE = 0.5
FORCA_PULO = -8
VEL_X = 4

# Item 9 - velocidade máxima de queda (menor que a espessura das plataformas, 15px)
VEL_QUEDA_MAX = 11

# Item 6 - altura de pulo variável: ao soltar a tecla, a subida é "cortada" para essa velocidade
CORTE_PULO = -3
PULO_MIN_FRAMES = 3          # o pulo dura pelo menos isso antes de poder ser cortado

# Item 7 - tolerâncias de pulo (em quadros; 60 quadros = 1 segundo)
COYOTE_FRAMES = 6            # ainda dá para pular logo depois de sair da borda
BUFFER_FRAMES = 6            # o pulo apertado um pouco antes de pousar fica guardado

# Item 8 - dash suave: 6 quadros x 9px = 54px (antes era um salto de 40px num quadro só)
DASH_VEL = 9
DASH_FRAMES = 6

# Item 1 - pulo na parede
WALL_SLIDE_VEL = 1.5         # velocidade máxima de queda deslizando na parede
WALL_PUSH = 5.5              # impulso horizontal do pulo na parede (diminui a cada quadro)
WALL_PUSH_DECAI = 0.88
WALL_LOCK_FRAMES = 12        # por esse tempo, não dá para "voltar" para a mesma parede apertando a direção
WALL_COYOTE = 5              # ainda dá para pular na parede logo depois de soltar dela

# Item 3 - golpe de purificação (tecla F)
ATAQUE_FRAMES = 8            # quanto tempo a área do golpe fica ativa
ATAQUE_COOLDOWN = 22         # tempo de espera entre golpes
ATAQUE_ALCANCE = 36          # largura da área do golpe, à frente do jogador

# Item 10 - quique ao pisar num inimigo
QUIQUE_PISADA = -7

# Item 12 - dano
INVENCIVEL_FRAMES = 90       # 1,5 segundo
STUN_FRAMES = 12             # tempo sem controle depois de ser empurrado
EMPURRAO = 6

# Item 5 - açaí
ACAI_FRAMES = 480            # 8 segundos
ACAI_VEL_X = 6
ACAI_MAX_PULOS = 3


class Player(pygame.Rect):
    def __init__(self, x, y, size, world_width):
        super().__init__(x, y, size, size)

        self.world_width = world_width

        # ===== SPRITES =====
        # Idle (parado)
        self.sprite_idle = carregar_imagem("player_idle.png")
        self.sprite_idle = pygame.transform.scale(self.sprite_idle, (size, size))

        # Run (7 frames)
        run_sheet = carregar_imagem("player_run.png")
        frame_width = run_sheet.get_width() // 7
        frame_height = run_sheet.get_height()

        self.run_frames = []
        for i in range(7):
            frame = run_sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            frame = pygame.transform.scale(frame, (size, size))
            self.run_frames.append(frame)

        # Controle de animação
        self.anim_index = 0
        self.anim_speed = 0.18
        self.current_sprite = self.sprite_idle

        # Versão com tom roxo para o efeito do açaí
        self.glow = pygame.Surface((size + 30, size + 30), pygame.SRCALPHA)
        pygame.draw.ellipse(self.glow, (170, 70, 255, 90), self.glow.get_rect())

        # Hitbox visual antiga (se quiser debug)
        self.color = (255, 0, 0)

        # Posição inicial (canto inferior esquerdo, onde o jogador nasce/renasce)
        self.start_pos = self.bottomleft

        # Posição X em decimais (o empurrão do pulo na parede não é inteiro).
        # O Y continua truncado como no jogo original, para o alcance dos pulos
        # (64px / 128px / 192px) não mudar e o nível continuar do mesmo jeito.
        self.fx = float(self.x)

        # Física
        self.vel_y = 0
        self.speed_x = VEL_X

        # Estados
        self.is_on_ground = False
        self.is_dashing = False
        self.can_dash = True
        self.direction = 1  # 1 direita, -1 esquerda
        self.tempo = 0

        # Pulo Duplo
        self.max_jumps = 2
        self.jumps_left = self.max_jumps

        # Item 6/7: estado do pulo
        self.subindo = False         # True enquanto o pulo pode ser cortado
        self.subindo_frames = 0
        self.coyote = 0
        self.buffer_pulo = 0

        # Item 8: dash
        self.dash_timer = 0
        self.dash_dir = 1
        self.rastro = []             # imagens fantasma do dash

        # Item 1: parede
        self.impulso_x = 0.0         # empurrão horizontal que vai diminuindo (pulo na parede e dano)
        self.wall_lock_dir = 0
        self.wall_lock_timer = 0
        self.wall_coyote = 0
        self.wall_dir_mem = 0
        self.na_parede = 0           # -1 parede na esquerda, 1 na direita, 0 nenhuma (para o desenho/testes)

        # Item 2: plataforma em que o jogador está em pé
        self.plataforma_atual = None
        self.bottom_anterior = self.bottom   # onde estavam os pés no começo do quadro (para a pisada)

        # Item 3: ataque
        self.ataque_timer = 0
        self.ataque_cooldown = 0
        self.ja_atingidos = set()

        # Item 12: dano
        self.invencivel = 0
        self.stun = 0

        # Item 5: açaí
        self.acai_timer = 0

    # ========================
    #      ANIMAÇÃO
    # ========================
    def animate(self, andando):
        # Escolhendo sprite idle ou run
        if andando:
            self.anim_index += self.anim_speed
            if self.anim_index >= len(self.run_frames):
                self.anim_index = 0
            self.current_sprite = self.run_frames[int(self.anim_index)]
        else:
            self.current_sprite = self.sprite_idle
            self.anim_index = 0

        # Flip automático quando anda pra esquerda
        if self.direction == -1:
            self.current_sprite = pygame.transform.flip(self.current_sprite, True, False)

    # ========================
    #     CONTROLES
    # ========================
    def reset(self, pos=None):
        """Coloca o jogador de pé em 'pos' (canto inferior esquerdo). Sem 'pos', vai para o início."""
        self.bottomleft = pos if pos is not None else self.start_pos
        self.fx = float(self.x)
        self.vel_y = 0
        self.is_on_ground = False
        self.is_dashing = False
        self.dash_timer = 0
        self.can_dash = True
        self.direction = 1
        self.rastro = []
        self.impulso_x = 0.0
        self.wall_lock_timer = 0
        self.wall_coyote = 0
        self.plataforma_atual = None
        self.subindo = False
        self.coyote = 0
        self.buffer_pulo = 0
        self.ataque_timer = 0
        self.ataque_cooldown = 0
        self.stun = 0
        self.invencivel = 0
        self._acabar_acai()
        self.jumps_left = self.max_jumps
        self.bottom_anterior = self.bottom

    def handle_input(self):
        keys = pygame.key.get_pressed()
        dx = 0

        if keys[K_a]:
            dx = -self.speed_x
            self.direction = -1
        if keys[K_d]:
            dx = self.speed_x
            self.direction = 1

        return dx, keys

    def jump(self):
        """Chamado ao apertar a tecla de pulo. O comando fica guardado por alguns quadros
        (item 7 - buffer) e o update decide se vira pulo no chão, no ar ou na parede."""
        self.buffer_pulo = BUFFER_FRAMES

    def start_dash(self):
        if self.can_dash and not self.is_dashing and self.stun == 0:
            self.is_dashing = True
            self.dash_timer = DASH_FRAMES
            self.dash_dir = self.direction
            self.can_dash = False
            self.impulso_x = 0.0

    def atacar(self):
        """ITEM 3 - golpe de purificação (tecla F)."""
        if self.ataque_cooldown == 0 and self.stun == 0:
            self.ataque_timer = ATAQUE_FRAMES
            self.ataque_cooldown = ATAQUE_COOLDOWN
            self.ja_atingidos = set()   # cada golpe só atinge cada inimigo uma vez
            return True
        return False

    @property
    def hitbox_ataque(self):
        """Retângulo do golpe à frente do jogador (ou None se não estiver golpeando)."""
        if self.ataque_timer <= 0:
            return None
        x = self.right if self.direction == 1 else self.left - ATAQUE_ALCANCE
        return pygame.Rect(x, self.top - 2, ATAQUE_ALCANCE, self.height + 4)

    # ---------- ações vindas do jogo ----------
    def quicar(self):
        """ITEM 10 - quique ao pisar num inimigo: sobe um pouco e recupera o dash."""
        self.vel_y = QUIQUE_PISADA
        self.can_dash = True
        self.subindo = False
        self.coyote = 0

    def levar_dano(self, empurrao_dir):
        """ITEM 12 - perde o controle por um instante, é empurrado para trás e fica invencível."""
        self.invencivel = INVENCIVEL_FRAMES
        self.stun = STUN_FRAMES
        self.impulso_x = empurrao_dir * EMPURRAO
        self.vel_y = -5
        self.is_dashing = False
        self.dash_timer = 0
        self.subindo = False
        self.coyote = 0
        self.buffer_pulo = 0

    def sincronizar_posicao(self):
        """Chame depois de mexer em x/left/right... de fora, para a posição decimal acompanhar."""
        self.fx = float(self.x)

    def ativar_acai(self):
        """ITEM 5 - mais velocidade e um pulo a mais por 8 segundos."""
        self.acai_timer = ACAI_FRAMES
        self.speed_x = ACAI_VEL_X
        self.max_jumps = ACAI_MAX_PULOS
        self.jumps_left = min(self.jumps_left + 1, self.max_jumps)

    def _acabar_acai(self):
        self.acai_timer = 0
        self.speed_x = VEL_X
        self.max_jumps = 2
        self.jumps_left = min(self.jumps_left, self.max_jumps)

    # ========================
    #   SENSORES (chão / parede)
    # ========================
    def _plataforma_sob_os_pes(self, solidos):
        """Olha 1 pixel abaixo dos pés. Mais confiável do que depender da colisão do quadro."""
        sonda = pygame.Rect(self.x, self.bottom, self.width, 1)
        for plat in solidos:
            if sonda.colliderect(plat):
                return plat
        return None

    def _contato_parede(self, paredes):
        """Devolve -1 se encosta numa parede à esquerda, 1 à direita, 0 se em nenhuma."""
        esq = pygame.Rect(self.left - 1, self.top + 4, 1, self.height - 8)
        dire = pygame.Rect(self.right, self.top + 4, 1, self.height - 8)
        for p in paredes:
            if esq.colliderect(p):
                return -1
            if dire.colliderect(p):
                return 1
        return 0

    # ========================
    #  PULOS (chão, ar e parede)
    # ========================
    def _comecar_pulo(self):
        self.subindo = True
        self.subindo_frames = 0
        self.buffer_pulo = 0
        self.coyote = 0
        self.wall_coyote = 0

    def _pulo_chao(self):
        self.vel_y = FORCA_PULO
        self.jumps_left = self.max_jumps - 1
        self._comecar_pulo()

    def _pulo_ar(self):
        self.vel_y = FORCA_PULO
        self.jumps_left -= 1
        self._comecar_pulo()

    def _pulo_parede(self, lado_parede):
        """ITEM 1 - sobe e é lançado para o lado OPOSTO da parede."""
        self.vel_y = FORCA_PULO
        self.impulso_x = -lado_parede * WALL_PUSH
        self.direction = -lado_parede
        self.wall_lock_dir = lado_parede
        self.wall_lock_timer = WALL_LOCK_FRAMES
        self._comecar_pulo()

    # ========================
    #    COLISÃO HORIZONTAL
    # ========================
    def check_horizontal_collision(self, dx, plataformas):
        self.fx += dx
        self.x = math.floor(self.fx)

        # limitar ao mundo
        self.left = max(0, self.left)
        self.right = min(self.world_width, self.right)

        for plat in plataformas:
            if self.colliderect(plat):
                if self.bottom > plat.top + 5 and self.top < plat.bottom - 5:
                    if dx > 0:
                        self.right = plat.left
                    elif dx < 0:
                        self.left = plat.right

        if self.x != math.floor(self.fx):   # alguma colisão mexeu na posição
            self.fx = float(self.x)

    # ========================
    #    COLISÃO VERTICAL
    # ========================
    def check_vertical_collision(self, plataformas):
        bottom_antes = self.bottom
        top_antes = self.top

        self.y = int(self.y + self.vel_y)   # a parte decimal é descartada, igual ao jogo original

        for plat in plataformas:
            if self.colliderect(plat):
                # caindo
                if bottom_antes <= plat.top and self.bottom >= plat.top and self.vel_y >= 0:
                    self.bottom = plat.top
                    self.vel_y = 0

                # batendo no teto
                elif top_antes >= plat.bottom and self.top <= plat.bottom and self.vel_y < 0:
                    self.top = plat.bottom
                    self.vel_y = 0

                # correção anti "ficar preso"
                elif self.centery < plat.centery:
                    self.bottom = plat.top
                    self.vel_y = 0

    # ========================
    #  PLATAFORMA MÓVEL (item 2)
    # ========================
    def _ser_levado(self):
        """Se estava em pé numa plataforma móvel, anda junto com ela neste quadro."""
        p = self.plataforma_atual
        if p is None or not getattr(p, "movel", False) or self.vel_y < 0:
            return
        antes = pygame.Rect(p.x - p.dx, p.y - p.dy, p.width, p.height)   # onde ela estava
        if self.bottom == antes.top and self.right > antes.left and self.left < antes.right:
            self.fx += p.dx
            self.x = math.floor(self.fx)
            self.bottom = p.top

    # ========================
    #        UPDATE
    # ========================
    def update(self, plataformas, keys=None):
        if keys is None:
            keys = pygame.key.get_pressed()

        self.tempo += 1
        self.bottom_anterior = self.bottom

        # ----- contadores -----
        if self.invencivel > 0:
            self.invencivel -= 1
        if self.stun > 0:
            self.stun -= 1
        if self.ataque_timer > 0:
            self.ataque_timer -= 1
        if self.ataque_cooldown > 0:
            self.ataque_cooldown -= 1
        if self.acai_timer > 0:
            self.acai_timer -= 1
            if self.acai_timer == 0:
                self._acabar_acai()
        self.rastro = [(x, y, s, v - 1) for (x, y, s, v) in self.rastro if v > 1]

        # ----- 0) plataforma móvel leva o jogador -----
        self._ser_levado()

        # ----- 1) sensores: onde estou? -----
        paredes = [p for p in plataformas if getattr(p, "parede", False)]
        plat_chao = self._plataforma_sob_os_pes(plataformas)
        no_chao = plat_chao is not None and self.vel_y >= 0

        if no_chao:
            self.coyote = COYOTE_FRAMES
            self.jumps_left = self.max_jumps
            self.can_dash = True
            self.vel_y = 0
        elif self.coyote > 0:
            self.coyote -= 1
            if self.coyote == 0:
                # Item 7: quem só caiu da borda fica apenas com o pulo extra no ar
                self.jumps_left = min(self.jumps_left, self.max_jumps - 1)

        lado_parede = 0 if no_chao else self._contato_parede(paredes)
        self.na_parede = lado_parede
        if lado_parede != 0:
            self.wall_coyote = WALL_COYOTE
            self.wall_dir_mem = lado_parede
        elif no_chao:
            self.wall_coyote = 0
        elif self.wall_coyote > 0:
            self.wall_coyote -= 1

        # ----- 2) entrada horizontal -----
        dx_in = 0
        if self.stun == 0:
            if keys[K_a]:
                dx_in = -self.speed_x
            if keys[K_d]:
                dx_in = self.speed_x
            # logo depois de um pulo na parede, apertar na direção da parede é ignorado
            if self.wall_lock_timer > 0:
                self.wall_lock_timer -= 1
                if dx_in * self.wall_lock_dir > 0:
                    dx_in = 0
            if dx_in != 0:
                self.direction = 1 if dx_in > 0 else -1

        # ----- 3) pulo (buffer + coyote + pulo duplo + parede) -----
        pulo_apertado = keys[K_w] or keys[K_SPACE]
        if self.buffer_pulo > 0 and self.stun == 0:
            if not no_chao and (lado_parede != 0 or self.wall_coyote > 0):
                self._pulo_parede(lado_parede or self.wall_dir_mem)
            elif no_chao or self.coyote > 0:
                self._pulo_chao()
            elif self.jumps_left > 0:
                self._pulo_ar()
        if self.buffer_pulo > 0:
            self.buffer_pulo -= 1

        # ----- 4) Item 6: altura variável (soltou a tecla = pulo mais baixo) -----
        if self.subindo:
            self.subindo_frames += 1
            if self.vel_y >= 0:
                self.subindo = False
            elif not pulo_apertado and self.vel_y < CORTE_PULO and self.subindo_frames >= PULO_MIN_FRAMES:
                self.vel_y = CORTE_PULO
                self.subindo = False

        # ----- 5) gravidade (com limite de queda e deslize na parede) -----
        if self.is_dashing:
            self.vel_y = 0   # durante o dash o personagem avança em linha reta, sem cair
        else:
            self.vel_y = min(self.vel_y + GRAVIDADE, VEL_QUEDA_MAX)
            if lado_parede != 0 and not no_chao and self.vel_y > WALL_SLIDE_VEL:
                apertando_na_parede = (lado_parede == -1 and keys[K_a]) or (lado_parede == 1 and keys[K_d])
                if apertando_na_parede:
                    self.vel_y = WALL_SLIDE_VEL   # Item 1: desliza devagar

        # ----- 6) movimento horizontal -----
        if self.is_dashing:
            dx = DASH_VEL * self.dash_dir
            self.rastro.append((self.x, self.y, self.current_sprite, 10))
            self.dash_timer -= 1
            if self.dash_timer <= 0:
                self.is_dashing = False
        else:
            dx = dx_in + self.impulso_x
            self.impulso_x *= WALL_PUSH_DECAI
            if abs(self.impulso_x) < 0.3:
                self.impulso_x = 0.0

        self.check_horizontal_collision(dx, plataformas)

        # ----- 7) movimento vertical -----
        self.check_vertical_collision(plataformas)

        # ----- 8) estado final do quadro -----
        self.plataforma_atual = self._plataforma_sob_os_pes(plataformas) if self.vel_y >= 0 else None
        self.is_on_ground = self.plataforma_atual is not None

        # Animação
        self.animate(dx_in != 0 or self.is_dashing)

    # ========================
    #        DRAW
    # ========================
    def draw(self, screen, camera):
        # rastro do dash (imagens fantasma que somem)
        for (x, y, sprite, vida) in self.rastro:
            fantasma = sprite.copy()
            fantasma.set_alpha(int(25 * vida))
            screen.blit(fantasma, camera.apply(pygame.Rect(x, y, self.width, self.height)))

        # piscando enquanto invencível (item 12)
        if self.invencivel > 0 and (self.tempo // 4) % 2 == 0:
            return

        rect_visivel = camera.apply(self)

        # brilho roxo do açaí (item 5); pisca no último segundo e meio para avisar que vai acabar
        if self.acai_timer > 0 and (self.acai_timer > 90 or (self.tempo // 6) % 2 == 0):
            screen.blit(self.glow, (rect_visivel.x - 15, rect_visivel.y - 15))
            sprite = self.current_sprite.copy()
            sprite.fill((70, 0, 110, 0), special_flags=BLEND_RGB_ADD)
        else:
            sprite = self.current_sprite
        screen.blit(sprite, rect_visivel)

        # efeito visual do golpe de purificação (item 3)
        golpe = self.hitbox_ataque
        if golpe is not None:
            forca = self.ataque_timer / ATAQUE_FRAMES
            surf = pygame.Surface((golpe.width, golpe.height), pygame.SRCALPHA)
            pygame.draw.ellipse(surf, (200, 255, 210, int(60 + 150 * forca)), surf.get_rect())
            pygame.draw.ellipse(surf, (255, 255, 255, int(200 * forca)), surf.get_rect(), 2)
            screen.blit(surf, camera.apply(golpe))
        # pygame.draw.rect(screen, (255, 0, 0), rect_visivel, 1)  # debug hitbox
