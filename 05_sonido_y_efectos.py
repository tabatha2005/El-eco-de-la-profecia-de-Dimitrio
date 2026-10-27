"""
05_sonido_y_efectos.py
----------------------
Audio y Efectos Sonoros con pygame.mixer:
- Inicialización del subsistema de audio.
- Generación procedimental de ondas de sonido (sin necesidad de archivos externos .wav/.mp3).
- Conversión de buffers de audio PCM en objetos pygame.mixer.Sound.
- Control de canales, reproducción y retroalimentación visual al reproducir audio.
"""

import math
import struct
import sys
import pygame


def sintetizar_tono(frecuencia, duracion_segundos, volumen=0.5, tipo="seno"):
    """
    Genera un objeto pygame.mixer.Sound mediante síntesis matemática.
    Evita depender de archivos .wav externos y garantiza portabilidad total.
    """
    frecuencia_muestreo = 44100
    total_muestras = int(frecuencia_muestreo * duracion_segundos)
    datos = bytearray()

    for i in range(total_muestras):
        t = i / frecuencia_muestreo
        # Envolvente de decaimiento para evitar chasquidos acústicos
        envolvente = max(0.0, 1.0 - (i / total_muestras))

        if tipo == "seno":
            valor = math.sin(2.0 * math.pi * frecuencia * t)
        elif tipo == "latido":
            # Modulación para simular el sístole/diástole de un corazón
            pulso = math.sin(2.0 * math.pi * frecuencia * t)
            envolvente = math.exp(-6.0 * (t % 0.4))
            valor = pulso * envolvente
        elif tipo == "campana":
            # Tono armónico con decaimiento suave
            valor = (
                0.6 * math.sin(2.0 * math.pi * frecuencia * t)
                + 0.3 * math.sin(2.0 * math.pi * (frecuencia * 2.0) * t)
                + 0.1 * math.sin(2.0 * math.pi * (frecuencia * 3.0) * t)
            )
        else:
            valor = 0.0

        muestra = int(valor * envolvente * volumen * 32767)
        muestra = max(-32768, min(32767, muestra))

        # Empaquetar como entero con signo de 16 bits (mono)
        datos.extend(struct.pack("<h", muestra))

    return pygame.mixer.Sound(buffer=bytes(datos))


def main():
    pygame.init()
    pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)

    ANCHO, ALTO = 800, 600
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("05 - Síntesis y Reproducción de Audio | Tutorial Pygame")

    reloj = pygame.time.Clock()
    fuente = pygame.font.SysFont("consolas", 20)

    # Sintetizar 3 efectos de sonido temáticos
    print(">> Sintetizando ondas de audio de suspenso...")
    sonido_latido = sintetizar_tono(frecuencia=65, duracion_segundos=0.6, volumen=0.9, tipo="latido")
    sonido_pista = sintetizar_tono(frecuencia=587.33, duracion_segundos=0.9, volumen=0.6, tipo="campana")
    sonido_maldicion = sintetizar_tono(frecuencia=110, duracion_segundos=1.5, volumen=0.8, tipo="seno")

    ultimo_sonido = "Ninguno"
    tiempo_retroalimentacion = 0

    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    ejecutando = False
                elif evento.key == pygame.K_SPACE:
                    sonido_latido.play()
                    ultimo_sonido = "Latido Cardíaco [ESPACIO]"
                    tiempo_retroalimentacion = 30
                elif evento.key == pygame.K_e:
                    sonido_pista.play()
                    ultimo_sonido = "Descubrimiento de Pista [E]"
                    tiempo_retroalimentacion = 30
                elif evento.key == pygame.K_c:
                    sonido_maldicion.play()
                    ultimo_sonido = "Acorde de Maldición Ancestral [C]"
                    tiempo_retroalimentacion = 30

        pantalla.fill((18, 16, 24))

        # Retroalimentación visual interactiva
        if tiempo_retroalimentacion > 0:
            tiempo_retroalimentacion -= 1
            color_borde = (190, 40, 50)
            radio_onda = (30 - tiempo_retroalimentacion) * 8
            pygame.draw.circle(pantalla, color_borde, (ANCHO // 2, 280), radio_onda, 3)

        # Instrucciones en pantalla
        txt1 = fuente.render("SISTEMA DE AUDIO INTEGRADO (PYGAME.MIXER)", True, (240, 210, 150))
        txt2 = fuente.render("[ESPACIO] -> Reproducir Latido Cardíaco (Suspenso)", True, (200, 200, 210))
        txt3 = fuente.render("[E]       -> Reproducir Hallazgo de Pista / Reliquia", True, (200, 200, 210))
        txt4 = fuente.render("[C]       -> Reproducir Alerta de Maldición Oscura", True, (200, 200, 210))
        txt5 = fuente.render(f"Último sonido reproducido: {ultimo_sonido}", True, (255, 120, 140))

        pantalla.blit(txt1, (80, 80))
        pantalla.blit(txt2, (80, 160))
        pantalla.blit(txt3, (80, 200))
        pantalla.blit(txt4, (80, 240))
        pantalla.blit(txt5, (80, 460))

        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
