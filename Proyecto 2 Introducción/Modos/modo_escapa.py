#Modo Escapa

import time
import random
from Modelos.mapa import Mapa
from Modelos.jugador import Jugador
from Modelos.enemigo import Enemigo

class ModoEscapa:
    def __init__(self, sistema_puntuacion, nombre_jugador, dificultad="normal"):
        self.sistema_puntuacion = sistema_puntuacion
        self.nombre_jugador = nombre_jugador
        self.dificultad = dificultad
        
        self.config_dificultad = {
            "facil": {"enemigos": 2, "velocidad": 0.5, "multiplicador": 1.0},
            "normal": {"enemigos": 3, "velocidad": 1.0, "multiplicador": 1.5},
            "dificil": {"enemigos": 5, "velocidad": 1.5, "multiplicador": 2.0}
        }

    def jugar(self):
        # Configuración según dificultad
        config = self.config_dificultad.get(self.dificultad, self.config_dificultad["normal"])
        num_enemigos = config["enemigos"]
        velocidad_enemigos = config["velocidad"]
        multiplicador_puntos = config["multiplicador"]
        
        # Crear mapa y jugador
        mapa = Mapa(10, 15)
        jugador = Jugador(0, 0)
        
        enemigos = []
        posiciones_validas = mapa.obtener_posiciones_validas_enemigo()
        
        for i in range(num_enemigos):
            if posiciones_validas:
                pos = random.choice(posiciones_validas)
                posiciones_validas.remove(pos)  # Evitar que dos enemigos empiecen en el mismo lugar
                enemigos.append(Enemigo(pos[0], pos[1], velocidad=velocidad_enemigos))
            else:
                # Si no hay más posiciones, usar una aleatoria
                enemigos.append(Enemigo(
                    random.randint(1, mapa.filas - 2),
                    random.randint(1, mapa.columnas - 2),
                    velocidad=velocidad_enemigos
                ))
        
        # Variables de juego
        tiempo_inicio = time.time()
        enemigos_eliminados_trampa = 0
        puntaje_base = 1000  # Puntaje base
        
        print("\n" + "="*50)
        print(f"{'MODO ESCAPA':^50}")
        print("="*50)
        print(f"Dificultad: {self.dificultad.upper()}")
        print(f"Enemigos: {num_enemigos}")
        print("\nObjetivo: Escapa hacia la salida (esquina inferior derecha)")
        print("\nControles:")
        print("  - Movimiento: arriba, abajo, izquierda, derecha")
        print("  - Correr: 'correr' (consume energía)")
        print("  - Trampa: 'trampa' (máximo 3 activas)")
        print("\nTips:")
        print("  - Usa túneles (T) para recuperar energía")
        print("  - Coloca trampas (X) para eliminar enemigos")
        print("  - ¡A menor tiempo, mayor puntaje!")
        print("="*50 + "\n")
        
        input("Presiona ENTER para comenzar...")
        
        # Loop principal del juego
        while True:
            # Limpiar pantalla (simulado con saltos de línea)
            print("\n" * 2)
            
            # Mostrar mapa
            mapa.mostrar_con_multiples_enemigos(jugador, enemigos)
            
            # Mostrar estadísticas
            tiempo_transcurrido = int(time.time() - tiempo_inicio)
            print(f"\n{'─'*50}")
            print(f"⏱️  Tiempo: {tiempo_transcurrido}s | ❤️  Vidas: {jugador.vida} | ⚡ Energía: {jugador.energia}/100")
            print(f"💣 Trampas: {len(jugador.trampas_activas)}/3 | 🎯 Enemigos eliminados: {enemigos_eliminados_trampa}")
            print(f"{'─'*50}")
            
            # Verificar reaparición de enemigos eliminados
            for enemigo in enemigos:
                enemigo.verificar_reaparicion(mapa)
            
            # Input del jugador
            accion = input("\n➤ Acción: ").lower().strip()
            
            # Procesar acción
            if accion == "trampa":
                jugador.colocar_trampa()
            elif accion == "correr":
                if jugador.correr(mapa):
                    print("💨 ¡Corriendo!")
            elif accion in ["arriba", "abajo", "izquierda", "derecha"]:
                if jugador.mover(accion, mapa):
                    pass  # Movimiento exitoso
                else:
                    print("❌ No puedes moverte ahí.")
            else:
                print("❌ Acción inválida.")
                continue
            
            for enemigo in enemigos:
                if not enemigo.eliminado:
                    enemigo.mover_hacia(jugador, mapa)
            
            for enemigo in enemigos:
                if not enemigo.eliminado:
                    if jugador.verificar_trampa_activada(enemigo.obtener_posicion()):
                        enemigo.eliminar()
                        enemigos_eliminados_trampa += 1
                        print(f"💥 ¡Trampa activada! Enemigo eliminado (+50 puntos)")
            
            if jugador.obtener_posicion() == mapa.pos_salida:
                tiempo_final = int(time.time() - tiempo_inicio)
                
                # Calcular puntaje según tiempo
                if tiempo_final < 30:
                    bonus_tiempo = 500
                elif tiempo_final < 60:
                    bonus_tiempo = 300
                elif tiempo_final < 120:
                    bonus_tiempo = 150
                else:
                    bonus_tiempo = 50
                
                puntaje_final = int((puntaje_base + bonus_tiempo + (enemigos_eliminados_trampa * 50)) * multiplicador_puntos)
                
                print("\n" + "="*50)
                print(f"{'🎉 ¡VICTORIA! 🎉':^50}")
                print("="*50)
                print(f"⏱️  Tiempo: {tiempo_final} segundos")
                print(f"🎯 Enemigos eliminados: {enemigos_eliminados_trampa}")
                print(f"⭐ Bonus por tiempo: +{bonus_tiempo}")
                print(f"🏆 Puntaje final: {puntaje_final}")
                print("="*50)
                
                self.sistema_puntuacion.guardar_puntaje(self.nombre_jugador, puntaje_final, "escapa")
                break
            
            for enemigo in enemigos:
                if not enemigo.eliminado and jugador.obtener_posicion() == enemigo.obtener_posicion():
                    if jugador.perder_vida():  # Retorna True si murió
                        tiempo_final = int(time.time() - tiempo_inicio)
                        puntaje_final = int((enemigos_eliminados_trampa * 50) * multiplicador_puntos)
                        
                        print("\n" + "="*50)
                        print(f"{'💀 GAME OVER 💀':^50}")
                        print("="*50)
                        print("Fuiste atrapado y perdiste todas tus vidas.")
                        print(f"⏱️  Sobreviviste: {tiempo_final} segundos")
                        print(f"🎯 Enemigos eliminados: {enemigos_eliminados_trampa}")
                        print(f"🏆 Puntaje final: {puntaje_final}")
                        print("="*50)
                        
                        self.sistema_puntuacion.guardar_puntaje(self.nombre_jugador, puntaje_final, "escapa")
                        return
                    else:
                        print(f"💔 ¡Atrapado! Pierdes 1 vida. Vidas restantes: {jugador.vida}")
                        # Reposicionar enemigo
                        posiciones_disponibles = mapa.obtener_posiciones_validas_enemigo()
                        if posiciones_disponibles:
                            nueva_pos = random.choice(posiciones_disponibles)
                            enemigo.fila, enemigo.columna = nueva_pos