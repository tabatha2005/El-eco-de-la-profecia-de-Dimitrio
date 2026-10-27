"""
01_ventana_y_bucle.py
---------------------
Fundamentos de Pygame:
- Inicialización de los módulos de Pygame.
- Creación y configuración de la ventana principal de la aplicación.
- Implementación del ciclo de vida del juego (Game Loop).
- Manejo de eventos básicos (cerrar ventana y tecla ESC).
- Control de la tasa de cuadros por segundo (FPS).
"""

import sys
import pygame


def main():
    # 1. Inicializar todos los módulos internos de Pygame
    pygame.init()

    # 2. Configurar dimensiones de la ventana
    ANCHO, ALTO = 800, 600
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("01 - Ventana Básica y Game Loop | Tutorial Pygame")

    # 3. Reloj para controlar los fotogramas por segundo (FPS)
    reloj = pygame.time.Clock()
    FPS = 60

    # 4. Paleta de colores en formato RGB (Rojo, Verde, Azul)
    COLOR_FONDO = (25, 30, 45)  # Azul oscuro elegante

    # 5. Variable de control del ciclo de vida
    ejecutando = True

    print(">> Aplicación iniciada con éxito. Presiona ESC o cierra la ventana para salir.")

    # 6. BUCLE PRINCIPAL (Game Loop)
    while ejecutando:
        # A) PROCESAMIENTO DE EVENTOS
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    ejecutando = False

        # B) ACTUALIZACIÓN DE ESTADO (Lógica futura del juego)

        # C) RENDERIZADO / DIBUJO
        pantalla.fill(COLOR_FONDO)

        # D) ACTUALIZAR PANTALLA
        pygame.display.flip()

        # E) LIMITAR TASA DE REFRESCO
        reloj.tick(FPS)

    # 7. Cierre limpio de recursos
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
