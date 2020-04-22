import time
import os
import numpy as np
import pygame

# Colocamos la ventana del juego en la mitad de la pantalla.
os.environ["SDL_VIDEO_CENTERED"] = "1"

# Título de la ventana.
pygame.display.set_caption("Juego de la vida")

# Dirección del icono del juego.
iconPath = "./icon.ico"
# Si el icono existe:
if os.path.exists(iconPath):
    # Carga el icono de la ventana
    icon = pygame.image.load(iconPath)
    # Establece el icono de la ventana
    pygame.display.set_icon(icon)

# Inicializa la libreria "pygame".
pygame.init()

# Ancho y alto de la ventana de juego.
width, height = 700, 700
# Coloca el juego al ancho y alto establecidos.
screen = pygame.display.set_mode((height, width))

# Color dle fondo.
bg = 25, 25, 25
# Rllena el fondo con el color establecido.
screen.fill(bg)

# Número de filas y columnas.
nxC, nyC = 60, 60

# Calcula la dimension de ancho y alto.
dimCW = width / nxC
dimCH = height / nyC

# Inicializa el tablero a celdas vacias.
gameState = np.zeros((nxC, nyC))

# Ejemplo de autómata "Palo".
# gameState[5, 3] = 1
# gameState[5, 4] = 1
# gameState[5, 5] = 1

# Ejemplo de autómata "Móvil".
gameState[21, 21] = 1
gameState[22, 22] = 1
gameState[22, 23] = 1
gameState[21, 23] = 1
gameState[20, 23] = 1

# Control de pausa/reanudación del juego.
pauseExec = False

# Controla la finalización del juego:
endGame = False

iteration = 0

# Mientras el juego no termine:
while not endGame:

    # Hacemos una copia del estado del juego.
    newGameState = np.copy(gameState)

    # Vuelvo a colorear la pantalla con el color de fondo para resetear la malla.
    screen.fill(bg)

    # Añadimos un pequeño tiempo de espera que alivia a la CPU.
    time.sleep(0.1)

    # Inicializamos la población a 0.
    population = 0

    # Registro de eventos de teclado y mouse
    ev = pygame.event.get()

    # Para todos los eventos registrados.
    for event in ev:

        # Cerrar la ventana finaliza el juego.
        if event.type == pygame.QUIT:
            endGame = True
            break

        # Si se aprieta alguna tecla:
        if event.type == pygame.KEYDOWN:

            # ESC finaliza el juego.
            if event.key == pygame.K_ESCAPE:
                endGame = True
                break

            # Tecla "r" reinicia el tablero.
            if event.key == pygame.K_r:
                # Coloca la iteración a 0
                iteration = 0
                # Reinicia celdas a 0.
                gameState = np.zeros((nxC, nyC))
                newGameState = np.copy(gameState)
                # Pausa la ejecución para dibujar.
                pauseExec = True

            else:
                # Cualquier otra tecla pausa/reanuda el juego.
                pauseExec = not pauseExec

        # Registramos el evento del ratón pulsado.
        mouseClick = pygame.mouse.get_pressed()

        # Si se aprieta algún botón del ratón.
        if sum(mouseClick) > 0:
            # Botón del medio pausa/reanuda ejecución.
            if mouseClick[1]:
                pauseExec = not pauseExec

            # Los otros botones
            else:
                # Pausan la ejecución para poder dibujar.
                if pauseExec == False:
                    pauseExec = True

                # Se calcula la posición en la que está el ratón.
                posX, posY = pygame.mouse.get_pos()

                # Se transforma esa posición en las celdas.
                celX, celY = int(np.floor(posX / dimCW)
                                 ), int(np.floor(posY / dimCH))

                # Click Izquierdo dibuja.
                if mouseClick[0]:
                    newGameState[celX, celY] = 1

                # Click derecho borra.
                elif mouseClick[2]:
                    newGameState[celX, celY] = 0

    # Si la ejecución no está pausada.
    if not pauseExec:
        # Incremento el contador de generaciones
        iteration += 1

    # Para todas las filas.
    for y in range(0, nyC):

        # Para todas las columnas.
        for x in range(0, nxC):

            # Si el juego no está pausado.
            if not pauseExec:
                # Calculamos el número de vecinos de la celda.
                n_neigh = (
                    gameState[(x - 1) % nxC, (y - 1) % nyC]
                    + gameState[x % nxC, (y - 1) % nyC]
                    + gameState[(x + 1) % nxC, (y - 1) % nyC]
                    + gameState[(x - 1) % nxC, y % nyC]
                    + gameState[(x + 1) % nxC, y % nyC]
                    + gameState[(x - 1) % nxC, (y + 1) % nyC]
                    + gameState[x % nxC, (y + 1) % nyC]
                    + gameState[(x + 1) % nxC, (y + 1) % nyC]
                )

                # Si la celda está "muerta"  y tiene exáctamente 3 vecinos -> "Muere".
                if gameState[x, y] == 0 and n_neigh == 3:
                    newGameState[x, y] = 1
                # Si la celda está "viva" y tiene menos de dos o más de 3 vecinos -> "Vive".
                elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGameState[x, y] = 0

            # Si la celda está llena, la sumamos a la población total.
            if gameState[x, y] == 1:
                population += 1

            # Poligono de 4 lados para el dibujo.
            poly = [
                (int(x * dimCW), int(y * dimCH)),
                (int((x + 1) * dimCW), int(y * dimCH)),
                (int((x + 1) * dimCW), int((y + 1) * dimCH)),
                (int(x * dimCW), int((y + 1) * dimCH)),
            ]

            # Si la celda está vacia:
            if newGameState[x, y] == 0:
                # Pintamos los bordes de gris.
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)

            else:
                if pauseExec:
                    # Si el juego está pausado, pintamos las celdas de gris.
                    pygame.draw.polygon(screen, (128, 128, 128), poly, 0)
                else:
                    # Pintamos las celdas de blanco.
                    pygame.draw.polygon(screen, (255, 255, 255), poly, 0)

    # Actualizamos la población y las generaciones en el título.
    title = f"Juego de la vida - Población: {population} - Generación: {iteration}"

    # Si la ventana está pausada cambiamos, lo indicamos en el título.
    if pauseExec:
        title += " - [PAUSADO]"

    # Actualizamos el título de la ventana.
    pygame.display.set_caption(title)

    # Devolvemos la copia modificada al original.
    gameState = np.copy(newGameState)

    # ACtualizamos la pantalla.
    pygame.display.flip()

# Juego termina.
print("Quiting game...")
