#Enemigo

import random
import threading
import time
from Modelos.terreno import Camino, Liana

class Enemigo:
    def __init__(self, fila, columna, velocidad=1.0):
        self.fila = fila
        self.columna = columna
        self.activo = True
        self.velocidad = velocidad  
        self.tiempo_eliminacion = None  

    def obtener_posicion(self):
        return self.fila, self.columna

    def puede_moverse(self, mapa, nueva_fila, nueva_columna):
        if 0 <= nueva_fila < mapa.filas and 0 <= nueva_columna < mapa.columnas:
            casilla_destino = mapa.matriz[nueva_fila][nueva_columna]
            return casilla_destino.puede_pasar_enemigo()
        return False

    def mover_aleatorio(self, mapa):
        """El enemigo se mueve aleatoriamente si hay casillas válidas."""
        direcciones = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(direcciones)

        for df, dc in direcciones:
            nueva_fila = self.fila + df
            nueva_columna = self.columna + dc
            if self.puede_moverse(mapa, nueva_fila, nueva_columna):
                self.fila = nueva_fila
                self.columna = nueva_columna
                break

    def mover_hacia(self, jugador, mapa):
        """El enemigo persigue al jugador (Modo Escapa)"""
        if self.eliminado:
            return
        
        jugador_fila, jugador_columna = jugador.obtener_posicion()
        
        # Calcular dirección hacia el jugador
        diff_fila = jugador_fila - self.fila
        diff_columna = jugador_columna - self.columna
        
        # Priorizar movimiento en el eje con mayor diferencia
        movimientos_posibles = []
        
        if diff_fila != 0:
            direccion_fila = 1 if diff_fila > 0 else -1
            movimientos_posibles.append((direccion_fila, 0))
        
        if diff_columna != 0:
            direccion_columna = 1 if diff_columna > 0 else -1
            movimientos_posibles.append((0, direccion_columna))
        
        # Intentar moverse en la dirección del jugador
        random.shuffle(movimientos_posibles)  # Añadir algo de aleatoriedad
        
        for df, dc in movimientos_posibles:
            nueva_fila = self.fila + df
            nueva_columna = self.columna + dc
            if self.puede_moverse(mapa, nueva_fila, nueva_columna):
                self.fila = nueva_fila
                self.columna = nueva_columna
                return
        
        # Si no puede moverse hacia el jugador, moverse aleatoriamente
        self.mover_aleatorio(mapa)

    def huir_de(self, jugador, mapa):
        """El enemigo huye del jugador (Modo Cazador)"""
        if self.eliminado:
            return
        
        jugador_fila, jugador_columna = jugador.obtener_posicion()
        
        # Calcular dirección OPUESTA al jugador
        diff_fila = self.fila - jugador_fila
        diff_columna = self.columna - jugador_columna
        
        # Priorizar movimiento alejándose
        movimientos_posibles = []
        
        if diff_fila != 0:
            direccion_fila = 1 if diff_fila > 0 else -1
            movimientos_posibles.append((direccion_fila, 0))
        
        if diff_columna != 0:
            direccion_columna = 1 if diff_columna > 0 else -1
            movimientos_posibles.append((0, direccion_columna))
        
        # Intentar alejarse del jugador
        random.shuffle(movimientos_posibles)
        
        for df, dc in movimientos_posibles:
            nueva_fila = self.fila + df
            nueva_columna = self.columna + dc
            if self.puede_moverse(mapa, nueva_fila, nueva_columna):
                self.fila = nueva_fila
                self.columna = nueva_columna
                return
        
        # Si no puede alejarse, moverse aleatoriamente
        self.mover_aleatorio(mapa)

    def eliminar(self):
        """Elimina temporalmente al enemigo (por trampa)"""
        self.eliminado = True
        self.tiempo_eliminacion = time.time()
        print(f"Enemigo eliminado en ({self.fila}, {self.columna})")

    def verificar_reaparicion(self, mapa):
        """Verifica si el enemigo debe reaparecer después de 10 segundos"""
        if self.eliminado and self.tiempo_eliminacion:
            if time.time() - self.tiempo_eliminacion >= 10:
                self.reaparecer(mapa)

    def reaparecer(self, mapa):
        """Reaparece en una posición aleatoria válida"""
        intentos = 0
        while intentos < 50:  # Máximo 50 intentos para encontrar posición
            nueva_fila = random.randint(0, mapa.filas - 1)
            nueva_columna = random.randint(0, mapa.columnas - 1)
            
            if self.puede_moverse(mapa, nueva_fila, nueva_columna):
                self.fila = nueva_fila
                self.columna = nueva_columna
                self.eliminado = False
                self.tiempo_eliminacion = None
                print(f"Enemigo reaparecido en ({self.fila}, {self.columna})")
                return
            intentos += 1

    def iniciar_movimiento(self, mapa):
        """El enemigo se mueve constantemente (usado en modo Cazador con hilos)"""
        def movimiento_continuo():
            while self.activo:
                if not self.eliminado:
                    self.mover_aleatorio(mapa)
                time.sleep(1.0 / self.velocidad)  # Controla velocidad
        
        hilo = threading.Thread(target=movimiento_continuo, daemon=True)
        hilo.start()
