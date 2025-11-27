#Enemigo

import random
import threading
from Modelos.terreno import Camino, Liana

class Enemigo:
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna
        self.activo = True

    def obtener_posicion(self):
        return self.fila, self.columna

    def puede_moverse(self, mapa, nueva_fila, nueva_columna):
        if 0 <= nueva_fila < mapa.filas and 0 <= nueva_columna < mapa.columnas:
            casilla_destino = mapa.matriz[nueva_fila][nueva_columna]
            return casilla_destino.puede_pasar_enemigo()
        return False

    def mover_aleatorio(self, mapa):
        """El enemigo se mueve constantemente si hay casillas válidas."""
        direcciones = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(direcciones)  # Para variar el movimiento

        for df, dc in direcciones:
            nueva_fila = self.fila + df
            nueva_columna = self.columna + dc
            if self.puede_moverse(mapa, nueva_fila, nueva_columna):
                self.fila = nueva_fila
                self.columna = nueva_columna
                break

    def iniciar_movimiento(self, mapa):
        """El enemigo se mueve constantemente."""
        def movimiento_continuo():
            while self.activo:
                self.mover_aleatorio(mapa)

        hilo = threading.Thread(target=movimiento_continuo, daemon=True)
        hilo.start()
