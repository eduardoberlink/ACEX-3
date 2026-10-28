import pygame
from pygame.locals import K_a, K_d, K_w

from config import RED
from objetos.entidade import Entidade
from recursos import imagem, superficie_solida

FRAMES_CORRIDA = 7


def _carregar_sprites(size):
    """Retorna (idle, lista de frames de corrida), já no tamanho do jogador."""
    idle = imagem("player_idle.png")
    idle = pygame.transform.scale(idle, (size, size)) if idle else superficie_solida((size, size), RED)

    sheet = imagem("player_run.png")
    if not sheet:
        return idle, [idle]

    largura = sheet.get_width() // FRAMES_CORRIDA
    altura = sheet.get_height()
    frames = [
        pygame.transform.scale(sheet.subsurface((i * largura, 0, largura, altura)), (size, size))
        for i in range(FRAMES_CORRIDA)
    ]
    return idle, frames


def _espelhar(surf):
    return pygame.transform.flip(surf, True, False)


class Player(Entidade):
    # --- Física ---
    GRAVITY = 0.5
    JUMP_FORCE = -8
    SPEED_X = 4
    MAX_JUMPS = 2          # pulo duplo
    DASH_SPEED = 40
    CLIMB_SPEED = 4
    SIDE_TOUCH_BUFFER = 5  # margem para considerar "encostado na lateral"
    ANIM_SPEED = 0.18

    def __init__(self, x, y, size, world_width):
        super().__init__(x, y, size, size)
        self.world_width = world_width
        self.start_pos = (x, y)

        # Sprites para a direita (1) e já espelhados para a esquerda (-1)
        idle, run = _carregar_sprites(size)
        self.sprite_idle = {1: idle, -1: _espelhar(idle)}
        self.run_frames = {1: run, -1: [_espelhar(f) for f in run]}

        self.reset()

    # ========================
    #       ESTADO
    # ========================
    def reset(self):
        self.topleft = self.start_pos
        self.vel_y = 0
        self.is_on_ground = False
        self.is_dashing = False
        self.can_dash = True
        self.jumps_left = self.MAX_JUMPS
        self.direction = 1  # 1 direita, -1 esquerda
        self.anim_index = 0
        self.image = self.sprite_idle[1]

    def _pousar(self, plat):
        """Coloca o jogador em cima da plataforma e recarrega pulo e dash."""
        self.bottom = plat.top
        self.vel_y = 0
        self.is_on_ground = True
        self.jumps_left = self.MAX_JUMPS
        self.can_dash = True

    # ========================
    #       CONTROLES
    # ========================
    def handle_input(self):
        keys = pygame.key.get_pressed()
        dx = 0
        if keys[K_a]:
            dx = -self.SPEED_X
            self.direction = -1
        if keys[K_d]:
            dx = self.SPEED_X
            self.direction = 1
        return dx, keys

    def jump(self):
        if self.jumps_left > 0:
            self.vel_y = self.JUMP_FORCE
            self.jumps_left -= 1
            self.is_on_ground = False

    def start_dash(self):
        if self.can_dash and not self.is_dashing:
            self.is_dashing = True
            self.can_dash = False

    # ========================
    #       COLISÕES
    # ========================
    def _sobreposicao_vertical(self, plat, margem):
        return self.bottom > plat.top + margem and self.top < plat.bottom - margem

    def check_horizontal_collision(self, dx, plataformas):
        self.x += dx

        # Limitar ao mundo
        self.left = max(0, self.left)
        self.right = min(self.world_width, self.right)

        for plat in plataformas:
            if self.colliderect(plat) and self._sobreposicao_vertical(plat, 5):
                if dx > 0:
                    self.right = plat.left
                elif dx < 0:
                    self.left = plat.right

    def check_vertical_collision(self, plataformas):
        prev_bottom = self.bottom - self.vel_y
        self.is_on_ground = False

        for plat in plataformas:
            if not self.colliderect(plat):
                continue

            caindo_em_cima = prev_bottom <= plat.top and self.bottom >= plat.top and self.vel_y >= 0
            bateu_no_teto = prev_bottom >= plat.bottom and self.top <= plat.bottom and self.vel_y < 0

            if caindo_em_cima:
                self._pousar(plat)
            elif bateu_no_teto:
                self.top = plat.bottom
                self.vel_y = 0
            elif self.centery < plat.centery:
                # Correção anti "ficar preso" dentro da plataforma
                self._pousar(plat)

    def check_climb(self, plataformas, keys):
        if not keys[K_w]:
            return
        encostado = any(
            self.colliderect(plat) and self._sobreposicao_vertical(plat, self.SIDE_TOUCH_BUFFER)
            for plat in plataformas
        )
        if encostado:
            self.y -= self.CLIMB_SPEED
            self.vel_y = 0

    # ========================
    #       ANIMAÇÃO
    # ========================
    def animate(self, dx):
        if dx != 0:
            frames = self.run_frames[self.direction]
            self.anim_index = (self.anim_index + self.ANIM_SPEED) % len(frames)
            self.image = frames[int(self.anim_index)]
        else:
            self.anim_index = 0
            self.image = self.sprite_idle[self.direction]

    # ========================
    #       UPDATE
    # ========================
    def update(self, plataformas):
        dx, keys = self.handle_input()

        # Dash: um impulso grande em um único frame
        if self.is_dashing:
            dx = self.DASH_SPEED * self.direction
            self.is_dashing = False

        self.check_horizontal_collision(dx, plataformas)

        self.vel_y += self.GRAVITY
        self.y += self.vel_y
        self.check_vertical_collision(plataformas)

        self.check_climb(plataformas, keys)
        self.animate(dx)
