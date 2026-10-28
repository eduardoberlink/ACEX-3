import pygame
from pygame.locals import *

class Player(pygame.Rect):
    def __init__(self, x, y, size, world_width):
        super().__init__(x, y, size, size)

        self.world_width = world_width

        # ===== SPRITES =====
        # Idle (parado)
        self.sprite_idle = pygame.image.load("fase6/assets/player_idle.png").convert_alpha()
        self.sprite_idle = pygame.transform.scale(self.sprite_idle, (size, size))

        # Run (7 frames)
        run_sheet = pygame.image.load("fase6/assets/player_run.png").convert_alpha()
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

        # Hitbox visual antiga (se quiser debug)
        self.color = (255, 0, 0)

        # Posição inicial
        self.start_pos = (x, y)

        # Física
        self.vel_y = 0
        self.gravity = 0.5
        self.jump_force = -8
        self.speed_x = 4

        # Estados
        self.is_on_ground = False
        self.is_dashing = False
        self.can_dash = True
        self.direction = 1  # 1 direita, -1 esquerda

        # Pulo Duplo
        self.max_jumps = 2
        self.jumps_left = self.max_jumps

        # Dash
        self.dash_speed = 40

        # Escalada
        self.climb_speed = 4
        self.side_touch_buffer = 5


    # ========================
    #      ANIMAÇÃO
    # ========================
    def animate(self, dx):
        # Escolhendo sprite idle ou run
        if dx != 0:
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


    # ========================
    #    COLISÃO HORIZONTAL
    # ========================
    def check_horizontal_collision(self, dx, plataformas):
        self.x += dx

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


    # ========================
    #    COLISÃO VERTICAL
    # ========================
    def check_vertical_collision(self, plataformas):
        on_platform = False
        prev_bottom = self.bottom - self.vel_y

        for plat in plataformas:
            if self.colliderect(plat):
                # caindo
                if prev_bottom <= plat.top and self.bottom >= plat.top and self.vel_y >= 0:
                    self.bottom = plat.top
                    self.vel_y = 0
                    self.is_on_ground = True
                    on_platform = True
                    self.jumps_left = self.max_jumps
                    self.can_dash = True

                # batendo no teto
                elif prev_bottom >= plat.bottom and self.top <= plat.bottom and self.vel_y < 0:
                    self.top = plat.bottom
                    self.vel_y = 0

                # correção anti "ficar preso"
                elif self.centery < plat.centery:
                    self.bottom = plat.top
                    self.vel_y = 0
                    self.is_on_ground = True
                    on_platform = True
                    self.jumps_left = self.max_jumps
                    self.can_dash = True

        if not on_platform:
            self.is_on_ground = False


    # ========================
    #        ESCALADA
    # ========================
    def check_climb(self, plataformas, keys):
        touching_side = False
        for plat in plataformas:
            if self.colliderect(plat):
                vertical_overlap = (self.bottom > plat.top + self.side_touch_buffer) and \
                                   (self.top < plat.bottom - self.side_touch_buffer)
                if vertical_overlap:
                    touching_side = True
                    break

        if touching_side and keys[K_w]:
            self.y -= self.climb_speed
            self.vel_y = 0


    # ========================
    #        UPDATE
    # ========================
    def update(self, plataformas):
        dx, keys = self.handle_input()

        # Dash
        if self.is_dashing:
            dx = self.dash_speed * self.direction
            self.is_dashing = False

        # Movimento horizontal
        self.check_horizontal_collision(dx, plataformas)

        # Gravidade
        self.vel_y += self.gravity
        self.y += self.vel_y

        # Colisões verticais
        self.check_vertical_collision(plataformas)

        # Escalada
        self.check_climb(plataformas, keys)

        # Animação
        self.animate(dx)


    # ========================
    #        DRAW
    # ========================
    def draw(self, screen, camera):
        rect_visivel = camera.apply(self)
        screen.blit(self.current_sprite, rect_visivel)
        # pygame.draw.rect(screen, (255, 0, 0), rect_visivel, 1)  # debug hitbox
