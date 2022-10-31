import pygame


class Alien(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        ruta_de_archivo = "../imagenes/" + color + ".png"
        self.image = pygame.image.load(ruta_de_archivo).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

        if color == 'red': self.value = 100
        elif color == 'azul': self.value = 200
        else: self.value = 300

    def update(self,direccion):
        self.rect.x += direccion
