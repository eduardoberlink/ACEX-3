import pygame
from pygame.locals import *

class Player(pygame.Rect):
    def __init__(self, x, y, size, screen_width):
        super().__init__(x, y, size, size)
        self.color = (255, 0, 0) # Vermelho
        
        # Posição de respawn (caindo do céu no meio da tela, conforme seu código)
        self.start_x = x
        self.start_y = y
        self.screen_width = screen_width

        # Física da Fase 1
        self.vel_y = 0
        self.gravity = 0.5
        self.jump_force = -10
        self.speed_x = 5
        
        self.is_on_ground = False

    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.vel_y = 0
        self.is_on_ground = False

    def jump(self):
        if self.is_on_ground:
            self.vel_y = self.jump_force
            self.is_on_ground = False

    def update(self, chao):
        keys = pygame.key.get_pressed()

        # 1. Movimento Horizontal
        if keys[K_a]:
            self.x -= self.speed_x
        if keys[K_d]:
            self.x += self.speed_x
            
        # Manter na tela (limites)
        self.left = max(0, self.left)
        self.right = min(self.screen_width, self.right)

        # 2. Movimento Vertical (Gravidade)
        self.vel_y += self.gravity
        self.y += self.vel_y

        # 3. Colisão com o Chão
        if self.colliderect(chao):
            self.bottom = chao.top
            self.vel_y = 0
            self.is_on_ground = True
        else:
            self.is_on_ground = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self)