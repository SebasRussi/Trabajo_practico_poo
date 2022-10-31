import pygame


class Laser(pygame.sprite.Sprite):
    def __init__(self, posicion, velocidad_rayo, alto_pantalla):
        super().__init__()
        self.image = pygame.Surface((4, 20))
        self.image.fill("white")
        self.rect = self.image.get_rect(center=posicion)
        self.velocidad_rayo = velocidad_rayo
        self.limite_altura = alto_pantalla

    def destruir(self):
        if self.rect.y <= -50 or self.rect.y >= self.limite_altura + 50:
            self.kill()

    def update(self):
        self.rect.y += self.velocidad_rayo
        self.destruir()
