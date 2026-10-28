import pygame
from pygame.locals import *

class Player(pygame.Rect):
    def __init__(self, x, y, size, world_width):
        super().__init__(x, y, size, size)
        self.color = (255, 0, 0) # Red
        
        # Posição inicial para reset
        self.start_pos = (x, y)
        self.world_width = world_width

        # Física e Movimento
        self.vel_y = 0
        self.gravity = 0.5
        self.jump_force = -8
        self.speed_x = 4
        
        # Estados
        self.is_on_ground = False
        self.is_dashing = False
        self.can_dash = True
        self.direction = 1 # 1 direita, -1 esquerda
        
        # Pulo Duplo
        self.max_jumps = 2
        self.jumps_left = self.max_jumps

        # Dash
        self.dash_speed = 40
        
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

        # Movimento Lateral
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

    def check_horizontal_collision(self, dx, plataformas):
        self.x += dx
        
        # Mantém dentro do mundo
        self.left = max(0, self.left)
        self.right = min(self.world_width, self.right)

        # Colisão lateral com plataformas
        for plat in plataformas:
            if self.colliderect(plat):
                # Somente se não estiver passando por cima/baixo (ajuste fino)
                if self.bottom > plat.top + 5 and self.top < plat.bottom - 5:
                    if dx > 0:
                        self.right = plat.left
                    elif dx < 0:
                        self.left = plat.right

    def check_vertical_collision(self, plataformas):
        on_platform = False
        prev_bottom = self.bottom - self.vel_y

        for plat in plataformas:
            if self.colliderect(plat):
                # Pouso (vinha de cima)
                if prev_bottom <= plat.top and self.bottom >= plat.top and self.vel_y >= 0:
                    self.bottom = plat.top
                    self.vel_y = 0
                    self.is_on_ground = True
                    on_platform = True
                    self.jumps_left = self.max_jumps
                    self.can_dash = True
                # Cabeçada (vinha de baixo)
                elif prev_bottom >= plat.bottom and self.top <= plat.bottom and self.vel_y < 0:
                    self.top = plat.bottom
                    self.vel_y = 0
                # Correção para evitar ficar preso dentro
                elif self.centery < plat.centery:
                     # Assume pouso
                    self.bottom = plat.top
                    self.vel_y = 0
                    self.is_on_ground = True
                    on_platform = True
                    self.jumps_left = self.max_jumps
                    self.can_dash = True

        if not on_platform:
            self.is_on_ground = False

    def check_climb(self, plataformas, keys):
        # Lógica de escalar parede
        touching_side = False
        for plat in plataformas:
            if self.colliderect(plat):
                vertical_overlap = (self.bottom > plat.top + self.side_touch_buffer) and \
                                   (self.top < plat.bottom - self.side_touch_buffer)
                if vertical_overlap:
                    touching_side = True
                    break # Basta tocar em uma

        if touching_side and keys[K_w]:
            self.y -= self.climb_speed
            self.vel_y = 0

    def update(self, plataformas):
        dx, keys = self.handle_input()

        # Dash Logic
        if self.is_dashing:
            dx = self.dash_speed * self.direction
            self.is_dashing = False # Dash dura apenas 1 frame de impulso neste código original

        # 1. Aplica movimento horizontal e checa colisão
        self.check_horizontal_collision(dx, plataformas)

        # 2. Aplica gravidade
        self.vel_y += self.gravity
        self.y += self.vel_y

        # 3. Checa colisão vertical (chão e teto)
        self.check_vertical_collision(plataformas)

        # 4. Checa escalada (sobrescreve gravidade se ativo)
        self.check_climb(plataformas, keys)

    def draw(self, screen, camera):
        rect_visivel = camera.apply(self)
        pygame.draw.rect(screen, self.color, rect_visivel)