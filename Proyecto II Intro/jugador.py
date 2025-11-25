from terreno import Camino, Tunel

class Jugador:
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna
        self.energia = 100
        self.trampas_disponibles = 3

    def obtener_posicion(self):
        """Devuelve la posición actual del jugador."""
        return self.fila, self.columna

    def puede_moverse(self, mapa, nueva_fila, nueva_columna):
        """Verifica si el jugador puede moverse a la nueva casilla."""
        if 0 <= nueva_fila < mapa.filas and 0 <= nueva_columna < mapa.columnas:
            casilla_destino = mapa.matriz[nueva_fila][nueva_columna]
            return casilla_destino.puede_pasar_jugador()
        return False

    def mover(self, direccion, mapa):
        """Intenta mover al jugador en una dirección dada."""
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
                print(f"Jugador se movió a {self.obtener_posicion()}")
                return True
            else:
                print("Movimiento bloqueado por terreno")
        return False

    def gastar_energia(self, cantidad):
        """Disminuye la energía del jugador si es posible."""
        if self.energia - cantidad >= 0:
            self.energia -= cantidad
            return True
        return False
