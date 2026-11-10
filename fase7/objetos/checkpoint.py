import pygame


class Checkpoint(pygame.Rect):
    """ITEM 11 - Bandeira de checkpoint.
    Ao ser tocada, muda de cor e passa a ser o local de renascimento."""

    def __init__(self, x, chao_y):
        # x = posição da bandeira, chao_y = altura do chão onde ela está fincada
        super().__init__(x, chao_y - 50, 24, 50)
        self.ativo = False
        self.respawn_pos = (x, chao_y)   # onde o jogador reaparece (canto inferior esquerdo)
        self.tempo = 0

    def ativar(self):
        self.ativo = True

    def reset(self):
        self.ativo = False

    def update(self):
        self.tempo += 1

    def draw(self, screen, camera):
        r = camera.apply(self)
        # mastro
        pygame.draw.rect(screen, (90, 60, 40), (r.x + 2, r.y, 4, r.height))
        pygame.draw.circle(screen, (230, 230, 230), (r.x + 4, r.y), 3)
        # bandeira (cinza = apagada, verde = ativa) balançando um pouquinho
        cor = (90, 220, 110) if self.ativo else (150, 150, 150)
        ondas = int(2 * pygame.math.Vector2(1, 0).rotate(self.tempo * 8).x) if self.ativo else 0
        pontos = [(r.x + 6, r.y + 3), (r.x + 24, r.y + 11 + ondas), (r.x + 6, r.y + 20)]
        pygame.draw.polygon(screen, cor, pontos)
        pygame.draw.polygon(screen, (30, 30, 30), pontos, 1)
