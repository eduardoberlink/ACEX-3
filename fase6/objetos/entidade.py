import pygame


class Entidade(pygame.Rect):
    """Base de tudo que aparece no mundo: um Rect (hitbox) com uma imagem.

    As subclasses só precisam definir `self.image`; o desenho com a câmera
    é igual para todas.
    """

    image: pygame.Surface

    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self))
