import pygame
from pygame.locals import K_a, K_d, K_w


class Player(pygame.Rect):
    # Física da FASE 4
    GRAVITY = 0.5
    JUMP_FORCE = -10
    SPEED_X = 5
    DASH_SPEED = 100        # dash longo
    MAX_JUMPS = 2           # pulo duplo
    CLIMB_SPEED = 4
    SIDE_TOUCH_BUFFER = 5   # margem para considerar "encostado na parede"
    COLOR = (255, 0, 0)

    def __init__(self, x, y, size, screen_width):
        super().__init__(x, y, size, size)
        self.start_pos = (x, y)
        self.screen_width = screen_width
        self.reset()

    def reset(self):
        self.topleft = self.start_pos
        self.vel_y = 0
        self.is_on_ground = False
        self.is_dashing = False
        self.can_dash = True
        self.direction = 1  # 1 direita, -1 esquerda
        self.jumps_left = self.MAX_JUMPS

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

    def _pousar(self, plat):
        """Fica em cima da plataforma e recarrega pulo e dash."""
        self.bottom = plat.top
        self.vel_y = 0
        self.is_on_ground = True
        self.jumps_left = self.MAX_JUMPS
        self.can_dash = True

    def update(self, plataformas):
        dx, keys = self.handle_input()

        # Dash: um impulso de um único frame
        if self.is_dashing:
            dx = self.DASH_SPEED * self.direction
            self.is_dashing = False

        # --- Movimento horizontal ---
        self.x += dx
        self.left = max(0, self.left)
        self.right = min(self.screen_width, self.right)

        for plat in plataformas:
            if self.colliderect(plat) and self.bottom > plat.top + 5 and self.top < plat.bottom - 5:
                if dx > 0:
                    self.right = plat.left
                elif dx < 0:
                    self.left = plat.right

        # --- Movimento vertical ---
        self.vel_y += self.GRAVITY

        # Escalada: segurando W encostado na lateral de uma plataforma
        encostado = any(
            self.colliderect(plat)
            and self.bottom > plat.top + self.SIDE_TOUCH_BUFFER
            and self.top < plat.bottom - self.SIDE_TOUCH_BUFFER
            for plat in plataformas
        )
        if encostado and keys[K_w]:
            self.y -= self.CLIMB_SPEED
            self.vel_y = 0
        else:
            self.y += self.vel_y

        # --- Colisão vertical (chão e teto) ---
        # Onde o pé estava antes de cair, para não atravessar a plataforma
        prev_bottom = self.bottom - self.vel_y
        self.is_on_ground = False

        for plat in plataformas:
            if not self.colliderect(plat):
                continue
            if prev_bottom <= plat.top and self.bottom >= plat.top and self.vel_y >= 0:
                self._pousar(plat)                     # caindo
            elif prev_bottom >= plat.bottom and self.top <= plat.bottom and self.vel_y < 0:
                self.top = plat.bottom                 # batendo a cabeça
                self.vel_y = 0
            elif self.centery < plat.centery:
                self._pousar(plat)                     # correção genérica

    def draw(self, screen):
        # Não existe "camera.apply(self)" ainda: desenha direto na tela.
        pygame.draw.rect(screen, self.COLOR, self)
