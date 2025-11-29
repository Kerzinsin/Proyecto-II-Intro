"""
Juego Escapa del Laberinto
Instituto Tecnológico de Costa Rica
Proyecto 2 - Introducción a la Programación
"""

import pygame
import sys
import time
import random
import math
from pathlib import Path

from Modelos.mapa import Mapa
from Modelos.jugador import Jugador
from Modelos.enemigo import Enemigo
from Sistema.puntuacion import Puntuacion
from Sistema.sonidos import GestorSonidos

pygame.init()

ANCHO_VENTANA = 1400
ALTO_VENTANA = 800
FPS = 60

TAMANO_CELDA = 35

BLANCO = (255, 255, 255)
NEGRO = (15, 15, 20)  # Negro más suave
GRIS = (180, 180, 190)
GRIS_OSCURO = (40, 40, 50)
GRIS_CLARO = (220, 220, 230)

VERDE = (50, 255, 100)
VERDE_OSCURO = (0, 150, 50)
VERDE_BRILLANTE = (100, 255, 150)
ROJO = (255, 80, 80)
ROJO_OSCURO = (180, 0, 0)
AZUL = (80, 150, 255)
AZUL_OSCURO = (0, 100, 200)
AMARILLO = (255, 220, 50)
NARANJA = (255, 150, 50)
MORADO = (150, 100, 255)
CYAN = (50, 220, 255)
CYAN_OSCURO = (0, 180, 220)
VERDE_LIANA = (50, 150, 80)

COLOR_CAMINO = (240, 240, 250)
COLOR_MURO = (50, 50, 60)
COLOR_TUNEL = CYAN
COLOR_LIANA = VERDE_LIANA
COLOR_JUGADOR = AZUL
COLOR_ENEMIGO = ROJO
COLOR_TRAMPA = AMARILLO
COLOR_SALIDA = VERDE_BRILLANTE

COLOR_FONDO = (25, 25, 35)

class JuegoPygame:
    def __init__(self):
        """Inicializa el juego con Pygame"""
        self.ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        pygame.display.set_caption("Escapa del Laberinto - TEC")
        self.reloj = pygame.time.Clock()
        
        try:
            self.fuente = pygame.font.Font("arial.ttf", 20)
            self.fuente_grande = pygame.font.Font("arial.ttf", 32)
            self.fuente_titulo = pygame.font.Font("arial.ttf", 56)
        except:
            self.fuente = pygame.font.Font(None, 22)
            self.fuente_grande = pygame.font.Font(None, 36)
            self.fuente_titulo = pygame.font.Font(None, 48)
        
        self.sistema_puntuacion = Puntuacion()
        self.gestor_sonidos = GestorSonidos()
        self.estado = "menu_principal"
        self.nombre_jugador = ""
        self.dificultad = "normal"
        self.modo_actual = None
        
        self.mapa = None
        self.jugador = None
        self.enemigos = []
        self.tiempo_inicio = None
        self.puntaje = 0
        self.mensaje = ""
        self.tiempo_mensaje = 0
        self.salidas = []
        
        self.ultimo_movimiento_enemigos = time.time()
        self.intervalo_enemigos = 1.0
        
        self.tiempo_limite_cazador = 120
        self.ultimo_spawn_cazador = None
        
        self.animacion_tiempo = 0
        self.ultima_posicion_jugador = None
        
        # Tracking de puntos de trampa para modo escapa
        self.puntos_trampa = 0
        
        self.gestor_sonidos.reproducir_musica()
        
    def ejecutar(self):
        """Loop principal del juego"""
        ejecutando = True
        
        while ejecutando:
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
                elif self.estado == "puntajes":
                    self.manejar_eventos_puntajes(evento)
            
            if self.estado == "jugando":
                self.actualizar_juego()
            
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
            elif self.estado == "puntajes":
                self.dibujar_puntajes()
            
            pygame.display.flip()
            self.reloj.tick(FPS)
        pygame.quit()
        sys.exit()
    
    def dibujar_menu_principal(self):
        """Dibuja el menú principal"""
        self.ventana.fill(COLOR_FONDO)
        
        self.animacion_tiempo += 0.05
        
        titulo_texto = "ESCAPA DEL LABERINTO"
        titulo_sombra = self.fuente_titulo.render(titulo_texto, True, (0, 0, 0))
        rect_sombra = titulo_sombra.get_rect(center=(ANCHO_VENTANA // 2 + 3, 153))
        self.ventana.blit(titulo_sombra, rect_sombra)
        brillo = int(50 * math.sin(self.animacion_tiempo)) + 205
        color_titulo = (min(255, brillo), 255, min(255, brillo + 50))
        titulo = self.fuente_titulo.render(titulo_texto, True, color_titulo)
        rect_titulo = titulo.get_rect(center=(ANCHO_VENTANA // 2, 150))
        self.ventana.blit(titulo, rect_titulo)
        
        subtitulo = self.fuente_grande.render("Instituto Tecnológico de Costa Rica", True, GRIS_CLARO)
        rect_sub = subtitulo.get_rect(center=(ANCHO_VENTANA // 2, 220))
        self.ventana.blit(subtitulo, rect_sub)
        
        opciones = [
            ("1. JUGAR", VERDE),
            ("2. VER PUNTAJES", AMARILLO),
            ("3. SALIR", ROJO)
        ]
        
        y = 320
        for opcion, color in opciones:
            fondo_opcion = pygame.Surface((400, 50))
            fondo_opcion.set_alpha(100)
            fondo_opcion.fill(color)
            rect_fondo = fondo_opcion.get_rect(center=(ANCHO_VENTANA // 2, y))
            self.ventana.blit(fondo_opcion, rect_fondo)
            
            texto = self.fuente_grande.render(opcion, True, BLANCO)
            rect = texto.get_rect(center=(ANCHO_VENTANA // 2, y))
            self.ventana.blit(texto, rect)
            y += 70
        
        alpha = int(128 + 127 * math.sin(self.animacion_tiempo * 2))
        inst = self.fuente.render("Presiona 1, 2 o 3 para seleccionar", True, GRIS)
        inst.set_alpha(alpha)
        rect_inst = inst.get_rect(center=(ANCHO_VENTANA // 2, 550))
        self.ventana.blit(inst, rect_inst)
    
    def manejar_eventos_menu(self, evento):
        """Maneja eventos del menú principal"""
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_1:
                self.gestor_sonidos.reproducir_sonido('menu_click')
                self.estado = "registro"
            elif evento.key == pygame.K_2:
                self.gestor_sonidos.reproducir_sonido('menu_click')
                self.estado = "puntajes"
            elif evento.key == pygame.K_3:
                self.gestor_sonidos.reproducir_sonido('menu_click')
                pygame.quit()
                sys.exit()
    
    def dibujar_puntajes(self):
        """Dibuja la pantalla de puntajes"""
        self.ventana.fill(COLOR_FONDO)
        
        titulo = self.fuente_titulo.render("TABLA DE PUNTAJES", True, VERDE)
        rect_titulo = titulo.get_rect(center=(ANCHO_VENTANA // 2, 80))
        self.ventana.blit(titulo, rect_titulo)
        
        x_izq = ANCHO_VENTANA // 4
        x_der = 3 * ANCHO_VENTANA // 4
        y_inicio = 150
        
        fondo_escapa = pygame.Surface((350, 400))
        fondo_escapa.fill((40, 40, 50))
        fondo_escapa.set_alpha(200)
        rect_fondo_escapa = fondo_escapa.get_rect(center=(x_izq, y_inicio + 150))
        self.ventana.blit(fondo_escapa, rect_fondo_escapa)
        pygame.draw.rect(self.ventana, AZUL, rect_fondo_escapa, 3)
        
        titulo_escapa = self.fuente_grande.render("TOP 5 - MODO ESCAPA", True, AZUL)
        rect_escapa = titulo_escapa.get_rect(center=(x_izq, y_inicio))
        self.ventana.blit(titulo_escapa, rect_escapa)
        
        y = y_inicio + 50
        top_escapa = self.sistema_puntuacion.obtener_top("escapa")
        for i, p in enumerate(top_escapa, 1):
            color_puesto = AMARILLO if i == 1 else BLANCO
            texto = self.fuente.render(f"{i}. {p['nombre']}: {p['puntaje']} pts", True, color_puesto)
            self.ventana.blit(texto, (x_izq - 150, y))
            y += 30
        
        fondo_cazador = pygame.Surface((350, 400))
        fondo_cazador.fill((40, 40, 50))
        fondo_cazador.set_alpha(200)
        rect_fondo_cazador = fondo_cazador.get_rect(center=(x_der, y_inicio + 150))
        self.ventana.blit(fondo_cazador, rect_fondo_cazador)
        pygame.draw.rect(self.ventana, NARANJA, rect_fondo_cazador, 3)
        
        titulo_cazador = self.fuente_grande.render("TOP 5 - MODO CAZADOR", True, NARANJA)
        rect_cazador = titulo_cazador.get_rect(center=(x_der, y_inicio))
        self.ventana.blit(titulo_cazador, rect_cazador)
        
        y = y_inicio + 50
        top_cazador = self.sistema_puntuacion.obtener_top("cazador")
        for i, p in enumerate(top_cazador, 1):
            color_puesto = AMARILLO if i == 1 else BLANCO
            texto = self.fuente.render(f"{i}. {p['nombre']}: {p['puntaje']} pts", True, color_puesto)
            self.ventana.blit(texto, (x_der - 150, y))
            y += 30
        
        inst = self.fuente.render("Presiona ESC para volver al menú", True, GRIS_CLARO)
        rect_inst = inst.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA - 50))
        self.ventana.blit(inst, rect_inst)
    
    def manejar_eventos_puntajes(self, evento):
        """Maneja eventos de la pantalla de puntajes"""
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                self.gestor_sonidos.reproducir_sonido('menu_click')
                self.estado = "menu_principal"
    
    def dibujar_registro(self):
        """Dibuja la pantalla de registro"""
        self.ventana.fill(COLOR_FONDO)
        
        titulo_texto = "REGISTRO DE JUGADOR"
        titulo_sombra = self.fuente_grande.render(titulo_texto, True, (0, 0, 0))
        rect_sombra = titulo_sombra.get_rect(center=(ANCHO_VENTANA // 2 + 2, 202))
        self.ventana.blit(titulo_sombra, rect_sombra)
        
        titulo = self.fuente_grande.render(titulo_texto, True, VERDE)
        rect_titulo = titulo.get_rect(center=(ANCHO_VENTANA // 2, 200))
        self.ventana.blit(titulo, rect_titulo)
        
        instruccion = self.fuente_grande.render("Ingresa tu nombre (min. 3 caracteres):", True, BLANCO)
        rect_inst = instruccion.get_rect(center=(ANCHO_VENTANA // 2, 300))
        self.ventana.blit(instruccion, rect_inst)
        
        # Campo de entrada con fondo
        nombre_display = self.nombre_jugador + ("_" if int(time.time() * 2) % 2 else " ")
        nombre_texto = self.fuente_grande.render(nombre_display, True, AMARILLO)
        rect_nombre = nombre_texto.get_rect(center=(ANCHO_VENTANA // 2, 350))
        
        fondo_campo = pygame.Surface((400, 50))
        fondo_campo.fill((40, 40, 50))
        rect_fondo = fondo_campo.get_rect(center=(ANCHO_VENTANA // 2, 350))
        self.ventana.blit(fondo_campo, rect_fondo)
        pygame.draw.rect(self.ventana, AMARILLO, rect_fondo, 2)
        
        self.ventana.blit(nombre_texto, rect_nombre)
        
        info = self.fuente.render("Presiona ENTER para continuar", True, GRIS_CLARO)
        rect_info = info.get_rect(center=(ANCHO_VENTANA // 2, 450))
        self.ventana.blit(info, rect_info)
    
    def manejar_eventos_registro(self, evento):
        """Maneja eventos del registro"""
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN:
                if len(self.nombre_jugador) >= 3:
                    self.gestor_sonidos.reproducir_sonido('menu_click')
                    self.sistema_puntuacion.registrar_jugador(self.nombre_jugador)
                    self.estado = "seleccion_dificultad"
            elif evento.key == pygame.K_BACKSPACE:
                if len(self.nombre_jugador) > 0:
                    self.nombre_jugador = self.nombre_jugador[:-1]
            elif evento.unicode.isalnum() or evento.unicode == " ":
                if len(self.nombre_jugador) < 20:
                    self.nombre_jugador += evento.unicode
    
    def dibujar_seleccion_dificultad(self):
        """Dibuja la selección de dificultad"""
        self.ventana.fill(COLOR_FONDO)
        
        titulo = self.fuente_grande.render("SELECCIONA DIFICULTAD", True, VERDE)
        rect_titulo = titulo.get_rect(center=(ANCHO_VENTANA // 2, 150))
        self.ventana.blit(titulo, rect_titulo)
        
        opciones = [
            ("1. FACIL", "Menos enemigos, más lentos - Multiplicador: x1.0", VERDE),
            ("2. NORMAL", "Balance de enemigos - Multiplicador: x1.5", AMARILLO),
            ("3. DIFICIL", "Más enemigos, más rápidos - Multiplicador: x2.0", ROJO)
        ]
        
        y = 250
        for opcion, desc, color in opciones:
            fondo_opcion = pygame.Surface((600, 60))
            fondo_opcion.set_alpha(120)
            fondo_opcion.fill(color)
            rect_fondo = fondo_opcion.get_rect(center=(ANCHO_VENTANA // 2, y))
            self.ventana.blit(fondo_opcion, rect_fondo)
            
            texto = self.fuente_grande.render(opcion, True, BLANCO)
            rect = texto.get_rect(center=(ANCHO_VENTANA // 2, y - 10))
            self.ventana.blit(texto, rect)
            
            desc_texto = self.fuente.render(desc, True, GRIS_CLARO)
            rect_desc = desc_texto.get_rect(center=(ANCHO_VENTANA // 2, y + 20))
            self.ventana.blit(desc_texto, rect_desc)
            y += 90
        
        inst = self.fuente.render("Presiona 1, 2 o 3 para seleccionar", True, GRIS_CLARO)
        rect_inst = inst.get_rect(center=(ANCHO_VENTANA // 2, 550))
        self.ventana.blit(inst, rect_inst)
    
    def manejar_eventos_dificultad(self, evento):
        """Maneja eventos de selección de dificultad"""
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_1:
                self.gestor_sonidos.reproducir_sonido('menu_click')
                self.dificultad = "facil"
                self.estado = "seleccion_modo"
            elif evento.key == pygame.K_2:
                self.gestor_sonidos.reproducir_sonido('menu_click')
                self.dificultad = "normal"
                self.estado = "seleccion_modo"
            elif evento.key == pygame.K_3:
                self.gestor_sonidos.reproducir_sonido('menu_click')
                self.dificultad = "dificil"
                self.estado = "seleccion_modo"
    
    def dibujar_seleccion_modo(self):
        """Dibuja la selección de modo"""
        self.ventana.fill(COLOR_FONDO)
        
        titulo = self.fuente_grande.render("SELECCIONA MODO DE JUEGO", True, VERDE)
        rect_titulo = titulo.get_rect(center=(ANCHO_VENTANA // 2, 150))
        self.ventana.blit(titulo, rect_titulo)
        
        opciones = [
            ("1. MODO ESCAPA", "Huye de los cazadores y llega a la salida", AZUL),
            ("2. MODO CAZADOR", "Atrapa a los enemigos antes de que escapen", NARANJA)
        ]
        
        y = 280
        for opcion, desc, color in opciones:
            fondo_opcion = pygame.Surface((700, 70))
            fondo_opcion.set_alpha(130)
            fondo_opcion.fill(color)
            rect_fondo = fondo_opcion.get_rect(center=(ANCHO_VENTANA // 2, y))
            self.ventana.blit(fondo_opcion, rect_fondo)
            
            texto = self.fuente_grande.render(opcion, True, BLANCO)
            rect = texto.get_rect(center=(ANCHO_VENTANA // 2, y - 10))
            self.ventana.blit(texto, rect)
            
            desc_texto = self.fuente.render(desc, True, GRIS_CLARO)
            rect_desc = desc_texto.get_rect(center=(ANCHO_VENTANA // 2, y + 25))
            self.ventana.blit(desc_texto, rect_desc)
            y += 120
        
        inst = self.fuente.render("Presiona 1 o 2 para seleccionar", True, GRIS_CLARO)
        rect_inst = inst.get_rect(center=(ANCHO_VENTANA // 2, 520))
        self.ventana.blit(inst, rect_inst)
    
    def manejar_eventos_modo(self, evento):
        """Maneja eventos de selección de modo"""
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_1:
                self.gestor_sonidos.reproducir_sonido('menu_click')
                self.modo_actual = "escapa"
                self.iniciar_juego()
            elif evento.key == pygame.K_2:
                self.gestor_sonidos.reproducir_sonido('menu_click')
                self.modo_actual = "cazador"
                self.iniciar_juego()
    
    def iniciar_juego(self):
        """Inicia una nueva partida"""
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
        
        self.mapa = Mapa(20, 25)
        
        if self.modo_actual == "escapa":
            self.salidas = [self.mapa.pos_salida]
            config = config_escapa[self.dificultad]
        else:
            config = config_cazador[self.dificultad]
            num_salidas = config["salidas"]
            self.salidas = self.mapa.generar_salidas_multiples(num_salidas)
        
        self.jugador = Jugador(*self.mapa.pos_inicio)
        
        num_enemigos = config["enemigos"]
        self.intervalo_enemigos = config["intervalo"]
        
        self.enemigos = []
        posiciones_validas = self.mapa.obtener_posiciones_validas_enemigo()
        
        for i in range(num_enemigos):
            if posiciones_validas:
                pos = random.choice(posiciones_validas)
                posiciones_validas.remove(pos)
                enemigo = Enemigo(pos[0], pos[1], dificultad=self.dificultad)
                self.enemigos.append(enemigo)
        
        if self.modo_actual == "escapa":
            self.puntaje = 1500
            self.puntos_trampa = 0
        else:
            self.puntaje = 0
            self.puntos_trampa = 0
        
        self.tiempo_inicio = time.time()
        self.ultimo_movimiento_enemigos = time.time()
        self.ultimo_spawn_cazador = time.time()
        self.estado = "jugando"
    
    def manejar_eventos_juego(self, evento):
        """Maneja eventos durante el juego"""
        if evento.type == pygame.KEYDOWN:
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
                if self.modo_actual == "escapa":
                    # Verificar cooldown de 5 segundos después de matar un enemigo
                    pos_actual = self.jugador.obtener_posicion()
                    tiempo_actual = time.time()
                    if pos_actual in self.jugador.cooldown_trampa:
                        tiempo_cooldown = self.jugador.cooldown_trampa[pos_actual]
                        if tiempo_actual - tiempo_cooldown < 5:
                            tiempo_restante = int(5 - (tiempo_actual - tiempo_cooldown))
                            self.mostrar_mensaje(f"Cooldown: {tiempo_restante}s", 1.0)
                            return
                    
                    if self.jugador.colocar_trampa():
                        self.gestor_sonidos.reproducir_sonido('trampa_colocada')
                        self.mostrar_mensaje("¡Trampa colocada!", 1.0)
            elif evento.key in [pygame.K_LSHIFT, pygame.K_RSHIFT]:
                if self.jugador.energia >= 100:
                    self.gestor_sonidos.reproducir_sonido('correr')
                self.jugador.activar_correr()
            
            if direccion:
                pos_anterior = self.jugador.obtener_posicion()
                if self.jugador.mover(direccion, self.mapa):
                    pos_nueva = self.jugador.obtener_posicion()
                    if pos_anterior != pos_nueva:
                        self.gestor_sonidos.reproducir_sonido('movimiento', 0.3)
                        self.ultima_posicion_jugador = pos_anterior
    
    def actualizar_juego(self):
        """Actualiza la lógica del juego"""
        tiempo_actual = time.time()
        
        self.jugador.actualizar_energia(self.mapa)
        
        if self.modo_actual == "cazador":
            tiempo_transcurrido = tiempo_actual - self.tiempo_inicio
            if tiempo_transcurrido >= self.tiempo_limite_cazador:
                self.finalizar_juego_tiempo_cazador()
                return
        
        if self.modo_actual == "escapa":
            tiempo_transcurrido = tiempo_actual - self.tiempo_inicio
            puntos_perdidos = int(tiempo_transcurrido / 5) * 50
            self.puntaje = max(0, 1500 - puntos_perdidos)
        
        if tiempo_actual - self.ultimo_movimiento_enemigos >= self.intervalo_enemigos:
            for enemigo in self.enemigos:
                if not enemigo.eliminado:
                    if self.modo_actual == "escapa":
                        enemigo.mover_hacia(self.jugador, self.mapa)
                    else:
                        enemigo.huir_hacia_salida(self.jugador, self.mapa, self.salidas)
            self.ultimo_movimiento_enemigos = tiempo_actual
        
        pos_jugador = self.jugador.obtener_posicion()
        for enemigo in self.enemigos:
            if not enemigo.eliminado:
                if pos_jugador == enemigo.obtener_posicion():
                    if self.modo_actual == "escapa":
                        if self.jugador.perder_vida():
                            self.gestor_sonidos.reproducir_sonido('derrota')
                            self.finalizar_juego_derrota()
                            return
                        else:
                            self.gestor_sonidos.reproducir_sonido('vida_perdida')
                            self.jugador.fila, self.jugador.columna = self.mapa.pos_inicio
                            self.mostrar_mensaje(f"¡Atrapado! Vidas: {self.jugador.vida}", 2.0)
                    else:
                        self.gestor_sonidos.reproducir_sonido('enemigo_atrapado')
                        self.enemigos.remove(enemigo)
                        self.puntaje += 100
                        self.mostrar_mensaje("¡Enemigo atrapado! +100 pts", 1.0)
                        self.generar_nuevo_enemigo()
        
        if self.modo_actual == "escapa":
            for enemigo in self.enemigos[:]:
                if not enemigo.eliminado:
                    if self.jugador.verificar_trampa_activada(enemigo.obtener_posicion()):
                        self.gestor_sonidos.reproducir_sonido('trampa_activada')
                        enemigo.eliminar()
                        puntos_trampa = 100
                        self.puntaje += puntos_trampa
                        self.puntos_trampa += puntos_trampa
                        self.mostrar_mensaje("¡Trampa activada! +100 pts", 1.0)
                        # Activar cooldown de 5 segundos para la posición de la trampa
                        pos_trampa = enemigo.obtener_posicion()
                        self.jugador.cooldown_trampa[pos_trampa] = time.time()
                        self.generar_nuevo_enemigo()
            
            for enemigo in self.enemigos:
                enemigo.verificar_reaparicion(self.mapa)
        
        if self.modo_actual == "cazador":
            for enemigo in self.enemigos[:]:
                if not enemigo.eliminado:
                    if enemigo.obtener_posicion() in self.salidas:
                        self.gestor_sonidos.reproducir_sonido('enemigo_escapo')
                        self.enemigos.remove(enemigo)
                        self.puntaje = max(0, self.puntaje - 50)
                        self.mostrar_mensaje("¡Enemigo escapó! -50 pts", 1.0)
                        self.generar_nuevo_enemigo()
        
        if pos_jugador in self.salidas:
            if self.modo_actual == "escapa":
                self.gestor_sonidos.reproducir_sonido('victoria')
                self.finalizar_juego_victoria()
        
        codigo_actual = self.mapa.obtener_codigo(pos_jugador[0], pos_jugador[1])
        if codigo_actual == self.mapa.CODIGO_TUNEL and self.jugador.energia < 100:
            if random.random() < 0.1:
                self.gestor_sonidos.reproducir_sonido('energia_recuperada', 0.2)
    
    def generar_nuevo_enemigo(self):
        """Genera un nuevo enemigo en una posición válida"""
        posiciones_validas = self.mapa.obtener_posiciones_validas_para_captura(self.jugador)
        if posiciones_validas:
            pos = random.choice(posiciones_validas)
            nuevo_enemigo = Enemigo(pos[0], pos[1], dificultad=self.dificultad)
            self.enemigos.append(nuevo_enemigo)
    
    def dibujar_juego(self):
        """Dibuja el estado del juego"""
        self.ventana.fill(COLOR_FONDO)
        
        ancho_mapa = self.mapa.columnas * TAMANO_CELDA
        alto_mapa = self.mapa.filas * TAMANO_CELDA
        offset_x = 50
        offset_y = (ALTO_VENTANA - alto_mapa) // 2
        
        self.animacion_tiempo += 0.1
        
        for fila in range(self.mapa.filas):
            for col in range(self.mapa.columnas):
                x = offset_x + col * TAMANO_CELDA
                y = offset_y + fila * TAMANO_CELDA
                
                codigo = self.mapa.obtener_codigo(fila, col)
                
                if codigo == 0:  # Camino
                    color_base = COLOR_CAMINO
                    color_borde = GRIS_CLARO
                elif codigo == 1:
                    color_base = COLOR_MURO
                    color_borde = GRIS_OSCURO
                elif codigo == 2:
                    pulsacion = int(20 * math.sin(self.animacion_tiempo * 2))
                    color_base = (min(255, CYAN[0] + pulsacion), 
                                 min(255, CYAN[1] + pulsacion), 
                                 min(255, CYAN[2] + pulsacion))
                    color_borde = CYAN_OSCURO
                elif codigo == 3:
                    color_base = COLOR_LIANA
                    color_borde = VERDE_OSCURO
                else:
                    color_base = NEGRO
                    color_borde = GRIS_OSCURO
                
                pygame.draw.rect(self.ventana, (0, 0, 0), 
                               (x + 2, y + 2, TAMANO_CELDA, TAMANO_CELDA))
                pygame.draw.rect(self.ventana, color_base, 
                               (x, y, TAMANO_CELDA, TAMANO_CELDA))
                pygame.draw.rect(self.ventana, color_borde, 
                               (x, y, TAMANO_CELDA, TAMANO_CELDA), 2)
                
                if (fila, col) in self.salidas:
                    brillo = int(50 * math.sin(self.animacion_tiempo * 3))
                    color_salida = (min(255, VERDE_BRILLANTE[0] + brillo),
                                   min(255, VERDE_BRILLANTE[1] + brillo),
                                   min(255, VERDE_BRILLANTE[2] + brillo))
                    pygame.draw.rect(self.ventana, color_salida, 
                                   (x + 2, y + 2, TAMANO_CELDA - 4, TAMANO_CELDA - 4), 3)
                    pygame.draw.circle(self.ventana, (255, 255, 255, 100), 
                                     (x + TAMANO_CELDA // 2, y + TAMANO_CELDA // 2), 
                                     TAMANO_CELDA // 3)
        
        if self.modo_actual == "escapa":
            for trampa in self.jugador.trampas_activas:
                fila, col = trampa['posicion']
                x = offset_x + col * TAMANO_CELDA
                y = offset_y + fila * TAMANO_CELDA
                centro_x = x + TAMANO_CELDA // 2
                centro_y = y + TAMANO_CELDA // 2
                
                pulsacion = int(5 * math.sin(self.animacion_tiempo * 4))
                radio = TAMANO_CELDA // 4 + pulsacion
                
                pygame.draw.circle(self.ventana, (0, 0, 0, 100),
                                 (centro_x + 2, centro_y + 2), radio)
                pygame.draw.circle(self.ventana, COLOR_TRAMPA,
                                 (centro_x, centro_y), radio)
                pygame.draw.circle(self.ventana, NARANJA,
                                 (centro_x, centro_y), radio, 2)
        
        for enemigo in self.enemigos:
            if not enemigo.eliminado:
                fila, col = enemigo.obtener_posicion()
                x = offset_x + col * TAMANO_CELDA
                y = offset_y + fila * TAMANO_CELDA
                centro_x = x + TAMANO_CELDA // 2
                centro_y = y + TAMANO_CELDA // 2
                radio = TAMANO_CELDA // 3
                
                pygame.draw.circle(self.ventana, (0, 0, 0, 150),
                                 (centro_x + 2, centro_y + 2), radio)
                pygame.draw.circle(self.ventana, COLOR_ENEMIGO,
                                 (centro_x, centro_y), radio)
                pygame.draw.circle(self.ventana, ROJO_OSCURO,
                                 (centro_x, centro_y), radio, 2)
                pygame.draw.circle(self.ventana, BLANCO,
                                 (centro_x - 4, centro_y - 4), 2)
                pygame.draw.circle(self.ventana, BLANCO,
                                 (centro_x + 4, centro_y - 4), 2)
        
        fila, col = self.jugador.obtener_posicion()
        x = offset_x + col * TAMANO_CELDA
        y = offset_y + fila * TAMANO_CELDA
        centro_x = x + TAMANO_CELDA // 2
        centro_y = y + TAMANO_CELDA // 2
        radio = TAMANO_CELDA // 3
        
        if self.jugador.corriendo:
            brillo = int(30 * math.sin(self.animacion_tiempo * 6))
            radio_brillo = radio + brillo // 3
            pygame.draw.circle(self.ventana, (255, 255, 255, 100), 
                             (centro_x, centro_y), radio_brillo)
        
        pygame.draw.circle(self.ventana, (0, 0, 0, 150),
                         (centro_x + 2, centro_y + 2), radio)
        pygame.draw.circle(self.ventana, COLOR_JUGADOR,
                         (centro_x, centro_y), radio)
        pygame.draw.circle(self.ventana, AZUL_OSCURO,
                         (centro_x, centro_y), radio, 2)
        pygame.draw.circle(self.ventana, BLANCO,
                         (centro_x - 3, centro_y - 3), 2)
        pygame.draw.circle(self.ventana, BLANCO,
                         (centro_x + 3, centro_y - 3), 2)
        
        hud_x = offset_x + self.mapa.columnas * TAMANO_CELDA + 40
        self.dibujar_hud(hud_x, offset_y)
        
        if self.mensaje and time.time() - self.tiempo_mensaje < 2.0:
            texto_msg = self.fuente_grande.render(self.mensaje, True, AMARILLO)
            rect_msg = texto_msg.get_rect(center=(ANCHO_VENTANA // 2, 50))
            
            fondo = pygame.Surface((texto_msg.get_width() + 30, texto_msg.get_height() + 20))
            fondo.fill(NEGRO)
            fondo.set_alpha(220)
            self.ventana.blit(fondo, (rect_msg.x - 15, rect_msg.y - 10))
            
            pygame.draw.rect(self.ventana, AMARILLO, 
                           (rect_msg.x - 15, rect_msg.y - 10, 
                            texto_msg.get_width() + 30, texto_msg.get_height() + 20), 3)
            
            self.ventana.blit(texto_msg, rect_msg)
    
    def dibujar_hud(self, x, y):
        """Dibuja el HUD con información del juego"""
        fondo_hud = pygame.Surface((280, ALTO_VENTANA - y))
        fondo_hud.fill((30, 30, 40))
        fondo_hud.set_alpha(230)
        self.ventana.blit(fondo_hud, (x - 20, y - 10))
        pygame.draw.rect(self.ventana, AZUL, (x - 20, y - 10, 280, ALTO_VENTANA - y), 2)
        
        y_actual = y
        
        if self.modo_actual == "escapa":
            tiempo_texto = f"Tiempo: {int(time.time() - self.tiempo_inicio)}s"
            color_tiempo = BLANCO
        else:
            tiempo_restante = self.tiempo_limite_cazador - int(time.time() - self.tiempo_inicio)
            tiempo_texto = f"Tiempo: {max(0, tiempo_restante)}s"
            if tiempo_restante <= 30:
                color_tiempo = ROJO
            elif tiempo_restante <= 60:
                color_tiempo = AMARILLO
            else:
                color_tiempo = BLANCO
        
        textos_info = [
            (f"JUGADOR: {self.nombre_jugador}", VERDE),
            (f"MODO: {self.modo_actual.upper()}", AMARILLO),
            (f"DIFICULTAD: {self.dificultad.upper()}", NARANJA),
            ("", None),
            (tiempo_texto, color_tiempo if self.modo_actual == "cazador" else BLANCO),
            (f"Puntaje: {self.puntaje}", AMARILLO),
        ]
        
        if self.modo_actual == "escapa":
            vidas_texto = f"Vidas: {'❤️ ' * self.jugador.vida}"
            textos_info.insert(5, (vidas_texto, ROJO if self.jugador.vida <= 1 else BLANCO))
        
        for texto, color in textos_info:
            if texto == "":
                y_actual += 10
            else:
                superficie = self.fuente.render(texto, True, color)
                self.ventana.blit(superficie, (x, y_actual))
                y_actual += 25
        
        y_actual += 10
        energia_texto = self.fuente.render("ENERGÍA:", True, BLANCO)
        self.ventana.blit(energia_texto, (x, y_actual))
        y_actual += 25
        
        barra_ancho = 200
        barra_alto = 25
        energia_porcentaje = self.jugador.energia / 100
        
        pygame.draw.rect(self.ventana, (0, 0, 0),
                       (x + 2, y_actual + 2, barra_ancho, barra_alto))
        
        pygame.draw.rect(self.ventana, BLANCO, (x, y_actual, barra_ancho, barra_alto), 2)
        
        if energia_porcentaje > 0.6:
            color_energia = VERDE
        elif energia_porcentaje > 0.3:
            color_energia = AMARILLO
        else:
            color_energia = ROJO
        
        if energia_porcentaje >= 1.0:
            brillo = int(30 * math.sin(self.animacion_tiempo * 4))
            color_energia = (min(255, VERDE[0] + brillo), 
                           min(255, VERDE[1] + brillo), 
                           min(255, VERDE[2] + brillo))
        
        pygame.draw.rect(self.ventana, color_energia, 
                        (x + 2, y_actual + 2, 
                         int((barra_ancho - 4) * energia_porcentaje), 
                         barra_alto - 4))
        
        texto_porcentaje = self.fuente.render(f"{self.jugador.energia}%", True, BLANCO)
        self.ventana.blit(texto_porcentaje, (x + barra_ancho + 10, y_actual))
        y_actual += 40
        
        y_actual += 20
        titulo_controles = self.fuente.render("CONTROLES:", True, CYAN)
        self.ventana.blit(titulo_controles, (x, y_actual))
        y_actual += 25
        
        controles = [
            "Flechas: Mover",
            "SHIFT: Correr (1s)",
        ]
        
        if self.modo_actual == "escapa":
            controles.insert(1, "ESPACIO: Trampa")
        
        for texto in controles:
            superficie = self.fuente.render(texto, True, GRIS_CLARO)
            self.ventana.blit(superficie, (x, y_actual))
            y_actual += 22
        
        y_actual += 10
        titulo_leyenda = self.fuente.render("LEYENDA:", True, CYAN)
        self.ventana.blit(titulo_leyenda, (x, y_actual))
        y_actual += 25
        
        leyenda_items = [
            ("Blanco", COLOR_CAMINO, "Camino"),
            ("Gris", COLOR_MURO, "Muro"),
            ("Cyan", COLOR_TUNEL, "Túnel (jugador)"),
            ("Verde oscuro", COLOR_LIANA, "Liana (enemigos)"),
            ("Verde brillante", COLOR_SALIDA, "Salida"),
            ("Azul", COLOR_JUGADOR, "Jugador"),
            ("Rojo", COLOR_ENEMIGO, "Enemigo"),
        ]
        
        if self.modo_actual == "escapa":
            leyenda_items.append(("Amarillo", COLOR_TRAMPA, "Trampa"))
        
        for color_nombre, color_rgb, descripcion in leyenda_items:
            pygame.draw.rect(self.ventana, color_rgb, (x, y_actual, 15, 15))
            texto_leyenda = self.fuente.render(f"{color_nombre}: {descripcion}", True, GRIS_CLARO)
            self.ventana.blit(texto_leyenda, (x + 20, y_actual))
            y_actual += 20
    
    def mostrar_mensaje(self, mensaje, duracion):
        """Muestra un mensaje temporal"""
        self.mensaje = mensaje
        self.tiempo_mensaje = time.time()
    
    def finalizar_juego_victoria(self):
        """Finaliza el juego con victoria"""
        tiempo_total = int(time.time() - self.tiempo_inicio)
        
        # Asegurar que los puntos de trampa estén incluidos
        # Los puntos de trampa ya están en self.puntaje, pero los guardamos explícitamente
        self.puntaje += 1000
        
        multiplicadores = {"facil": 1.0, "normal": 1.5, "dificil": 2.0}
        mult = multiplicadores[self.dificultad]
        
        # El puntaje ya incluye los puntos de trampa (self.puntos_trampa está incluido en self.puntaje)
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
        self.gestor_sonidos.reproducir_sonido('derrota')
        multiplicadores = {"facil": 1.0, "normal": 1.5, "dificil": 2.0}
        mult = multiplicadores[self.dificultad]
        
        self.puntaje = int(self.puntaje * mult)
        self.sistema_puntuacion.guardar_puntaje(self.nombre_jugador, self.puntaje, self.modo_actual)
        
        self.estado = "game_over"
        self.mensaje = "TIEMPO AGOTADO"
    
    def dibujar_game_over(self):
        """Dibuja la pantalla de game over"""
        self.ventana.fill(COLOR_FONDO)
        
        self.animacion_tiempo += 0.1
        
        es_victoria = "VICTORIA" in self.mensaje
        color_titulo = VERDE if es_victoria else ROJO
        
        if es_victoria:
            brillo = int(50 * math.sin(self.animacion_tiempo * 3))
            color_titulo = (min(255, VERDE[0] + brillo), 
                           min(255, VERDE[1] + brillo), 
                           min(255, VERDE[2] + brillo))
        
        titulo_sombra = self.fuente_titulo.render(self.mensaje, True, (0, 0, 0))
        rect_sombra = titulo_sombra.get_rect(center=(ANCHO_VENTANA // 2 + 3, 203))
        self.ventana.blit(titulo_sombra, rect_sombra)
        
        titulo = self.fuente_titulo.render(self.mensaje, True, color_titulo)
        rect_titulo = titulo.get_rect(center=(ANCHO_VENTANA // 2, 200))
        self.ventana.blit(titulo, rect_titulo)
        
        puntaje_texto = self.fuente_grande.render(f"Puntaje Final: {self.puntaje}", True, AMARILLO)
        rect_puntaje = puntaje_texto.get_rect(center=(ANCHO_VENTANA // 2, 300))
        
        fondo_puntaje = pygame.Surface((puntaje_texto.get_width() + 40, puntaje_texto.get_height() + 20))
        fondo_puntaje.fill((40, 40, 50))
        fondo_puntaje.set_alpha(200)
        rect_fondo_puntaje = fondo_puntaje.get_rect(center=(ANCHO_VENTANA // 2, 300))
        self.ventana.blit(fondo_puntaje, rect_fondo_puntaje)
        pygame.draw.rect(self.ventana, AMARILLO, rect_fondo_puntaje, 2)
        
        self.ventana.blit(puntaje_texto, rect_puntaje)
        
        inst = self.fuente.render("Presiona ESPACIO para volver al menú", True, GRIS_CLARO)
        rect_inst = inst.get_rect(center=(ANCHO_VENTANA // 2, 400))
        self.ventana.blit(inst, rect_inst)
    
    def manejar_eventos_game_over(self, evento):
        """Maneja eventos de game over"""
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                self.gestor_sonidos.reproducir_sonido('menu_click')
                self.nombre_jugador = ""
                self.estado = "menu_principal"

if __name__ == "__main__":
    juego = JuegoPygame()
    juego.ejecutar()