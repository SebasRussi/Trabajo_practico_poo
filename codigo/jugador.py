import pygame
from laser import Laser


class Jugador(pygame.sprite.Sprite):
    def __init__(self, posicion, limitar, velocidad_pos, velocidad_neg):
        super().__init__()

        self.image = pygame.image.load('../imagenes/nave 16bit.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=posicion)
        self.velocidad_pos = velocidad_pos
        self.velocidad_neg = velocidad_neg
        self.ready = True
        self.tiempo_laser = 0
        self.cooldown_laser = 600
        self.lasers = pygame.sprite.Group()

    def inputs(self):
        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_RIGHT]:
            self.rect.x += self.velocidad_pos
        elif teclas[pygame.K_LEFT]:
            self.rect.x -= self.velocidad_neg

        if teclas[pygame.K_SPACE] and self.ready:
            self.disparar_laser()
            self.ready = False
            self.tiempo_laser = pygame.time.get_ticks()

    def recargar(self):
        if not self.ready:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.tiempo_laser >= self.cooldown_laser:
                self.ready = True

    def disparar_laser(self):
        self.lasers.add(Laser(self.rect.center, -12, self.rect.bottom))

    def limitar(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 600:
            self.rect.right = 600

    def update(self):
        self.inputs()
        self.limitar()
        self.recargar()
        self.lasers.update()
