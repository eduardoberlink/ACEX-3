class Camera:
    """Câmera horizontal que segue um alvo sem sair dos limites do mundo."""

    def __init__(self, world_width, screen_width):
        self.world_width = world_width
        self.screen_width = screen_width
        self.x = 0

    def update(self, target_rect, offset_ratio=3):
        # offset_ratio=3 deixa o alvo a 1/3 da tela, a partir da esquerda
        target_x = target_rect.x - self.screen_width // offset_ratio
        self.x = max(0, min(target_x, self.world_width - self.screen_width))

    def apply(self, rect):
        """Retorna o rect deslocado para a posição na tela."""
        return rect.move(-self.x, 0)
