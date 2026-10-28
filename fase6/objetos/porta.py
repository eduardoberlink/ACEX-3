from config import BLACK
from objetos.entidade import Entidade
from recursos import superficie_solida


class Porta(Entidade):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        self.image = superficie_solida((size, size), BLACK)
