#Jugar

from mapa import Mapa
from jugador import Jugador
from enemigo import Enemigo
from puntuacion import Puntuacion
import time
import random


class Juego:
    def __init__(self, nombre_jugador):
        self.nombre_jugador = nombre_jugador
        self.sistema_puntuacion = Puntuacion()  # Crear instancia del sistema de puntuación
        self.sistema_puntuacion.registrar_jugador(nombre_jugador)

    def jugar_modo_escapa(self):
        mapa = Mapa(10, 15)
        jugador = Jugador(0, 0)
        enemigo = Enemigo(mapa.filas - 1, mapa.columnas - 1)

        print("\n=== MODO ESCAPA ===")
        print("Llega a la salida sin que el enemigo te atrape.\n")

        while True:
            mapa.mostrar_con_jugador_enemigo(jugador, enemigo)
            movimiento = input("\nMovimiento (arriba, abajo, izquierda, derecha): ").lower()

            jugador.mover(movimiento, mapa)
            enemigo.mover_hacia(jugador, mapa)

            if jugador.obtener_posicion() == (mapa.filas - 1, mapa.columnas - 1):
                print("\n¡Has escapado exitosamente! Ganaste 200 puntos.")
                puntaje_final = 200
                break

            if jugador.obtener_posicion() == enemigo.obtener_posicion():
                print("\nEl enemigo te atrapó. No obtienes puntos.")
                puntaje_final = 0
                break

        self.sistema_puntuacion.guardar_puntaje(self.nombre_jugador, puntaje_final, "escapa")
        print(f"Puntaje registrado: {puntaje_final}\n")

    def jugar_modo_cazador(self):
        mapa = Mapa(10, 15)
        jugador = Jugador(0, 0)

        enemigos = [
            Enemigo(random.randint(0, mapa.filas - 1),
                    random.randint(0, mapa.columnas - 1))
            for _ in range(3)
        ]

        puntaje = 0
        tiempo_limite = 120
        tiempo_inicio = time.time()

        print("\n=== MODO CAZADOR ===")
        print("Atrapa enemigos (+100 pts), si escapan (-50 pts).")
        print("Tiempo límite: 2 minutos. Acumula la mayor cantidad de puntos posible.\n")

        while time.time() - tiempo_inicio < tiempo_limite:
            mapa.mostrar_con_jugador_enemigo(jugador, enemigos[0])
            movimiento = input("\nMovimiento (arriba, abajo, izquierda, derecha): ").lower()
            jugador.mover(movimiento, mapa)

            for enemigo in enemigos:
                enemigo.mover_hacia(jugador, mapa)

                if jugador.obtener_posicion() == enemigo.obtener_posicion():
                    print("Enemigo atrapado. +100 puntos.")
                    puntaje += 100
                    enemigo.fila = random.randint(0, mapa.filas - 1)
                    enemigo.columna = random.randint(0, mapa.columnas - 1)

            if random.random() < 0.05:
                print("Un enemigo escapó. -50 puntos.")
                puntaje -= 50

        print("\nTiempo agotado.")
        print(f"Puntaje final obtenido: {puntaje}")

        self.sistema_puntuacion.guardar_puntaje(self.nombre_jugador, puntaje, "cazador")
        print("Puntaje registrado.\n")

    def iniciar(self):
        print("\nSeleccione el modo de juego:")
        print("1. Escapa")
        print("2. Cazador")
        opcion = input("Modo: ")
        if opcion == "1":
            self.jugar_modo_escapa()
        elif opcion == "2":
            self.jugar_modo_cazador()
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    nombre = input("Ingrese su nombre: ")
    juego = Juego(nombre)
    juego.iniciar()
    mostrar_top(modo)

if __name__ == "__main__":
    main()
