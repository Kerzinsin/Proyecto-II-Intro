from Sistema.puntuacion import Puntuacion
from Modos.modo_escapa import ModoEscapa
from Modos.modo_cazador import ModoCazador

class ControladorJuego:
    def __init__(self):
        self.sistema_puntuacion = Puntuacion()

    def iniciar_sesion(self):
        nombre = input("Ingrese su nombre: ")
        self.nombre_jugador = nombre
        self.sistema_puntuacion.registrar_jugador(nombre)

    def seleccionar_modo(self):
        print("\nSeleccione el modo de juego:")
        print("1. Escapa")
        print("2. Cazador")

        opcion = input("Modo: ")

        if opcion == "1":
            modo = ModoEscapa(self.sistema_puntuacion, self.nombre_jugador)
            modo.jugar()
        elif opcion == "2":
            modo = ModoCazador(self.sistema_puntuacion, self.nombre_jugador)
            modo.jugar()
        else:
            print("Opción inválida.")

    def mostrar_resultados(self):
        print("\nTop Escapa:")
        for p in self.sistema_puntuacion.obtener_top("escapa"):
            print(p)

        print("\nTop Cazador:")
        for p in self.sistema_puntuacion.obtener_top("cazador"):
            print(p)
