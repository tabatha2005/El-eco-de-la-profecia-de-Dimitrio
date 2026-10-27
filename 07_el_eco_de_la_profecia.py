"""
07_el_eco_de_la_profecia.py
=============================================================
PROYECTO INTEGRADOR: "EL ECO DE LA SOMBRA: LA PROFECÍA CARMESÍ"
=============================================================
Videojuego hiperrealista de terror psicológico, investigación y suspenso en 2D.

SISTEMA DE MÚLTIPLES FASES Y LABERINTOS:
- FASE 1: La Biblioteca Maldita (Laberinto de estanterías de caoba -> Diario de Dimitrio)
- FASE 2: El Laboratorio Alquímico (Laberinto de venenos y vitrinas -> Frasco de María)
- FASE 3: Las Catacumbas Subterráneas (Laberinto de sarcófagos -> Daga Ritual)
- FASE 4: La Capilla Prohibida (Laberinto de columnas arcanas -> Pergamino de la Profecía)
- FASE 5: El Gran Salón del Sacrificio (Cadáver de Dimitrio, Altar, Resolución de María y Clímax)

JUMPSCARES Y MOVIMIENTO EN FALSO:
- Sombras errantes que patrullan los estrechos pasillos y trampas de sangre ocultas.
- Si cometes un paso en falso, ¡la pantalla estalla con la imagen HD jumpscare.png,
  temblor violento y un alarido ensordecedor!

CONTROLES:
- W, A, S, D / Flechas : Mover al Detective humano
- Shift (mantener)     : Correr
- E / Espacio          : Recoger evidencias / Avanzar de fase / Altar / Cerrar notas
- F                    : Encender / Apagar linterna
- ESC                  : Salir del juego
- R                    : Reiniciar (en pantalla final o tras jumpscare)
"""

import math
import os
import random
import struct
import sys
import pygame

# -------------------------------------------------------------
# CONSTANTES DE PANTALLA Y GRID
# -------------------------------------------------------------
ANCHO_VENTANA = 960
ALTO_VENTANA = 640
FPS = 60

TAM_CASILLA = 40
FILAS_MAPA = 14
COLUMNAS_MAPA = 24
DESP_Y_MAPA = 48  # Espacio superior reservado para el HUD

# Paleta de colores realista
COLOR_FONDO_OSCURO = (10, 10, 14)
COLOR_DORADO_ANTIGUO = (212, 175, 55)
COLOR_SANGRE_FRESCA = (195, 18, 28)
COLOR_SANGRE_SECA = (85, 12, 18)
COLOR_GABARDINA = (48, 54, 65)
COLOR_SOMBRERO = (35, 38, 48)
COLOR_PIEL = (225, 195, 170)
COLOR_PIEL_CADAVER = (175, 180, 195)


# -------------------------------------------------------------
# SÍNTESIS DE AUDIO PROCEDIMENTAL (CERO DEPENDENCIAS EXTERNAS)
# -------------------------------------------------------------
def generar_sonido_procedimental(tipo):
    frecuencia_muestreo = 44100
    datos = bytearray()

    if tipo == "paso":
        muestras = int(frecuencia_muestreo * 0.08)
        for i in range(muestras):
            t = i / muestras
            ruido = (random.random() * 2.0 - 1.0) * (1.0 - t) ** 2
            val = int(ruido * 0.16 * 32767)
            datos.extend(struct.pack("<h", max(-32768, min(32767, val))))

    elif tipo == "recolectar":
        muestras = int(frecuencia_muestreo * 0.7)
        for i in range(muestras):
            t = i / frecuencia_muestreo
            env = math.exp(-3.8 * t)
            tono = (
                math.sin(2 * math.pi * 587.33 * t) * 0.5
                + math.sin(2 * math.pi * 739.99 * t) * 0.3
                + math.sin(2 * math.pi * 880.00 * t) * 0.2
            )
            val = int(tono * env * 0.55 * 32767)
            datos.extend(struct.pack("<h", max(-32768, min(32767, val))))

    elif tipo == "puerta":
        muestras = int(frecuencia_muestreo * 0.5)
        for i in range(muestras):
            t = i / frecuencia_muestreo
            env = math.exp(-4.5 * t)
            tono = math.sin(2 * math.pi * 140.0 * t) + math.sin(2 * math.pi * 210.0 * t) * 0.5
            val = int(tono * env * 0.5 * 32767)
            datos.extend(struct.pack("<h", max(-32768, min(32767, val))))

    elif tipo == "latido":
        muestras = int(frecuencia_muestreo * 0.35)
        for i in range(muestras):
            t = i / frecuencia_muestreo
            env = math.exp(-9.0 * t)
            tono = math.sin(2 * math.pi * 52.0 * t)
            val = int(tono * env * 0.75 * 32767)
            datos.extend(struct.pack("<h", max(-32768, min(32767, val))))

    elif tipo == "grito_jumpscare":
        # ALARIDO ENSORDECEDOR: Frecuencias disonantes, choque estridente y sub-bass destructivo
        muestras = int(frecuencia_muestreo * 1.8)
        for i in range(muestras):
            t = i / frecuencia_muestreo
            env = min(1.0, t * 45.0) * max(0.0, 1.0 - (t / 1.8) ** 0.6)
            freq = 1400.0 + 700.0 * math.sin(2 * math.pi * 18.0 * t) + 300.0 * math.sin(2 * math.pi * 38.0 * t)
            tono = math.sin(2 * math.pi * freq * t)
            armonico = 0.55 * math.sin(4 * math.pi * freq * t)
            chillido = 0.4 * math.sin(2 * math.pi * (freq * 2.6) * t)
            ruido = (random.random() * 2.0 - 1.0) * 0.42
            sub_boom = 0.85 * math.sin(2 * math.pi * 56.0 * t) * math.exp(-3.5 * t)
            total = (tono + armonico + chillido + ruido + sub_boom) * env * 0.98
            val = int(max(-1.0, min(1.0, total)) * 32767)
            datos.extend(struct.pack("<h", val))

    elif tipo == "maldicion":
        muestras = int(frecuencia_muestreo * 2.8)
        for i in range(muestras):
            t = i / frecuencia_muestreo
            env = min(1.0, t * 1.2) * max(0.0, 1.0 - (t / 2.8))
            tono = (
                math.sin(2 * math.pi * 65.4 * t) * 0.45
                + math.sin(2 * math.pi * 77.78 * t) * 0.35
                + math.sin(2 * math.pi * 92.5 * t) * 0.25
                + (random.random() * 2.0 - 1.0) * 0.15
            )
            val = int(tono * env * 0.9 * 32767)
            datos.extend(struct.pack("<h", max(-32768, min(32767, val))))

    try:
        return pygame.mixer.Sound(buffer=bytes(datos))
    except Exception:
        return None


# -------------------------------------------------------------
# DETECTIVE HUMANO (VISTA CENITAL REALISTA)
# -------------------------------------------------------------
class DetectiveHumano:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.rect = pygame.Rect(x - 11, y - 11, 22, 22)
        self.velocidad_caminar = 3.3
        self.velocidad_correr = 4.8
        self.angulo = 0.0
        self.linterna_activa = True
        self.radio_linterna = 190
        self.contador_pasos = 0.0
        self.tiempo_movimiento = 0.0

    def mover(self, teclas, muros, snd_paso):
        dx, dy = 0.0, 0.0
        if teclas[pygame.K_w] or teclas[pygame.K_UP]:
            dy -= 1.0
        if teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
            dy += 1.0
        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
            dx -= 1.0
        if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
            dx += 1.0

        corriendo = teclas[pygame.K_LSHIFT] or teclas[pygame.K_RSHIFT]
        velocidad = self.velocidad_correr if corriendo else self.velocidad_caminar

        if dx != 0 and dy != 0:
            dx *= 0.7071
            dy *= 0.7071

        # Resolución de colisión suave eje por eje contra los muros del laberinto
        nuevo_x = self.x + dx * velocidad
        rect_x = pygame.Rect(nuevo_x - 11, self.y - 11, 22, 22)
        if not any(rect_x.colliderect(muro) for muro in muros):
            self.x = nuevo_x

        nuevo_y = self.y + dy * velocidad
        rect_y = pygame.Rect(self.x - 11, nuevo_y - 11, 22, 22)
        if not any(rect_y.colliderect(muro) for muro in muros):
            self.y = nuevo_y

        self.rect.center = (int(self.x), int(self.y))

        # Sonido de pasos con cadencia humana
        if dx != 0 or dy != 0:
            self.tiempo_movimiento += 0.22 if corriendo else 0.14
            self.contador_pasos += 1
            if self.contador_pasos > (14 if corriendo else 22):
                self.contador_pasos = 0
                if snd_paso:
                    snd_paso.play()

    def apuntar(self, pos_mouse):
        rel_x = pos_mouse[0] - self.rect.centerx
        rel_y = pos_mouse[1] - self.rect.centery
        self.angulo = math.atan2(rel_y, rel_x)

    def dibujar(self, superficie):
        cx, cy = self.rect.center
        cos_a = math.cos(self.angulo)
        sin_a = math.sin(self.angulo)

        balanceo = math.sin(self.tiempo_movimiento) * 3
        perp_cos = -sin_a
        perp_sin = cos_a

        # Hombros de la gabardina
        hombro_izq = (cx + perp_cos * 11 - cos_a * 2, cy + perp_sin * 11 - sin_a * 2)
        hombro_der = (cx - perp_cos * 11 - cos_a * 2, cy - perp_sin * 11 - sin_a * 2)

        # Torso gabardina
        pygame.draw.circle(superficie, COLOR_GABARDINA, (cx, cy), 11)
        pygame.draw.line(superficie, (32, 36, 46), hombro_izq, hombro_der, 5)

        # Mano izquierda balanceándose
        m_izq_x = hombro_izq[0] + cos_a * 6 + perp_cos * balanceo
        m_izq_y = hombro_izq[1] + sin_a * 6 + perp_sin * balanceo
        pygame.draw.circle(superficie, COLOR_GABARDINA, (int(m_izq_x), int(m_izq_y)), 3)
        pygame.draw.circle(superficie, COLOR_PIEL, (int(m_izq_x + cos_a * 2), int(m_izq_y + sin_a * 2)), 2)

        # Mano derecha con linterna metálica
        m_der_x = hombro_der[0] + cos_a * 10
        m_der_y = hombro_der[1] + sin_a * 10
        pygame.draw.line(superficie, COLOR_GABARDINA, hombro_der, (m_der_x, m_der_y), 4)
        pygame.draw.circle(superficie, COLOR_PIEL, (int(m_der_x), int(m_der_y)), 3)

        # Linterna
        luz_x = m_der_x + cos_a * 6
        luz_y = m_der_y + sin_a * 6
        pygame.draw.line(superficie, (180, 185, 195), (m_der_x, m_der_y), (luz_x, luz_y), 3)
        color_lente = (255, 245, 180) if self.linterna_activa else (70, 75, 85)
        pygame.draw.circle(superficie, color_lente, (int(luz_x), int(luz_y)), 3)

        # Cabeza y Sombrero Fedora
        cab_x = cx + cos_a * 2
        cab_y = cy + sin_a * 2
        pygame.draw.circle(superficie, COLOR_SOMBRERO, (int(cab_x), int(cab_y)), 8)
        pygame.draw.circle(superficie, (24, 26, 34), (int(cab_x + cos_a * 2), int(cab_y + sin_a * 2)), 5)
        pygame.draw.circle(superficie, COLOR_DORADO_ANTIGUO, (int(cab_x + cos_a * 2), int(cab_y + sin_a * 2)), 5, 1)


# -------------------------------------------------------------
# SOMBRAS ERRANTES PATRULLERAS (JUMPSCARE)
# -------------------------------------------------------------
class SombraErrante:
    def __init__(self, x_inicio, y_inicio, rango, eje="horizontal", velocidad=1.4):
        self.x = float(x_inicio)
        self.y = float(y_inicio)
        self.origen_x = float(x_inicio)
        self.origen_y = float(y_inicio)
        self.rango = rango
        self.eje = eje
        self.velocidad = velocidad
        self.direccion = 1
        self.rect = pygame.Rect(x_inicio - 14, y_inicio - 14, 28, 28)
        self.tiempo = random.random() * 8.0

    def actualizar(self):
        self.tiempo += 0.05
        if self.eje == "horizontal":
            self.x += self.velocidad * self.direccion
            if abs(self.x - self.origen_x) > self.rango:
                self.direccion *= -1
        else:
            self.y += self.velocidad * self.direccion
            if abs(self.y - self.origen_y) > self.rango:
                self.direccion *= -1

        self.rect.center = (int(self.x), int(self.y))

    def dibujar(self, superficie):
        cx, cy = self.rect.center
        desp_x = cx + int(math.sin(self.tiempo * 3.5) * 3)
        desp_y = cy + int(math.cos(self.tiempo * 2.5) * 3)

        pygame.draw.circle(superficie, (20, 4, 8), (desp_x, desp_y), 15)
        pygame.draw.circle(superficie, (65, 8, 14), (desp_x, desp_y), 11)
        # Ojos demoníacos
        pygame.draw.circle(superficie, (255, 30, 40), (desp_x - 4, desp_y - 2), 2)
        pygame.draw.circle(superficie, (255, 30, 40), (desp_x + 4, desp_y - 2), 2)


# -------------------------------------------------------------
# TRAMPAS DE SANGRE MALDITAS
# -------------------------------------------------------------
class TrampaSangre:
    def __init__(self, x, y, radio=18):
        self.x = x
        self.y = y
        self.radio = radio
        self.rect = pygame.Rect(x - radio, y - radio, radio * 2, radio * 2)

    def dibujar(self, sup, tiempo):
        pulso = math.sin(tiempo * 0.08) * 2
        pygame.draw.circle(sup, (90, 10, 16), (self.x, self.y), int(self.radio + pulso), 1)
        pygame.draw.line(sup, (140, 15, 25), (self.x - 7, self.y), (self.x + 7, self.y), 1)
        pygame.draw.line(sup, (140, 15, 25), (self.x, self.y - 7), (self.x, self.y + 7), 1)


# -------------------------------------------------------------
# DEFINICIÓN DE LAS 5 FASES Y SUS LABERINTOS
# -------------------------------------------------------------
DATOS_FASES = [
    {
        "id": 1,
        "nombre": "FASE 1: LA BIBLIOTECA MALDITA",
        "subtitulo": "Laberinto de estanterías de caoba | Halla el Diario de Dimitrio",
        "color_muro": (45, 32, 22),
        "color_borde": (75, 55, 38),
        "color_suelo1": (55, 40, 28),
        "color_suelo2": (42, 30, 20),
        "item_nombre": "Diario Rasgado de Dimitrio",
        "item_icono": "diario",
        "item_lore": (
            "'María ya no esconde su devoción a la Orden del Ocaso. La vi en el sótano\n"
            "con el grimorio prohibido... Me miró con una frialdad glacial y murmuró:\n"
            "Lo siento, Dimitrio, pero la profecía exige la sangre del primogénito.'"
        ),
        "item_desc": "Manuscrito de Dimitrio escrito con tinta temblorosa poco antes de morir.",
        "mapa": [
            "########################",
            "#P...#.........#.......#",
            "#.##.#.#######.#.#####.#",
            "#..#.#.#.....#.#.#...#.#",
            "##.#.###.###.#.#.#.#.#.#",
            "#..#.....#...#.#...#.#.#",
            "#.######.#.###.#####.#.#",
            "#.#....#.#.#.........#.#",
            "#.#.##.#.#.#.#########.#",
            "#...#..#...#.#.........#",
            "#####.######.#.#######.#",
            "#............#.......#E#",
            "#.##################.#.#",
            "########################",
        ],
        "sombras": [(10, 5, 80, "horizontal"), (16, 7, 70, "vertical")],
        "trampas": [(5, 3), (18, 9)],
    },
    {
        "id": 2,
        "nombre": "FASE 2: EL LABORATORIO ALQUÍMICO",
        "subtitulo": "Laberinto de vitrinas y frascos | Halla el Veneno de María",
        "color_muro": (28, 42, 35),
        "color_borde": (48, 70, 58),
        "color_suelo1": (22, 32, 26),
        "color_suelo2": (18, 25, 20),
        "item_nombre": "Frasco de Cicuta con Pañuelo de María",
        "item_icono": "veneno",
        "item_lore": (
            "El informe toxicológico confirma que Dimitrio fue envenenado con esta mezcla.\n"
            "El pañuelo de seda hallado junto al frasco lleva bordada la inicial 'M'\n"
            "y el perfume de lavanda amarga de María Blackwood."
        ),
        "item_desc": "Frasco de cristal sellado con veneno mortal y seda con monograma M.",
        "mapa": [
            "########################",
            "#P...#.....#.......#...#",
            "####.#.###.#.#####.#.#.#",
            "#....#...#.#.#...#...#.#",
            "#.######.#.#.#.#.#####.#",
            "#.#......#.#...#.#.....#",
            "#.#.######.#####.#.###.#",
            "#.#.#..........#.#...#.#",
            "#.#.#.########.#.###.#.#",
            "#...#.#......#.#.#...#.#",
            "#####.#.####.#.#.#.###.#",
            "#.......#....#.......#E#",
            "#.##################.#.#",
            "########################",
        ],
        "sombras": [(6, 3, 90, "horizontal"), (14, 5, 80, "vertical")],
        "trampas": [(4, 9), (18, 7)],
    },
    {
        "id": 3,
        "nombre": "FASE 3: LAS CATACUMBAS SUBTERRÁNEAS",
        "subtitulo": "Laberinto de sarcófagos de piedra | Halla la Daga de María",
        "color_muro": (34, 36, 44),
        "color_borde": (58, 62, 74),
        "color_suelo1": (22, 24, 30),
        "color_suelo2": (17, 18, 24),
        "item_nombre": "Daga Ritual con el Sello de María",
        "item_icono": "daga",
        "item_lore": (
            "Daga de obsidiana con la que apuñalaron en el corazón a Dimitrio.\n"
            "En la empuñadura de oro están grabadas las huellas dactilares de María\n"
            "y su anillo de compromiso ceremonial de la Orden."
        ),
        "item_desc": "Arma homicida manchada de sangre seca con el escudo Blackwood.",
        "mapa": [
            "########################",
            "#P.....#.......#.......#",
            "#.####.#.#####.#.#####.#",
            "#.#....#.#...#.#.#...#.#",
            "#.#.####.#.#.#.#.#.#.#.#",
            "#.#......#.#.#...#.#.#.#",
            "#.########.#.#####.#.#.#",
            "#..........#.#.....#.#.#",
            "#.##########.#.#####.#.#",
            "#.#..........#.#.....#.#",
            "#.#.##########.#.#####.#",
            "#.#............#.....#E#",
            "#.##################.#.#",
            "########################",
        ],
        "sombras": [(8, 7, 100, "horizontal"), (16, 9, 80, "vertical")],
        "trampas": [(3, 5), (14, 3), (20, 9)],
    },
    {
        "id": 4,
        "nombre": "FASE 4: LA CAPILLA PROHIBIDA",
        "subtitulo": "Laberinto de columnas arcanas | Halla el Pergamino de la Profecía",
        "color_muro": (40, 20, 26),
        "color_borde": (70, 35, 45),
        "color_suelo1": (30, 16, 20),
        "color_suelo2": (22, 12, 16),
        "item_nombre": "Pergamino de la Profecía Maldita",
        "item_icono": "pergamino",
        "item_lore": (
            "'El sacrificio de Dimitrio consumará la apertura del Séptimo Sello.\n"
            "Cuando las cuatro ofrendas sean depositadas sobre el altar de piedra,\n"
            "la maldición se despertará y consumirá las almas de los mortales.'"
        ),
        "item_desc": "Papiro milenario firmado con sangre por María para consagrar el pacto.",
        "mapa": [
            "########################",
            "#P.......#.............#",
            "########.#.###########.#",
            "#........#...........#.#",
            "#.##################.#.#",
            "#.#................#.#.#",
            "#.#.##############.#.#.#",
            "#.#.#............#.#.#.#",
            "#.#.#.##########.#.#.#.#",
            "#.#.#.#........#.#.#.#.#",
            "#.#.#.########.#.#.#.#.#",
            "#...#..........#.#...#E#",
            "################.#####.#",
            "########################",
        ],
        "sombras": [(6, 5, 110, "horizontal"), (12, 7, 90, "horizontal"), (18, 9, 70, "vertical")],
        "trampas": [(5, 3), (14, 5), (16, 9)],
    },
    {
        "id": 5,
        "nombre": "FASE FINAL: EL GRAN SALÓN DEL SACRIFICIO",
        "subtitulo": "El Altar de los Cuatro Sellos y el Cadáver de Dimitrio",
        "color_muro": (36, 38, 48),
        "color_borde": (65, 68, 82),
        "color_suelo1": (26, 28, 36),
        "color_suelo2": (20, 22, 28),
        "item_nombre": "Altar Central",
        "item_icono": "altar",
        "item_lore": "",
        "item_desc": "El epicentro del ritual donde yace Dimitrio y aguardan los pedestales.",
        "mapa": [
            "########################",
            "#P.........#...........#",
            "#.########.#.#########.#",
            "#.#........#.........#.#",
            "#.#.######...#######.#.#",
            "#.#.#..............#.#.#",
            "#.#.#.....AAAA.....#.#.#",
            "#.#.#.....AAAA.....#.#.#",
            "#.#.#..............#.#.#",
            "#.#.######...#######.#.#",
            "#.#........#.........#.#",
            "#.########.#.#########.#",
            "#..........#...........#",
            "########################",
        ],
        "sombras": [(5, 5, 80, "vertical"), (18, 5, 80, "vertical")],
        "trampas": [(7, 3), (16, 11)],
    },
]


# -------------------------------------------------------------
# CLASE PRINCIPAL DEL MOTOR DEL JUEGO
# -------------------------------------------------------------
class JuegoLaberintosTerror:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            self.audio_disponible = True
        except Exception:
            self.audio_disponible = False

        self.pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        pygame.display.set_caption("El Eco de la Sombra: La Profecía Carmesí | Las 5 Fases del Horror")
        self.reloj = pygame.time.Clock()

        # Cargar imagen HD para JUMPSCARE si está presente
        ruta_img = os.path.join(os.path.dirname(__file__), "jumpscare.png")
        if os.path.exists(ruta_img):
            try:
                img = pygame.image.load(ruta_img).convert()
                self.img_jumpscare = pygame.transform.scale(img, (ANCHO_VENTANA, ALTO_VENTANA))
            except Exception:
                self.img_jumpscare = None
        else:
            self.img_jumpscare = None

        # Tipografías del sistema
        self.fuente_titular = pygame.font.SysFont("georgia", 26, bold=True)
        self.fuente_subtitular = pygame.font.SysFont("georgia", 18, bold=True)
        self.fuente_texto = pygame.font.SysFont("consolas", 14)
        self.fuente_narrativa = pygame.font.SysFont("georgia", 16)
        self.fuente_alerta = pygame.font.SysFont("impact", 32)
        self.fuente_jumpscare = pygame.font.SysFont("impact", 48)

        # Sonidos procedimentales
        self.snd_paso = generar_sonido_procedimental("paso") if self.audio_disponible else None
        self.snd_item = generar_sonido_procedimental("recolectar") if self.audio_disponible else None
        self.snd_puerta = generar_sonido_procedimental("puerta") if self.audio_disponible else None
        self.snd_latido = generar_sonido_procedimental("latido") if self.audio_disponible else None
        self.snd_grito = generar_sonido_procedimental("grito_jumpscare") if self.audio_disponible else None
        self.snd_maldicion = generar_sonido_procedimental("maldicion") if self.audio_disponible else None

        self.superficie_oscuridad = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA), pygame.SRCALPHA)

        # Partículas de polvo que flotan en la linterna
        self.particulas = [
            {"x": random.randint(20, ANCHO_VENTANA - 20), "y": random.randint(48, ALTO_VENTANA - 20), "v": random.uniform(0.2, 0.5)}
            for _ in range(40)
        ]

        # Reiniciar partida
        self.reiniciar_juego_completo()

    def reiniciar_juego_completo(self):
        self.fase_actual_idx = 0
        self.inventario = []  # Nombres de las evidencias obtenidas
        self.tiempo_juego = 0
        self.estado = "EXPLORANDO"  # EXPLORANDO, MODAL_EVIDENCIA, JUMPSCARE, CLIMAX_FINAL
        self.tiempo_jumpscare = 0
        self.temblor_pantalla = 0
        self.latido_timer = 0
        self.notificacion = "Explora el laberinto y encuentra la evidencia oculta."
        self.notif_timer = 200

        self.cargar_fase(self.fase_actual_idx)

    def cargar_fase(self, idx):
        self.fase_actual_idx = idx
        self.fase_data = DATOS_FASES[idx]
        self.muros = []
        self.pos_jugador_inicio = (60, 68)
        self.pos_evidencia = None
        self.pos_altar = None
        self.evidencia_recogida_en_fase = False
        self.puerta_salida_activa = False

        # Parsear el mapa 24x14
        mapa = self.fase_data["mapa"]
        for fila in range(FILAS_MAPA):
            for col in range(COLUMNAS_MAPA):
                char = mapa[fila][col]
                rx = col * TAM_CASILLA
                ry = DESP_Y_MAPA + fila * TAM_CASILLA
                rect_celda = pygame.Rect(rx, ry, TAM_CASILLA, TAM_CASILLA)

                if char == "#":
                    self.muros.append(rect_celda)
                elif char == "P":
                    self.pos_jugador_inicio = (rx + 20, ry + 20)
                elif char == "E":
                    self.pos_evidencia = (rx + 20, ry + 20)
                    self.rect_evidencia = pygame.Rect(rx + 8, ry + 8, 24, 24)
                elif char == "A":
                    self.pos_altar = (480, DESP_Y_MAPA + 280)
                    self.rect_altar = pygame.Rect(435, DESP_Y_MAPA + 235, 90, 90)

        # Ubicar al detective en el inicio
        self.detective = DetectiveHumano(self.pos_jugador_inicio[0], self.pos_jugador_inicio[1])

        # Crear sombras errantes
        self.sombras = []
        for sx, sy, rango, eje in self.fase_data["sombras"]:
            px = sx * TAM_CASILLA + 20
            py = DESP_Y_MAPA + sy * TAM_CASILLA + 20
            self.sombras.append(SombraErrante(px, py, rango=rango, eje=eje))

        # Crear trampas
        self.trampas = []
        for tx, ty in self.fase_data["trampas"]:
            px = tx * TAM_CASILLA + 20
            py = DESP_Y_MAPA + ty * TAM_CASILLA + 20
            self.trampas.append(TrampaSangre(px, py))

        self.notificacion = f"Entrando a: {self.fase_data['nombre']}. Ten cuidado en la oscuridad."
        self.notif_timer = 200

    def activar_jumpscare(self, motivo):
        if self.estado == "JUMPSCARE":
            return
        self.estado = "JUMPSCARE"
        self.tiempo_jumpscare = 75  # ~1.25 segundos
        self.temblor_pantalla = 45
        if self.snd_grito:
            self.snd_grito.play()
        self.notificacion = f"¡PASO EN FALSO! {motivo}"
        self.notif_timer = 180

    def avanzar_fase(self):
        if self.fase_actual_idx < len(DATOS_FASES) - 1:
            self.fase_actual_idx += 1
            if self.snd_puerta:
                self.snd_puerta.play()
            self.cargar_fase(self.fase_actual_idx)
        else:
            # Clímax
            self.estado = "CLIMAX_FINAL"

    def ejecutar(self):
        ejecutando = True
        while ejecutando:
            self.tiempo_juego += 1

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutando = False

                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        ejecutando = False

                    if evento.key == pygame.K_f and self.estado not in ("JUMPSCARE", "CLIMAX_FINAL"):
                        self.detective.linterna_activa = not self.detective.linterna_activa

                    if evento.key == pygame.K_r:
                        if self.estado in ("CLIMAX_FINAL", "JUMPSCARE"):
                            self.reiniciar_juego_completo()

                    if evento.key in (pygame.K_e, pygame.K_SPACE):
                        if self.estado == "MODAL_EVIDENCIA":
                            self.estado = "EXPLORANDO"
                        elif self.estado == "EXPLORANDO":
                            self.intentar_interaccion()

            self.actualizar()
            self.dibujar()
            self.reloj.tick(FPS)

        pygame.quit()
        sys.exit()

    def intentar_interaccion(self):
        cx, cy = self.detective.rect.center

        # 1. En Fases 1 a 4: Recoger Evidencia o cruzar la puerta
        if self.fase_actual_idx < 4:
            if not self.evidencia_recogida_en_fase and self.pos_evidencia:
                dist = math.hypot(cx - self.pos_evidencia[0], cy - self.pos_evidencia[1])
                if dist < 45:
                    self.evidencia_recogida_en_fase = True
                    self.puerta_salida_activa = True
                    self.inventario.append(self.fase_data["item_nombre"])
                    self.estado = "MODAL_EVIDENCIA"
                    if self.snd_item:
                        self.snd_item.play()
                    self.notificacion = f"¡Evidencia asegurada! Se abrió el pasaje a la siguiente fase."
                    self.notif_timer = 200
                    return

            # Si ya recogió la evidencia y está sobre el punto de salida (la misma casilla de la evidencia o portal)
            if self.puerta_salida_activa and self.pos_evidencia:
                dist_puerta = math.hypot(cx - self.pos_evidencia[0], cy - self.pos_evidencia[1])
                if dist_puerta < 45:
                    self.avanzar_fase()
                    return

        # 2. En Fase 5: Interactuar con el Altar Central
        elif self.fase_actual_idx == 4:
            dist_altar = math.hypot(cx - 480, cy - (DESP_Y_MAPA + 280))
            if dist_altar < 80:
                # Activar Clímax de Resolución y Maldición
                self.estado = "CLIMAX_FINAL"
                self.temblor_pantalla = 60
                if self.snd_maldicion:
                    self.snd_maldicion.play()

    def actualizar(self):
        if self.estado == "EXPLORANDO":
            teclas = pygame.key.get_pressed()
            pos_mouse = pygame.mouse.get_pos()
            self.detective.mover(teclas, self.muros, self.snd_paso)
            self.detective.apuntar(pos_mouse)

            # Sombras errantes
            for s in self.sombras:
                s.actualizar()
                if self.detective.rect.colliderect(s.rect):
                    self.activar_jumpscare("Una aparición espectral te atrapó en el corredor.")
                    # Reposicionar al detective al inicio de la fase
                    self.detective.x = self.pos_jugador_inicio[0]
                    self.detective.y = self.pos_jugador_inicio[1]
                    break

            # Trampas de sangre
            cx, cy = self.detective.rect.center
            for trampa in self.trampas:
                if math.hypot(cx - trampa.x, cy - trampa.y) < trampa.radio:
                    self.activar_jumpscare("Pisaste una runa maldita oculta en el suelo.")
                    self.detective.x = self.pos_jugador_inicio[0]
                    self.detective.y = self.pos_jugador_inicio[1]
                    break

            # Latidos en presencia de peligro o altar
            if self.fase_actual_idx == 4 and math.hypot(cx - 480, cy - 328) < 160:
                self.latido_timer += 1
                if self.latido_timer > 40 and self.snd_latido:
                    self.latido_timer = 0
                    self.snd_latido.play()

            # Partículas flotantes
            for p in self.particulas:
                p["y"] += p["v"]
                if p["y"] > ALTO_VENTANA - 20:
                    p["y"] = DESP_Y_MAPA + 5
                    p["x"] = random.randint(20, ANCHO_VENTANA - 20)

        elif self.estado == "JUMPSCARE":
            self.tiempo_jumpscare -= 1
            if self.tiempo_jumpscare <= 0:
                self.estado = "EXPLORANDO"
                self.temblor_pantalla = 0

        elif self.estado == "CLIMAX_FINAL":
            if self.temblor_pantalla > 0:
                self.temblor_pantalla -= 1

        if self.notif_timer > 0:
            self.notif_timer -= 1

    def dibujar_suelo_y_laberinto(self, sup):
        mapa = self.fase_data["mapa"]
        c_muro = self.fase_data["color_muro"]
        c_borde = self.fase_data["color_borde"]
        c_s1 = self.fase_data["color_suelo1"]
        c_s2 = self.fase_data["color_suelo2"]

        # 1. Dibujar baldosas transitables
        for fila in range(FILAS_MAPA):
            for col in range(COLUMNAS_MAPA):
                rx = col * TAM_CASILLA
                ry = DESP_Y_MAPA + fila * TAM_CASILLA
                color_suelo = c_s1 if (fila + col) % 2 == 0 else c_s2
                pygame.draw.rect(sup, color_suelo, (rx, ry, TAM_CASILLA, TAM_CASILLA))

        # 2. Trampas de sangre
        for trampa in self.trampas:
            trampa.dibujar(sup, self.tiempo_juego)

        # 3. Sombras errantes
        for s in self.sombras:
            s.dibujar(sup)

        # 4. En Fase 5: Dibujar el Altar y el Cadáver de Dimitrio
        if self.fase_actual_idx == 4:
            self.dibujar_escena_crimen_dimitrio(sup)

        # 5. Dibujar Muros del Laberinto con biselado realista
        for muro in self.muros:
            # Sombra de muro
            pygame.draw.rect(sup, (4, 4, 8), muro.move(3, 3))
            pygame.draw.rect(sup, c_muro, muro)
            pygame.draw.line(sup, c_borde, muro.topleft, muro.topright, 2)
            pygame.draw.line(sup, c_borde, muro.topleft, muro.bottomleft, 2)
            pygame.draw.line(sup, (12, 14, 18), muro.bottomleft, muro.bottomright, 2)
            pygame.draw.line(sup, (12, 14, 18), muro.topright, muro.bottomright, 2)

        # 6. Dibujar Evidencia / Portal en Fases 1 a 4
        if self.fase_actual_idx < 4 and self.pos_evidencia:
            ex, ey = self.pos_evidencia
            pulso = math.sin(self.tiempo_juego * 0.08) * 3

            if not self.evidencia_recogida_en_fase:
                # Halo de reliquia
                pygame.draw.circle(sup, COLOR_DORADO_ANTIGUO, (ex, ey), int(16 + pulso), 2)
                # Ícono según la evidencia
                icono = self.fase_data["item_icono"]
                if icono == "diario":
                    pygame.draw.rect(sup, (85, 48, 25), (ex - 8, ey - 8, 16, 16), border_radius=2)
                    pygame.draw.rect(sup, (220, 210, 180), (ex - 6, ey - 6, 12, 12))
                elif icono == "veneno":
                    pygame.draw.rect(sup, (50, 190, 100), (ex - 5, ey - 4, 10, 13), border_radius=2)
                    pygame.draw.rect(sup, (180, 190, 205), (ex - 3, ey - 8, 6, 4))
                elif icono == "daga":
                    pygame.draw.line(sup, (230, 235, 245), (ex, ey - 8), (ex, ey + 6), 3)
                    pygame.draw.line(sup, COLOR_DORADO_ANTIGUO, (ex - 5, ey + 6), (ex + 5, ey + 6), 2)
                elif icono == "pergamino":
                    pygame.draw.rect(sup, (225, 200, 145), (ex - 9, ey - 6, 18, 12), border_radius=3)
                    pygame.draw.circle(sup, (180, 20, 30), (ex, ey), 3)
            else:
                # Portal / Puerta hacia la siguiente fase
                pygame.draw.circle(sup, (60, 140, 230), (ex, ey), int(18 + pulso), 3)
                pygame.draw.circle(sup, (180, 225, 255), (ex, ey), int(10 + pulso * 0.5), 1)

    def dibujar_escena_crimen_dimitrio(self, sup):
        cx, cy = 480, DESP_Y_MAPA + 280

        # Altar Central de los Cuatro Sellos
        radio_altar = 55
        color_runa = COLOR_SANGRE_FRESCA if self.estado == "CLIMAX_FINAL" else COLOR_DORADO_ANTIGUO
        pygame.draw.circle(sup, (22, 24, 32), (cx, cy), radio_altar)
        pygame.draw.circle(sup, color_runa, (cx, cy), radio_altar, 2)
        pygame.draw.circle(sup, color_runa, (cx, cy), radio_altar - 14, 1)

        # 4 pedestales iluminados
        pedestales = [(cx, cy - 38), (cx + 38, cy), (cx, cy + 38), (cx - 38, cy)]
        for px, py in pedestales:
            pygame.draw.circle(sup, COLOR_SANGRE_FRESCA, (px, py), 6)

        # Cadáver detallado de Dimitrio tendido sobre el altar
        pygame.draw.ellipse(sup, COLOR_SANGRE_SECA, (cx - 34, cy - 18, 68, 40))
        pygame.draw.ellipse(sup, COLOR_SANGRE_FRESCA, (cx - 20, cy - 10, 40, 22))
        pygame.draw.ellipse(sup, (210, 215, 225), (cx - 35, cy - 19, 70, 42), 1)

        # Cuerpo
        pygame.draw.ellipse(sup, (215, 215, 220), (cx - 10, cy - 6, 20, 16))
        pygame.draw.circle(sup, COLOR_SANGRE_FRESCA, (cx - 2, cy), 3)
        pygame.draw.circle(sup, COLOR_PIEL_CADAVER, (cx, cy - 12), 6)
        pygame.draw.circle(sup, (40, 25, 18), (cx, cy - 14), 5)

        t_dimitrio = self.fuente_texto.render("CADÁVER DE DIMITRIO", True, (245, 140, 140))
        sup.blit(t_dimitrio, (cx - 75, cy + 38))

    def aplicar_iluminacion_volumetrica(self):
        if self.estado == "CLIMAX_FINAL":
            self.superficie_oscuridad.fill((32, 5, 8, 225))
        else:
            self.superficie_oscuridad.fill((6, 7, 10, 248))

        cx, cy = self.detective.rect.center
        cos_a = math.cos(self.detective.angulo)
        sin_a = math.sin(self.detective.angulo)

        if self.detective.linterna_activa or self.estado == "CLIMAX_FINAL":
            longitud = self.detective.radio_linterna
            apertura = math.radians(38.0)

            p1 = (cx, cy)
            p2 = (cx + int(math.cos(self.detective.angulo - apertura) * longitud), cy + int(math.sin(self.detective.angulo - apertura) * longitud))
            p3 = (cx + int(math.cos(self.detective.angulo + apertura) * longitud), cy + int(math.sin(self.detective.angulo + apertura) * longitud))

            s_luz = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA), pygame.SRCALPHA)
            col_luz = (210, 30, 40) if self.estado == "CLIMAX_FINAL" else (255, 245, 205)

            # Cono de luz
            pygame.draw.polygon(s_luz, (col_luz[0], col_luz[1], col_luz[2], 225), [p1, p2, p3])
            # Halo suave en los pies
            pygame.draw.circle(s_luz, (col_luz[0], col_luz[1], col_luz[2], 185), (cx, cy), 50)

            self.superficie_oscuridad.blit(s_luz, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)

        self.pantalla.blit(self.superficie_oscuridad, (0, 0))

        # Partículas de polvo en la luz
        for p in self.particulas:
            dist = math.hypot(p["x"] - cx, p["y"] - cy)
            if dist < self.detective.radio_linterna:
                alpha = int((1.0 - dist / self.detective.radio_linterna) * 150)
                sp = pygame.Surface((3, 3), pygame.SRCALPHA)
                sp.fill((255, 245, 220, alpha))
                self.pantalla.blit(sp, (p["x"], int(p["y"])))

    def dibujar_hud(self):
        # Barra superior con estilo victoriano
        pygame.draw.rect(self.pantalla, (10, 12, 16), (0, 0, ANCHO_VENTANA, 48))
        pygame.draw.line(self.pantalla, (45, 50, 65), (0, 48), (ANCHO_VENTANA, 48), 2)

        # Nombre de la fase
        txt_fase = self.fuente_subtitular.render(self.fase_data["nombre"], True, COLOR_DORADO_ANTIGUO)
        self.pantalla.blit(txt_fase, (20, 14))

        # Inventario
        iconos = ["📜 Diario", "🧪 Veneno", "🗡️ Daga", "🔮 Pergamino"]
        for i, nombre in enumerate(iconos):
            tenido = i < len(self.inventario)
            col = COLOR_DORADO_ANTIGUO if tenido else (80, 85, 100)
            txt_i = self.fuente_texto.render(f"[{'X' if tenido else ' '}] {nombre}", True, col)
            self.pantalla.blit(txt_i, (340 + i * 125, 16))

        # Linterna
        estado_l = "LINTERNA: ON [F]" if self.detective.linterna_activa else "LINTERNA: OFF [F]"
        t_l = self.fuente_texto.render(estado_l, True, (200, 205, 220))
        self.pantalla.blit(t_l, (ANCHO_VENTANA - 150, 16))

        # Notificación inferior
        if self.notif_timer > 0:
            t_notif = self.fuente_texto.render(f">> {self.notificacion}", True, (245, 230, 160))
            rect_n = t_notif.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA - 18))
            bg_n = rect_n.inflate(26, 10)
            pygame.draw.rect(self.pantalla, (10, 12, 16), bg_n, border_radius=5)
            pygame.draw.rect(self.pantalla, (140, 120, 60), bg_n, 1, border_radius=5)
            self.pantalla.blit(t_notif, rect_n)

        # Prompts flotantes
        cx, cy = self.detective.rect.center
        if self.fase_actual_idx < 4 and self.pos_evidencia:
            dist_e = math.hypot(cx - self.pos_evidencia[0], cy - self.pos_evidencia[1])
            if dist_e < 45:
                if not self.evidencia_recogida_en_fase:
                    t_p = self.fuente_texto.render("[E] Recoger Evidencia", True, (255, 240, 140))
                else:
                    t_p = self.fuente_texto.render("[E] Entrar a la siguiente fase", True, (130, 210, 255))
                self.pantalla.blit(t_p, (cx - 75, cy - 32))

        elif self.fase_actual_idx == 4:
            dist_a = math.hypot(cx - 480, cy - (DESP_Y_MAPA + 280))
            if dist_a < 80:
                t_alt = self.fuente_texto.render("[E] Colocar Evidencias en el Altar", True, COLOR_SANGRE_FRESCA)
                self.pantalla.blit(t_alt, (cx - 110, cy - 32))

    def dibujar_modal_evidencia(self):
        overlay = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA), pygame.SRCALPHA)
        overlay.fill((5, 5, 8, 220))
        self.pantalla.blit(overlay, (0, 0))

        ancho, alto = 700, 350
        tx = (ANCHO_VENTANA - ancho) // 2
        ty = (ALTO_VENTANA - alto) // 2

        pygame.draw.rect(self.pantalla, (18, 20, 26), (tx, ty, ancho, alto), border_radius=10)
        pygame.draw.rect(self.pantalla, COLOR_DORADO_ANTIGUO, (tx, ty, ancho, alto), 2, border_radius=10)

        t_tit = self.fuente_titular.render(self.fase_data["item_nombre"], True, COLOR_DORADO_ANTIGUO)
        t_sub = self.fuente_subtitular.render(f"Fase Completada: {self.fase_data['nombre']}", True, (140, 185, 235))
        self.pantalla.blit(t_tit, (tx + 30, ty + 24))
        self.pantalla.blit(t_sub, (tx + 30, ty + 62))

        pygame.draw.line(self.pantalla, (60, 65, 80), (tx + 30, ty + 95), (tx + ancho - 30, ty + 95), 1)

        t_desc = self.fuente_texto.render(f"Descripción: {self.fase_data['item_desc']}", True, (160, 165, 180))
        self.pantalla.blit(t_desc, (tx + 30, ty + 112))

        t_rev = self.fuente_subtitular.render("Informe / Revelación de la Evidencia:", True, (240, 220, 180))
        self.pantalla.blit(t_rev, (tx + 30, ty + 150))

        for idx, lin in enumerate(self.fase_data["item_lore"].split("\n")):
            t_l = self.fuente_narrativa.render(lin, True, (240, 240, 245))
            self.pantalla.blit(t_l, (tx + 30, ty + 185 + idx * 26))

        t_btn = self.fuente_texto.render("[Presiona E o ESPACIO para guardar e iluminar el pasaje de salida]", True, (255, 230, 120))
        self.pantalla.blit(t_btn, (tx + 80, ty + alto - 38))

    def dibujar_jumpscare(self):
        shake_x = random.randint(-18, 18)
        shake_y = random.randint(-18, 18)

        if self.img_jumpscare:
            escala = 1.05 + 0.05 * math.sin(self.tiempo_juego * 1.5)
            w_zoom = int(ANCHO_VENTANA * escala)
            h_zoom = int(ALTO_VENTANA * escala)
            img_z = pygame.transform.scale(self.img_jumpscare, (w_zoom, h_zoom))
            dx = (w_zoom - ANCHO_VENTANA) // 2
            dy = (h_zoom - ALTO_VENTANA) // 2
            self.pantalla.blit(img_z, (shake_x - dx, shake_y - dy))
        else:
            self.pantalla.fill((20, 2, 5))
            cx, cy = ANCHO_VENTANA // 2 + shake_x, ALTO_VENTANA // 2 + shake_y
            pygame.draw.ellipse(self.pantalla, (200, 205, 215), (cx - 160, cy - 210, 320, 420))
            pygame.draw.ellipse(self.pantalla, (0, 0, 0), (cx - 100, cy - 90, 70, 90))
            pygame.draw.ellipse(self.pantalla, (0, 0, 0), (cx + 30, cy - 90, 70, 90))
            pygame.draw.circle(self.pantalla, (255, 0, 0), (cx - 65, cy - 45), 6)
            pygame.draw.circle(self.pantalla, (255, 0, 0), (cx + 65, cy - 45), 6)
            pygame.draw.ellipse(self.pantalla, (0, 0, 0), (cx - 60, cy + 30, 120, 150))

        if random.random() < 0.4:
            velo = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA), pygame.SRCALPHA)
            velo.fill((255, 10, 20, 95))
            self.pantalla.blit(velo, (0, 0))

        t_espanto = self.fuente_jumpscare.render("¡EL MAL TE HA ALCANZADO!", True, (255, 235, 100))
        self.pantalla.blit(t_espanto, t_espanto.get_rect(center=(ANCHO_VENTANA // 2 + shake_x, ALTO_VENTANA - 60 + shake_y)))

    def dibujar_climax(self):
        overlay = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA), pygame.SRCALPHA)
        overlay.fill((25, 4, 8, 240))
        self.pantalla.blit(overlay, (0, 0))

        pygame.draw.rect(self.pantalla, COLOR_SANGRE_FRESCA, (40, 30, ANCHO_VENTANA - 80, ALTO_VENTANA - 60), 3, border_radius=10)

        # 1. RESOLUCIÓN DEL ASESINATO: MARÍA
        t1 = self.fuente_alerta.render("¡EL ASESINATO DE DIMITRIO HA SIDO RESUELTO!", True, (255, 235, 120))
        self.pantalla.blit(t1, t1.get_rect(center=(ANCHO_VENTANA // 2, 70)))

        t_culpable = self.fuente_subtitular.render(
            "LA ASESINA FUE: MARÍA BLACKWOOD (Hermana y Consejera)",
            True,
            (255, 130, 130),
        )
        self.pantalla.blit(t_culpable, t_culpable.get_rect(center=(ANCHO_VENTANA // 2, 115)))

        t_exp = self.fuente_narrativa.render(
            "Las 4 pistas coinciden: María envenenó a Dimitrio con la Cicuta y le atravesó el corazón con la Daga.",
            True,
            (240, 240, 245),
        )
        self.pantalla.blit(t_exp, t_exp.get_rect(center=(ANCHO_VENTANA // 2, 150)))

        pygame.draw.line(self.pantalla, (130, 20, 30), (80, 185), (ANCHO_VENTANA - 80, 185), 2)

        # 2. LA PROFECÍA DE LA MALDICIÓN
        t_profecia = self.fuente_alerta.render("PERO EL ASESINATO ERA SOLO LA PROFECÍA DEL SACRIFICIO...", True, COLOR_SANGRE_FRESCA)
        self.pantalla.blit(t_profecia, t_profecia.get_rect(center=(ANCHO_VENTANA // 2, 225)))

        lore = [
            "María no mató a Dimitrio por codicia terrenal ni rencores familiares.",
            "Dimitrio era el primogénito exigido por la Profecía Maldita de 1692.",
            "",
            "Al recorrer los cuatro laberintos y depositar las ofrendas en el altar,",
            "¡TÚ HAS QUEBRADO EL ÚLTIMO SELLO Y COMPLETADO LA MALDICIÓN!",
            "",
            "La entidad de las sombras reclama ahora el alma del detective que completó el ritual.",
        ]

        for i, parrafo in enumerate(lore):
            col_l = (255, 220, 220) if "COMPLETADO" not in parrafo else (255, 70, 80)
            txt_p = self.fuente_narrativa.render(parrafo, True, col_l)
            self.pantalla.blit(txt_p, txt_p.get_rect(center=(ANCHO_VENTANA // 2, 270 + i * 26)))

        t_opc = self.fuente_subtitular.render("[R] Jugar de Nuevo desde la Fase 1       [ESC] Salir del Juego", True, COLOR_DORADO_ANTIGUO)
        self.pantalla.blit(t_opc, t_opc.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA - 65)))

    def dibujar(self):
        desp_x = random.randint(-4, 4) if self.temblor_pantalla > 0 else 0
        desp_y = random.randint(-4, 4) if self.temblor_pantalla > 0 else 0

        sup_base = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA))
        self.dibujar_suelo_y_laberinto(sup_base)
        self.detective.dibujar(sup_base)

        self.pantalla.blit(sup_base, (desp_x, desp_y))
        self.aplicar_iluminacion_volumetrica()
        self.dibujar_hud()

        if self.estado == "MODAL_EVIDENCIA":
            self.dibujar_modal_evidencia()
        elif self.estado == "JUMPSCARE":
            self.dibujar_jumpscare()
        elif self.estado == "CLIMAX_FINAL":
            self.dibujar_climax()

        pygame.display.flip()


# -------------------------------------------------------------
# PUNTO DE ENTRADA
# -------------------------------------------------------------
if __name__ == "__main__":
    juego = JuegoLaberintosTerror()
    juego.ejecutar()
