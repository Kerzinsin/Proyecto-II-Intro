#Mapa

import random
from terreno import Camino, Muro, Tunel, Liana

class Mapa:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.matriz = []
        self.pos_inicio = None
        self.pos_salida = None
        self.generar_mapa()

    def generar_mapa(self):
        tipos_casillas = [Camino, Muro, Tunel, Liana]

        self.matriz = [
            [random.choice(tipos_casillas)() for _ in range(self.columnas)]
            for _ in range(self.filas)
        ]

        self.pos_inicio = (0, 0)
        self.pos_salida = (self.filas - 1, self.columnas - 1)

        self.matriz[0][0] = Camino()
        self.matriz[self.filas - 1][self.columnas - 1] = Camino()

    def mostrar_matriz(self):
        for fila in self.matriz:
            print("".join(c.simbolo for c in fila))

    def mostrar_con_jugador_enemigo(self, jugador, enemigo=None):
        for f in range(self.filas):
            fila_str = ""
            for c in range(self.columnas):
                if (f, c) == jugador.obtener_posicion():
                    fila_str += "J"
                elif enemigo and (f, c) == enemigo.obtener_posicion():
                    fila_str += "E"
                else:
                    fila_str += self.matriz[f][c].simbolo
            print(fila_str)
