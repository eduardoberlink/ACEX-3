import pygame
from pygame.locals import *

class Player(pygame.Rect):
    def __init__(self, x, y, size, screen_width):
        super().__init__(x, y, size, size)
        self.color = (255, 0, 0) # Vermelho
        
        self.start_pos = (x, y)
        self.screen_width = screen_width

        # Física (Configuração Básica)
        self.vel_y = 0
        self.gravity = 0.5
        self.jump_force = -12  # Pulo um pouco mais forte para alcançar plataformas
        self.speed_x = 5
        
        self.is_on_ground = False

    def reset(self):
        self.bottomleft = self.start_pos
        self.vel_y = 0
        self.is_on_ground = False

    def jump(self):
        if self.is_on_ground:
            self.vel_y = self.jump_force
            self.is_on_ground = False

    def update(self, plataformas): # Agora recebe uma LISTA de plataformas
        keys = pygame.key.get_pressed()

        # 1. Movimento Horizontal
        dx = 0
        if keys[K_a]:
            dx = -self.speed_x
        if keys[K_d]:
            dx = self.speed_x
            
        self.x += dx
        
        # Limites da tela
        self.left = max(0, self.left)
        self.right = min(self.screen_width, self.right)

        # Colisão Horizontal (Simples)
        # Impede de atravessar paredes das plataformas
        for plat in plataformas:
            if self.colliderect(plat):
                if dx > 0: # Indo para direita
                    self.right = plat.left
                elif dx < 0: # Indo para esquerda
                    self.left = plat.right

        # 2. Movimento Vertical
        self.vel_y += self.gravity
        self.y += self.vel_y

        # 3. Colisão Vertical (Pouso)
        self.is_on_ground = False
        
        # Salvamos o "pé" do boneco para verificação
        for plat in plataformas:
            if self.colliderect(plat):
                # Se estava caindo (vel_y > 0) e bateu no topo da plataforma
                if self.vel_y > 0:
                    # Verifica se o pé estava acima ou no nível da plataforma
                    # (Tolerância de 10px para garantir o pouso)
                    if self.bottom - self.vel_y <= plat.top + 10:
                        self.bottom = plat.top
                        self.vel_y = 0
                        self.is_on_ground = True
                
                # Se bateu a cabeça subindo (vel_y < 0)
                elif self.vel_y < 0:
                    self.top = plat.bottom
                    self.vel_y = 0

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self)