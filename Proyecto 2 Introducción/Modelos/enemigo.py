import random
import time
from Modelos.terreno import Camino, Liana

class Enemigo:    
    def __init__(self, fila, columna, dificultad="normal"):
        self.fila = fila
        self.columna = columna
        self.eliminado = False
        self.tiempo_eliminacion = None
        self.dificultad = dificultad
        
        # Tiempos de reaparición según dificultad (en segundos)
        # Fácil: 10 minutos = 600 segundos
        # Normal (intermedio): 5 segundos
        # Difícil: 3 segundos
        self.tiempos_reaparicion = {
            "facil": 600,    # 10 minutos
            "normal": 5,     # 5 segundos
            "dificil": 3     # 3 segundos
        }

    def obtener_posicion(self):
        return self.fila, self.columna

    def puede_moverse(self, mapa, nueva_fila, nueva_columna):
        """Verifica si el enemigo puede moverse a una posición"""
        return mapa.puede_pasar_enemigo(nueva_fila, nueva_columna)

    def mover_aleatorio(self, mapa):
        """Mueve el enemigo aleatoriamente"""
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
        """Mueve el enemigo hacia el jugador"""
        if self.eliminado:
            return
        
        jugador_fila, jugador_columna = jugador.obtener_posicion()
        
        diff_fila = jugador_fila - self.fila
        diff_columna = jugador_columna - self.columna
        
        movimientos_posibles = []
        
        if abs(diff_fila) > abs(diff_columna):
            if diff_fila != 0:
                direccion_fila = 1 if diff_fila > 0 else -1
                movimientos_posibles.append((direccion_fila, 0))
            if diff_columna != 0:
                direccion_columna = 1 if diff_columna > 0 else -1
                movimientos_posibles.append((0, direccion_columna))
        else:
            if diff_columna != 0:
                direccion_columna = 1 if diff_columna > 0 else -1
                movimientos_posibles.append((0, direccion_columna))
            if diff_fila != 0:
                direccion_fila = 1 if diff_fila > 0 else -1
                movimientos_posibles.append((direccion_fila, 0))
        
        for df, dc in movimientos_posibles:
            nueva_fila = self.fila + df
            nueva_columna = self.columna + dc
            if self.puede_moverse(mapa, nueva_fila, nueva_columna):
                self.fila = nueva_fila
                self.columna = nueva_columna
                return
        
        self.mover_aleatorio(mapa)

    def huir_de(self, jugador, mapa):
        """Huir del jugador (modo cazador básico)"""
        if self.eliminado:
            return
        
        jugador_fila, jugador_columna = jugador.obtener_posicion()
        
        diff_fila = self.fila - jugador_fila
        diff_columna = self.columna - jugador_columna
        
        movimientos_posibles = []
        
        if abs(diff_fila) > abs(diff_columna):
            if diff_fila != 0:
                direccion_fila = 1 if diff_fila > 0 else -1
                movimientos_posibles.append((direccion_fila, 0))
            if diff_columna != 0:
                direccion_columna = 1 if diff_columna > 0 else -1
                movimientos_posibles.append((0, direccion_columna))
        else:
            if diff_columna != 0:
                direccion_columna = 1 if diff_columna > 0 else -1
                movimientos_posibles.append((0, direccion_columna))
            if diff_fila != 0:
                direccion_fila = 1 if diff_fila > 0 else -1
                movimientos_posibles.append((direccion_fila, 0))
        
        for df, dc in movimientos_posibles:
            nueva_fila = self.fila + df
            nueva_columna = self.columna + dc
            if self.puede_moverse(mapa, nueva_fila, nueva_columna):
                self.fila = nueva_fila
                self.columna = nueva_columna
                return
        
        self.mover_aleatorio(mapa)
    
    def huir_hacia_salida(self, jugador, mapa, salidas):
        """Enemigo huye del jugador pero se dirige hacia las salidas
        
        Si el jugador está cerca (distancia <= 3), huye directamente.
        Si está lejos, se dirige a la salida más cercana.
        """
        if self.eliminado:
            return
        
        jugador_fila, jugador_columna = jugador.obtener_posicion()
        
        dist_jugador = abs(self.fila - jugador_fila) + abs(self.columna - jugador_columna)
        
        if dist_jugador <= 3:
            self.huir_de(jugador, mapa)
            return
        
        salida_mas_cercana = None
        distancia_minima = float('inf')
        
        for salida in salidas:
            dist = abs(self.fila - salida[0]) + abs(self.columna - salida[1])
            if dist < distancia_minima:
                distancia_minima = dist
                salida_mas_cercana = salida
        
        if salida_mas_cercana:
            diff_fila = salida_mas_cercana[0] - self.fila
            diff_columna = salida_mas_cercana[1] - self.columna
            
            movimientos_posibles = []
            
            if abs(diff_fila) > abs(diff_columna):
                if diff_fila != 0:
                    direccion_fila = 1 if diff_fila > 0 else -1
                    movimientos_posibles.append((direccion_fila, 0))
                if diff_columna != 0:
                    direccion_columna = 1 if diff_columna > 0 else -1
                    movimientos_posibles.append((0, direccion_columna))
            else:
                if diff_columna != 0:
                    direccion_columna = 1 if diff_columna > 0 else -1
                    movimientos_posibles.append((0, direccion_columna))
                if diff_fila != 0:
                    direccion_fila = 1 if diff_fila > 0 else -1
                    movimientos_posibles.append((direccion_fila, 0))
            
            for df, dc in movimientos_posibles:
                nueva_fila = self.fila + df
                nueva_columna = self.columna + dc
                if self.puede_moverse(mapa, nueva_fila, nueva_columna):
                    self.fila = nueva_fila
                    self.columna = nueva_columna
                    return
        
        self.mover_aleatorio(mapa)

    def eliminar(self):
        """Marca al enemigo como eliminado"""
        self.eliminado = True
        self.tiempo_eliminacion = time.time()

    def verificar_reaparicion(self, mapa):
        """Verifica si el enemigo debe reaparecer según el tiempo de dificultad"""
        if self.eliminado and self.tiempo_eliminacion:
            tiempo_reaparicion = self.tiempos_reaparicion.get(self.dificultad, 300)
            if time.time() - self.tiempo_eliminacion >= tiempo_reaparicion:
                self.reaparecer(mapa)

    def reaparecer(self, mapa):
        """Reaparece el enemigo en una posición válida"""
        posiciones_validas = []
        for f in range(mapa.filas):
            for c in range(mapa.columnas):
                if self.puede_moverse(mapa, f, c):
                    if (f, c) != mapa.pos_inicio and (f, c) not in [mapa.pos_salida]:
                        posiciones_validas.append((f, c))
        
        if posiciones_validas:
            nueva_fila, nueva_columna = random.choice(posiciones_validas)
            self.fila = nueva_fila
            self.columna = nueva_columna
            self.eliminado = False
            self.tiempo_eliminacion = None