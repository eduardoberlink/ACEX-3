import pygame
from pygame.locals import *

class Player(pygame.Rect):
    def __init__(self, x, y, size, screen_width):
        super().__init__(x, y, size, size)
        self.color = (255, 0, 0) # Vermelho
        
        self.start_pos = (x, y)
        self.screen_width = screen_width

        # Física SIMPLIFICADA (Fase 3)
        self.vel_y = 0
        self.gravity = 0.5
        self.jump_force = -10
        self.speed_x = 5
        
        # Apenas estado de chão (sem dash, sem pulo duplo)
        self.is_on_ground = False

    def reset(self):
        self.bottomleft = self.start_pos
        self.vel_y = 0
        self.is_on_ground = False

    def jump(self):
        # Só pula se estiver no chão (Sem pulo duplo)
        if self.is_on_ground:
            self.vel_y = self.jump_force
            self.is_on_ground = False

    def update(self, chao): # Recebe apenas o chão, não lista de plataformas
        keys = pygame.key.get_pressed()

        # 1. Movimento Horizontal
        if keys[K_a]:
            self.x -= self.speed_x
        if keys[K_d]:
            self.x += self.speed_x
            
        # Manter na tela (limites)
        self.left = max(0, self.left)
        self.right = min(self.screen_width, self.right)

        # 2. Gravidade
        self.vel_y += self.gravity
        self.y += self.vel_y

        # 3. Colisão Simples (Apenas com o Chão)
        if self.colliderect(chao):
            # Se bater no chão, para de cair e fica em cima dele
            self.bottom = chao.top
            self.vel_y = 0
            self.is_on_ground = True
        else:
            # Se não está tocando no chão, está voando
            self.is_on_ground = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self)