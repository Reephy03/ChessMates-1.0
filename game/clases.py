import pygame


class Pieza:
    def __init__(self, color, nombre):
        self.color = color
        self.nombre = nombre

    def movimientos_validos(self, posicion, tablero):
        movimientos = []
        return movimientos

    def __str__(self):
        return f"{self.color}{self.nombre}"


class Peon(Pieza):
    def __init__(self, color):
        super().__init__(color, "peon")

    def movimientos_validos(self, posicion, tablero):
        movimientos = []
        fila, columna = posicion
        direccion = -1 if self.color == "negro" else 1
        fila_inicio = 6 if self.color == "negro" else 1

        # Avance simple y doble
        if 0 <= fila + direccion < 8:
            if tablero.tablero[fila + direccion][columna] == "  ":
                movimientos.append((fila + direccion, columna))
                if fila == fila_inicio and tablero.tablero[fila + 2 * direccion][columna] == "  ":
                    movimientos.append((fila + 2 * direccion, columna))

        # Captura en diagonal
        for desplazamiento in [-1, 1]:
            col_diagonal = columna + desplazamiento
            if 0 <= col_diagonal < 8:
                if 0 <= fila + direccion < 8:
                    casilla_objetivo = tablero.tablero[fila + direccion][col_diagonal]
                    if isinstance(casilla_objetivo, Pieza) and casilla_objetivo.color != self.color:
                        movimientos.append((fila + direccion, col_diagonal))

        # En passant
        if fila == (4 if self.color == "blanco" else 3):  # Solo en la fila específica para cada color
            for desplazamiento in [-1, 1]:
                col_en_passant = columna + desplazamiento
                if 0 <= col_en_passant < 8:
                    en_passant_pieza = tablero.tablero[fila][col_en_passant]
                    if (isinstance(en_passant_pieza, Peon) and en_passant_pieza.color != self.color and
                            tablero.ultimo_movimiento == (
                                    (fila + 2 * direccion, col_en_passant), (fila, col_en_passant))):
                        movimientos.append((fila + direccion, col_en_passant))

        return movimientos


class Torre(Pieza):
    def __init__(self, color):
        super().__init__(color, "torre")
        self.ha_movido = False

    def movimientos_validos(self, posicion, tablero):
        movimientos = []
        fila, columna = posicion
        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Vertical y horizontal

        for df, dc in direcciones:
            f, c = fila, columna
            while True:
                f += df
                c += dc
                if 0 <= f < 8 and 0 <= c < 8:
                    casilla_objetivo = tablero.tablero[f][c]
                    if casilla_objetivo == "  ":
                        movimientos.append((f, c))
                    elif isinstance(casilla_objetivo, Pieza) and casilla_objetivo.color != self.color:
                        movimientos.append((f, c))
                        break
                    else:
                        break
                else:
                    break

        return movimientos


class Caballo(Pieza):
    def __init__(self, color):
        super().__init__(color, "caballo")

    def movimientos_validos(self, posicion, tablero):
        movimientos = []
        fila, columna = posicion
        desplazamientos = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]

        for df, dc in desplazamientos:
            f, c = fila + df, columna + dc
            if 0 <= f < 8 and 0 <= c < 8:
                casilla_objetivo = tablero.tablero[f][c]
                if casilla_objetivo == "  " or (isinstance(casilla_objetivo, Pieza) and casilla_objetivo.color != self.color):
                    movimientos.append((f, c))

        return movimientos


class Alfil(Pieza):
    def __init__(self, color):
        super().__init__(color, "alfil")

    def movimientos_validos(self, posicion, tablero):
        movimientos = []
        fila, columna = posicion
        direcciones = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for df, dc in direcciones:
            f, c = fila, columna
            while True:
                f += df
                c += dc
                if 0 <= f < 8 and 0 <= c < 8:
                    casilla_objetivo = tablero.tablero[f][c]
                    if casilla_objetivo == "  ":
                        movimientos.append((f, c))
                    elif isinstance(casilla_objetivo, Pieza) and casilla_objetivo.color != self.color:
                        movimientos.append((f, c))
                        break
                    else:
                        break
                else:
                    break

        return movimientos


class Rey(Pieza):
    def __init__(self, color):
        super().__init__(color, "rey")
        self.ha_movido = False

    def movimientos_validos(self, posicion, tablero):
        movimientos = []
        fila, columna = posicion
        desplazamientos = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        for df, dc in desplazamientos:
            f, c = fila + df, columna + dc
            if 0 <= f < 8 and 0 <= c < 8:
                casilla_objetivo = tablero.tablero[f][c]
                if casilla_objetivo == "  " or (isinstance(casilla_objetivo, Pieza) and casilla_objetivo.color != self.color):
                    movimientos.append((f, c))

        return movimientos


class Reina(Pieza):
    def __init__(self, color):
        super().__init__(color, "reina")

    def movimientos_validos(self, posicion, tablero):
        movimientos = []
        fila, columna = posicion
        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for df, dc in direcciones:
            f, c = fila, columna
            while True:
                f += df
                c += dc
                if 0 <= f < 8 and 0 <= c < 8:
                    casilla_objetivo = tablero.tablero[f][c]
                    if casilla_objetivo == "  ":
                        movimientos.append((f, c))
                    elif isinstance(casilla_objetivo, Pieza) and casilla_objetivo.color != self.color:
                        movimientos.append((f, c))
                        break
                    else:
                        break
                else:
                    break

        return movimientos


class Tablero:
    def __init__(self):
        self.tablero = [["  " for _ in range(8)] for _ in range(8)]
        self.inicializar_piezas()
        self.turno_actual = "blanco"
        self.ultimo_movimiento = None
        self.posicion_pieza_jaque = None
        
    def cambiar_turno(self):
        self.turno_actual = "negro" if self.turno_actual == "blanco" else "blanco"
        print(f"Turno del jugador {self.turno_actual}")

    def inicializar_piezas(self):
        self.tablero[0][0] = Torre("blanco")
        self.tablero[0][7] = Torre("blanco")
        self.tablero[0][1] = Caballo("blanco")
        self.tablero[0][2] = Alfil("blanco")
        self.tablero[0][3] = Reina("blanco")
        self.tablero[0][4] = Rey("blanco")
        self.tablero[0][5] = Alfil("blanco")
        self.tablero[0][6] = Caballo("blanco")
        self.tablero[7][0] = Torre("negro")
        self.tablero[7][7] = Torre("negro")
        self.tablero[7][1] = Caballo("negro")
        self.tablero[7][2] = Alfil("negro")
        self.tablero[7][3] = Reina("negro")
        self.tablero[7][4] = Rey("negro")
        self.tablero[7][5] = Alfil("negro")
        self.tablero[7][6] = Caballo("negro")

        for i in range(8):
            self.tablero[1][i] = Peon("blanco")
            self.tablero[6][i] = Peon("negro")

    def validar_pieza_seleccionada(self, inicio):
        pieza = self.tablero[inicio[0]][inicio[1]]
        if not pieza or not isinstance(pieza, Pieza):  # Verificar que selecciono una pieza
            from graficos import mostrar_mensaje
            ventana = pygame.display.get_surface()
            tamano_celda = ventana.get_width() // 8
            mostrar_mensaje(ventana, "No has seleccionado ninguna pieza.", tamano_celda)
            return False

        if pieza.color != self.turno_actual:  # Verificar que es el turno correcto
            from graficos import mostrar_mensaje
            ventana = pygame.display.get_surface()
            tamano_celda = ventana.get_width() // 8
            mostrar_mensaje(ventana, "No es tu turno.", tamano_celda)
            return False

        return True

    def es_movimiento_valido(self, inicio, fin):
        pieza = self.tablero[inicio[0]][inicio[1]]

        if not self.validar_pieza_seleccionada(inicio):  # Verificar si selecciono una pieza correcta
            return False

        movimientos = pieza.movimientos_validos(inicio, self)
        if fin in movimientos:
            return True
        return False

    def mover_pieza(self, inicio, fin):
        pieza = self.tablero[inicio[0]][inicio[1]]

        if not isinstance(pieza, Pieza):
            print("No hay pieza en la posición inicial.")
            from graficos import mostrar_mensaje
            ventana = pygame.display.get_surface()
            tamano_celda = ventana.get_width() // 8
            mostrar_mensaje(ventana, "No hay pieza en la posición inicial.", tamano_celda)
            return False

        if pieza.color != self.turno_actual:
            print("No es tu turno.")
            from graficos import mostrar_mensaje
            ventana = pygame.display.get_surface()
            tamano_celda = ventana.get_width() // 8
            mostrar_mensaje(ventana, "No es tu turno.", tamano_celda)
            return False

        if isinstance(pieza, Pieza):
            print(f"Intentando mover {pieza.nombre} {pieza.color} de {inicio} a {fin}")

        if not self.es_movimiento_valido(inicio, fin):
            from graficos import mostrar_mensaje
            ventana = pygame.display.get_surface()
            tamano_celda = ventana.get_width() // 8
            mostrar_mensaje(ventana, "Movimiento no válido, intenta de nuevo.", tamano_celda)
            return False

        # Simular el movimiento
        pieza_destino_original = self.tablero[fin[0]][fin[1]]
        self.tablero[fin[0]][fin[1]] = pieza
        self.tablero[inicio[0]][inicio[1]] = "  "

        # Verificar si el rey queda en jaque después del movimiento
        if self.esta_en_jaque(pieza.color):
            # Revertir el movimiento si deja al rey en jaque
            self.tablero[inicio[0]][inicio[1]] = pieza
            self.tablero[fin[0]][fin[1]] = pieza_destino_original
            from graficos import mostrar_mensaje
            ventana = pygame.display.get_surface()
            tamano_celda = ventana.get_width() // 8
            mostrar_mensaje(ventana, "No puedes realizar ese movimiento, tu rey estaría en jaque.", tamano_celda)
            return False
        else:
            self.ultimo_movimiento = (inicio, fin)
            # Verificar si es un movimiento en passant y eliminar el peón capturado
            if isinstance(pieza, Peon) and abs(inicio[1] - fin[1]) == 1 and pieza_destino_original == "  ":
                self.tablero[inicio[0]][fin[1]] = "  "  # Eliminar el peón capturado en passant

            if isinstance(pieza, Peon) and (fin[0] == 0 or fin[0] == 7):
                self.promocion_peon(fin)

            # Actualizar la pieza que está haciendo jaque
            self.posicion_pieza_jaque = self.obtener_pieza_jaque(self.turno_actual)
            return True

    def obtener_pieza_jaque(self, color):
        pos_rey = None
        for f in range(8):
            for c in range(8):
                pieza = self.tablero[f][c]
                if isinstance(pieza, Rey) and pieza.color == color:
                    pos_rey = (f, c)
                    break
            if pos_rey:
                break  # Salir del bucle una vez encontrado el rey

        color_oponente = "blanco" if color == "negro" else "negro"
        for f in range(8):
            for c in range(8):
                pieza = self.tablero[f][c]
                if isinstance(pieza, Pieza) and pieza.color == color_oponente:
                    if pos_rey in pieza.movimientos_validos((f, c), self):
                        return (f, c)
        return None

    def es_enroque_valido(self, inicio, fin):
        pieza = self.tablero[inicio[0]][inicio[1]]

        # Verificar si la pieza es un rey y si no se ha movido
        if not isinstance(pieza, Rey) or pieza.ha_movido:
            return False

        # Dirección del enroque (1 para enroque corto, -1 para enroque largo)
        direccion = 1 if fin[1] > inicio[1] else -1

        # Verificar que el espacio entre el rey y la torre está libre
        for i in range(1, 3 if direccion == 1 else 4):
            if self.tablero[inicio[0]][inicio[1] + i * direccion] != "  ":
                return False

        # Verificar que la torre en la esquina correspondiente no se ha movido
        torre_pos = 7 if direccion == 1 else 0
        torre = self.tablero[inicio[0]][torre_pos]
        if not isinstance(torre, Torre) or torre.ha_movido:
            return False

        for i in range(0, 3):
            casilla_rey = (inicio[0], inicio[1] + i * direccion)
            if self.esta_en_jaque_en_posicion(casilla_rey, pieza.color):
                return False

        return True

    def esta_en_jaque(self, color):
        pos_rey = None
        for f in range(8):
            for c in range(8):
                pieza = self.tablero[f][c]
                if isinstance(pieza, Rey) and pieza.color == color:
                    pos_rey = (f, c)
                    break
            if pos_rey:
                break  # Salir del bucle una vez encontrado el rey

        if not pos_rey:
            return False  # No se encontró el rey, no debería suceder

        color_oponente = "blanco" if color == "negro" else "negro"
        for f in range(8):
            for c in range(8):
                pieza = self.tablero[f][c]
                if isinstance(pieza, Pieza) and pieza.color == color_oponente:
                    if pos_rey in pieza.movimientos_validos((f, c), self):
                        return True
        return False

    def esta_en_jaque_en_posicion(self, posicion, color):
        color_oponente = "blanco" if color == "negro" else "negro"
        for f in range(8):
            for c in range(8):
                pieza = self.tablero[f][c]
                if isinstance(pieza, Pieza) and pieza.color == color_oponente:
                    if posicion in pieza.movimientos_validos((f, c), self):
                        return True
        return False

    def realizar_enroque(self, inicio, fin):
        direccion = 1 if fin[1] > inicio[1] else -1
        fila_rey = inicio[0]

        # Mover el rey
        self.tablero[fila_rey][fin[1]] = self.tablero[fila_rey][inicio[1]]
        self.tablero[fila_rey][inicio[1]] = "  "

        # Mover la torre
        col_torre_origen = 7 if direccion == 1 else 0
        col_torre_destino = fin[1] - direccion

        self.tablero[fila_rey][col_torre_destino] = self.tablero[fila_rey][col_torre_origen]
        self.tablero[fila_rey][col_torre_origen] = "  "

        self.cambiar_turno()

    def promocion_peon(self, posicion):
        color_peon = self.tablero[posicion[0]][posicion[1]].color
        from graficos import dibujar_menu_promocion, obtener_eleccion_promocion

        ventana = pygame.display.get_surface()
        tamano_celda = ventana.get_width() // 8

        dibujar_menu_promocion(ventana, color_peon, tamano_celda)
        nueva_pieza = obtener_eleccion_promocion(ventana, tamano_celda)

        if nueva_pieza:
            if nueva_pieza == 'Reina':
                self.tablero[posicion[0]][posicion[1]] = Reina(color_peon)
            elif nueva_pieza == 'Torre':
                self.tablero[posicion[0]][posicion[1]] = Torre(color_peon)
            elif nueva_pieza == 'Alfil':
                self.tablero[posicion[0]][posicion[1]] = Alfil(color_peon)
            elif nueva_pieza == 'Caballo':
                self.tablero[posicion[0]][posicion[1]] = Caballo(color_peon)
            print(f"Peón promocionado a {self.tablero[posicion[0]][posicion[1]]}")

    def jaque_mate(self, color):
        if not self.esta_en_jaque(color):
            return False
        for f in range(8):
            for c in range(8):
                pieza = self.tablero[f][c]
                if isinstance(pieza, Pieza) and pieza.color == color:  # Verifica si es una instancia de Pieza
                    pos_inicial = (f, c)
                    movimientos_validos = pieza.movimientos_validos(pos_inicial, self)
                    for mov in movimientos_validos:
                        pieza_destino_original = self.tablero[mov[0]][mov[1]]
                        self.tablero[mov[0]][mov[1]] = pieza
                        self.tablero[f][c] = "  "
                        sigue_en_jaque = self.esta_en_jaque(color)
                        # Revertir el movimiento
                        self.tablero[f][c] = pieza
                        self.tablero[mov[0]][mov[1]] = pieza_destino_original
                        if not sigue_en_jaque:
                            return False
        return True
