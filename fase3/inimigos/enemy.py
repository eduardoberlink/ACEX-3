import pygame

class Inimigo(pygame.Rect):
    def __init__(self, x, y, size, limit_left, limit_right, speed=8):
        super().__init__(x, y, size, size)
        self.color = (255, 0, 255) # Magenta
        self.speed = speed
        self.limit_left = limit_left
        self.limit_right = limit_right
        
        # Posição inicial para reset
        self.start_x = x
        self.start_y = y

    def update(self):
        self.x += self.speed

        # BLOQUEIO ESQUERDO
        # Se bateu no limite esquerdo E está andando para a esquerda (< 0)
        if self.left <= self.limit_left and self.speed < 0:
            self.speed *= -1
            
        # BLOQUEIO DIREITO
        # Se bateu no limite direito E está andando para a direita (> 0)
        elif self.right >= self.limit_right and self.speed > 0:
            self.speed *= -1
    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.speed = abs(self.speed) # Reseta velocidade positiva

    def draw(self, screen):
        # Desenha direto na posição x,y (Sem câmera)
        pygame.draw.rect(screen, self.color, self)