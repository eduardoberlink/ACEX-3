import pygame


class Porta(pygame.Rect):
    """Porta final. ITEM 4: começa trancada e só abre com a chave."""

    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        self.color = (0, 0, 0)  # Preto
        self.trancada = True

    def destrancar(self):
        self.trancada = False

    def reset(self):
        self.trancada = True

    def draw(self, screen, camera):
        r = camera.apply(self)
        if self.trancada:
            pygame.draw.rect(screen, (20, 20, 25), r)                  # porta escura
            pygame.draw.rect(screen, (90, 90, 100), r, 3)              # moldura de ferro
            # cadeado
            cx, cy = r.centerx, r.centery
            pygame.draw.rect(screen, (200, 160, 40), (cx - 7, cy - 2, 14, 11))
            pygame.draw.arc(screen, (200, 160, 40), (cx - 6, cy - 11, 12, 14), 0, 3.14159, 3)
            pygame.draw.circle(screen, (60, 40, 10), (cx, cy + 3), 2)
        else:
            pygame.draw.rect(screen, (60, 210, 120), r)                # destrancada: verde
            pygame.draw.rect(screen, (255, 235, 140), r, 3)            # moldura dourada
            pygame.draw.rect(screen, (30, 120, 70), r.inflate(-16, -10).move(0, 5))  # vão aberto
