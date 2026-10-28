import pygame

class Camera:
    def __init__(self, width, height, screen_width):
        # width: largura total do mundo (background)
        # screen_width: largura da janela
        self.camera_rect = pygame.Rect(0, 0, width, height)
        self.width = width
        self.screen_width = screen_width
        self.x = 0

    def update(self, target_rect, offset_ratio=3):
        # target_rect: geralmente o player
        # offset_ratio: divisor (ex: 3 para o player ficar a 1/3 da tela)
        target_x = target_rect.x - (self.screen_width // offset_ratio)
        
        # Limitar a câmera (não sair do mundo)
        self.x = max(0, min(target_x, self.width - self.screen_width))
        self.camera_rect.x = self.x

    def apply(self, entity_rect):
        # Retorna um novo Rect deslocado pela câmera para desenhar
        return entity_rect.move(-self.x, 0)