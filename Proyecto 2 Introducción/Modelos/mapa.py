#Mapa - VERSIÓN CORREGIDA

import random
from collections import deque
from Modelos.terreno import Camino, Muro, Tunel, Liana

class Mapa:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.matriz = []
        self.pos_inicio = None
        self.pos_salida = None
        self.trampas = []  
        self.generar_mapa()

    def generar_mapa(self):
        """✅ CORRECCIÓN: Genera un mapa aleatorio garantizando camino válido y salidas solo en caminos"""
        intentos = 0
        max_intentos = 100
        
        while intentos < max_intentos:
            # Generar mapa aleatorio
            tipos_casillas = [Camino, Muro, Tunel, Liana]
            pesos = [50, 20, 15, 15]  # Mayor probabilidad de caminos
            
            self.matriz = [
                [random.choices(tipos_casillas, weights=pesos)[0]() for _ in range(self.columnas)]
                for _ in range(self.filas)
            ]
            
            # ✅ CORRECCIÓN: Asegurar inicio como camino
            self.pos_inicio = (0, 0)
            self.matriz[0][0] = Camino()
            
            # ✅ CORRECCIÓN: Buscar una posición válida para la salida (solo en caminos)
            self.pos_salida = self._generar_salida_valida()
            
            # Verificar si existe camino válido
            if self._existe_camino_valido():
                return
            
            intentos += 1
        
        # Si después de 100 intentos no se generó un camino válido,
        # crear un camino forzado
        self._crear_camino_forzado()
    
    def _generar_salida_valida(self):
        """✅ CORRECCIÓN: Genera una salida válida solo en caminos"""
        # Intentar en la esquina inferior derecha primero
        if isinstance(self.matriz[self.filas - 1][self.columnas - 1], Camino):
            return (self.filas - 1, self.columnas - 1)
        
        # Si no es camino, forzar que lo sea
        self.matriz[self.filas - 1][self.columnas - 1] = Camino()
        return (self.filas - 1, self.columnas - 1)
    
    def generar_salidas_multiples(self, num_salidas):
        """✅ NUEVO: Genera múltiples salidas en posiciones válidas (solo caminos)"""
        salidas = [self.pos_salida]  # Incluir la salida principal
        
        if num_salidas <= 1:
            return salidas
        
        # Buscar posiciones válidas en los bordes del mapa (solo caminos)
        posiciones_borde = []
        
        # Borde superior (excluyendo inicio)
        for c in range(1, self.columnas):
            if isinstance(self.matriz[0][c], Camino):
                posiciones_borde.append((0, c))
        
        # Borde inferior
        for c in range(self.columnas - 1):
            if isinstance(self.matriz[self.filas - 1][c], Camino):
                posiciones_borde.append((self.filas - 1, c))
        
        # Borde izquierdo (excluyendo inicio)
        for f in range(1, self.filas):
            if isinstance(self.matriz[f][0], Camino):
                posiciones_borde.append((f, 0))
        
        # Borde derecho
        for f in range(self.filas - 1):
            if isinstance(self.matriz[f][self.columnas - 1], Camino):
                posiciones_borde.append((f, self.columnas - 1))
        
        # Seleccionar salidas adicionales
        num_adicionales = min(num_salidas - 1, len(posiciones_borde))
        if num_adicionales > 0:
            salidas_adicionales = random.sample(posiciones_borde, num_adicionales)
            salidas.extend(salidas_adicionales)
        
        return salidas

    def _existe_camino_valido(self):
        """Verifica si existe un camino válido del inicio a la salida usando BFS"""
        visitados = set()
        cola = deque([self.pos_inicio])
        visitados.add(self.pos_inicio)
        
        while cola:
            fila, columna = cola.popleft()
            
            # Si llegamos a la salida, hay camino válido
            if (fila, columna) == self.pos_salida:
                return True
            
            # Explorar vecinos (arriba, abajo, izquierda, derecha)
            direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            
            for df, dc in direcciones:
                nueva_fila = fila + df
                nueva_columna = columna + dc
                
                # Verificar límites
                if 0 <= nueva_fila < self.filas and 0 <= nueva_columna < self.columnas:
                    if (nueva_fila, nueva_columna) not in visitados:
                        casilla = self.matriz[nueva_fila][nueva_columna]
                        
                        # El jugador puede pasar por Camino y Túnel
                        if casilla.puede_pasar_jugador():
                            visitados.add((nueva_fila, nueva_columna))
                            cola.append((nueva_fila, nueva_columna))
        return False

    def _crear_camino_forzado(self):
        """Crea un camino forzado desde inicio hasta salida"""
        fila_actual, columna_actual = self.pos_inicio
        fila_destino, columna_destino = self.pos_salida
        
        # Crear camino en forma de "L" o zigzag
        while fila_actual != fila_destino:
            self.matriz[fila_actual][columna_actual] = Camino()
            if fila_actual < fila_destino:
                fila_actual += 1
            else:
                fila_actual -= 1
        
        while columna_actual != columna_destino:
            self.matriz[fila_actual][columna_actual] = Camino()
            if columna_actual < columna_destino:
                columna_actual += 1
            else:
                columna_actual -= 1
        
        # Asegurar la casilla final
        self.matriz[fila_destino][columna_destino] = Camino()

    def mostrar_matriz(self):
        """Muestra el mapa con símbolos"""
        for fila in self.matriz:
            print("".join(c.simbolo for c in fila))

    def mostrar_con_jugador_enemigo(self, jugador, enemigos=None):
        """Muestra el mapa con jugador, enemigos y trampas"""
        for f in range(self.filas):
            fila_str = ""
            for c in range(self.columnas):
                pos_actual = (f, c)
                
                # Verificar si hay trampa
                trampa_aqui = any(t['posicion'] == pos_actual for t in jugador.trampas_activas)
                if pos_actual == jugador.obtener_posicion():
                    fila_str += "J"
                elif trampa_aqui:
                    fila_str += "X"  
                elif enemigos:
                    # Verificar si hay algún enemigo en esta posición
                    enemigo_aqui = False
                    if isinstance(enemigos, list):
                        for enemigo in enemigos:
                            if not enemigo.eliminado and pos_actual == enemigo.obtener_posicion():
                                fila_str += "E"
                                enemigo_aqui = True
                                break
                    else:
                        if not enemigos.eliminado and pos_actual == enemigos.obtener_posicion():
                            fila_str += "E"
                            enemigo_aqui = True
                    
                    if not enemigo_aqui:
                        fila_str += self.matriz[f][c].simbolo
                else:
                    fila_str += self.matriz[f][c].simbolo
            print(fila_str)
        print("\nLeyenda: J=Jugador | E=Enemigo | X=Trampa | #=Muro | T=Túnel | L=Liana | (espacio)=Camino")

    def mostrar_con_multiples_enemigos(self, jugador, enemigos):
        """Muestra el mapa con múltiples enemigos"""
        self.mostrar_con_jugador_enemigo(jugador, enemigos)

    def obtener_posiciones_validas_enemigo(self):
        """✅ CORRECCIÓN: Retorna lista de posiciones válidas para spawneo de enemigos (caminos y lianas)"""
        posiciones = []
        for f in range(self.filas):
            for c in range(self.columnas):
                casilla = self.matriz[f][c]
                # Los enemigos pueden spawnearse en caminos y lianas
                if casilla.puede_pasar_enemigo():
                    # No spawn en inicio ni salida
                    if (f, c) != self.pos_inicio and (f, c) != self.pos_salida:
                        posiciones.append((f, c))
        return posiciones
    
    def obtener_posiciones_validas_para_captura(self, jugador):
        """✅ NUEVO: Retorna posiciones donde los enemigos pueden ser capturados (no en túneles)"""
        posiciones = []
        pos_jugador = jugador.obtener_posicion()
        
        for f in range(self.filas):
            for c in range(self.columnas):
                casilla = self.matriz[f][c]
                # Solo caminos y lianas (no túneles, porque el jugador no puede ir ahí)
                if isinstance(casilla, Camino) or isinstance(casilla, Liana):
                    # No spawn en inicio, salida, ni muy cerca del jugador
                    if (f, c) != self.pos_inicio and (f, c) != self.pos_salida:
                        # No muy cerca del jugador
                        dist = abs(f - pos_jugador[0]) + abs(c - pos_jugador[1])
                        if dist >= 5:  # Al menos 5 casillas de distancia
                            posiciones.append((f, c))
        
        return posiciones if posiciones else self.obtener_posiciones_validas_enemigo()