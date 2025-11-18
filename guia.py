import pygame
import sys

pygame.init()

ANCHO = 800
ALTURA = 600

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
VERDE = (0, 255, 0)
FUKSIA =  (255, 84, 175)

pantalla = pygame.display.set_mode((ANCHO, ALTURA))
pygame.display.set_caption("Guía del Juego - Pinky la Serpiente")

fondo = pygame.image.load("data/imagen/fondo_start.png").convert()
fondo = pygame.transform.scale(fondo, (ANCHO, ALTURA))

fuente_titulo = pygame.font.SysFont("Arial", 60)
fuente_texto = pygame.font.SysFont("Arial", 30)


def mostrar_guia():
    """Muestra una pantalla de instrucciones antes del juego."""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:   # Enter → iniciar juego
                    return
                if event.key == pygame.K_q:        # Q → salir
                    pygame.quit()
                    sys.exit()

        pantalla.blit(fondo, (0, 0))

        # Nombre del juego
        nombre_juego = fuente_titulo.render("Pinky la Serpiente", True, FUKSIA)
        rect_nombre = nombre_juego.get_rect(center=(ANCHO // 2, 60))
        pantalla.blit(nombre_juego, rect_nombre)
        
        # Título
        titulo = fuente_titulo.render("¿Cómo jugar?", True, NEGRO)
        rect_titulo = titulo.get_rect(center=(ANCHO // 2, 120))
        pantalla.blit(titulo, rect_titulo)

        # Instrucciones
        instrucciones = [
            "Usa las flechas del teclado para mover la serpiente:",
            "  ↑  Arriba",
            "  ↓  Abajo",
            "  ←  Izquierda",
            "  →  Derecha",
            "",
            "Objetivo: Come las manzanas para sumar puntos.",
            "Pierdes si tocas una pared o tu propio cuerpo.",
            "",
            "Presiona ENTER para comenzar.",
            "Presiona Q para salir."
        ]

        y = 220
        for linea in instrucciones:
            texto = fuente_texto.render(linea, True, NEGRO)
            rect_texto = texto.get_rect(center=(ANCHO // 2, y))
            pantalla.blit(texto, rect_texto)
            y += 40

        pygame.display.update()


# Ejecutar guía automáticamente si se abre este archivo directamente
if __name__ == "__main__":
    mostrar_guia()