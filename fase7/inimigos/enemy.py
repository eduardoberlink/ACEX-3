import pygame
from support import carregar_imagem


def _recolorir_purificada(img):
    """Transforma a capivara corrompida (verde, com ferida vermelha) numa capivara
    curada: pelagem marrom natural e a ferida vira um tom claro."""
    novo = img.copy()
    for x in range(novo.get_width()):
        for y in range(novo.get_height()):
            r, g, b, a = novo.get_at((x, y))
            if a == 0:
                continue
            if r > g + 50 and r > b + 50:               # ferida vermelha -> clara
                novo.set_at((x, y), (255, 236, 228, a))
            elif g >= r and g >= b:                      # pelagem verde -> marrom
                lum = (r + g + b) / 3
                novo.set_at((x, y), (min(255, int(lum * 1.3 + 35)),
                                     min(255, int(lum * 1.0 + 12)),
                                     min(255, int(lum * 0.55 + 5)), a))
    return novo


class Inimigo(pygame.Rect):
    def __init__(self, x, y, size, limit_left, limit_right, speed=3, vida=1):
        super().__init__(x, y, size, size)

        # Quando purificada, a capivara é tratada como plataforma pelo jogador (item 3).
        # Essas flags dizem que ela não é parede nem plataforma móvel.
        self.parede = False
        self.movel = False

        self.base_speed = speed
        self.speed = speed
        self.limit_left = limit_left
        self.limit_right = limit_right
        self.start_x = x
        self.start_y = y

        # ===== ITEM 3: PURIFICAÇÃO =====
        self.vida_max = vida        # quantos golpes precisa para ser purificado (guardião = 3)
        self.vida = vida
        self.purificado = False     # purificada: não anda, não machuca e vira plataforma
        self.cooldown_golpe = 0     # quadros sem poder ser atingida de novo (para o guardião)
        self.flash = 0              # quadros piscando em branco depois de levar um golpe
        self.tempo = 0              # contador para animar o brilho

        # Carrega a Capivara
        sprite_normal = pygame.Surface((size, size))
        sprite_normal.fill((255, 0, 255))  # Cor de erro (Magenta)
        sprite_curada = sprite_normal

        try:
            img = carregar_imagem("capivara-corrompida.png")
            sprite_normal = pygame.transform.scale(img, (size, size))
            sprite_curada = pygame.transform.scale(_recolorir_purificada(img), (size, size))
        except Exception:
            pass  # Mantém o quadrado magenta se falhar

        # Guardamos as versões olhando para os dois lados
        self.sprite_original = sprite_normal
        self._sprites = {
            False: {"esq": sprite_normal, "dir": pygame.transform.flip(sprite_normal, True, False)},
            True:  {"esq": sprite_curada, "dir": pygame.transform.flip(sprite_curada, True, False)},
        }
        self._lado = "esq"
        self.current_sprite = self._sprites[False]["esq"]

    # ---------- golpe de purificação ----------
    def receber_purificacao(self):
        """Chamado quando o golpe (F) ou a pisada acerta. Devolve True se contou."""
        if self.purificado or self.cooldown_golpe > 0:
            return False
        self.vida -= 1
        if self.vida <= 0:
            self.purificado = True
            self.speed = 0
        else:
            self.cooldown_golpe = 30   # meio segundo de folga antes do próximo golpe valer
            self.flash = 12
        return True

    def update(self):
        self.tempo += 1
        if self.cooldown_golpe > 0:
            self.cooldown_golpe -= 1
        if self.flash > 0:
            self.flash -= 1

        if self.purificado:
            self.current_sprite = self._sprites[True][self._lado]
            return  # purificada: fica parada

        self.x += self.speed

        # Patrulha
        if self.left <= self.limit_left and self.speed < 0:
            self.speed *= -1
        elif self.right >= self.limit_right and self.speed > 0:
            self.speed *= -1

        # Vira o sprite conforme a direção
        self._lado = "dir" if self.speed > 0 else "esq"
        self.current_sprite = self._sprites[False][self._lado]

    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.speed = abs(self.base_speed)
        self.vida = self.vida_max
        self.purificado = False
        self.cooldown_golpe = 0
        self.flash = 0

    def draw(self, screen, camera):
        rect_visivel = camera.apply(self)

        if self.purificado:
            # brilho verde-claro suave embaixo, para indicar que está curada
            pulso = 0.5 + 0.5 * pygame.math.Vector2(1, 0).rotate(self.tempo * 6).x
            aura = pygame.Surface((self.width + 16, self.height + 16), pygame.SRCALPHA)
            pygame.draw.ellipse(aura, (190, 255, 190, int(40 + 40 * pulso)), aura.get_rect())
            screen.blit(aura, (rect_visivel.x - 8, rect_visivel.y - 8))

        sprite = self.current_sprite
        if self.flash > 0 and (self.flash // 2) % 2 == 0:
            sprite = sprite.copy()
            sprite.fill((150, 150, 150, 0), special_flags=pygame.BLEND_RGB_ADD)  # pisca branco
        screen.blit(sprite, rect_visivel)

        if self.purificado:
            # duas estrelinhas girando
            for k in range(2):
                v = pygame.math.Vector2(self.width * 0.55, 0).rotate(self.tempo * 4 + k * 180)
                pygame.draw.circle(screen, (255, 255, 220),
                                   (int(rect_visivel.centerx + v.x), int(rect_visivel.top - 6 + v.y * 0.4)), 2)

        # Barrinha de vida para quem precisa de mais de um golpe (o guardião)
        if self.vida_max > 1 and not self.purificado:
            for i in range(self.vida_max):
                cor = (120, 255, 120) if i < self.vida else (70, 70, 70)
                pygame.draw.rect(screen, cor, (rect_visivel.x + i * 12, rect_visivel.y - 9, 10, 5))
