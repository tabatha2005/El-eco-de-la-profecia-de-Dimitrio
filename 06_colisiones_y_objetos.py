"""
06_colisiones_y_objetos.py
--------------------------
Colisiones, Proximidad y Sistema de Inventario:
- Detección de colisiones mediante rectángulos (pygame.Rect.colliderect).
- Verificación de distancia euclidiana para interacción por proximidad.
- Gestión de estado: recolección de evidencias y almacenamiento en inventario.
- Visualización de interfaz gráfica de usuario (HUD) para objetos recolectados.
"""

import math
import sys
import pygame


def main():
    pygame.init()
    pygame.font.init()

    ANCHO, ALTO = 800, 600
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("06 - Colisiones e Inventario de Evidencias | Tutorial Pygame")

    reloj = pygame.time.Clock()
    fuente = pygame.font.SysFont("consolas", 16)
    fuente_hud = pygame.font.SysFont("georgia", 18, bold=True)

    # Jugador
    jugador_rect = pygame.Rect(100, 100, 32, 32)
    velocidad = 4.5

    # Lista de artículos/evidencias en el mapa
    # Cada evidencia tiene rect, nombre, color y estado (recolectado o no)
    evidencias = [
        {"rect": pygame.Rect(450, 150, 26, 26), "nombre": "Nota Sospechosa", "color": (230, 220, 140), "recogido": False},
        {"rect": pygame.Rect(650, 380, 26, 26), "nombre": "Frasco de Veneno", "color": (60, 200, 120), "recogido": False},
        {"rect": pygame.Rect(200, 420, 26, 26), "nombre": "Llave Oxidada", "color": (210, 160, 80), "recogido": False},
    ]

    inventario = []
    mensaje_notificacion = "Usa WASD para moverte y acércate a los objetos."

    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT or (
                evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE
            ):
                ejecutando = False

            # Interacción con la tecla 'E'
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_e:
                for item in evidencias:
                    if not item["recogido"]:
                        # Comprobar cercanía por distancia entre centros
                        dist = math.hypot(
                            jugador_rect.centerx - item["rect"].centerx,
                            jugador_rect.centery - item["rect"].centery,
                        )
                        if dist < 55:
                            item["recogido"] = True
                            inventario.append(item["nombre"])
                            mensaje_notificacion = f"¡Evidencia recolectada: {item['nombre']}!"

        # Movimiento del jugador
        teclas = pygame.key.get_pressed()
        dx, dy = 0, 0
        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
            dx -= 1
        if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
            dx += 1
        if teclas[pygame.K_w] or teclas[pygame.K_UP]:
            dy -= 1
        if teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
            dy += 1

        if dx != 0 and dy != 0:
            dx *= 0.7071
            dy *= 0.7071

        jugador_rect.x += int(dx * velocidad)
        jugador_rect.y += int(dy * velocidad)

        # Restringir bordes
        jugador_rect.clamp_ip(pantalla.get_rect())

        # --- DIBUJADO ---
        pantalla.fill((22, 24, 32))

        # Dibujar evidencias en el mapa
        item_cercano = None
        for item in evidencias:
            if not item["recogido"]:
                pygame.draw.rect(pantalla, item["color"], item["rect"], border_radius=4)
                pygame.draw.rect(pantalla, (255, 255, 255), item["rect"], 1, border_radius=4)

                # Calcular proximidad
                dist = math.hypot(
                    jugador_rect.centerx - item["rect"].centerx,
                    jugador_rect.centery - item["rect"].centery,
                )
                if dist < 55:
                    item_cercano = item

        # Dibujar al jugador
        pygame.draw.rect(pantalla, (50, 140, 240), jugador_rect, border_radius=6)
        pygame.draw.circle(pantalla, (255, 255, 255), jugador_rect.center, 4)

        # Mensaje flotante si está cerca de un objeto
        if item_cercano:
            txt_accion = fuente.render(f"[E] Recoger {item_cercano['nombre']}", True, (255, 240, 150))
            pantalla.blit(txt_accion, (jugador_rect.centerx - 80, jugador_rect.top - 25))

        # --- PANEL HUD SUPERIOR ---
        pygame.draw.rect(pantalla, (14, 16, 22), (0, 0, ANCHO, 65))
        pygame.draw.line(pantalla, (60, 65, 80), (0, 65), (ANCHO, 65), 2)

        txt_inv = fuente_hud.render(f"INVENTARIO ({len(inventario)}/3):", True, (220, 200, 160))
        pantalla.blit(txt_inv, (20, 12))

        if inventario:
            txt_items = fuente.render(" | ".join(inventario), True, (130, 210, 255))
            pantalla.blit(txt_items, (230, 14))
        else:
            txt_vacio = fuente.render("(vacío)", True, (120, 120, 130))
            pantalla.blit(txt_vacio, (230, 14))

        txt_notif = fuente.render(f"> {mensaje_notificacion}", True, (200, 210, 225))
        pantalla.blit(txt_notif, (20, 38))

        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
