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

# =================================
#   JUEGO DE PINKY LA  SERPIENTE :3
# =================================

import pygame
import sys
import random
import guia

pygame.init() # INICIALIZAR PYGAME
pygame.mixer.init()  # INICIALIZAR SONIDO

# Configuración del Juego
ANCHO = 800 # ancho de la ventana
ALTURA = 600 # altura de la ventana
TAMAÑO_BLOQUE = 40 # tamaño de cada bloque de la serpiente y manzana
VELOCIDAD_JUEGO = 6 # velocidad del juego (mayor es más rápido)

# Colores
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
BLANCO = (255, 255, 255)
ROSA = (255, 192, 203)

# Pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTURA)) # crear ventana
pygame.display.set_caption("Pinky la Serpiente") # título de la ventana

clock = pygame.time.Clock() # reloj para controlar FPS
fuente_game_over = pygame.font.SysFont('Arial', 70) # fuente para "Game Over"
fuente_mensaje = pygame.font.SysFont('Arial', 30) # fuente para mensajes
fuente_puntuacion = pygame.font.SysFont('Arial', 20) # fuente para puntuación

# ============================
#   CARGA DE FONDO
# ============================

fondo = pygame.image.load("data/imagen/fondo.png").convert() # cargar imagen de fondo
fondo = pygame.transform.scale(fondo, (ANCHO, ALTURA)) # escalar al tamaño de la ventana

# ============================
#   SONIDOS
# ============================

sonido_gameover = pygame.mixer.Sound("data/sonido/gameover.mp3") # cargar sonido de gameover
sonido_start = pygame.mixer.Sound("data/sonido/startgame.mp3") # cargar sonido de inicio
sonido_manzana = pygame.mixer.Sound("data/sonido/recogermanzana.mp3") # cargar sonido al comer manzana
sonido_explosion = pygame.mixer.Sound("data/sonido/explosion.mp3") # cargar sonido de explosión

pygame.mixer.music.load("data/sonido/musicafondo.mp3") # cargar música de fondo
pygame.mixer.music.set_volume(0.3) # volumen de la música
pygame.mixer.music.play(-1)    # Música de fondo infinita 

# Estado inicial
posicion_serpiente = [100, 50] #
cuerpo_serpiente = [[100, 50], [60, 50], [20, 50]]
direccion = "RIGHT"
prox_direccion = "RIGHT"
game_over = False
puntuacion = 0
posicion_manzana = [0, 0]
bombas = []
ultima_bomba = 0 # contador para controlar generación de bombas
# ============================
#   CARGA DE IMÁGENES
# ============================

# Cabeza
imagen_cabeza = pygame.image.load("data/imagen/cabezasnike.png").convert_alpha() # cargar imagen de la cabeza
imagen_cabeza = pygame.transform.scale(imagen_cabeza, (TAMAÑO_BLOQUE, TAMAÑO_BLOQUE)) # escalar al tamaño del bloque

# Cuerpo
imagen_cuerpo = pygame.image.load("data/imagen/cuerposnike.png").convert_alpha() # cargar imagen del cuerpo
imagen_cuerpo = pygame.transform.scale(imagen_cuerpo, (TAMAÑO_BLOQUE, TAMAÑO_BLOQUE)) # escalar al tamaño del bloque

# Bomba
imagen_bomba = pygame.image.load("data/imagen/bomba.png").convert_alpha() # cargar imagen de la bomba
imagen_bomba = pygame.transform.scale(imagen_bomba, (TAMAÑO_BLOQUE, TAMAÑO_BLOQUE)) # escalar al tamaño del bloque

# Manzana
manzana_base = pygame.image.load("data/imagen/manzana.png").convert_alpha() # cargar imagen de la manzana
manzana_base = pygame.transform.scale(manzana_base, (TAMAÑO_BLOQUE, TAMAÑO_BLOQUE)) # escalar al tamaño del bloque

brillo_escala = 1.0 # escala inicial para animación de la manzana
creciendo = True

# ============================
#   FUNCIONES
# ============================

def generar_manzana(serpiente_cuerpo, bombas): # Genera una posición para la manzana
    global posicion_manzana
    grid_x = ANCHO // TAMAÑO_BLOQUE
    grid_y = ALTURA // TAMAÑO_BLOQUE

    while True:
        x = random.randrange(0, grid_x) * TAMAÑO_BLOQUE # posición x aleatoria en la cuadrícula
        y = random.randrange(0, grid_y) * TAMAÑO_BLOQUE # posición y aleatoria en la cuadrícula
        if [x, y] not in serpiente_cuerpo and [x, y] not in bombas: # evitar que la manzana aparezca sobre la serpiente y bombas
            posicion_manzana = [x, y] # asignar posición de la manzana
            break

generar_manzana(cuerpo_serpiente, bombas) # generar la primera manzana

def generar_bomba(serpiente_cuerpo, posicion_manzana):
    global bombas
    grid_x = ANCHO // TAMAÑO_BLOQUE
    grid_y = ALTURA // TAMAÑO_BLOQUE

    while True:
        x = random.randrange(0, grid_x) * TAMAÑO_BLOQUE
        y = random.randrange(0, grid_y) * TAMAÑO_BLOQUE
        if [x, y] not in serpiente_cuerpo and [x, y] != posicion_manzana:
            bombas.append([x, y])
            break

if puntuacion % 50 == 0:
    generar_bomba(cuerpo_serpiente, posicion_manzana) # generar la bomba

# Variables para animación de la bomba
brillo_bomba = 1.0
creciendo_bomba = True




def mostrar_game_over(): # Muestra la pantalla de Game Over
    pantalla.blit(fuente_game_over.render("GAME OVER", True, ROJO), # texto de Game Over
                  (ANCHO // 2 - 200, ALTURA // 2 - 100)) # posición centrada

    pantalla.blit(fuente_mensaje.render(f"Puntuación: {puntuacion}", True, BLANCO), # mostrar puntuación final
                  (ANCHO // 2 - 120, ALTURA // 2)) # posición centrada

    pantalla.blit(fuente_mensaje.render("R para Reiniciar | Q para Salir", True, BLANCO), # instrucciones para reiniciar o salir 
                  (ANCHO // 2 - 200, ALTURA // 2 + 50)) # posición centrada

    pygame.display.update() # actualizar pantalla

def reiniciar_juego(): # Reinicia el estado del juego
    global posicion_serpiente, cuerpo_serpiente, direccion, prox_direccion, game_over, puntuacion, bombas, ultima_bomba # reiniciar variables globales
    posicion_serpiente = [100, 50] # posición inicial de la serpiente
    cuerpo_serpiente = [[100, 50], [60, 50], [20, 50]]
    direccion = "RIGHT"
    prox_direccion = "RIGHT"
    puntuacion = 0
    game_over = False
    bombas = []
    ultima_bomba = 0
    generar_manzana(cuerpo_serpiente, bombas) # generar nueva manzana
    generar_bomba(cuerpo_serpiente, posicion_manzana) # generar nueva bomba
    
    # Volver a activar música al reiniciar
    pygame.mixer.music.load("data/sonido/musicafondo.mp3")
    pygame.mixer.music.play(-1)

def mostrar_puntuacion(): # Muestra la puntuación en la pantalla
    pantalla.blit(fuente_puntuacion.render(f"Puntuación: {puntuacion}", True, NEGRO), (10, 10)) 

def rotar_sprite(sprite, dir):  # rota la imagen de la serpiente
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
    for event in pygame.event.get(): # espera que se ejecute un evento
        if event.type == pygame.QUIT: # Si el evento es cerrar la ventana
            pygame.quit() # cierra pygame
            sys.exit() # termina el programa

        if game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Presionando R: reiniciar juego
                    reiniciar_juego()
                elif event.key == pygame.K_q: # Presionando Q: salir del juego
                    pygame.quit()
                    sys.exit()

        else:
            if event.type == pygame.KEYDOWN: # Si se presiona una tecla
                if event.key == pygame.K_UP and direccion != "DOWN": # Flecha Arriba
                    prox_direccion = "UP"
                elif event.key == pygame.K_DOWN and direccion != "UP": # Flecha Abajo
                    prox_direccion = "DOWN"
                elif event.key == pygame.K_LEFT and direccion != "RIGHT": # Flecha Izquierda
                    prox_direccion = "LEFT"
                elif event.key == pygame.K_RIGHT and direccion != "LEFT": # Flecha Derecha
                    prox_direccion = "RIGHT"

    if not game_over:

        direccion = prox_direccion # actualizar dirección

        # Movimiento
        if direccion == "UP":
            posicion_serpiente[1] -= TAMAÑO_BLOQUE # mover hacia arriba
        elif direccion == "DOWN":
            posicion_serpiente[1] += TAMAÑO_BLOQUE # mover hacia abajo
        elif direccion == "LEFT":
            posicion_serpiente[0] -= TAMAÑO_BLOQUE # mover hacia izquierda
        elif direccion == "RIGHT":
            posicion_serpiente[0] += TAMAÑO_BLOQUE # mover hacia derecha

        posicion_serpiente[0] = (posicion_serpiente[0] // TAMAÑO_BLOQUE) * TAMAÑO_BLOQUE # ajustar a la cuadrícula
        posicion_serpiente[1] = (posicion_serpiente[1] // TAMAÑO_BLOQUE) * TAMAÑO_BLOQUE # ajustar a la cuadrícula

        cuerpo_serpiente.insert(0, list(posicion_serpiente)) # agregar nueva posición al cuerpo

        # Comer manzana
        if posicion_serpiente == posicion_manzana: # si la serpiente colisiona con la manzana
            puntuacion += 10 # aumentar puntuación
            generar_manzana(cuerpo_serpiente, bombas) # generar nueva manzana
            sonido_manzana.play()   # sonido al comer

        else:
            cuerpo_serpiente.pop() # Si no se comió manzana, elimina la última parte del cuerpo para mantener la longitud.

        if puntuacion // 50 > ultima_bomba:
            generar_bomba(cuerpo_serpiente, posicion_manzana)
            ultima_bomba += 1

        
        # --- Colisiones ---
        
        # colisión con paredes
        if (posicion_serpiente[0] < 0 or posicion_serpiente[0] >= ANCHO or 
                posicion_serpiente[1] < 0 or posicion_serpiente[1] >= ALTURA): # fuera de los límites
            game_over = True
            pygame.mixer.music.stop()   # DETENER MÚSICA
            sonido_gameover.play()  # reproducir sonido de gameover

        # colisión con el cuerpo
        for parte in cuerpo_serpiente[1:]: 
            if posicion_serpiente == parte: # colisión detectada
                game_over = True # marcar como game over
                pygame.mixer.music.stop()   # DETENER MÚSICA
                sonido_gameover.play() # reproducir sonido de gameover
                break # salir del bucle
        
        # Colisión con bomba
        for b in bombas:
            if posicion_serpiente == b: # si la serpiente colisiona con una bomba
                game_over = True
                pygame.mixer.music.stop()   # DETENER MÚSICA
                sonido_explosion.play() # reproducir sonido de explosión


        # Dibujar fondo
        pantalla.blit(fondo, (0, 0))

        # Manzana animada
        if creciendo: # aumentar tamaño
            brillo_escala += 0.01  
            if brillo_escala >= 1.15:
                creciendo = False # cambiar dirección
        else:
            brillo_escala -= 0.01 
            if brillo_escala <= 1.00:
                creciendo = True # cambiar dirección

        tamaño_anim = int(TAMAÑO_BLOQUE * brillo_escala) # tamaño animado
        manzana_animada = pygame.transform.scale(manzana_base, (tamaño_anim, tamaño_anim))
        ajuste_posicion = (tamaño_anim - TAMAÑO_BLOQUE) // 2 # centrar la manzana animada
        pantalla.blit(manzana_animada, (posicion_manzana[0] - ajuste_posicion, posicion_manzana[1] - ajuste_posicion)) # dibujar manzana

        # Dibujar todas las bombas
        for b in bombas:
            if creciendo_bomba:
                brillo_bomba += 0.01
                if brillo_bomba >= 1.2:
                    creciendo_bomba = False
            else:
                brillo_bomba -= 0.01
                if brillo_bomba <= 1.0:
                    creciendo_bomba = True

            tamaño_bomba_anim = int(TAMAÑO_BLOQUE * brillo_bomba)
            bomba_animada = pygame.transform.scale(imagen_bomba, (tamaño_bomba_anim, tamaño_bomba_anim))
            ajuste_bomba = (tamaño_bomba_anim - TAMAÑO_BLOQUE) // 2
            pantalla.blit(bomba_animada, (b[0] - ajuste_bomba, b[1] - ajuste_bomba))


        
        # Dibujar serpiente
        for i, (x, y) in enumerate(cuerpo_serpiente): # dibujar cada parte del cuerpo
            if i == 0:
                sprite = rotar_sprite(imagen_cabeza, direccion) # cabeza
            else:
                sprite = imagen_cuerpo # cuerpo

            pantalla.blit(sprite, (x, y))

        mostrar_puntuacion() # mostrar puntuación
        pygame.display.update() # actualizar pantalla

    else:
        mostrar_game_over() # mostrar pantalla de game over

    clock.tick(VELOCIDAD_JUEGO) # controlar velocidad del juego
