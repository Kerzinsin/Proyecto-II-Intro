import time

class Jugador:
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna
        self.energia = 100
        self.vida = 3  
        self.trampas_disponibles = 3  
        self.trampas_activas = []  
        self.cooldown_trampa = {}  
        
        self.corriendo = False
        self.tiempo_inicio_correr = None
        self.duracion_correr = 1.0
        
        self.en_tunel = False
        self.tiempo_en_tunel = None

    def obtener_posicion(self):
        return self.fila, self.columna

    def puede_moverse(self, mapa, nueva_fila, nueva_columna):
        return mapa.puede_pasar_jugador(nueva_fila, nueva_columna)

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
        """Activa el modo correr por 1 segundo"""
        if self.energia >= 100:
            self.corriendo = True
            self.tiempo_inicio_correr = time.time()
            self.energia = 0  # Consume toda la energía
    
    def actualizar_energia(self, mapa):
        """Actualiza la energía del jugador"""
        tiempo_actual = time.time()
        
        if self.corriendo:
            if tiempo_actual - self.tiempo_inicio_correr >= self.duracion_correr:
                self.corriendo = False
                self.tiempo_inicio_correr = None
        
        codigo_actual = mapa.obtener_codigo(self.fila, self.columna)
        
        if codigo_actual == mapa.CODIGO_TUNEL:
            if not self.en_tunel:
                self.en_tunel = True
                self.tiempo_en_tunel = tiempo_actual
            else:
                if self.energia < 100:
                    self.energia = min(100, self.energia + 10)
        else:
            self.en_tunel = False
            self.tiempo_en_tunel = None

    def colocar_trampa(self):
        """Coloca una trampa en la posición actual del jugador
        
        Máximo 3 trampas activas simultáneamente.
        Cooldown de 5 segundos por posición para evitar spam.
        """
        if len(self.trampas_activas) >= 3:
            return False
        
        posicion = (self.fila, self.columna)
        
        tiempo_actual = time.time()
        if posicion in self.cooldown_trampa:
            if tiempo_actual - self.cooldown_trampa[posicion] < 5:
                return False
        
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
                self.trampas_activas.pop(i)
                return True
        return False

    def perder_vida(self):
        """Reduce una vida del jugador"""
        self.vida -= 1
        return self.vida <= 0