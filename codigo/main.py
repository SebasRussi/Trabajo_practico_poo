import pygame, sys
from jugador import Jugador
from aliens import Alien
from random import choice
from laser import Laser

class Juego:
    def __init__(self):
        # Configuracion del jugador
        imagen_jugador = Jugador((ancho_pantalla / 2, 700), ancho_pantalla, 5, 5)
        self.jugador = pygame.sprite.GroupSingle(imagen_jugador)

        # vida y puntuacion
        self.vidas = 3
        self.imagen_vida = pygame.image.load('../imagenes/vida.png').convert_alpha()
        self.posicion_vida = ancho_pantalla - (self.imagen_vida.get_size()[0] * 2 + 20)
        self.puntuacion = 0
        self.fuente = pygame.font.Font('../fuente/Pixeled.ttf', 20)





        # Configuracion alien
        self.aliens = pygame.sprite.Group()
        self.alien_setup(filas=6, columnas=8)
        self.movimiento_alien = 1
        self.laser_alien = pygame.sprite.Group()

    def alien_setup(self, filas, columnas, distancia_x=60, distancia_y=48, x_offset=70, y_offset=100):
        for indice_filas, fila in enumerate(range(filas)):
            for indice_columna, columna in enumerate(range(columnas)):
                x = indice_columna * distancia_x + x_offset
                y = indice_filas * distancia_y + y_offset

                if indice_filas == 0:
                    alien_sprite = Alien("morado", x, y)
                elif 1 <= indice_filas <= 2:
                    alien_sprite = Alien("azulado", x, y)
                else:
                    alien_sprite = alien_sprite = Alien("red", x, y)
                self.aliens.add(alien_sprite)

    def movimiento_aliens(self):
        alienigenas = self.aliens.sprites()
        for alien in alienigenas:
            if alien.rect.right >= ancho_pantalla:
                self.movimiento_alien = -2
                self.movimiento_alien_abajo(1)
            elif alien.rect.left <= 0:
                self.movimiento_alien = 2
                self.movimiento_alien_abajo(1)

    def movimiento_alien_abajo(self, distancia):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distancia

    def ataque_alien(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center, 6, alto_pantalla)
            self.laser_alien.add(laser_sprite)



    def colisiones(self):
        # laser del jugador
        if self.jugador.sprite.lasers:
            for laser in self.jugador.sprite.lasers:

                disparo_al_alien = pygame.sprite.spritecollide(laser, self.aliens, True)
                if disparo_al_alien:
                    for alien in disparo_al_alien:
                        self.puntuacion += alien.value
                    laser.kill()
        # laser de los aliens
        if self.laser_alien:
            for laser in self.laser_alien:
                if pygame.sprite.spritecollide(laser, self.jugador, False):
                    laser.kill()
                    self.vidas -= 1
                    if self.vidas <= 0:
                        pygame.quit()
                        sys.exit()

        if self.aliens:
            for alien in self.aliens:
                if pygame.sprite.spritecollide(alien, self.jugador, False):
                    pygame.quit()
                    sys.exit()

    def configuracion_vidas(self):
        for vida in range(self.vidas - 1):
            x = self.posicion_vida + (vida * self.imagen_vida.get_size()[0] + 10)
            pantalla.blit(self.imagen_vida, (x, 8))

    def configuracion_puntuacion(self):
        puntuacion = self.fuente.render(f'Puntuacion: {self.puntuacion}', False, 'white')
        puntuacion_rect  = puntuacion.get_rect(topleft=(0, 0))
        pantalla.blit(puntuacion, puntuacion_rect)

    def mensaje_de_victoria(self):
        if not self.aliens.sprites():
            mensaje = self.fuente.render('GANASTE', False, 'white')
            mensaje_rect = mensaje.get_rect(center=(ancho_pantalla / 2, alto_pantalla / 2))
            pantalla.blit(mensaje, mensaje_rect)

    def correr(self):
        self.aliens.update(self.movimiento_alien)
        self.jugador.update()
        self.movimiento_aliens()

        self.laser_alien.update()
        self.colisiones()

        self.jugador.sprite.lasers.draw(pantalla)

        self.jugador.draw(pantalla)
        self.aliens.draw(pantalla)
        self.laser_alien.draw(pantalla)
        self.configuracion_vidas()
        self.configuracion_puntuacion()
        self.mensaje_de_victoria()

if __name__ == "__main__":
    pygame.init()
    ancho_pantalla = 600
    alto_pantalla = 700
    pantalla = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
    clock = pygame.time.Clock()
    juego = Juego()

    laser_de_alien = pygame.USEREVENT + 1
    pygame.time.set_timer(laser_de_alien, 800)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == laser_de_alien:
                juego.ataque_alien()

        pantalla.fill((30, 30, 30))
        juego.correr()

        pygame.display.flip()
        clock.tick(60)
