"""
Juego Escapa del Laberinto - Versión Pygame CORREGIDA
Instituto Tecnológico de Costa Rica
Proyecto 2 - Introducción a la Programación

CORRECCIONES APLICADAS:
1. Enemigos se mueven cada 1 segundo (no instantáneo)
2. Cyan = Túneles (solo jugador)
3. Verde oscuro = Lianas (solo enemigos, jugador NO puede entrar)
4. Verde brillante = Salidas (máximo 2)
5. Barra de energía visual implementada
"""

import pygame
import sys
import time
import random
from pathlib import Path

# Importar las clases del proyecto
from mapa import Mapa
from jugador import Jugador
from enemigo import Enemigo
from puntuacion import Puntuacion

# Inicializar Pygame
pygame.init()

# Constantes de la ventana
ANCHO_VENTANA = 1400
ALTO_VENTANA = 800
FPS = 30

# Tamaño de celda
TAMANO_CELDA = 35

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (128, 128, 128)
GRIS_OSCURO = (64, 64, 64)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
AZUL = (0, 100, 255)
AMARILLO = (255, 255, 0)
NARANJA = (255, 165, 0)
MORADO = (128, 0, 128)
CYAN = (0, 255, 255)  # TÚNELES (solo jugador)
VERDE_OSCURO = (0, 100, 0)  # LIANAS (solo enemigos)
VERDE_BRILLANTE = (0, 255, 100)  # SALIDAS

# Colores para terrenos
COLOR_CAMINO = BLANCO
COLOR_MURO = GRIS_OSCURO
COLOR_TUNEL = CYAN  # ✅ Cyan para túneles
COLOR_LIANA = VERDE_OSCURO  # ✅ Verde oscuro para lianas (NO el jugador)
COLOR_JUGADOR = AZUL
COLOR_ENEMIGO = ROJO
COLOR_TRAMPA = AMARILLO
COLOR_SALIDA = VERDE_BRILLANTE  # ✅ Verde brillante para salidas


class JuegoPygame:
    """Clase principal del juego con interfaz Pygame CORREGIDA"""
    
    def __init__(self):
        """Inicializa el juego con Pygame"""
        self.ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        pygame.display.set_caption("Escapa del Laberinto - TEC")
        self.reloj = pygame.time.Clock()
        self.fuente = pygame.font.Font(None, 22)
        self.fuente_grande = pygame.font.Font(None, 36)
        self.fuente_titulo = pygame.font.Font(None, 48)
        
        self.sistema_puntuacion = Puntuacion()
        self.estado = "menu_principal"
        self.nombre_jugador = ""
        self.dificultad = "normal"
        self.modo_actual = None
        
        # Variables del juego
        self.mapa = None
        self.jugador = None
        self.enemigos = []
        self.tiempo_inicio = None
        self.puntaje = 0
        self.mensaje = ""
        self.tiempo_mensaje = 0
        
        # ✅ CORRECCIÓN: Control de velocidad de enemigos
        self.ultimo_movimiento_enemigos = time.time()
        self.intervalo_enemigos = 1.0  # 1 segundo entre movimientos
        
    def ejecutar(self):
        """Loop principal del juego"""
        ejecutando = True
        
        while ejecutando:
            # Manejar eventos
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutando = False
                
                if self.estado == "menu_principal":
                    self.manejar_eventos_menu(evento)
                elif self.estado == "registro":
                    self.manejar_eventos_registro(evento)
                elif self.estado == "seleccion_dificultad":
                    self.manejar_eventos_dificultad(evento)
                elif self.estado == "seleccion_modo":
                    self.manejar_eventos_modo(evento)
                elif self.estado == "jugando":
                    self.manejar_eventos_juego(evento)
                elif self.estado == "game_over":
                    self.manejar_eventos_game_over(evento)
            
            # Actualizar
            if self.estado == "jugando":
                self.actualizar_juego()
            
            # Dibujar
            self.ventana.fill(NEGRO)
            
            if self.estado == "menu_principal":
                self.dibujar_menu_principal()
            elif self.estado == "registro":
                self.dibujar_registro()
            elif self.estado == "seleccion_dificultad":
                self.dibujar_seleccion_dificultad()
            elif self.estado == "seleccion_modo":
                self.dibujar_seleccion_modo()
            elif self.estado == "jugando":
                self.dibujar_juego()
            elif self.estado == "game_over":
                self.dibujar_game_over()
            
            pygame.display.flip()
            self.reloj.tick(FPS)
        
        pygame.quit()
        sys.exit()
    
    def dibujar_menu_principal(self):
        """Dibuja el menú principal"""
        titulo = self.fuente_titulo.render("ESCAPA DEL LABERINTO", True, VERDE)
        rect_titulo = titulo.get_rect(center=(ANCHO_VENTANA // 2, 150))
        self.ventana.blit(titulo, rect_titulo)
        
        subtitulo = self.fuente.render("Instituto Tecnológico de Costa Rica", True, GRIS)
        rect_sub = subtitulo.get_rect(center=(ANCHO_VENTANA // 2, 200))
        self.ventana.blit(subtitulo, rect_sub)
        
        opciones = [
            "1. JUGAR",
            "2. VER PUNTAJES",
            "3. SALIR"
        ]
        
        y = 300
        for opcion in opciones:
            texto = self.fuente_grande.render(opcion, True, BLANCO)
            rect = texto.get_rect(center=(ANCHO_VENTANA // 2, y))
            self.ventana.blit(texto, rect)
            y += 60
        
        inst = self.fuente.render("Presiona 1, 2 o 3 para seleccionar", True, GRIS)
        rect_inst = inst.get_rect(center=(ANCHO_VENTANA // 2, 550))
        self.ventana.blit(inst, rect_inst)
    
    def manejar_eventos_menu(self, evento):
        """Maneja eventos del menú principal"""
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_1:
                self.estado = "registro"
            elif evento.key == pygame.K_2:
                self.mostrar_puntajes()
            elif evento.key == pygame.K_3:
                pygame.quit()
                sys.exit()
    
    def dibujar_registro(self):
        """Dibuja la pantalla de registro"""
        titulo = self.fuente_grande.render("REGISTRO DE JUGADOR", True, VERDE)
        rect_titulo = titulo.get_rect(center=(ANCHO_VENTANA // 2, 200))
        self.ventana.blit(titulo, rect_titulo)
        
        instruccion = self.fuente.render("Ingresa tu nombre (min. 3 caracteres):", True, BLANCO)
        rect_inst = instruccion.get_rect(center=(ANCHO_VENTANA // 2, 300))
        self.ventana.blit(instruccion, rect_inst)
        
        nombre_texto = self.fuente_grande.render(self.nombre_jugador + "_", True, AMARILLO)
        rect_nombre = nombre_texto.get_rect(center=(ANCHO_VENTANA // 2, 350))
        self.ventana.blit(nombre_texto, rect_nombre)
        
        info = self.fuente.render("Presiona ENTER para continuar", True, GRIS)
        rect_info = info.get_rect(center=(ANCHO_VENTANA // 2, 450))
        self.ventana.blit(info, rect_info)
    
    def manejar_eventos_registro(self, evento):
        """Maneja eventos del registro"""
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN:
                if len(self.nombre_jugador) >= 3:
                    self.sistema_puntuacion.registrar_jugador(self.nombre_jugador)
                    self.estado = "seleccion_dificultad"
            elif evento.key == pygame.K_BACKSPACE:
                self.nombre_jugador = self.nombre_jugador[:-1]
            elif evento.unicode.isalnum() or evento.unicode == " ":
                if len(self.nombre_jugador) < 20:
                    self.nombre_jugador += evento.unicode
    
    def dibujar_seleccion_dificultad(self):
        """Dibuja la selección de dificultad"""
        titulo = self.fuente_grande.render("SELECCIONA DIFICULTAD", True, VERDE)
        rect_titulo = titulo.get_rect(center=(ANCHO_VENTANA // 2, 150))
        self.ventana.blit(titulo, rect_titulo)
        
        opciones = [
            ("1. FACIL", "Menos enemigos, más lentos - Multiplicador: x1.0"),
            ("2. NORMAL", "Balance de enemigos - Multiplicador: x1.5"),
            ("3. DIFICIL", "Más enemigos, más rápidos - Multiplicador: x2.0")
        ]
        
        y = 250
        for titulo_opcion, desc in opciones:
            texto_titulo = self.fuente_grande.render(titulo_opcion, True, BLANCO)
            rect = texto_titulo.get_rect(center=(ANCHO_VENTANA // 2, y))
            self.ventana.blit(texto_titulo, rect)
            
            texto_desc = self.fuente.render(desc, True, GRIS)
            rect_desc = texto_desc.get_rect(center=(ANCHO_VENTANA // 2, y + 30))
            self.ventana.blit(texto_desc, rect_desc)
            y += 100
    
    def manejar_eventos_dificultad(self, evento):
        """Maneja eventos de selección de dificultad"""
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_1:
                self.dificultad = "facil"
                self.intervalo_enemigos = 1.5  # Más lento
                self.estado = "seleccion_modo"
            elif evento.key == pygame.K_2:
                self.dificultad = "normal"
                self.intervalo_enemigos = 1.0  # Normal
                self.estado = "seleccion_modo"
            elif evento.key == pygame.K_3:
                self.dificultad = "dificil"
                self.intervalo_enemigos = 0.7  # Más rápido
                self.estado = "seleccion_modo"
    
    def dibujar_seleccion_modo(self):
        """Dibuja la selección de modo"""
        titulo = self.fuente_grande.render("SELECCIONA MODO DE JUEGO", True, VERDE)
        rect_titulo = titulo.get_rect(center=(ANCHO_VENTANA // 2, 150))
        self.ventana.blit(titulo, rect_titulo)
        
        opciones = [
            ("1. MODO ESCAPA", "Huye de los cazadores y llega a la salida"),
            ("2. MODO CAZADOR", "Atrapa a los enemigos antes de que escapen")
        ]
        
        y = 300
        for titulo_opcion, desc in opciones:
            texto_titulo = self.fuente_grande.render(titulo_opcion, True, BLANCO)
            rect = texto_titulo.get_rect(center=(ANCHO_VENTANA // 2, y))
            self.ventana.blit(texto_titulo, rect)
            
            texto_desc = self.fuente.render(desc, True, GRIS)
            rect_desc = texto_desc.get_rect(center=(ANCHO_VENTANA // 2, y + 30))
            self.ventana.blit(texto_desc, rect_desc)
            y += 100
    
    def manejar_eventos_modo(self, evento):
        """Maneja eventos de selección de modo"""
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_1:
                self.iniciar_modo_escapa()
            elif evento.key == pygame.K_2:
                self.iniciar_modo_cazador()
    
    def iniciar_modo_escapa(self):
        """Inicia el modo escapa"""
        self.modo_actual = "escapa"
        self.inicializar_juego()
    
    def iniciar_modo_cazador(self):
        """Inicia el modo cazador"""
        self.modo_actual = "cazador"
        self.inicializar_juego()
    
    def inicializar_juego(self):
        """Inicializa el estado del juego"""
        # Crear mapa
        self.mapa = Mapa(15, 20)
        
        # ✅ CORRECCIÓN: Crear máximo 2 salidas
        self.crear_salidas()
        
        # Crear jugador
        self.jugador = Jugador(0, 0)
        
        # Configuración según dificultad
        config = {
            "facil": {"enemigos": 2},
            "normal": {"enemigos": 3},
            "dificil": {"enemigos": 5}
        }
        
        cfg = config[self.dificultad]
        
        # Crear enemigos
        self.enemigos = []
        posiciones_validas = self.mapa.obtener_posiciones_validas_enemigo()
        
        for i in range(cfg["enemigos"]):
            if posiciones_validas:
                pos = random.choice(posiciones_validas)
                posiciones_validas.remove(pos)
                enemigo = Enemigo(pos[0], pos[1])
                enemigo.eliminado = False  # Asegurar inicialización
                self.enemigos.append(enemigo)
        
        self.tiempo_inicio = time.time()
        self.ultimo_movimiento_enemigos = time.time()
        self.puntaje = 0
        self.estado = "jugando"
    
    def crear_salidas(self):
        """✅ CORRECCIÓN: Crear máximo 2 salidas en el mapa"""
        self.salidas = []
        
        # Primera salida: esquina inferior derecha
        salida1 = (self.mapa.filas - 1, self.mapa.columnas - 1)
        self.salidas.append(salida1)
        
        # Segunda salida: posición aleatoria en el borde
        bordes = []
        # Borde superior
        for col in range(self.mapa.columnas):
            if (0, col) != (0, 0):  # No en inicio
                bordes.append((0, col))
        # Borde inferior
        for col in range(self.mapa.columnas):
            if (self.mapa.filas - 1, col) != salida1:
                bordes.append((self.mapa.filas - 1, col))
        # Borde izquierdo
        for fila in range(1, self.mapa.filas - 1):
            bordes.append((fila, 0))
        # Borde derecho
        for fila in range(1, self.mapa.filas - 1):
            bordes.append((fila, self.mapa.columnas - 1))
        
        if bordes:
            salida2 = random.choice(bordes)
            self.salidas.append(salida2)
    
    def manejar_eventos_juego(self, evento):
        """Maneja eventos durante el juego"""
        if evento.type == pygame.KEYDOWN:
            movido = False
            
            if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                movido = self.jugador.mover("arriba", self.mapa)
            elif evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                movido = self.jugador.mover("abajo", self.mapa)
            elif evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                movido = self.jugador.mover("izquierda", self.mapa)
            elif evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                movido = self.jugador.mover("derecha", self.mapa)
            elif evento.key == pygame.K_SPACE:
                if self.modo_actual == "escapa":
                    if self.jugador.colocar_trampa():
                        self.mostrar_mensaje("Trampa colocada!", 1.0)
            elif evento.key == pygame.K_LSHIFT or evento.key == pygame.K_RSHIFT:
                if self.jugador.correr(self.mapa):
                    self.mostrar_mensaje("¡Corriendo!", 0.5)
            
            if movido:
                # Verificar colisiones con trampas
                if self.modo_actual == "escapa":
                    for enemigo in self.enemigos:
                        if not enemigo.eliminado:
                            if self.jugador.verificar_trampa_activada(enemigo.obtener_posicion()):
                                enemigo.eliminar()
                                self.puntaje += 50
                                self.mostrar_mensaje("¡Trampa activada! +50 puntos", 1.0)
    
    def actualizar_juego(self):
        """Actualiza el estado del juego"""
        # ✅ CORRECCIÓN: Mover enemigos solo cada X segundos
        tiempo_actual = time.time()
        if tiempo_actual - self.ultimo_movimiento_enemigos >= self.intervalo_enemigos:
            self.mover_enemigos()
            self.ultimo_movimiento_enemigos = tiempo_actual
        
        if self.modo_actual == "escapa":
            self.actualizar_modo_escapa()
        elif self.modo_actual == "cazador":
            self.actualizar_modo_cazador()
        
        # Verificar reaparición de enemigos
        for enemigo in self.enemigos:
            if hasattr(enemigo, 'verificar_reaparicion'):
                enemigo.verificar_reaparicion(self.mapa)
    
    def mover_enemigos(self):
        """Mueve todos los enemigos"""
        if self.modo_actual == "escapa":
            for enemigo in self.enemigos:
                if not enemigo.eliminado:
                    enemigo.mover_hacia(self.jugador, self.mapa)
        elif self.modo_actual == "cazador":
            for enemigo in self.enemigos:
                if not enemigo.eliminado:
                    enemigo.huir_de(self.jugador, self.mapa)
    
    def actualizar_modo_escapa(self):
        """Actualiza la lógica del modo escapa"""
        # Verificar si llegó a alguna salida
        pos_jugador = self.jugador.obtener_posicion()
        if pos_jugador in self.salidas:
            self.finalizar_juego_victoria()
        
        # Verificar colisiones con enemigos
        for enemigo in self.enemigos:
            if not enemigo.eliminado and pos_jugador == enemigo.obtener_posicion():
                if self.jugador.perder_vida():
                    self.finalizar_juego_derrota()
                else:
                    self.mostrar_mensaje(f"¡Atrapado! Vidas: {self.jugador.vida}", 2.0)
                    # Reposicionar enemigo
                    posiciones = self.mapa.obtener_posiciones_validas_enemigo()
                    if posiciones:
                        nueva_pos = random.choice(posiciones)
                        enemigo.fila, enemigo.columna = nueva_pos
    
    def actualizar_modo_cazador(self):
        """Actualiza la lógica del modo cazador"""
        # Verificar si atrapó un enemigo
        pos_jugador = self.jugador.obtener_posicion()
        for enemigo in self.enemigos:
            if not enemigo.eliminado and pos_jugador == enemigo.obtener_posicion():
                self.puntaje += 100
                enemigo.eliminado = True
                self.mostrar_mensaje("¡Enemigo atrapado! +100 puntos", 1.0)
                # Reposicionar enemigo
                posiciones = self.mapa.obtener_posiciones_validas_enemigo()
                if posiciones:
                    nueva_pos = random.choice(posiciones)
                    enemigo.fila, enemigo.columna = nueva_pos
                    enemigo.eliminado = False
    
    def dibujar_juego(self):
        """Dibuja el estado del juego"""
        # Calcular offset para centrar el mapa
        offset_x = 50
        offset_y = (ALTO_VENTANA - self.mapa.filas * TAMANO_CELDA) // 2
        
        # Dibujar mapa
        for fila in range(self.mapa.filas):
            for col in range(self.mapa.columnas):
                x = offset_x + col * TAMANO_CELDA
                y = offset_y + fila * TAMANO_CELDA
                
                # Determinar color según tipo de casilla
                casilla = self.mapa.matriz[fila][col]
                if casilla.codigo == 0:  # Camino
                    color = COLOR_CAMINO
                elif casilla.codigo == 1:  # Muro
                    color = COLOR_MURO
                elif casilla.codigo == 2:  # Túnel (CYAN - solo jugador)
                    color = COLOR_TUNEL
                elif casilla.codigo == 3:  # Liana (VERDE OSCURO - solo enemigos)
                    color = COLOR_LIANA
                
                # Dibujar casilla
                pygame.draw.rect(self.ventana, color, (x, y, TAMANO_CELDA, TAMANO_CELDA))
                pygame.draw.rect(self.ventana, GRIS, (x, y, TAMANO_CELDA, TAMANO_CELDA), 1)
                
                # ✅ CORRECCIÓN: Marcar salidas con verde brillante
                if (fila, col) in self.salidas:
                    pygame.draw.rect(self.ventana, COLOR_SALIDA, 
                                   (x + 3, y + 3, TAMANO_CELDA - 6, TAMANO_CELDA - 6), 3)
        
        # Dibujar trampas
        for trampa in self.jugador.trampas_activas:
            fila, col = trampa['posicion']
            x = offset_x + col * TAMANO_CELDA
            y = offset_y + fila * TAMANO_CELDA
            pygame.draw.circle(self.ventana, COLOR_TRAMPA, 
                             (x + TAMANO_CELDA // 2, y + TAMANO_CELDA // 2), TAMANO_CELDA // 4)
        
        # Dibujar enemigos
        for enemigo in self.enemigos:
            if not enemigo.eliminado:
                fila, col = enemigo.obtener_posicion()
                x = offset_x + col * TAMANO_CELDA
                y = offset_y + fila * TAMANO_CELDA
                pygame.draw.circle(self.ventana, COLOR_ENEMIGO, 
                                 (x + TAMANO_CELDA // 2, y + TAMANO_CELDA // 2), TAMANO_CELDA // 3)
        
        # Dibujar jugador
        fila, col = self.jugador.obtener_posicion()
        x = offset_x + col * TAMANO_CELDA
        y = offset_y + fila * TAMANO_CELDA
        pygame.draw.circle(self.ventana, COLOR_JUGADOR, 
                         (x + TAMANO_CELDA // 2, y + TAMANO_CELDA // 2), TAMANO_CELDA // 3)
        
        # Dibujar HUD
        hud_x = offset_x + self.mapa.columnas * TAMANO_CELDA + 40
        self.dibujar_hud(hud_x, offset_y)
        
        # Mostrar mensaje temporal
        if self.mensaje and time.time() - self.tiempo_mensaje < 2.0:
            texto_msg = self.fuente_grande.render(self.mensaje, True, AMARILLO)
            rect_msg = texto_msg.get_rect(center=(ANCHO_VENTANA // 2, 50))
            # Fondo semi-transparente
            fondo = pygame.Surface((texto_msg.get_width() + 20, texto_msg.get_height() + 10))
            fondo.fill(NEGRO)
            fondo.set_alpha(200)
            self.ventana.blit(fondo, (rect_msg.x - 10, rect_msg.y - 5))
            self.ventana.blit(texto_msg, rect_msg)
    
    def dibujar_hud(self, x, y):
        """Dibuja el HUD con información del juego"""
        y_actual = y
        
        # Información del jugador
        textos_info = [
            f"JUGADOR: {self.nombre_jugador}",
            f"MODO: {self.modo_actual.upper()}",
            f"DIFICULTAD: {self.dificultad.upper()}",
            "",
            f"Tiempo: {int(time.time() - self.tiempo_inicio)}s",
            f"Vidas: {'❤️ ' * self.jugador.vida}",
            f"Puntaje: {self.puntaje}",
        ]
        
        for texto in textos_info:
            if texto == "":
                y_actual += 10
            else:
                superficie = self.fuente.render(texto, True, BLANCO)
                self.ventana.blit(superficie, (x, y_actual))
                y_actual += 25
        
        # ✅ CORRECCIÓN: BARRA DE ENERGÍA VISUAL
        y_actual += 10
        energia_texto = self.fuente.render("ENERGÍA:", True, BLANCO)
        self.ventana.blit(energia_texto, (x, y_actual))
        y_actual += 25
        
        # Barra de energía
        barra_ancho = 200
        barra_alto = 25
        energia_porcentaje = self.jugador.energia / 100
        
        # Borde de la barra
        pygame.draw.rect(self.ventana, BLANCO, (x, y_actual, barra_ancho, barra_alto), 2)
        
        # Relleno de la barra (color según nivel)
        if energia_porcentaje > 0.6:
            color_energia = VERDE
        elif energia_porcentaje > 0.3:
            color_energia = AMARILLO
        else:
            color_energia = ROJO
        
        pygame.draw.rect(self.ventana, color_energia, 
                        (x + 2, y_actual + 2, 
                         int((barra_ancho - 4) * energia_porcentaje), 
                         barra_alto - 4))
        
        # Texto de porcentaje
        texto_porcentaje = self.fuente.render(f"{self.jugador.energia}%", True, BLANCO)
        self.ventana.blit(texto_porcentaje, (x + barra_ancho + 10, y_actual))
        
        y_actual += 40
        
        # Controles
        y_actual += 20
        controles = [
            "CONTROLES:",
            "WASD / Flechas: Mover",
            "ESPACIO: Trampa",
            "SHIFT: Correr",
            "",
            "LEYENDA:",
            "⚪ Blanco: Camino",
            "⬛ Gris: Muro",
            "🔵 Cyan: Túnel (solo jugador)",
            "🟢 Verde oscuro: Liana (solo enemigos)",
            "✨ Verde brillante: Salida",
            "🔵 Azul: Jugador",
            "🔴 Rojo: Enemigo",
            "🟡 Amarillo: Trampa"
        ]
        
        for texto in controles:
            if texto == "":
                y_actual += 10
            else:
                superficie = self.fuente.render(texto, True, GRIS)
                self.ventana.blit(superficie, (x, y_actual))
                y_actual += 22
    
    def mostrar_mensaje(self, mensaje, duracion):
        """Muestra un mensaje temporal"""
        self.mensaje = mensaje
        self.tiempo_mensaje = time.time()
    
    def finalizar_juego_victoria(self):
        """Finaliza el juego con victoria"""
        tiempo_total = int(time.time() - self.tiempo_inicio)
        
        # Calcular bonificación por tiempo
        if tiempo_total < 30:
            bonus = 500
        elif tiempo_total < 60:
            bonus = 300
        else:
            bonus = 150
        
        # Multiplicador por dificultad
        multiplicadores = {"facil": 1.0, "normal": 1.5, "dificil": 2.0}
        mult = multiplicadores[self.dificultad]
        
        self.puntaje = int((1000 + bonus + self.puntaje) * mult)
        self.sistema_puntuacion.guardar_puntaje(self.nombre_jugador, self.puntaje, self.modo_actual)
        
        self.estado = "game_over"
        self.mensaje = "¡VICTORIA!"
    
    def finalizar_juego_derrota(self):
        """Finaliza el juego con derrota"""
        multiplicadores = {"facil": 1.0, "normal": 1.5, "dificil": 2.0}
        mult = multiplicadores[self.dificultad]
        
        self.puntaje = int(self.puntaje * mult)
        self.sistema_puntuacion.guardar_puntaje(self.nombre_jugador, self.puntaje, self.modo_actual)
        
        self.estado = "game_over"
        self.mensaje = "GAME OVER"
    
    def dibujar_game_over(self):
        """Dibuja la pantalla de game over"""
        titulo = self.fuente_titulo.render(self.mensaje, True, 
                                          VERDE if "VICTORIA" in self.mensaje else ROJO)
        rect_titulo = titulo.get_rect(center=(ANCHO_VENTANA // 2, 200))
        self.ventana.blit(titulo, rect_titulo)
        
        puntaje_texto = self.fuente_grande.render(f"Puntaje Final: {self.puntaje}", True, AMARILLO)
        rect_puntaje = puntaje_texto.get_rect(center=(ANCHO_VENTANA // 2, 300))
        self.ventana.blit(puntaje_texto, rect_puntaje)
        
        inst = self.fuente.render("Presiona ESPACIO para volver al menú", True, BLANCO)
        rect_inst = inst.get_rect(center=(ANCHO_VENTANA // 2, 400))
        self.ventana.blit(inst, rect_inst)
    
    def manejar_eventos_game_over(self, evento):
        """Maneja eventos de game over"""
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                self.nombre_jugador = ""
                self.estado = "menu_principal"
    
    def mostrar_puntajes(self):
        """Muestra los puntajes en consola"""
        print("\n" + "="*50)
        print("TOP 5 - MODO ESCAPA")
        print("="*50)
        for i, p in enumerate(self.sistema_puntuacion.obtener_top("escapa"), 1):
            print(f"{i}. {p['nombre']}: {p['puntaje']} pts")
        
        print("\n" + "="*50)
        print("TOP 5 - MODO CAZADOR")
        print("="*50)
        for i, p in enumerate(self.sistema_puntuacion.obtener_top("cazador"), 1):
            print(f"{i}. {p['nombre']}: {p['puntaje']} pts")
        print("="*50 + "\n")


if __name__ == "__main__":
    juego = JuegoPygame()
    juego.ejecutar()
