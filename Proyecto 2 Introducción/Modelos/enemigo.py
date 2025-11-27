##Enemigo

import random
import threading
import time
from Modelos.terreno import Camino, Liana

class Enemigo:
    """
    Representa un enemigo en el juego que puede perseguir o huir del jugador.
    
    Atributos:
        fila (int): Posición vertical en el mapa
        columna (int): Posición horizontal en el mapa
        activo (bool): Indica si el enemigo está activo en el juego
        velocidad (float): Multiplicador de velocidad (0.5 = lento, 1.5 = rápido)
        eliminado (bool): Indica si el enemigo fue eliminado por una trampa
        tiempo_eliminacion (float): Timestamp de cuando fue eliminado
    """
    
    def __init__(self, fila, columna, velocidad=1.0):
        """
        Inicializa un nuevo enemigo.
        
        Args:
            fila (int): Posición inicial en fila
            columna (int): Posición inicial en columna
            velocidad (float): Velocidad del enemigo (default: 1.0)
        """
        self.fila = fila
        self.columna = columna
        self.activo = True
        self.velocidad = velocidad
        self.eliminado = False  # ✅ FIX: Inicializar el atributo eliminado
        self.tiempo_eliminacion = None

    def obtener_posicion(self):
        """
        Obtiene la posición actual del enemigo.
        
        Returns:
            tuple: (fila, columna)
        """
        return self.fila, self.columna

    def puede_moverse(self, mapa, nueva_fila, nueva_columna):
        """
        Verifica si el enemigo puede moverse a una posición específica.
        
        Args:
            mapa (Mapa): Instancia del mapa del juego
            nueva_fila (int): Fila destino
            nueva_columna (int): Columna destino
            
        Returns:
            bool: True si el movimiento es válido, False en caso contrario
        """
        if 0 <= nueva_fila < mapa.filas and 0 <= nueva_columna < mapa.columnas:
            casilla_destino = mapa.matriz[nueva_fila][nueva_columna]
            return casilla_destino.puede_pasar_enemigo()
        return False

    def mover_aleatorio(self, mapa):
        """
        El enemigo se mueve aleatoriamente a una casilla válida adyacente.
        
        Args:
            mapa (Mapa): Instancia del mapa del juego
        """
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
        """
        El enemigo persigue al jugador (usado en Modo Escapa).
        
        Calcula la dirección hacia el jugador y se mueve en esa dirección.
        Si no puede acercarse, se mueve aleatoriamente.
        
        Args:
            jugador (Jugador): Instancia del jugador a perseguir
            mapa (Mapa): Instancia del mapa del juego
        """
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
        """
        El enemigo huye del jugador (usado en Modo Cazador).
        
        Calcula la dirección opuesta al jugador y se mueve alejándose.
        Si no puede alejarse, se mueve aleatoriamente.
        
        Args:
            jugador (Jugador): Instancia del jugador del cual huir
            mapa (Mapa): Instancia del mapa del juego
        """
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
        """
        Elimina temporalmente al enemigo (activado por trampa).
        
        El enemigo será marcado como eliminado y registrará el tiempo
        para poder reaparecer después de 10 segundos.
        """
        self.eliminado = True
        self.tiempo_eliminacion = time.time()
        print(f"Enemigo eliminado en ({self.fila}, {self.columna})")

    def verificar_reaparicion(self, mapa):
        """
        Verifica si el enemigo debe reaparecer después de 10 segundos.
        
        Args:
            mapa (Mapa): Instancia del mapa del juego
        """
        if self.eliminado and self.tiempo_eliminacion:
            if time.time() - self.tiempo_eliminacion >= 10:
                self.reaparecer(mapa)

    def reaparecer(self, mapa):
        """
        Reaparece el enemigo en una posición aleatoria válida del mapa.
        
        Intenta hasta 50 veces encontrar una posición válida donde
        el enemigo pueda moverse.
        
        Args:
            mapa (Mapa): Instancia del mapa del juego
        """
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
        """
        Inicia el movimiento continuo del enemigo en un hilo separado.
        
        Usado principalmente en el Modo Cazador para que los enemigos
        se muevan automáticamente sin esperar acciones del jugador.
        
        Args:
            mapa (Mapa): Instancia del mapa del juego
        """
        def movimiento_continuo():
            while self.activo:
                if not self.eliminado:
                    self.mover_aleatorio(mapa)
                time.sleep(1.0 / self.velocidad)  # Controla velocidad
        
        hilo = threading.Thread(target=movimiento_continuo, daemon=True)
        hilo.start()