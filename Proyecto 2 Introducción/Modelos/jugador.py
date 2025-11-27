#Jugador

import time
from Modelos.terreno import Tunel

class Jugador:
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna
        self.energia = 100
        self.puede_correr = True
        self.en_tunel = False
        self.tiempo_en_tunel = None
        self.vida = 3  
        self.trampas_disponibles = 3  
        self.trampas_activas = []  
        self.cooldown_trampa = {}  

    def obtener_posicion(self):
        return self.fila, self.columna

    def puede_moverse(self, mapa, nueva_fila, nueva_columna):
        if 0 <= nueva_fila < mapa.filas and 0 <= nueva_columna < mapa.columnas:
            casilla_destino = mapa.matriz[nueva_fila][nueva_columna]
            return casilla_destino.puede_pasar_jugador()
        return False

    def mover(self, direccion, mapa):
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

                casilla = mapa.matriz[nueva_fila][nueva_columna]
                self._gestionar_energia(casilla)
                return True
        return False

    def correr(self, mapa):
        if not self.puede_correr or self.energia < 100:
            print("No tienes energía para correr.")
            return False

        self.energia = 0
        self.puede_correr = False
        print("Corriendo durante 0.5 segundos...")

        time.sleep(0.5)
        return True

    def _gestionar_energia(self, casilla_actual):
        """Gestiona la recuperación de energía"""
        if isinstance(casilla_actual, Tunel):
            if not self.en_tunel:
                self.en_tunel = True
                self.tiempo_en_tunel = time.time()
            else:
                if time.time() - self.tiempo_en_tunel >= 1:
                    self.energia = 100
                    self.puede_correr = True
                    print("Has recuperado energía completamente.")
        else:
            self.en_tunel = False
            self.tiempo_en_tunel = None
            if self.energia < 100:
                self.energia = min(100, self.energia + 5)  # Recupera 5 por movimiento

    def colocar_trampa(self):
        """Coloca una trampa en la posición actual del jugador"""
        if len(self.trampas_activas) >= 3:
            print("Ya tienes 3 trampas activas. Espera a que se usen.")
            return False
        
        posicion = (self.fila, self.columna)
        
        # Verificar cooldown
        tiempo_actual = time.time()
        if posicion in self.cooldown_trampa:
            if tiempo_actual - self.cooldown_trampa[posicion] < 5:
                tiempo_restante = 5 - (tiempo_actual - self.cooldown_trampa[posicion])
                print(f"Espera {tiempo_restante:.1f} segundos para colocar otra trampa aquí.")
                return False
        
        # Colocar trampa
        self.trampas_activas.append({
            'posicion': posicion,
            'tiempo': tiempo_actual
        })
        self.cooldown_trampa[posicion] = tiempo_actual
        print(f"Trampa colocada en {posicion}. Trampas activas: {len(self.trampas_activas)}/3")
        return True

    def verificar_trampa_activada(self, posicion_enemigo):
        """Verifica si un enemigo activó una trampa"""
        for i, trampa in enumerate(self.trampas_activas):
            if trampa['posicion'] == posicion_enemigo:
                # Trampa activada
                self.trampas_activas.pop(i)
                print("¡Trampa activada! Enemigo eliminado.")
                return True
        return False

    def perder_vida(self):
        """Reduce una vida del jugador"""
        self.vida -= 1
        return self.vida <= 0  # Retorna True si murió