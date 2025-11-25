import random
from terreno import Camino, Muro, Tunel, Liana

class Mapa:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.matriz = []  # Aquí se guardará la matriz del mapa
        self.pos_inicio = None
        self.pos_salida = None
        self.generar_mapa()

    def generar_mapa(self):
        """Genera la matriz del mapa con casillas aleatorias."""
        tipos_casillas = [Camino, Muro, Tunel, Liana]

        self.matriz = [
            [random.choice(tipos_casillas)() for _ in range(self.columnas)]
            for _ in range(self.filas)
        ]

        # Establecer posición inicial y salida
        self.pos_inicio = (0, 0)
        self.pos_salida = (self.filas - 1, self.columnas - 1)

        # Forzar que esas posiciones sean Camino
        self.matriz[0][0] = Camino()
        self.matriz[self.filas - 1][self.columnas - 1] = Camino()

    def mostrar_matriz(self):
        """Muestra la matriz en texto (solo para pruebas)."""
        for fila in self.matriz:
            print("".join(c.simbolo for c in fila))

# Prueba rápida
if __name__ == "__main__":
    mapa = Mapa(10, 15)
    mapa.mostrar_matriz()
    print(" Inicio:", mapa.pos_inicio)
    print(" Salida:", mapa.pos_salida)
