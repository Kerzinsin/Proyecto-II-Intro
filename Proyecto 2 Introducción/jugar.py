"""
Juego Escapa del Laberinto
Instituto Tecnológico de Costa Rica
Proyecto 2 - Introducción a la Programación
VERSIÓN CORREGIDA
"""

import pygame
import sys
import time
import random
from pathlib import Path

# Importar las clases del proyecto
from Modelos.mapa import Mapa
from Modelos.jugador import Jugador
from Modelos.enemigo import Enemigo
from Sistema.puntuacion import Puntuacion

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
COLOR_TUNEL = CYAN
COLOR_LIANA = VERDE_OSCURO
COLOR_JUGADOR = AZUL
COLOR_ENEMIGO = ROJO
COLOR_TRAMPA = AMARILLO
COLOR_SALIDA = VERDE_BRILLANTE

class JuegoPygame:
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
        self.salidas = []  # ✅ Lista de salidas (puede haber múltiples)
        
        # ✅ CORRECCIÓN: Control de velocidad de enemigos mejorado
        self.ultimo_movimiento_enemigos = time.time()
        self.intervalo_enemigos = 1.0
        
        # ✅ CORRECCIÓN: Control del tiempo de juego para modo cazador
        self.tiempo_limite_cazador = 120  # 2 minutos
        self.ultimo_spawn_cazador = None
        
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
                elif self.estado == "puntajes":  # ✅ Nuevo estado
                    self.manejar_eventos_puntajes(evento)
            
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
            elif self.estado == "puntajes":  # ✅ Nuevo estado
                self.dibujar_puntajes()
            
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
                # ✅ CORRECCIÓN: Cambiar a pantalla de puntajes en lugar de consola
                self.estado = "puntajes"
            elif evento.key == pygame.K_3:
                pygame.quit()
                sys.exit()
    
    # ✅ NUEVO: Pantalla de puntajes en Pygame
    def dibujar_puntajes(self):
        """Dibuja la pantalla de puntajes"""
        titulo = self.fuente_titulo.render("TABLA DE PUNTAJES", True, VERDE)
        rect_titulo = titulo.get_rect(center=(ANCHO_VENTANA // 2, 80))
        self.ventana.blit(titulo, rect_titulo)
        
        # Dividir en dos columnas
        x_izq = ANCHO_VENTANA // 4
        x_der = 3 * ANCHO_VENTANA // 4
        y_inicio = 150
        
        # Modo Escapa (izquierda)
        titulo_escapa = self.fuente_grande.render("TOP 5 - MODO ESCAPA", True, AMARILLO)
        rect_escapa = titulo_escapa.get_rect(center=(x_izq, y_inicio))
        self.ventana.blit(titulo_escapa, rect_escapa)
        
        y = y_inicio + 50
        top_escapa = self.sistema_puntuacion.obtener_top("escapa")
        for i, p in enumerate(top_escapa, 1):
            texto = self.fuente.render(f"{i}. {p['nombre']}: {p['puntaje']} pts", True, BLANCO)
            self.ventana.blit(texto, (x_izq - 150, y))
            y += 30
        
        # Modo Cazador (derecha)
        titulo_cazador = self.fuente_grande.render("TOP 5 - MODO CAZADOR", True, AMARILLO)
        rect_cazador = titulo_cazador.get_rect(center=(x_der, y_inicio))
        self.ventana.blit(titulo_cazador, rect_cazador)
        
        y = y_inicio + 50
        top_cazador = self.sistema_puntuacion.obtener_top("cazador")
        for i, p in enumerate(top_cazador, 1):
            texto = self.fuente.render(f"{i}. {p['nombre']}: {p['puntaje']} pts", True, BLANCO)
            self.ventana.blit(texto, (x_der - 150, y))
            y += 30
        
        # Instrucción
        inst = self.fuente.render("Presiona ESC para volver al menú", True, GRIS)
        rect_inst = inst.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA - 50))
        self.ventana.blit(inst, rect_inst)
    
    def manejar_eventos_puntajes(self, evento):
        """Maneja eventos de la pantalla de puntajes"""
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                self.estado = "menu_principal"
    
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
        for opcion, desc in opciones:
            texto = self.fuente_grande.render(opcion, True, BLANCO)
            rect = texto.get_rect(center=(ANCHO_VENTANA // 2, y))
            self.ventana.blit(texto, rect)
            
            desc_texto = self.fuente.render(desc, True, GRIS)
            rect_desc = desc_texto.get_rect(center=(ANCHO_VENTANA // 2, y + 30))
            self.ventana.blit(desc_texto, rect_desc)
            y += 90
        
        inst = self.fuente.render("Presiona 1, 2 o 3 para seleccionar", True, GRIS)
        rect_inst = inst.get_rect(center=(ANCHO_VENTANA // 2, 550))
        self.ventana.blit(inst, rect_inst)
    
    def manejar_eventos_dificultad(self, evento):
        """Maneja eventos de selección de dificultad"""
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_1:
                self.dificultad = "facil"
                self.estado = "seleccion_modo"
            elif evento.key == pygame.K_2:
                self.dificultad = "normal"
                self.estado = "seleccion_modo"
            elif evento.key == pygame.K_3:
                self.dificultad = "dificil"
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
        
        y = 280
        for opcion, desc in opciones:
            texto = self.fuente_grande.render(opcion, True, BLANCO)
            rect = texto.get_rect(center=(ANCHO_VENTANA // 2, y))
            self.ventana.blit(texto, rect)
            
            desc_texto = self.fuente.render(desc, True, GRIS)
            rect_desc = desc_texto.get_rect(center=(ANCHO_VENTANA // 2, y + 30))
            self.ventana.blit(desc_texto, rect_desc)
            y += 100
        
        inst = self.fuente.render("Presiona 1 o 2 para seleccionar", True, GRIS)
        rect_inst = inst.get_rect(center=(ANCHO_VENTANA // 2, 520))
        self.ventana.blit(inst, rect_inst)
    
    def manejar_eventos_modo(self, evento):
        """Maneja eventos de selección de modo"""
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_1:
                self.modo_actual = "escapa"
                self.iniciar_juego()
            elif evento.key == pygame.K_2:
                self.modo_actual = "cazador"
                self.iniciar_juego()
    
    def iniciar_juego(self):
        """Inicia una nueva partida"""
        # ✅ CORRECCIÓN: Configuración según dificultad y modo
        config_escapa = {
            "facil": {"enemigos": 3, "intervalo": 1.0},
            "normal": {"enemigos": 5, "intervalo": 0.75},
            "dificil": {"enemigos": 6, "intervalo": 0.5}
        }
        
        config_cazador = {
            "facil": {"enemigos": 5, "intervalo": 1.0, "salidas": 1},
            "normal": {"enemigos": 5, "intervalo": 0.75, "salidas": 2},
            "dificil": {"enemigos": 4, "intervalo": 0.5, "salidas": 2}
        }
        
        # Crear mapa
        self.mapa = Mapa(20, 25)
        
        # ✅ CORRECCIÓN: Generar múltiples salidas según el modo
        if self.modo_actual == "escapa":
            # Modo Escapa: solo 1 salida
            self.salidas = [self.mapa.pos_salida]
            config = config_escapa[self.dificultad]
        else:
            # Modo Cazador: 1 o 2 salidas según dificultad
            config = config_cazador[self.dificultad]
            num_salidas = config["salidas"]
            self.salidas = self.mapa.generar_salidas_multiples(num_salidas)
        
        # Crear jugador en posición inicial
        self.jugador = Jugador(*self.mapa.pos_inicio)
        
        # ✅ CORRECCIÓN: Crear enemigos con configuración correcta
        num_enemigos = config["enemigos"]
        self.intervalo_enemigos = config["intervalo"]
        
        self.enemigos = []
        posiciones_validas = self.mapa.obtener_posiciones_validas_enemigo()
        
        for i in range(num_enemigos):
            if posiciones_validas:
                pos = random.choice(posiciones_validas)
                posiciones_validas.remove(pos)
                enemigo = Enemigo(pos[0], pos[1])
                self.enemigos.append(enemigo)
        
        # ✅ CORRECCIÓN: Inicializar puntaje según modo
        if self.modo_actual == "escapa":
            self.puntaje = 1500  # Inicia con 1500
        else:
            self.puntaje = 0  # Inicia en 0
        
        self.tiempo_inicio = time.time()
        self.ultimo_movimiento_enemigos = time.time()
        self.ultimo_spawn_cazador = time.time()
        self.estado = "jugando"
    
    def manejar_eventos_juego(self, evento):
        """Maneja eventos durante el juego"""
        if evento.type == pygame.KEYDOWN:
            # Movimiento del jugador
            direccion = None
            if evento.key == pygame.K_UP:
                direccion = "arriba"
            elif evento.key == pygame.K_DOWN:
                direccion = "abajo"
            elif evento.key == pygame.K_LEFT:
                direccion = "izquierda"
            elif evento.key == pygame.K_RIGHT:
                direccion = "derecha"
            elif evento.key == pygame.K_SPACE:
                # ✅ CORRECCIÓN: Solo permitir trampas en modo escapa
                if self.modo_actual == "escapa":
                    if self.jugador.colocar_trampa():
                        self.mostrar_mensaje("¡Trampa colocada!", 1.0)
            elif evento.key in [pygame.K_LSHIFT, pygame.K_RSHIFT]:
                # ✅ CORRECCIÓN: Correr consume energía y permite movimiento rápido
                self.jugador.activar_correr()
            
            if direccion:
                # ✅ CORRECCIÓN: Movimiento con correr
                if self.jugador.mover(direccion, self.mapa):
                    pass  # Movimiento exitoso
    
    def actualizar_juego(self):
        """Actualiza la lógica del juego"""
        tiempo_actual = time.time()
        
        # ✅ CORRECCIÓN: Actualizar energía del jugador
        self.jugador.actualizar_energia(self.mapa)
        
        # ✅ CORRECCIÓN: Modo Cazador - verificar tiempo límite
        if self.modo_actual == "cazador":
            tiempo_transcurrido = tiempo_actual - self.tiempo_inicio
            if tiempo_transcurrido >= self.tiempo_limite_cazador:
                self.finalizar_juego_tiempo_cazador()
                return
        
        # ✅ CORRECCIÓN: Modo Escapa - reducir puntos cada 5 segundos
        if self.modo_actual == "escapa":
            tiempo_transcurrido = tiempo_actual - self.tiempo_inicio
            # Cada 5 segundos, reducir 50 puntos
            puntos_perdidos = int(tiempo_transcurrido / 5) * 50
            self.puntaje = max(0, 1500 - puntos_perdidos)
        
        # Mover enemigos según intervalo
        if tiempo_actual - self.ultimo_movimiento_enemigos >= self.intervalo_enemigos:
            for enemigo in self.enemigos:
                if not enemigo.eliminado:
                    if self.modo_actual == "escapa":
                        enemigo.mover_hacia(self.jugador, self.mapa)
                    else:  # modo cazador
                        # ✅ CORRECCIÓN: Enemigos huyen hacia las salidas
                        enemigo.huir_hacia_salida(self.jugador, self.mapa, self.salidas)
            self.ultimo_movimiento_enemigos = tiempo_actual
        
        # Verificar colisiones con enemigos
        pos_jugador = self.jugador.obtener_posicion()
        for enemigo in self.enemigos:
            if not enemigo.eliminado:
                if pos_jugador == enemigo.obtener_posicion():
                    if self.modo_actual == "escapa":
                        # ✅ CORRECCIÓN: Perder vida y reaparecer en inicio
                        if self.jugador.perder_vida():
                            self.finalizar_juego_derrota()
                            return
                        else:
                            # Reaparecer en posición inicial
                            self.jugador.fila, self.jugador.columna = self.mapa.pos_inicio
                            self.mostrar_mensaje(f"¡Atrapado! Vidas: {self.jugador.vida}", 2.0)
                    else:  # modo cazador
                        # ✅ CORRECCIÓN: Atrapar enemigo
                        self.enemigos.remove(enemigo)
                        self.puntaje += 100
                        self.mostrar_mensaje("¡Enemigo atrapado! +100 pts", 1.0)
                        # Generar nuevo enemigo inmediatamente
                        self.generar_nuevo_enemigo()
        
        # ✅ CORRECCIÓN: Modo Escapa - verificar trampas
        if self.modo_actual == "escapa":
            for enemigo in self.enemigos[:]:  # Copiar lista para modificar
                if not enemigo.eliminado:
                    if self.jugador.verificar_trampa_activada(enemigo.obtener_posicion()):
                        enemigo.eliminar()
                        self.puntaje += 100  # ✅ +100 por trampa
                        self.mostrar_mensaje("¡Trampa activada! +100 pts", 1.0)
                        # ✅ CORRECCIÓN: Reaparecer inmediatamente
                        self.generar_nuevo_enemigo()
            
            # Verificar reaparición de enemigos (después de 10 segundos)
            for enemigo in self.enemigos:
                enemigo.verificar_reaparicion(self.mapa)
        
        # ✅ CORRECCIÓN: Modo Cazador - enemigos escapan por salidas
        if self.modo_actual == "cazador":
            for enemigo in self.enemigos[:]:  # Copiar lista
                if not enemigo.eliminado:
                    if enemigo.obtener_posicion() in self.salidas:
                        self.enemigos.remove(enemigo)
                        self.puntaje = max(0, self.puntaje - 50)  # ✅ -50 puntos
                        self.mostrar_mensaje("¡Enemigo escapó! -50 pts", 1.0)
                        # Generar nuevo enemigo
                        self.generar_nuevo_enemigo()
        
        # ✅ CORRECCIÓN: Verificar victoria (llegar a la salida)
        if pos_jugador in self.salidas:
            if self.modo_actual == "escapa":
                self.finalizar_juego_victoria()
    
    def generar_nuevo_enemigo(self):
        """Genera un nuevo enemigo en una posición válida"""
        posiciones_validas = self.mapa.obtener_posiciones_validas_para_captura(self.jugador)
        if posiciones_validas:
            pos = random.choice(posiciones_validas)
            nuevo_enemigo = Enemigo(pos[0], pos[1])
            self.enemigos.append(nuevo_enemigo)
    
    def dibujar_juego(self):
        """Dibuja el estado del juego"""
        # Calcular offset para centrar el mapa
        ancho_mapa = self.mapa.columnas * TAMANO_CELDA
        alto_mapa = self.mapa.filas * TAMANO_CELDA
        offset_x = 50
        offset_y = (ALTO_VENTANA - alto_mapa) // 2
        
        # Dibujar mapa
        for fila in range(self.mapa.filas):
            for col in range(self.mapa.columnas):
                x = offset_x + col * TAMANO_CELDA
                y = offset_y + fila * TAMANO_CELDA
                
                # Determinar color según tipo de terreno
                casilla = self.mapa.matriz[fila][col]
                codigo = casilla.codigo
                
                if codigo == 0:  # Camino
                    color = COLOR_CAMINO
                elif codigo == 1:  # Muro
                    color = COLOR_MURO
                elif codigo == 2:  # Túnel
                    color = COLOR_TUNEL
                elif codigo == 3:  # Liana
                    color = COLOR_LIANA
                else:
                    color = NEGRO
                
                pygame.draw.rect(self.ventana, color, (x, y, TAMANO_CELDA, TAMANO_CELDA))
                pygame.draw.rect(self.ventana, GRIS, (x, y, TAMANO_CELDA, TAMANO_CELDA), 1)
                
                # ✅ CORRECCIÓN: Dibujar todas las salidas
                if (fila, col) in self.salidas:
                    pygame.draw.rect(self.ventana, COLOR_SALIDA, 
                                   (x + 3, y + 3, TAMANO_CELDA - 6, TAMANO_CELDA - 6), 3)
        
        # ✅ CORRECCIÓN: Solo dibujar trampas en modo escapa
        if self.modo_actual == "escapa":
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
            fondo = pygame.Surface((texto_msg.get_width() + 20, texto_msg.get_height() + 10))
            fondo.fill(NEGRO)
            fondo.set_alpha(200)
            self.ventana.blit(fondo, (rect_msg.x - 10, rect_msg.y - 5))
            self.ventana.blit(texto_msg, rect_msg)
    
    def dibujar_hud(self, x, y):
        """Dibuja el HUD con información del juego"""
        y_actual = y
        
        # ✅ CORRECCIÓN: Mostrar tiempo según modo
        if self.modo_actual == "escapa":
            tiempo_texto = f"Tiempo: {int(time.time() - self.tiempo_inicio)}s"
        else:  # cazador
            tiempo_restante = self.tiempo_limite_cazador - int(time.time() - self.tiempo_inicio)
            tiempo_texto = f"Tiempo: {max(0, tiempo_restante)}s"
        
        # Información del jugador
        textos_info = [
            f"JUGADOR: {self.nombre_jugador}",
            f"MODO: {self.modo_actual.upper()}",
            f"DIFICULTAD: {self.dificultad.upper()}",
            "",
            tiempo_texto,
            f"Puntaje: {self.puntaje}",
        ]
        
        # ✅ Solo mostrar vidas en modo escapa
        if self.modo_actual == "escapa":
            textos_info.insert(5, f"Vidas: {'❤️ ' * self.jugador.vida}")
        
        for texto in textos_info:
            if texto == "":
                y_actual += 10
            else:
                superficie = self.fuente.render(texto, True, BLANCO)
                self.ventana.blit(superficie, (x, y_actual))
                y_actual += 25
        
        # BARRA DE ENERGÍA VISUAL
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
            "Flechas: Mover",
            "SHIFT: Correr (1s)",
        ]
        
        # ✅ Solo mostrar trampa en modo escapa
        if self.modo_actual == "escapa":
            controles.insert(2, "ESPACIO: Trampa")
        
        controles.extend([
            "",
            "LEYENDA:",
            "⚪ Blanco: Camino",
            "⬛ Gris: Muro",
            "🔵 Cyan: Túnel (solo jugador)",
            "🟢 Verde oscuro: Liana (solo enemigos)",
            "✨ Verde brillante: Salida",
            "🔵 Azul: Jugador",
            "🔴 Rojo: Enemigo",
        ])
        
        if self.modo_actual == "escapa":
            controles.append("🟡 Amarillo: Trampa")
        
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
        
        # ✅ CORRECCIÓN: Bonificación por salir + 1000 puntos
        self.puntaje += 1000
        
        # Multiplicador por dificultad
        multiplicadores = {"facil": 1.0, "normal": 1.5, "dificil": 2.0}
        mult = multiplicadores[self.dificultad]
        
        self.puntaje = int(self.puntaje * mult)
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
    
    def finalizar_juego_tiempo_cazador(self):
        """Finaliza el juego por tiempo en modo cazador"""
        multiplicadores = {"facil": 1.0, "normal": 1.5, "dificil": 2.0}
        mult = multiplicadores[self.dificultad]
        
        self.puntaje = int(self.puntaje * mult)
        self.sistema_puntuacion.guardar_puntaje(self.nombre_jugador, self.puntaje, self.modo_actual)
        
        self.estado = "game_over"
        self.mensaje = "TIEMPO AGOTADO"
    
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

if __name__ == "__main__":
    juego = JuegoPygame()
    juego.ejecutar()