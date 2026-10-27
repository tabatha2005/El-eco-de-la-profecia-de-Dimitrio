"""
03_movimiento_teclado.py
------------------------
Entrada de Usuario y Movimiento en Tiempo Real:
- Consulta continua del estado del teclado con pygame.key.get_pressed().
- Movimiento bidimensional en 8 direcciones (WASD y teclas de flechas).
- Normalización de velocidad para evitar mayor rapidez en movimientos diagonales.
- Restricción de límites de la ventana (bounding box clamp).
"""

import math
import sys
import pygame


def main():
    pygame.init()
    ANCHO, ALTO = 800, 600
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("03 - Movimiento Suave por Teclado | Tutorial Pygame")

    reloj = pygame.time.Clock()

    # Estado del jugador
    jugador_x = ANCHO // 2
    jugador_y = ALTO // 2
    radio_jugador = 22
    velocidad_base = 5.0
    rastro_posiciones = []

    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT or (
                evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE
            ):
                ejecutando = False

        # 1. Obtener estado de todas las teclas presionadas
        teclas = pygame.key.get_pressed()

        dx = 0
        dy = 0

        # Soporte tanto para flechas como para WASD
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            dx -= 1
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            dx += 1
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            dy -= 1
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            dy += 1

        # 2. Correr con tecla SHIFT
        velocidad_actual = velocidad_base * (1.6 if teclas[pygame.K_LSHIFT] else 1.0)

        # 3. Normalizar vector para evitar velocidad excesiva en diagonal
        if dx != 0 and dy != 0:
            longitud = math.sqrt(dx * dx + dy * dy)
            dx /= longitud
            dy /= longitud

        # 4. Actualizar posición
        jugador_x += dx * velocidad_actual
        jugador_y += dy * velocidad_actual

        # 5. Restringir posición a los bordes de la pantalla
        jugador_x = max(radio_jugador, min(ANCHO - radio_jugador, jugador_x))
        jugador_y = max(radio_jugador, min(ALTO - radio_jugador, jugador_y))

        # Registrar rastro de pasos si se está moviendo
        if dx != 0 or dy != 0:
            rastro_posiciones.append((int(jugador_x), int(jugador_y)))
            if len(rastro_posiciones) > 25:
                rastro_posiciones.pop(0)

        # --- DIBUJO ---
        pantalla.fill((20, 24, 34))

        # Dibujar rastro
        for i, pos in enumerate(rastro_posiciones):
            alpha = int((i / len(rastro_posiciones)) * 140)
            tam = max(3, int((i / len(rastro_posiciones)) * 10))
            pygame.draw.circle(pantalla, (70, 90, 130), pos, tam)

        # Dibujar al jugador (cuerpo e indicador de linterna)
        pygame.draw.circle(pantalla, (35, 140, 225), (int(jugador_x), int(jugador_y)), radio_jugador)
        pygame.draw.circle(pantalla, (230, 245, 255), (int(jugador_x), int(jugador_y)), radio_jugador, 3)

        # Pequeño núcleo
        pygame.draw.circle(pantalla, (255, 220, 100), (int(jugador_x), int(jugador_y)), 7)

        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
