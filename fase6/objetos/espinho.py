import pygame

class Espinho(pygame.Rect):
    def __init__(self, x, y, width):
        # Altura 16px para caber o sprite
        super().__init__(x, y, width, 25)
        
        self.image = pygame.Surface((width, 26), pygame.SRCALPHA)
        
        try:
            tileset = pygame.image.load("fase6/assets/tileset.png").convert_alpha()
            # Recorta os espinhos do tileset
            # Estimativa visual: x=16, y=48, w=16, h=16
            tile_espinho = tileset.subsurface((64, 105, 23, 12))
            
            # Repete o espinho lado a lado
            quantidade = (width // 16) + 1
            for i in range(quantidade):
                self.image.blit(tile_espinho, (i * 16, 0))
        except:
            self.image.fill((255, 0, 0)) # Se der erro, fica vermelho

    def draw(self, screen, camera):
        rect_visivel = camera.apply(self)
        screen.blit(self.image, rect_visivel)