import random
from collections import deque
from Modelos.terreno import Camino, Muro, Tunel, Liana

class Mapa:
    # Códigos numéricos para la matriz (obligatorio según instrucciones)
    CODIGO_CAMINO = 0
    CODIGO_MURO = 1
    CODIGO_TUNEL = 2
    CODIGO_LIANA = 3
    
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.matriz = []  # Matriz numérica obligatoria
        self.pos_inicio = None
        self.pos_salida = None
        self.trampas = []  
        self.generar_mapa()
    
    def puede_pasar_jugador(self, fila, columna):
        """Verifica si el jugador puede pasar por una posición"""
        if 0 <= fila < self.filas and 0 <= columna < self.columnas:
            codigo = self.matriz[fila][columna]
            # Jugador puede pasar por Camino (0) y Tunel (2)
            return codigo == self.CODIGO_CAMINO or codigo == self.CODIGO_TUNEL
        return False
    
    def puede_pasar_enemigo(self, fila, columna):
        """Verifica si el enemigo puede pasar por una posición"""
        if 0 <= fila < self.filas and 0 <= columna < self.columnas:
            codigo = self.matriz[fila][columna]
            # Enemigo puede pasar por Camino (0) y Liana (3)
            return codigo == self.CODIGO_CAMINO or codigo == self.CODIGO_LIANA
        return False
    
    def obtener_codigo(self, fila, columna):
        """Obtiene el código numérico de una posición"""
        if 0 <= fila < self.filas and 0 <= columna < self.columnas:
            return self.matriz[fila][columna]
        return self.CODIGO_MURO
    
    def obtener_simbolo(self, fila, columna):
        """Obtiene el símbolo de una posición basado en su código"""
        codigo = self.obtener_codigo(fila, columna)
        simbolos = {
            self.CODIGO_CAMINO: " ",
            self.CODIGO_MURO: "#",
            self.CODIGO_TUNEL: "T",
            self.CODIGO_LIANA: "L"
        }
        return simbolos.get(codigo, "#")

    def generar_mapa(self):
        """Genera un mapa aleatorio garantizando camino válido"""
        intentos = 0
        max_intentos = 100
        
        while intentos < max_intentos:
            # Generar matriz numérica (obligatorio según instrucciones)
            codigos = [self.CODIGO_CAMINO, self.CODIGO_MURO, self.CODIGO_TUNEL, self.CODIGO_LIANA]
            pesos = [50, 20, 15, 15]
            
            self.matriz = [
                [random.choices(codigos, weights=pesos)[0] for _ in range(self.columnas)]
                for _ in range(self.filas)
            ]
            
            self.pos_inicio = (0, 0)
            self.matriz[0][0] = self.CODIGO_CAMINO
            
            self.pos_salida = self._generar_salida_valida()
            
            if self._existe_camino_valido():
                return
            
            intentos += 1
        
        self._crear_camino_forzado()
    
    def _generar_salida_valida(self):
        """Genera una salida válida en un camino"""
        if self.matriz[self.filas - 1][self.columnas - 1] == self.CODIGO_CAMINO:
            return (self.filas - 1, self.columnas - 1)
        
        self.matriz[self.filas - 1][self.columnas - 1] = self.CODIGO_CAMINO
        return (self.filas - 1, self.columnas - 1)
    
    def generar_salidas_multiples(self, num_salidas):
        """Genera múltiples salidas en posiciones válidas"""
        salidas = [self.pos_salida]
        
        if num_salidas <= 1:
            return salidas
        
        posiciones_borde = []
        
        for c in range(1, self.columnas):
            if self.matriz[0][c] == self.CODIGO_CAMINO:
                posiciones_borde.append((0, c))
        
        for c in range(self.columnas - 1):
            if self.matriz[self.filas - 1][c] == self.CODIGO_CAMINO:
                posiciones_borde.append((self.filas - 1, c))
        
        for f in range(1, self.filas):
            if self.matriz[f][0] == self.CODIGO_CAMINO:
                posiciones_borde.append((f, 0))
        
        for f in range(self.filas - 1):
            if self.matriz[f][self.columnas - 1] == self.CODIGO_CAMINO:
                posiciones_borde.append((f, self.columnas - 1))
        
        num_adicionales = min(num_salidas - 1, len(posiciones_borde))
        if num_adicionales > 0:
            salidas_adicionales = random.sample(posiciones_borde, num_adicionales)
            salidas.extend(salidas_adicionales)
        
        return salidas

    def _existe_camino_valido(self):
        """Verifica si existe un camino válido del inicio a la salida usando BFS
        
        Usa búsqueda en anchura para garantizar que siempre haya un camino
        desde el inicio hasta la salida antes de aceptar el mapa generado.
        """
        visitados = set()
        cola = deque([self.pos_inicio])
        visitados.add(self.pos_inicio)
        
        while cola:
            fila, columna = cola.popleft()
            
            if (fila, columna) == self.pos_salida:
                return True
            
            direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            
            for df, dc in direcciones:
                nueva_fila = fila + df
                nueva_columna = columna + dc
                
                if 0 <= nueva_fila < self.filas and 0 <= nueva_columna < self.columnas:
                    if (nueva_fila, nueva_columna) not in visitados:
                        if self.puede_pasar_jugador(nueva_fila, nueva_columna):
                            visitados.add((nueva_fila, nueva_columna))
                            cola.append((nueva_fila, nueva_columna))
        return False

    def _crear_camino_forzado(self):
        """Crea un camino forzado desde inicio hasta salida"""
        fila_actual, columna_actual = self.pos_inicio
        fila_destino, columna_destino = self.pos_salida
        
        while fila_actual != fila_destino:
            self.matriz[fila_actual][columna_actual] = self.CODIGO_CAMINO
            if fila_actual < fila_destino:
                fila_actual += 1
            else:
                fila_actual -= 1
        
        while columna_actual != columna_destino:
            self.matriz[fila_actual][columna_actual] = self.CODIGO_CAMINO
            if columna_actual < columna_destino:
                columna_actual += 1
            else:
                columna_actual -= 1
        
        self.matriz[fila_destino][columna_destino] = self.CODIGO_CAMINO

    def mostrar_matriz(self):
        """Muestra el mapa con símbolos"""
        for f in range(self.filas):
            fila_str = ""
            for c in range(self.columnas):
                fila_str += self.obtener_simbolo(f, c)
            print(fila_str)

    def mostrar_con_jugador_enemigo(self, jugador, enemigos=None):
        """Muestra el mapa con jugador, enemigos y trampas"""
        for f in range(self.filas):
            fila_str = ""
            for c in range(self.columnas):
                pos_actual = (f, c)
                
                trampa_aqui = any(t['posicion'] == pos_actual for t in jugador.trampas_activas)
                if pos_actual == jugador.obtener_posicion():
                    fila_str += "J"
                elif trampa_aqui:
                    fila_str += "X"  
                elif enemigos:
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
                        fila_str += self.obtener_simbolo(f, c)
                else:
                    fila_str += self.obtener_simbolo(f, c)
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
                if self.puede_pasar_enemigo(f, c):
                    if (f, c) != self.pos_inicio and (f, c) != self.pos_salida:
                        posiciones.append((f, c))
        return posiciones
    
    def obtener_posiciones_validas_para_captura(self, jugador):
        """Retorna posiciones donde los enemigos pueden ser capturados"""
        posiciones = []
        pos_jugador = jugador.obtener_posicion()
        
        for f in range(self.filas):
            for c in range(self.columnas):
                codigo = self.matriz[f][c]
                if codigo == self.CODIGO_CAMINO or codigo == self.CODIGO_LIANA:
                    if (f, c) != self.pos_inicio and (f, c) != self.pos_salida:
                        dist = abs(f - pos_jugador[0]) + abs(c - pos_jugador[1])
                        if dist >= 5:
                            posiciones.append((f, c))
        
        return posiciones if posiciones else self.obtener_posiciones_validas_enemigo()