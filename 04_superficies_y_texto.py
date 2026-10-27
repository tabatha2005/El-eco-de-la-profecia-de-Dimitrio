"""
04_superficies_y_texto.py
-------------------------
Manejo de Superficies (Surface), Fuentes y Transparencias:
- Inicialización y renderizado de texto con pygame.font.
- Creación de superficies independientes con canal alfa (transparencia).
- Técnica de máscara de oscuridad y luz (prototipo de linterna para juegos de terror).
- Composición de capas mediante pantalla.blit().
"""

import sys
import pygame


def main():
    pygame.init()
    pygame.font.init()

    ANCHO, ALTO = 800, 600
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("04 - Fuentes, Superficies y Capas Alfa | Tutorial Pygame")

    reloj = pygame.time.Clock()

    # Fuentes del sistema
    fuente_titulo = pygame.font.SysFont("georgia", 32, bold=True)
    fuente_cuerpo = pygame.font.SysFont("consolas", 18)

    # 1. Crear una superficie para el efecto de niebla/oscuridad
    superficie_oscuridad = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)

    # 2. Superficie para el diálogo translúcido
    caja_dialogo = pygame.Surface((720, 140), pygame.SRCALPHA)
    caja_dialogo.fill((15, 18, 28, 220))  # RGBA: 220 de opacidad (semitransparente)
    pygame.draw.rect(caja_dialogo, (180, 150, 90), (0, 0, 720, 140), 2, border_radius=10)

    # Textos renderizados
    texto_titulo = fuente_titulo.render("EXPEDIENTE #404: LA MANSIÓN EN SOMBRAS", True, (240, 220, 170))
    texto_linea1 = fuente_cuerpo.render("> Pista detectada: El reloj se detuvo a las 03:17 a. m.", True, (210, 215, 230))
    texto_linea2 = fuente_cuerpo.render("> Mueve el mouse para usar la linterna sobre las pistas.", True, (130, 195, 255))

    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT or (
                evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE
            ):
                ejecutando = False

        pos_mouse = pygame.mouse.get_pos()

        # --- DIBUJO DE FONDO ---
        pantalla.fill((30, 20, 25))

        # Dibujar algunos objetos en la "escena del crimen" (fondo)
        # Mancha de sangre
        pygame.draw.circle(pantalla, (120, 15, 25), (320, 240), 45)
        pygame.draw.circle(pantalla, (100, 10, 20), (350, 260), 25)
        # Nota misteriosa
        pygame.draw.rect(pantalla, (230, 220, 190), (450, 200, 70, 90))
        pygame.draw.line(pantalla, (50, 50, 50), (460, 220), (510, 220), 2)
        pygame.draw.line(pantalla, (50, 50, 50), (460, 240), (505, 240), 2)

        # --- EFECTO DE LINTERNA CON CAPA DE OSCURIDAD ---
        # Llenamos la superficie con negro casi total (245 de opacidad)
        superficie_oscuridad.fill((8, 10, 15, 245))

        # "Cortamos" un agujero de luz donde está el mouse usando círculos con canal alfa 0 o colores aditivos
        # Círculo exterior tenue
        pygame.draw.circle(superficie_oscuridad, (255, 240, 190, 80), pos_mouse, 150)
        # Círculo interior nítido con color transparente (0, 0, 0, 0) usando BLEND_RGBA_MIN
        luz_directa = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        luz_directa.fill((0, 0, 0, 0))
        pygame.draw.circle(luz_directa, (0, 0, 0, 0), pos_mouse, 110)

        # Aplicar la máscara de oscuridad
        pantalla.blit(superficie_oscuridad, (0, 0))

        # --- DIBUJAR CAJA DE DIÁLOGO / TEXTO ENCIMA ---
        pantalla.blit(caja_dialogo, (40, 430))
        pantalla.blit(texto_titulo, (60, 445))
        pantalla.blit(texto_linea1, (60, 495))
        pantalla.blit(texto_linea2, (60, 525))

        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
