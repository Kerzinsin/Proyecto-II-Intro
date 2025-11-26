#Enemigo

import random
from terreno import Camino, Liana

class Enemigo:
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna

    def obtener_posicion(self):
        return self.fila, self.columna

    def puede_moverse(self, mapa, nueva_fila, nueva_columna):
        if 0 <= nueva_fila < mapa.filas and 0 <= nueva_columna < mapa.columnas:
            casilla_destino = mapa.matriz[nueva_fila][nueva_columna]
            return casilla_destino.puede_pasar_enemigo()
        return False

    def mover_hacia(self, jugador, mapa):
        jf, jc = jugador.obtener_posicion()
        df = jf - self.fila
        dc = jc - self.columna

        if abs(df) > abs(dc):
            paso = (1 if df > 0 else -1, 0)
        else:
            paso = (0, 1 if dc > 0 else -1)

        nueva_fila = self.fila + paso[0]
        nueva_columna = self.columna + paso[1]

        if self.puede_moverse(mapa, nueva_fila, nueva_columna):
            self.fila = nueva_fila
            self.columna = nueva_columna
