"""
Juego Escapa del Laberinto - Versión Pygame
Interfaz gráfica para el proyecto de Introducción a la Programación
"""

import pygame
import sys
import time
from pathlib import Path

# Importar las clases del proyecto original
sys.path.insert(0, str(Path(__file__).parent / "Proyecto 2 Introducción"))
from Modelos.mapa import Mapa
from Modelos.jugador import Jugador
from Modelos.enemigo import Enemigo
from Sistema.puntuacion import Puntuacion

# Inicializar Pygame
pygame.init()

# Constantes de la ventana
ANCHO_VENTANA = 1200
ALTO_VENTANA = 800
FPS = 30

# Tamaño de celda
TAMANO_CELDA = 40

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (128, 128, 128)
GRIS_OSCURO = (64, 64, 64)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)
NARANJA = (255, 165, 0)
MORADO = (128, 0, 128)
CYAN = (0, 255, 255)
VERDE_OSCURO = (0, 128, 0)

# Colores para terrenos
COLOR_CAMINO = BLANCO
COLOR_MURO = GRIS_OSCURO
COLOR_TUNEL = CYAN
COLOR_LIANA = VERDE_OSCURO
COLOR_JUGADOR = AZUL
COLOR_ENEMIGO = ROJO
COLOR_TRAMPA = AMARILLO
COLOR_SALIDA = VERDE


class JuegoPygame:
    """Clase principal del juego con interfaz Pygame"""
    
    def __init__(self):
        """Inicializa el juego con Pygame"""
        self.ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        pygame.display.set_caption("Escapa del Laberinto")
        self.reloj = pygame.time.Clock()
        self.fuente = pygame.font.Font(None, 24)
        self.fuente_grande = pygame.font.Font(None, 36)
        self.fuente_titulo = pygame.font.Font(None, 48)
        
        self.sistema_puntuacion = Puntuacion()
        self.estado = "menu_principal"  # menu_principal, registro, seleccion_dificultad, seleccion_modo, jugando, game_over
        self.nombre_jugador = ""
        self.dificultad = "normal"
        self.modo_actual = None  # "escapa" o "cazador"
        
        # Variables del juego
        self.mapa = None
        self.jugador = None
        self.enemigos = []
        self.tiempo_inicio = None
        self.puntaje = 0
        self.mensaje = ""
        self.tiempo_mensaje = 0
        
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
        # Título
        titulo = self.fuente_titulo.render("ESCAPA DEL LABERINTO", True, VERDE)
        rect_titulo = titulo.get_rect(center=(ANCHO_VENTANA // 2, 150))
        self.ventana.blit(titulo, rect_titulo)
        
        # Opciones
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
        
        # Instrucciones
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
        
        # Mostrar nombre actual
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
        import random
        
        # Crear mapa
        self.mapa = Mapa(15, 20)  # Más pequeño para mejor visualización
        
        # Crear jugador
        self.jugador = Jugador(0, 0)
        
        # Configuración según dificultad
        config = {
            "facil": {"enemigos": 2, "velocidad": 0.5},
            "normal": {"enemigos": 3, "velocidad": 1.0},
            "dificil": {"enemigos": 5, "velocidad": 1.5}
        }
        
        cfg = config[self.dificultad]
        
        # Crear enemigos
        self.enemigos = []
        posiciones_validas = self.mapa.obtener_posiciones_validas_enemigo()
        
        for i in range(cfg["enemigos"]):
            if posiciones_validas:
                pos = random.choice(posiciones_validas)
                posiciones_validas.remove(pos)
                self.enemigos.append(Enemigo(pos[0], pos[1], velocidad=cfg["velocidad"]))
        
        self.tiempo_inicio = time.time()
        self.puntaje = 0
        self.estado = "jugando"
    
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
            
            if movido and self.modo_actual == "escapa":
                # Mover enemigos en modo escapa
                for enemigo in self.enemigos:
                    if not enemigo.eliminado:
                        enemigo.mover_hacia(self.jugador, self.mapa)
                
                # Verificar colisiones con trampas
                for enemigo in self.enemigos:
                    if not enemigo.eliminado:
                        if self.jugador.verificar_trampa_activada(enemigo.obtener_posicion()):
                            enemigo.eliminar()
                            self.puntaje += 50
                            self.mostrar_mensaje("¡Trampa activada! +50 puntos", 1.0)
    
    def actualizar_juego(self):
        """Actualiza el estado del juego"""
        if self.modo_actual == "escapa":
            self.actualizar_modo_escapa()
        elif self.modo_actual == "cazador":
            self.actualizar_modo_cazador()
        
        # Verificar reaparición de enemigos
        for enemigo in self.enemigos:
            enemigo.verificar_reaparicion(self.mapa)
    
    def actualizar_modo_escapa(self):
        """Actualiza la lógica del modo escapa"""
        # Verificar si llegó a la salida
        if self.jugador.obtener_posicion() == self.mapa.pos_salida:
            self.finalizar_juego_victoria()
        
        # Verificar colisiones con enemigos
        for enemigo in self.enemigos:
            if not enemigo.eliminado and self.jugador.obtener_posicion() == enemigo.obtener_posicion():
                if self.jugador.perder_vida():
                    self.finalizar_juego_derrota()
                else:
                    self.mostrar_mensaje(f"¡Atrapado! Vidas: {self.jugador.vida}", 2.0)
    
    def actualizar_modo_cazador(self):
        """Actualiza la lógica del modo cazador"""
        # Mover enemigos (huyen del jugador)
        for enemigo in self.enemigos:
            if not enemigo.eliminado:
                enemigo.huir_de(self.jugador, self.mapa)
        
        # Verificar si atrapó un enemigo
        for enemigo in self.enemigos:
            if not enemigo.eliminado and self.jugador.obtener_posicion() == enemigo.obtener_posicion():
                self.puntaje += 100
                enemigo.eliminar()
                self.mostrar_mensaje("¡Enemigo atrapado! +100 puntos", 1.0)
    
    def dibujar_juego(self):
        """Dibuja el estado del juego"""
        # Calcular offset para centrar el mapa
        offset_x = (ANCHO_VENTANA - self.mapa.columnas * TAMANO_CELDA) // 2 - 100
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
                elif casilla.codigo == 2:  # Tunel
                    color = COLOR_TUNEL
                elif casilla.codigo == 3:  # Liana
                    color = COLOR_LIANA
                
                # Dibujar casilla
                pygame.draw.rect(self.ventana, color, (x, y, TAMANO_CELDA, TAMANO_CELDA))
                pygame.draw.rect(self.ventana, GRIS, (x, y, TAMANO_CELDA, TAMANO_CELDA), 1)
                
                # Marcar salida
                if (fila, col) == self.mapa.pos_salida:
                    pygame.draw.rect(self.ventana, COLOR_SALIDA, (x + 5, y + 5, TAMANO_CELDA - 10, TAMANO_CELDA - 10))
        
        # Dibujar trampas
        for trampa in self.jugador.trampas_activas:
            fila, col = trampa['posicion']
            x = offset_x + col * TAMANO_CELDA
            y = offset_y + fila * TAMANO_CELDA
            pygame.draw.circle(self.ventana, COLOR_TRAMPA, (x + TAMANO_CELDA // 2, y + TAMANO_CELDA // 2), TAMANO_CELDA // 3)
        
        # Dibujar enemigos
        for enemigo in self.enemigos:
            if not enemigo.eliminado:
                fila, col = enemigo.obtener_posicion()
                x = offset_x + col * TAMANO_CELDA
                y = offset_y + fila * TAMANO_CELDA
                pygame.draw.circle(self.ventana, COLOR_ENEMIGO, (x + TAMANO_CELDA // 2, y + TAMANO_CELDA // 2), TAMANO_CELDA // 3)
        
        # Dibujar jugador
        fila, col = self.jugador.obtener_posicion()
        x = offset_x + col * TAMANO_CELDA
        y = offset_y + fila * TAMANO_CELDA
        pygame.draw.circle(self.ventana, COLOR_JUGADOR, (x + TAMANO_CELDA // 2, y + TAMANO_CELDA // 2), TAMANO_CELDA // 3)
        
        # Dibujar HUD (panel derecho)
        self.dibujar_hud(offset_x + self.mapa.columnas * TAMANO_CELDA + 20, offset_y)
        
        # Mostrar mensaje temporal si existe
        if self.mensaje and time.time() - self.tiempo_mensaje < 2.0:
            texto_msg = self.fuente.render(self.mensaje, True, AMARILLO)
            rect_msg = texto_msg.get_rect(center=(ANCHO_VENTANA // 2, 50))
            self.ventana.blit(texto_msg, rect_msg)
    
    def dibujar_hud(self, x, y):
        """Dibuja el HUD con información del juego"""
        textos = [
            f"Jugador: {self.nombre_jugador}",
            f"Modo: {self.modo_actual.upper()}",
            f"Dificultad: {self.dificultad.upper()}",
            "",
            f"Tiempo: {int(time.time() - self.tiempo_inicio)}s",
            f"Vidas: {self.jugador.vida}",
            f"Energia: {self.jugador.energia}/100",
            f"Puntaje: {self.puntaje}",
            "",
            "CONTROLES:",
            "WASD / Flechas: Mover",
            "ESPACIO: Trampa",
            "SHIFT: Correr",
            "",
            "LEYENDA:",
            "• Blanco: Camino",
            "• Gris: Muro",
            "• Cyan: Tunel",
            "• Verde: Liana/Salida",
            "• Azul: Jugador",
            "• Rojo: Enemigo",
            "• Amarillo: Trampa"
        ]
        
        y_actual = y
        for texto in textos:
            if texto == "":
                y_actual += 10
            else:
                superficie = self.fuente.render(texto, True, BLANCO)
                self.ventana.blit(superficie, (x, y_actual))
                y_actual += 25
    
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
        titulo = self.fuente_titulo.render(self.mensaje, True, VERDE if "VICTORIA" in self.mensaje else ROJO)
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
        """Muestra los puntajes (simplificado para Pygame)"""
        # Por ahora solo imprime en consola
        # Podrías hacer una pantalla dedicada si quieres
        print("\n=== TOP 5 MODO ESCAPA ===")
        for p in self.sistema_puntuacion.obtener_top("escapa"):
            print(f"{p['nombre']}: {p['puntaje']}")
        
        print("\n=== TOP 5 MODO CAZADOR ===")
        for p in self.sistema_puntuacion.obtener_top("cazador"):
            print(f"{p['nombre']}: {p['puntaje']}")


if __name__ == "__main__":
    juego = JuegoPygame()
    juego.ejecutar()