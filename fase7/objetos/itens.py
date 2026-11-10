import pygame

# Itens pegáveis: Chave (item 4), Açaí (item 5) e Gema (item 13).
# Todos são só retângulos para colisão; o desenho usa formas simples do pygame.


class Item(pygame.Rect):
    def __init__(self, x, y, tamanho):
        super().__init__(x, y, tamanho, tamanho)
        self.coletado = False
        self.tempo = 0
        self.y_base = y

    def reset(self):
        self.coletado = False
        self.y = self.y_base

    def update(self):
        self.tempo += 1
        # flutua devagarinho para chamar atenção
        self.y = self.y_base + int(3 * pygame.math.Vector2(1, 0).rotate(self.tempo * 4).x)

    def draw(self, screen, camera):
        if not self.coletado:
            self.desenhar(screen, camera.apply(self))

    def desenhar(self, screen, r):
        raise NotImplementedError


class Chave(Item):
    """ITEM 4 - Chave da porta final."""
    def __init__(self, x, y):
        super().__init__(x, y, 22)

    def desenhar(self, screen, r):
        ouro = (255, 205, 40)
        escuro = (140, 100, 10)
        brilho = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(brilho, (255, 240, 120, 70), (20, 20), 18)
        screen.blit(brilho, (r.centerx - 20, r.centery - 20))
        pygame.draw.circle(screen, ouro, (r.x + 6, r.y + 6), 6)         # argola
        pygame.draw.circle(screen, escuro, (r.x + 6, r.y + 6), 2)
        pygame.draw.rect(screen, ouro, (r.x + 10, r.y + 5, 11, 3))      # haste
        pygame.draw.rect(screen, ouro, (r.x + 16, r.y + 8, 3, 5))       # dentes
        pygame.draw.rect(screen, ouro, (r.x + 20, r.y + 8, 3, 7))


class Acai(Item):
    """ITEM 5 - Tigela de açaí (power-up de 8 segundos)."""
    def __init__(self, x, y):
        super().__init__(x, y, 24)

    def desenhar(self, screen, r):
        brilho = pygame.Surface((44, 44), pygame.SRCALPHA)
        pygame.draw.circle(brilho, (190, 90, 255, 70), (22, 22), 20)
        screen.blit(brilho, (r.centerx - 22, r.centery - 22))
        # tigela
        pygame.draw.ellipse(screen, (110, 40, 150), (r.x, r.y + 6, 24, 18))
        pygame.draw.ellipse(screen, (70, 20, 100), (r.x + 2, r.y + 8, 20, 8))
        pygame.draw.polygon(screen, (235, 225, 210),
                            [(r.x + 3, r.y + 15), (r.x + 21, r.y + 15), (r.x + 17, r.y + 24), (r.x + 7, r.y + 24)])
        # granola / bolinhas de açaí por cima
        for dx, dy in ((5, 8), (11, 5), (17, 8), (9, 10), (15, 11)):
            pygame.draw.circle(screen, (60, 15, 90), (r.x + dx, r.y + dy), 3)


class Gema(Item):
    """ITEM 13 - Coletável (gema)."""
    def __init__(self, x, y):
        super().__init__(x, y, 16)

    def desenhar(self, screen, r):
        cx, cy = r.center
        pts = [(cx, cy - 9), (cx + 8, cy), (cx, cy + 9), (cx - 8, cy)]
        pygame.draw.polygon(screen, (80, 220, 255), pts)
        pygame.draw.polygon(screen, (230, 255, 255), [(cx, cy - 9), (cx + 8, cy), (cx, cy - 1), (cx - 8, cy)])
        pygame.draw.polygon(screen, (20, 90, 130), pts, 2)
