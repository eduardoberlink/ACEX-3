import pygame
from pygame.locals import K_a, K_d, K_w


class Player(pygame.Rect):
    # --- Física ---
    GRAVITY = 0.5
    JUMP_FORCE = -8
    SPEED_X = 4
    MAX_JUMPS = 2          # pulo duplo
    DASH_SPEED = 40
    CLIMB_SPEED = 4
    SIDE_TOUCH_BUFFER = 5  # margem para considerar "encostado na parede"
    COLOR = (255, 0, 0)

    def __init__(self, x, y, size, world_width):
        super().__init__(x, y, size, size)
        self.start_pos = (x, y)
        self.world_width = world_width
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
        self.direction = 1  # 1 direita, -1 esquerda
        self.jumps_left = self.MAX_JUMPS

    def _pousar(self, plat):
        """Fica em cima da plataforma e recarrega pulo e dash."""
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

        # Mantém dentro do mundo
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
            if prev_bottom <= plat.top and self.bottom >= plat.top and self.vel_y >= 0:
                self._pousar(plat)                     # pouso (vinha de cima)
            elif prev_bottom >= plat.bottom and self.top <= plat.bottom and self.vel_y < 0:
                self.top = plat.bottom                 # cabeçada (vinha de baixo)
                self.vel_y = 0
            elif self.centery < plat.centery:
                self._pousar(plat)                     # evita ficar preso dentro

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
    #       UPDATE
    # ========================
    def update(self, plataformas):
        dx, keys = self.handle_input()

        # Dash: um impulso de um único frame
        if self.is_dashing:
            dx = self.DASH_SPEED * self.direction
            self.is_dashing = False

        self.check_horizontal_collision(dx, plataformas)   # 1. horizontal

        self.vel_y += self.GRAVITY                         # 2. gravidade
        self.y += self.vel_y

        self.check_vertical_collision(plataformas)         # 3. chão e teto
        self.check_climb(plataformas, keys)                # 4. escalada

    def draw(self, screen, camera):
        pygame.draw.rect(screen, self.COLOR, camera.apply(self))
