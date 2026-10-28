import pygame

class Plataforma(pygame.Rect):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height)
        self.color = color
        
        # Cria uma superfície vazia do tamanho da plataforma para desenhar a textura nela
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # --- LÓGICA DO CHÃO (VERDE) ---
        if color == (0, 255, 0): # Se for o VERDE (Green)
            try:
                tileset = pygame.image.load("fase6/assets/tileset.png").convert_alpha()
                # Recorta um quadrado de grama do tileset
                tile_grama = tileset.subsurface((68, 184, 27, 7)) 
                tile_grama = pygame.transform.scale(tile_grama, (height, height)) # Escala para altura do chão
                
                # Repete a grama lado a lado até preencher a largura
                quantidade = (width // height) + 1
                for i in range(quantidade):
                    self.image.blit(tile_grama, (i * height, 0))
            except:
                self.image.fill(color) # Se der erro, pinta de verde

        # --- LÓGICA DAS PLATAFORMAS VOADORAS (AMARELO) ---
        elif color == (255, 255, 0): # Se for AMARELO (Yellow)
            try:
                sprites_amb = pygame.image.load("fase6/assets/sprites-ambiente.png").convert_alpha()
                # Recorta o galho da árvore (lado direito da imagem)
                galho = sprites_amb.subsurface((155, 28, 21, 7))
                # Estica o galho para ficar do tamanho da plataforma
                self.image = pygame.transform.scale(galho, (width, height))
            except:
                self.image.fill(color) # Se der erro, pinta de amarelo
        
        # --- OUTROS CASOS ---
        else:
            self.image.fill(color)

    def draw(self, screen, camera):
        rect_visivel = camera.apply(self)
        screen.blit(self.image, rect_visivel)