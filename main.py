# CREADO POR: ELIAS NUÑEZ, YURIANGEL PEREZ
# COMISION 1

# ============================
#   CONSIGNAS
# ============================

#Juego final debe tener
# un paisaje de fondo
# 1 jugador
# 1 objeto que interactue con el jugador
#3 eventos ( que se mueva o salte )
# colision

# ============================
#   JUEGO DE SERPIENTE
# ============================

import pygame
import sys
import random
import guia

pygame.init()
pygame.mixer.init()  # INICIALIZAR SONIDO

# --- Configuración del Juego ---
ANCHO = 800
ALTURA = 600
TAMAÑO_BLOQUE = 40
VELOCIDAD_JUEGO = 8

# --- Colores ---
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
BLANCO = (255, 255, 255)
ROSA = (255, 192, 203)

# Pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTURA))
pygame.display.set_caption("Serpiente con Sprites")

clock = pygame.time.Clock()
fuente_game_over = pygame.font.SysFont('Arial', 70)
fuente_mensaje = pygame.font.SysFont('Arial', 30)
fuente_puntuacion = pygame.font.SysFont('Arial', 20)

# ============================
#   CARGA DE FONDO
# ============================

fondo = pygame.image.load("data/imagen/fondo.png").convert()
fondo = pygame.transform.scale(fondo, (ANCHO, ALTURA))

# ============================
#   SONIDOS
# ============================

sonido_gameover = pygame.mixer.Sound("data/sonido/gameover.mp3")
sonido_start = pygame.mixer.Sound("data/sonido/startgame.mp3")
sonido_manzana = pygame.mixer.Sound("data/sonido/recogermanzana.mp3")

pygame.mixer.music.load("data/sonido/musicafondo.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)    # Música de fondo infinita

# Estado inicial
pos_serpiente = [100, 50]
cuerpo_serpiente = [[100, 50], [60, 50], [20, 50]]
direccion = "RIGHT"
prox_direccion = "RIGHT"
game_over = False
puntuacion = 0
pos_manzana = [0, 0]

# ============================
#   CARGA DE IMÁGENES
# ============================

# Cabeza
imagen_cabeza = pygame.image.load("data/imagen/cabezasnike.png").convert_alpha()
imagen_cabeza = pygame.transform.scale(imagen_cabeza, (TAMAÑO_BLOQUE, TAMAÑO_BLOQUE))

# Cuerpo
imagen_cuerpo = pygame.image.load("data/imagen/cuerposnike.png").convert_alpha()
imagen_cuerpo = pygame.transform.scale(imagen_cuerpo, (TAMAÑO_BLOQUE, TAMAÑO_BLOQUE))

# Manzana
manzana_base = pygame.image.load("data/imagen/manzana.png").convert_alpha()
manzana_base = pygame.transform.scale(manzana_base, (TAMAÑO_BLOQUE, TAMAÑO_BLOQUE))

brillo_escala = 1.0
creciendo = True

# ============================
#   FUNCIONES
# ============================

def generar_manzana(serpiente_cuerpo):
    global pos_manzana
    grid_x = ANCHO // TAMAÑO_BLOQUE
    grid_y = ALTURA // TAMAÑO_BLOQUE

    while True:
        x = random.randrange(0, grid_x) * TAMAÑO_BLOQUE
        y = random.randrange(0, grid_y) * TAMAÑO_BLOQUE
        if [x, y] not in serpiente_cuerpo:
            pos_manzana = [x, y]
            break

generar_manzana(cuerpo_serpiente)

def mostrar_game_over():
    pantalla.blit(fuente_game_over.render("GAME OVER", True, ROJO),
                  (ANCHO // 2 - 200, ALTURA // 2 - 100))

    pantalla.blit(fuente_mensaje.render(f"Puntuación: {puntuacion}", True, BLANCO),
                  (ANCHO // 2 - 120, ALTURA // 2))

    pantalla.blit(fuente_mensaje.render("R para Reiniciar | Q para Salir", True, BLANCO),
                  (ANCHO // 2 - 200, ALTURA // 2 + 50))

    pygame.display.update()

def reiniciar_juego():
    global pos_serpiente, cuerpo_serpiente, direccion, prox_direccion, game_over, puntuacion
    pos_serpiente = [100, 50]
    cuerpo_serpiente = [[100, 50], [60, 50], [20, 50]]
    direccion = "RIGHT"
    prox_direccion = "RIGHT"
    puntuacion = 0
    game_over = False
    generar_manzana(cuerpo_serpiente)
    
    # Volver a activar música al reiniciar
    pygame.mixer.music.load("data/sonido/musicafondo.mp3")
    pygame.mixer.music.play(-1)

def mostrar_puntuacion():
    pantalla.blit(fuente_puntuacion.render(f"Puntuación: {puntuacion}", True, NEGRO), (10, 10))

def rotar_sprite(sprite, dir):
    if dir == "UP":
        return pygame.transform.rotate(sprite, 0)
    elif dir == "RIGHT":
        return pygame.transform.rotate(sprite, -90)
    elif dir == "DOWN":
        return pygame.transform.rotate(sprite, 180)
    elif dir == "LEFT":
        return pygame.transform.rotate(sprite, 90)
    return sprite

# ============================
#   MOSTRAR GUÍA
# ============================

guia.mostrar_guia()
sonido_start.play()

# ============================
#   BUCLE PRINCIPAL
# ============================

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reiniciar_juego()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direccion != "DOWN":
                    prox_direccion = "UP"
                elif event.key == pygame.K_DOWN and direccion != "UP":
                    prox_direccion = "DOWN"
                elif event.key == pygame.K_LEFT and direccion != "RIGHT":
                    prox_direccion = "LEFT"
                elif event.key == pygame.K_RIGHT and direccion != "LEFT":
                    prox_direccion = "RIGHT"

    if not game_over:

        direccion = prox_direccion

        # Movimiento
        if direccion == "UP":
            pos_serpiente[1] -= TAMAÑO_BLOQUE
        elif direccion == "DOWN":
            pos_serpiente[1] += TAMAÑO_BLOQUE
        elif direccion == "LEFT":
            pos_serpiente[0] -= TAMAÑO_BLOQUE
        elif direccion == "RIGHT":
            pos_serpiente[0] += TAMAÑO_BLOQUE

        pos_serpiente[0] = (pos_serpiente[0] // TAMAÑO_BLOQUE) * TAMAÑO_BLOQUE
        pos_serpiente[1] = (pos_serpiente[1] // TAMAÑO_BLOQUE) * TAMAÑO_BLOQUE

        cuerpo_serpiente.insert(0, list(pos_serpiente))

        # Comer manzana
        if pos_serpiente == pos_manzana:
            puntuacion += 10
            generar_manzana(cuerpo_serpiente)
            sonido_manzana.play()   # sonido al comer

        else:
            cuerpo_serpiente.pop()

        # Colisiones
        if (pos_serpiente[0] < 0 or pos_serpiente[0] >= ANCHO or
                pos_serpiente[1] < 0 or pos_serpiente[1] >= ALTURA):
            game_over = True
            pygame.mixer.music.stop()   # ← DETENER MÚSICA
            sonido_gameover.play()


        for parte in cuerpo_serpiente[1:]:
            if pos_serpiente == parte:
                game_over = True
                pygame.mixer.music.stop()   # ← DETENER MÚSICA
                sonido_gameover.play()
                break


        # Dibujar fondo
        pantalla.blit(fondo, (0, 0))

        # Manzana animada
        if creciendo:
            brillo_escala += 0.01
            if brillo_escala >= 1.15:
                creciendo = False
        else:
            brillo_escala -= 0.01
            if brillo_escala <= 1.00:
                creciendo = True

        tamaño_anim = int(TAMAÑO_BLOQUE * brillo_escala)
        manzana_animada = pygame.transform.scale(manzana_base, (tamaño_anim, tamaño_anim))
        offset = (tamaño_anim - TAMAÑO_BLOQUE) // 2
        pantalla.blit(manzana_animada, (pos_manzana[0] - offset, pos_manzana[1] - offset))

        # Serpiente con sprites
        for i, (x, y) in enumerate(cuerpo_serpiente):
            if i == 0:
                sprite = rotar_sprite(imagen_cabeza, direccion)
            else:
                sprite = imagen_cuerpo

            pantalla.blit(sprite, (x, y))

        mostrar_puntuacion()
        pygame.display.update()

    else:
        mostrar_game_over()

    clock.tick(VELOCIDAD_JUEGO)
