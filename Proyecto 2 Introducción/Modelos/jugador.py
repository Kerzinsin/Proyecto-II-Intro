#Jugador - VERSIÓN CORREGIDA

import time
from Modelos.terreno import Tunel

class Jugador:
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna
        self.energia = 100
        self.vida = 3  
        self.trampas_disponibles = 3  
        self.trampas_activas = []  
        self.cooldown_trampa = {}  
        
        # ✅ CORRECCIÓN: Nuevo sistema de correr
        self.corriendo = False
        self.tiempo_inicio_correr = None
        self.duracion_correr = 1.0  # 1 segundo corriendo
        
        # Recuperación de energía en túnel
        self.en_tunel = False
        self.tiempo_en_tunel = None

    def obtener_posicion(self):
        return self.fila, self.columna

    def puede_moverse(self, mapa, nueva_fila, nueva_columna):
        if 0 <= nueva_fila < mapa.filas and 0 <= nueva_columna < mapa.columnas:
            casilla_destino = mapa.matriz[nueva_fila][nueva_columna]
            return casilla_destino.puede_pasar_jugador()
        return False

    def mover(self, direccion, mapa):
        """Mueve al jugador en la dirección especificada"""
        movimientos = {
            "arriba": (-1, 0),
            "abajo": (1, 0),
            "izquierda": (0, -1),
            "derecha": (0, 1)
        }

        if direccion in movimientos:
            df, dc = movimientos[direccion]
            nueva_fila = self.fila + df
            nueva_columna = self.columna + dc

            if self.puede_moverse(mapa, nueva_fila, nueva_columna):
                self.fila = nueva_fila
                self.columna = nueva_columna
                return True
        return False

    def activar_correr(self):
        """✅ CORRECCIÓN: Activa el modo correr por 1 segundo consecutivo"""
        if self.energia >= 100:
            self.corriendo = True
            self.tiempo_inicio_correr = time.time()
            self.energia = 0  # Consume toda la energía
    
    def actualizar_energia(self, mapa):
        """✅ CORRECCIÓN: Actualiza la energía del jugador"""
        tiempo_actual = time.time()
        
        # Verificar si está corriendo
        if self.corriendo:
            if tiempo_actual - self.tiempo_inicio_correr >= self.duracion_correr:
                self.corriendo = False
                self.tiempo_inicio_correr = None
        
        # Recuperación de energía
        casilla_actual = mapa.matriz[self.fila][self.columna]
        
        if isinstance(casilla_actual, Tunel):
            # ✅ CORRECCIÓN: En túnel recupera 10 cada paso
            if not self.en_tunel:
                self.en_tunel = True
                self.tiempo_en_tunel = tiempo_actual
            else:
                # Recuperar 10 puntos de energía cada vez que pasa por el túnel
                if self.energia < 100:
                    self.energia = min(100, self.energia + 10)
        else:
            self.en_tunel = False
            self.tiempo_en_tunel = None

    def colocar_trampa(self):
        """Coloca una trampa en la posición actual del jugador"""
        if len(self.trampas_activas) >= 3:
            return False
        
        posicion = (self.fila, self.columna)
        
        # Verificar cooldown (5 segundos)
        tiempo_actual = time.time()
        if posicion in self.cooldown_trampa:
            if tiempo_actual - self.cooldown_trampa[posicion] < 5:
                return False
        
        # Colocar trampa
        self.trampas_activas.append({
            'posicion': posicion,
            'tiempo': tiempo_actual
        })
        self.cooldown_trampa[posicion] = tiempo_actual
        return True

    def verificar_trampa_activada(self, posicion_enemigo):
        """Verifica si un enemigo activó una trampa"""
        for i, trampa in enumerate(self.trampas_activas):
            if trampa['posicion'] == posicion_enemigo:
                # Trampa activada
                self.trampas_activas.pop(i)
                return True
        return False

    def perder_vida(self):
        """Reduce una vida del jugador"""
        self.vida -= 1
        return self.vida <= 0  # Retorna True si murió