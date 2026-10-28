import pygame
from pygame.locals import *

class Player(pygame.Rect):
    def __init__(self, x, y, size, screen_width):
        super().__init__(x, y, size, size)
        self.color = (255, 0, 0) # Vermelho
        
        self.start_pos = (x, y)
        self.screen_width = screen_width

        # Física da FASE 4 (Valores altos)
        self.vel_y = 0
        self.gravity = 0.5
        self.jump_force = -10     # Pulo alto
        self.speed_x = 5          # Movimento rápido
        self.dash_speed = 100     # Dash longo
        
        # Estados
        self.is_on_ground = False
        self.is_dashing = False
        self.can_dash = True
        self.direction = 1 
        
        self.max_jumps = 2
        self.jumps_left = self.max_jumps

        # Escalada
        self.climb_speed = 4
        self.side_touch_buffer = 5

    def reset(self):
        self.bottomleft = self.start_pos
        self.vel_y = 0
        self.is_on_ground = False
        self.jumps_left = self.max_jumps
        self.can_dash = True
        self.is_dashing = False
        self.direction = 1

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
        if self.jumps_left > 0:
            self.vel_y = self.jump_force
            self.jumps_left -= 1
            self.is_on_ground = False

    def start_dash(self):
        if self.can_dash and not self.is_dashing:
            self.is_dashing = True
            self.can_dash = False

    def update(self, plataformas):
        dx, keys = self.handle_input()

        # Lógica do Dash
        if self.is_dashing:
            dx = self.dash_speed * self.direction
            self.is_dashing = False

        # --- Movimento Horizontal ---
        self.x += dx
        # Manter na tela
        self.left = max(0, self.left)
        self.right = min(self.screen_width, self.right)

        # Colisão Horizontal
        for plat in plataformas:
            if self.colliderect(plat):
                if self.bottom > plat.top + 5 and self.top < plat.bottom - 5:
                    if dx > 0:
                        self.right = plat.left
                    elif dx < 0:
                        self.left = plat.right

        # --- Movimento Vertical ---
        self.vel_y += self.gravity
        
        # Lógica de Escalar (se pressionar W na parede)
        touching_side = False
        for plat in plataformas:
             if self.colliderect(plat):
                # Verifica sobreposição vertical (ignora teto/chão)
                if (self.bottom > plat.top + self.side_touch_buffer) and \
                   (self.top < plat.bottom - self.side_touch_buffer):
                    touching_side = True
                    break
        
        if touching_side and keys[K_w]:
            self.y -= self.climb_speed
            self.vel_y = 0
        else:
            self.y += self.vel_y

        # Colisão Vertical (Chão e Teto)
        on_platform = False
        # Calculamos onde "estávamos" antes de cair para evitar atravessar (tunneling)
        prev_bottom = self.bottom - self.vel_y

        for plat in plataformas:
            if self.colliderect(plat):
                # Caindo
                if prev_bottom <= plat.top and self.bottom >= plat.top and self.vel_y >= 0:
                    self.bottom = plat.top
                    self.vel_y = 0
                    self.is_on_ground = True
                    on_platform = True
                    self.jumps_left = self.max_jumps
                    self.can_dash = True
                # Batendo a cabeça
                elif prev_bottom >= plat.bottom and self.top <= plat.bottom and self.vel_y < 0:
                    self.top = plat.bottom
                    self.vel_y = 0
                # Correção genérica
                elif self.centery < plat.centery:
                    self.bottom = plat.top
                    self.vel_y = 0
                    self.is_on_ground = True
                    on_platform = True
                    self.jumps_left = self.max_jumps
                    self.can_dash = True

        if not on_platform:
            self.is_on_ground = False

    def draw(self, screen):
        # AQUI É O PULO DO GATO DIDÁTICO:
        # Não existe "camera.apply(self)". O aluno vê que desenha direto.
        pygame.draw.rect(screen, self.color, self)