#Modo Escapa

from Modelos.mapa import Mapa
from Modelos.jugador import Jugador
from Modelos.enemigo import Enemigo

class ModoEscapa:
    def __init__(self, sistema_puntuacion, nombre_jugador):
        self.sistema_puntuacion = sistema_puntuacion
        self.nombre_jugador = nombre_jugador

    def jugar(self):
        mapa = Mapa(10, 15)
        jugador = Jugador(0, 0)
        enemigo = Enemigo(mapa.filas - 1, mapa.columnas - 1)

        print("\n=== MODO ESCAPA ===")
        print("Objetivo: Escapa hacia la salida.")
        print("Puedes correr solo si tienes energía.\n")

        while True:
            mapa.mostrar_con_jugador_enemigo(jugador, enemigo)
            print(f"Energía: {jugador.energia} | Puede correr: {jugador.puede_correr} | Vida: {jugador.vida}")

            accion = input("\nMovimiento (arriba, abajo, izquierda, derecha, correr): ").lower()

            if accion == "correr":
                jugador.correr(mapa)
            else:
                jugador.mover(accion, mapa)

            enemigo.mover_hacia(jugador, mapa)

            if jugador.obtener_posicion() == (mapa.filas - 1, mapa.columnas - 1):
                print("\n¡Has escapado exitosamente! Ganaste 200 puntos.")
                self.sistema_puntuacion.guardar_puntaje(self.nombre_jugador, 200, "escapa")
                break

            if jugador.obtener_posicion() == enemigo.obtener_posicion():
                print("\nFuiste atrapado.")
                self.sistema_puntuacion.guardar_puntaje(self.nombre_jugador, 0, "escapa")
                break
