import pygame
from pygame.locals import K_a, K_d


class Player(pygame.Rect):
    # Física (configuração básica)
    GRAVITY = 0.5
    JUMP_FORCE = -12   # pulo mais forte para alcançar as plataformas
    SPEED_X = 5
    TOLERANCIA_POUSO = 10
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

    def jump(self):
        if self.is_on_ground:
            self.vel_y = self.JUMP_FORCE
            self.is_on_ground = False

    def update(self, plataformas):  # Agora recebe uma LISTA de plataformas
        keys = pygame.key.get_pressed()

        # 1. Movimento horizontal
        dx = 0
        if keys[K_a]:
            dx = -self.SPEED_X
        if keys[K_d]:
            dx = self.SPEED_X
        self.x += dx

        # Limites da tela
        self.left = max(0, self.left)
        self.right = min(self.screen_width, self.right)

        # Colisão horizontal: impede de atravessar as laterais
        for plat in plataformas:
            if self.colliderect(plat):
                if dx > 0:
                    self.right = plat.left
                elif dx < 0:
                    self.left = plat.right

        # 2. Movimento vertical
        self.vel_y += self.GRAVITY
        self.y += self.vel_y

        # 3. Colisão vertical
        self.is_on_ground = False
        for plat in plataformas:
            if not self.colliderect(plat):
                continue

            if self.vel_y > 0:
                # Caindo: só pousa se o pé estava acima do topo (com tolerância)
                if self.bottom - self.vel_y <= plat.top + self.TOLERANCIA_POUSO:
                    self.bottom = plat.top
                    self.vel_y = 0
                    self.is_on_ground = True
            elif self.vel_y < 0:
                # Subindo: bateu a cabeça
                self.top = plat.bottom
                self.vel_y = 0

    def draw(self, screen):
        pygame.draw.rect(screen, self.COLOR, self)
