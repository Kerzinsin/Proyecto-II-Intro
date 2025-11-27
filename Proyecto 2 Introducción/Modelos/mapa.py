#Mapa

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
        """Genera un mapa aleatorio garantizando un camino válido"""
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
            
            # Asegurar inicio y salida como caminos
            self.pos_inicio = (0, 0)
            self.pos_salida = (self.filas - 1, self.columnas - 1)
            
            self.matriz[0][0] = Camino()
            self.matriz[self.filas - 1][self.columnas - 1] = Camino()
            
            # Verificar si existe camino válido
            if self._existe_camino_valido():
                print("Mapa generado con camino válido.")
                return
            
            intentos += 1
        
        # Si después de 100 intentos no se generó un camino válido,
        # crear un camino forzado
        print("Creando camino forzado...")
        self._crear_camino_forzado()

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
        """Retorna lista de posiciones válidas para spawneo de enemigos"""
        posiciones = []
        for f in range(self.filas):
            for c in range(self.columnas):
                if self.matriz[f][c].puede_pasar_enemigo():
                    # No spawn en inicio ni salida
                    if (f, c) != self.pos_inicio and (f, c) != self.pos_salida:
                        posiciones.append((f, c))
        return posiciones