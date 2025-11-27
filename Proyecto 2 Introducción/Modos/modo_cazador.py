#Modo cazador

import time
import random
from Modelos.mapa import Mapa
from Modelos.jugador import Jugador
from Modelos.enemigo import Enemigo

class ModoCazador:
    def __init__(self, sistema_puntuacion, nombre_jugador):
        self.sistema_puntuacion = sistema_puntuacion
        self.nombre_jugador = nombre_jugador

    def jugar(self):
        mapa = Mapa(10, 15)
        jugador = Jugador(0, 0)

        enemigos = [
            Enemigo(random.randint(0, mapa.filas - 1),
                    random.randint(0, mapa.columnas - 1))
            for _ in range(3)
        ]

        for enemigo in enemigos:
            enemigo.iniciar_movimiento(mapa)

        puntaje = 0
        tiempo_limite = 120
        tiempo_inicio = time.time()

        print("\n=== MODO CAZADOR ===")
        print("Atrapa enemigos (+100), si escapan (-50).")
        print("Puedes correr solo si tienes energía disponible.\n")

        while time.time() - tiempo_inicio < tiempo_limite:
            mapa.mostrar_con_jugador_enemigo(jugador, enemigos[0])
            print(f"Energía: {jugador.energia} | Puede correr: {jugador.puede_correr} | Vida: {jugador.vida}")

            accion = input("\nMovimiento (arriba, abajo, izquierda, derecha, correr): ").lower()

            if accion == "correr":
                if jugador.correr(mapa):
                    continue
                else:
                    continue  

            else:
                jugador.mover(accion, mapa)

            for enemigo in enemigos:
                if jugador.obtener_posicion() == enemigo.obtener_posicion():
                    print("Enemigo atrapado. Pierdes 1 vida. +100 puntos.")
                    puntaje += 100
                    jugador.vida -= 1

                    enemigo.fila = random.randint(0, mapa.filas - 1)
                    enemigo.columna = random.randint(0, mapa.columnas - 1)

                    if jugador.vida <= 0:
                        print("\nHas perdido todas tus vidas.")
                        break

            if random.random() < 0.05:
                print("Un enemigo escapó. -50 puntos.")
                puntaje -= 50

        print("\nTiempo agotado.")
        print(f"Puntaje final: {puntaje}")

        for enemigo in enemigos:
            enemigo.activo = False

        self.sistema_puntuacion.guardar_puntaje(self.nombre_jugador, puntaje, "cazador")
