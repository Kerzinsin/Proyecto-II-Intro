#Modos

import time
import random
from mapa import Mapa
from jugador import Jugador
from enemigo import Enemigo


class ModoJuego:
    """Clase base para los modos de juego."""

    def __init__(self, jugador_nombre, puntuacion):
        self.jugador_nombre = jugador_nombre
        self.puntuacion = puntuacion
        self.mapa = Mapa(10, 15)  # Podrá variar con niveles
        self.jugador = Jugador(0, 0)  # Aparición inicial
        self.enemigos = []  # Lista de enemigos (cada modo la configura)

    def mostrar_estado(self):
        """Muestra mapa con jugador y enemigos."""
        if self.enemigos:
            self.mapa.mostrar_con_jugador_enemigo(self.jugador, self.enemigos[0])
        else:
            self.mapa.mostrar_con_jugador_enemigo(self.jugador)

class ModoEscapa(ModoJuego):
    def __init__(self, jugador_nombre, puntuacion):
        super().__init__(jugador_nombre, puntuacion)
        self.enemigos = [Enemigo(self.mapa.filas - 1, self.mapa.columnas - 1)]

    def jugar(self):
        print("\n=== MODO ESCAPA ===")
        print("Llega a la salida sin ser atrapado.")

        while True:
            self.mostrar_estado()
            mov = input("\nMovimiento (arriba, abajo, izquierda, derecha): ").lower()

            self.jugador.mover(mov, self.mapa)
            self.enemigos[0].mover_hacia(self.jugador, self.mapa)

            if self.jugador.obtener_posicion() == self.mapa.pos_salida:
                puntaje = 200
                print("\nEscapaste. +200 puntos.")
                break

            if self.jugador.obtener_posicion() == self.enemigos[0].obtener_posicion():
                puntaje = 0
                print("\nFuiste atrapado. 0 puntos.")
                break

        self.puntuacion.guardar_puntaje(self.jugador_nombre, puntaje, "escapa")
        print(f"Puntaje final: {puntaje}")

class ModoCazador(ModoJuego):
    def __init__(self, jugador_nombre, puntuacion):
        super().__init__(jugador_nombre, puntuacion)
        self.enemigos = [
            Enemigo(random.randint(0, self.mapa.filas - 1),
                    random.randint(0, self.mapa.columnas - 1))
            for _ in range(3)
        ]
        self.tiempo_limite = 120

    def jugar(self):
        print("\n=== MODO CAZADOR ===")
        print("Atrapa enemigos (+100). Si escapan (-50). Tiempo: 2 minutos.")

        puntaje = 0
        inicio = time.time()

        while time.time() - inicio < self.tiempo_limite:
            self.mostrar_estado()
            mov = input("\nMovimiento: ").lower()
            self.jugador.mover(mov, self.mapa)

            for enemigo in self.enemigos:
                enemigo.mover_hacia(self.jugador, self.mapa)

                if self.jugador.obtener_posicion() == enemigo.obtener_posicion():
                    puntaje += 100
                    print("Atrapaste un enemigo. +100")
                    enemigo.fila = random.randint(0, self.mapa.filas - 1)
                    enemigo.columna = random.randint(0, self.mapa.columnas - 1)

            if random.random() < 0.05:
                puntaje -= 50
                print("Un enemigo escapó. -50")

        print("\nTiempo agotado.")
        self.puntuacion.guardar_puntaje(self.jugador_nombre, puntaje, "cazador")
        print(f"Puntaje final: {puntaje}")
