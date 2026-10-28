import pygame

class Porta(pygame.Rect):
    def __init__(self, x, y, size):
        # Cria um retângulo preto na posição X, Y com largura e altura = size
        super().__init__(x, y, size, size)
        self.color = (0, 0, 0) # Cor Preta

    def draw(self, screen):
        # Desenha diretamente na tela (sem cálculo de câmera)
        pygame.draw.rect(screen, self.color, self)