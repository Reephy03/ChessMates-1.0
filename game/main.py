import pygame
from clases import Tablero, Pieza
from graficos import dibujar_tablero, dibujar_piezas, cargar_imagenes, mostrar_mensaje

# Inicializa Pygame
pygame.init()

# Constantes
ANCHO, ALTO = 600, 600
DIMENSIONES = 8
TAMANO_CELDA = ANCHO // DIMENSIONES
FPS = 30

# Crear la ventana
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("ChessMates")

def main():
    reloj = pygame.time.Clock()
    tablero = Tablero()
    imagenes = cargar_imagenes(TAMANO_CELDA)
    activo = True

    pieza_seleccionada = None
    inicio = None

    while activo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                activo = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                fila = pos[1] // TAMANO_CELDA
                columna = pos[0] // TAMANO_CELDA
                seleccion_actual = (fila, columna)

                if pieza_seleccionada:
                    if tablero.mover_pieza(inicio, seleccion_actual):
                        tablero.cambiar_turno()
                        if tablero.jaque_mate(tablero.turno_actual):
                            mostrar_mensaje(VENTANA, "Jaque Mate! Ganador: " + ("Negro" if tablero.turno_actual == "Blanco" else "Blanco"), TAMANO_CELDA)
                            pygame.display.flip()  # Actualiza la pantalla para mostrar el mensaje
                            pygame.time.wait(3000)  # Espera 3 segundos para que el mensaje sea visible
                            activo = False
                        elif tablero.esta_en_jaque(tablero.turno_actual):
                            mostrar_mensaje(VENTANA, "¡Cuidado! Tu rey está en jaque.", TAMANO_CELDA)
                    pieza_seleccionada = None
                    inicio = None
                else:
                    if tablero.tablero[fila][columna] != "  " and isinstance(tablero.tablero[fila][columna], Pieza):
                        if tablero.tablero[fila][columna].color == tablero.turno_actual:
                            pieza_seleccionada = tablero.tablero[fila][columna]
                            inicio = seleccion_actual
                        else:
                            mostrar_mensaje(VENTANA, "No es tu turno.", TAMANO_CELDA)
                    else:
                        mostrar_mensaje(VENTANA, "No hay pieza en la posición seleccionada.", TAMANO_CELDA)

        # Obtener la posición de la pieza que está en jaque
        posicion_jaque = tablero.obtener_pieza_jaque(tablero.turno_actual) if tablero.esta_en_jaque(tablero.turno_actual) else None

        dibujar_tablero(VENTANA, TAMANO_CELDA, seleccionada=inicio, en_jaque=posicion_jaque)
        dibujar_piezas(VENTANA, tablero, imagenes, seleccionada=inicio, en_jaque=posicion_jaque)
        pygame.display.flip()
        reloj.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
