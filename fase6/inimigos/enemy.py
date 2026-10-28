import pygame

class Inimigo(pygame.Rect):
    def __init__(self, x, y, size, limit_left, limit_right, speed=3):
        super().__init__(x, y, size, size)
        
        self.base_speed = speed 
        self.speed = speed
        self.limit_left = limit_left
        self.limit_right = limit_right
        self.start_x = x
        self.start_y = y
        
        # Carrega a Capivara
        self.sprite_original = pygame.Surface((size, size))
        self.sprite_original.fill((255, 0, 255)) # Cor de erro (Magenta)
        
        try:
            img = pygame.image.load("fase6/assets/capivara-corrompida.png").convert_alpha()
            self.sprite_original = pygame.transform.scale(img, (size, size))
        except:
            pass # Mantém o quadrado magenta se falhar

        self.current_sprite = self.sprite_original

    def update(self):
        self.x += self.speed

        # Patrulha
        if self.left <= self.limit_left and self.speed < 0:
            self.speed *= -1
        elif self.right >= self.limit_right and self.speed > 0:
            self.speed *= -1
            
        # Vira o sprite conforme a direção
        if self.speed > 0: # Indo pra direita
            self.current_sprite = pygame.transform.flip(self.sprite_original, True, False)
        else: # Indo pra esquerda
            self.current_sprite = self.sprite_original

    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.speed = abs(self.base_speed)

    def draw(self, screen, camera):
        rect_visivel = camera.apply(self)
        screen.blit(self.current_sprite, rect_visivel)