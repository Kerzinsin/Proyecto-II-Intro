##Enemigo - VERSIÓN CORREGIDA

import random
import time
from Modelos.terreno import Camino, Liana

class Enemigo:    
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna
        self.eliminado = False
        self.tiempo_eliminacion = None

    def obtener_posicion(self):
        return self.fila, self.columna

    def puede_moverse(self, mapa, nueva_fila, nueva_columna):
        """✅ CORRECCIÓN: Verifica si el enemigo puede moverse a una posición"""
        if 0 <= nueva_fila < mapa.filas and 0 <= nueva_columna < mapa.columnas:
            casilla_destino = mapa.matriz[nueva_fila][nueva_columna]
            # ✅ Los enemigos pueden pasar por lianas y caminos
            return casilla_destino.puede_pasar_enemigo()
        return False

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
        """✅ CORRECCIÓN: Movimiento mejorado hacia el jugador (Modo Escapa)"""
        if self.eliminado:
            return
        
        jugador_fila, jugador_columna = jugador.obtener_posicion()
        
        # Calcular dirección hacia el jugador
        diff_fila = jugador_fila - self.fila
        diff_columna = jugador_columna - self.columna
        
        # Crear lista de movimientos priorizados
        movimientos_posibles = []
        
        # Priorizar movimiento en el eje con mayor diferencia
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
        
        # Intentar moverse hacia el jugador
        for df, dc in movimientos_posibles:
            nueva_fila = self.fila + df
            nueva_columna = self.columna + dc
            if self.puede_moverse(mapa, nueva_fila, nueva_columna):
                self.fila = nueva_fila
                self.columna = nueva_columna
                return
        
        # Si no puede moverse hacia el jugador, intentar movimiento alternativo
        self.mover_aleatorio(mapa)

    def huir_de(self, jugador, mapa):
        """Huir del jugador (modo cazador básico)"""
        if self.eliminado:
            return
        
        jugador_fila, jugador_columna = jugador.obtener_posicion()
        
        # Calcular dirección OPUESTA al jugador
        diff_fila = self.fila - jugador_fila
        diff_columna = self.columna - jugador_columna
        
        # Priorizar movimiento alejándose
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
        
        # Intentar alejarse del jugador
        for df, dc in movimientos_posibles:
            nueva_fila = self.fila + df
            nueva_columna = self.columna + dc
            if self.puede_moverse(mapa, nueva_fila, nueva_columna):
                self.fila = nueva_fila
                self.columna = nueva_columna
                return
        
        # Si no puede alejarse, moverse aleatoriamente
        self.mover_aleatorio(mapa)
    
    def huir_hacia_salida(self, jugador, mapa, salidas):
        """✅ CORRECCIÓN: Enemigo huye del jugador pero se dirige hacia las salidas (Modo Cazador)"""
        if self.eliminado:
            return
        
        jugador_fila, jugador_columna = jugador.obtener_posicion()
        
        # Calcular distancia al jugador
        dist_jugador = abs(self.fila - jugador_fila) + abs(self.columna - jugador_columna)
        
        # Si el jugador está muy cerca (distancia <= 3), huir
        if dist_jugador <= 3:
            self.huir_de(jugador, mapa)
            return
        
        # Si el jugador está lejos, dirigirse a la salida más cercana
        salida_mas_cercana = None
        distancia_minima = float('inf')
        
        for salida in salidas:
            dist = abs(self.fila - salida[0]) + abs(self.columna - salida[1])
            if dist < distancia_minima:
                distancia_minima = dist
                salida_mas_cercana = salida
        
        if salida_mas_cercana:
            # Moverse hacia la salida
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
        
        # Si no puede moverse, movimiento aleatorio
        self.mover_aleatorio(mapa)

    def eliminar(self):
        """Marca al enemigo como eliminado"""
        self.eliminado = True
        self.tiempo_eliminacion = time.time()

    def verificar_reaparicion(self, mapa):
        """✅ CORRECCIÓN: Verifica si el enemigo debe reaparecer (después de 10 segundos)"""
        if self.eliminado and self.tiempo_eliminacion:
            if time.time() - self.tiempo_eliminacion >= 10:
                self.reaparecer(mapa)

    def reaparecer(self, mapa):
        """✅ CORRECCIÓN: Reaparece el enemigo en una posición válida donde puede ser capturado"""
        # Obtener posiciones válidas (caminos y lianas, no túneles)
        posiciones_validas = []
        for f in range(mapa.filas):
            for c in range(mapa.columnas):
                if self.puede_moverse(mapa, f, c):
                    # No reaparecer en inicio ni salida
                    if (f, c) != mapa.pos_inicio and (f, c) not in [mapa.pos_salida]:
                        posiciones_validas.append((f, c))
        
        if posiciones_validas:
            nueva_fila, nueva_columna = random.choice(posiciones_validas)
            self.fila = nueva_fila
            self.columna = nueva_columna
            self.eliminado = False
            self.tiempo_eliminacion = None