import pygame
from pygame.locals import K_a, K_d


class Player(pygame.Rect):
    # Física da Fase 1
    GRAVITY = 0.5
    JUMP_FORCE = -10
    SPEED_X = 5
    COLOR = (255, 0, 0)

    def __init__(self, x, y, size, screen_width):
        super().__init__(x, y, size, size)
        self.start_pos = (x, y)  # posição de respawn
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

    def update(self, chao):
        keys = pygame.key.get_pressed()

        # 1. Movimento horizontal
        if keys[K_a]:
            self.x -= self.SPEED_X
        if keys[K_d]:
            self.x += self.SPEED_X

        # Manter dentro da tela
        self.left = max(0, self.left)
        self.right = min(self.screen_width, self.right)

        # 2. Gravidade
        self.vel_y += self.GRAVITY
        self.y += self.vel_y

        # 3. Colisão com o chão
        self.is_on_ground = self.colliderect(chao)
        if self.is_on_ground:
            self.bottom = chao.top
            self.vel_y = 0

    def draw(self, screen):
        pygame.draw.rect(screen, self.COLOR, self)
