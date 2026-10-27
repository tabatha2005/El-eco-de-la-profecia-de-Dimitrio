"""
02_formas_y_colores.py
----------------------
Dibujo de Primitivas Gráficas y Sistema de Coordenadas:
- Sistema de ejes cartesianos de Pygame (Origen (0, 0) en la esquina superior izquierda).
- Definición de colores mediante tuplas RGB (0 a 255).
- Dibujo de rectángulos, círculos, líneas y polígonos con pygame.draw.
- Formas rellenas versus formas con bordes (parámetro 'width').
"""

import math
import sys
import pygame


def main():
    pygame.init()
    ANCHO, ALTO = 800, 600
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("02 - Formas Primitivas y Colores | Tutorial Pygame")

    reloj = pygame.time.Clock()

    # Definición de paleta de colores RGB
    NEGRO = (15, 15, 20)
    BLANCO = (240, 240, 245)
    GRIS_OSCURO = (45, 48, 58)
    GRIS_CLARO = (120, 125, 140)
    ROJO_CARMESI = (180, 25, 45)
    DORADO_ANTIGUO = (212, 175, 55)
    CIAN_MAGICO = (60, 200, 220)
    PURPURA_MISTICO = (128, 40, 160)

    angulo = 0.0
    ejecutando = True

    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT or (
                evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE
            ):
                ejecutando = False

        # Actualizar animación sutil
        angulo += 0.03

        # Limpiar fondo
        pantalla.fill(NEGRO)

        # 1. Dibujar Cuadrícula de baldosas (líneas)
        for x in range(0, ANCHO, 50):
            pygame.draw.line(pantalla, GRIS_OSCURO, (x, 0), (x, ALTO), 1)
        for y in range(0, ALTO, 50):
            pygame.draw.line(pantalla, GRIS_OSCURO, (0, y), (ANCHO, y), 1)

        # 2. Rectángulos: pygame.draw.rect(superficie, color, rect, ancho_borde)
        # Rectángulo sólido (ancho = 0 por defecto)
        pygame.draw.rect(pantalla, (35, 38, 50), (100, 100, 220, 140))
        # Borde exterior del rectángulo
        pygame.draw.rect(pantalla, DORADO_ANTIGUO, (100, 100, 220, 140), 3)

        # Rectángulo redondeado
        pygame.draw.rect(pantalla, ROJO_CARMESI, (100, 320, 220, 140), border_radius=15)
        pygame.draw.rect(pantalla, BLANCO, (100, 320, 220, 140), width=3, border_radius=15)

        # 3. Círculos: pygame.draw.circle(superficie, color, centro, radio, ancho_borde)
        centro_circulo = (550, 180)
        # Círculo base
        pygame.draw.circle(pantalla, PURPURA_MISTICO, centro_circulo, 70)
        # Anillos concéntricos con borde
        pygame.draw.circle(pantalla, CIAN_MAGICO, centro_circulo, 85, 3)
        radio_pulso = 70 + int(math.sin(angulo) * 10)
        pygame.draw.circle(pantalla, DORADO_ANTIGUO, centro_circulo, radio_pulso, 2)

        # 4. Polígonos: pygame.draw.polygon(superficie, color, lista_puntos, ancho_borde)
        # Dibujar un rombo místico giratorio en la zona inferior
        cx, cy = 550, 400
        radio_puntos = 60
        puntos_rombo = [
            (cx + math.cos(angulo) * radio_puntos, cy + math.sin(angulo) * radio_puntos),
            (cx - math.sin(angulo) * radio_puntos, cy + math.cos(angulo) * radio_puntos),
            (cx - math.cos(angulo) * radio_puntos, cy - math.sin(angulo) * radio_puntos),
            (cx + math.sin(angulo) * radio_puntos, cy - math.cos(angulo) * radio_puntos),
        ]
        pygame.draw.polygon(pantalla, ROJO_CARMESI, puntos_rombo, 0)
        pygame.draw.polygon(pantalla, BLANCO, puntos_rombo, 3)

        # 5. Línea conectora con grosor
        pygame.draw.line(pantalla, DORADO_ANTIGUO, (320, 170), (465, 180), 4)

        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
