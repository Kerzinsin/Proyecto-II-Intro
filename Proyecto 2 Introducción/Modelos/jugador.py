#Jugador

import time
from Modelos.terreno import Tunel

class Jugador:
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna
        self.energia = 100
        self.puede_correr = True
        self.en_tunel = False
        self.tiempo_en_tunel = None

    def obtener_posicion(self):
        return self.fila, self.columna

    def puede_moverse(self, mapa, nueva_fila, nueva_columna):
        if 0 <= nueva_fila < mapa.filas and 0 <= nueva_columna < mapa.columnas:
            casilla_destino = mapa.matriz[nueva_fila][nueva_columna]
            return casilla_destino.puede_pasar_jugador()
        return False

    def mover(self, direccion, mapa):
        movimientos = {
            "arriba": (-1, 0),
            "abajo": (1, 0),
            "izquierda": (0, -1),
            "derecha": (0, 1)
        }

        if direccion in movimientos:
            df, dc = movimientos[direccion]
            nueva_fila = self.fila + df
            nueva_columna = self.columna + dc

            if self.puede_moverse(mapa, nueva_fila, nueva_columna):
                self.fila = nueva_fila
                self.columna = nueva_columna

                casilla = mapa.matriz[nueva_fila][nueva_columna]
                self._gestionar_energia(casilla)
                return True
        return False

    def correr(self, mapa):
        if not self.puede_correr or self.energia < 100:
            print("No tienes energía para correr.")
            return False

        self.energia = 0
        self.puede_correr = False
        print("Corriendo durante 0.5 segundos...")

        time.sleep(0.5)
        return True

    def _gestionar_energia(self, casilla_actual):
        if isinstance(casilla_actual, Tunel):
            if not self.en_tunel:
                self.en_tunel = True
                self.tiempo_en_tunel = time.time()
            else:
                if time.time() - self.tiempo_en_tunel >= 1:
                    self.energia = 100
                    self.puede_correr = True
                    print("Has recuperado energía completamente.")
        else:
            self.en_tunel = False
            self.tiempo_en_tunel = None
