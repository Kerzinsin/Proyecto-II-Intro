#Jugar

from puntuacion import Puntuacion
from modos import ModoEscapa, ModoCazador


class Juego:
    def __init__(self, nombre_jugador):
        self.nombre_jugador = nombre_jugador
        self.sistema_puntuacion = Puntuacion()
        self.sistema_puntuacion.registrar_jugador(nombre_jugador)

    def iniciar(self):
        print("\nSeleccione el modo de juego:")
        print("1. Escapa")
        print("2. Cazador")

        opcion = input("Modo: ")

        if opcion == "1":
            modo = ModoEscapa(self.nombre_jugador, self.sistema_puntuacion)
        elif opcion == "2":
            modo = ModoCazador(self.nombre_jugador, self.sistema_puntuacion)
        else:
            print("Opción inválida.")
            return

        modo.jugar()


if __name__ == "__main__":
    nombre = input("Ingrese su nombre: ")
    juego = Juego(nombre)
    juego.iniciar()
