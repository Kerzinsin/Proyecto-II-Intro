#Modo Cazador

import time
import random
from Modelos.mapa import Mapa
from Modelos.jugador import Jugador
from Modelos.enemigo import Enemigo

class ModoCazador:
    def __init__(self, sistema_puntuacion, nombre_jugador, dificultad="normal"):
        self.sistema_puntuacion = sistema_puntuacion
        self.nombre_jugador = nombre_jugador
        self.dificultad = dificultad
        
        self.config_dificultad = {
            "facil": {"enemigos": 2, "velocidad": 0.5, "tiempo": 180, "multiplicador": 1.0},
            "normal": {"enemigos": 3, "velocidad": 1.0, "tiempo": 120, "multiplicador": 1.5},
            "dificil": {"enemigos": 5, "velocidad": 1.5, "tiempo": 90, "multiplicador": 2.0}
        }

    def jugar(self):
        # Configuración según dificultad
        config = self.config_dificultad.get(self.dificultad, self.config_dificultad["normal"])
        num_enemigos_iniciales = config["enemigos"]
        velocidad_enemigos = config["velocidad"]
        tiempo_limite = config["tiempo"]
        multiplicador_puntos = config["multiplicador"]
        
        # Crear mapa y jugador
        mapa = Mapa(10, 15)
        jugador = Jugador(0, 0)
        
        enemigos = []
        posiciones_validas = mapa.obtener_posiciones_validas_enemigo()
        
        for i in range(num_enemigos_iniciales):
            if posiciones_validas:
                pos = random.choice(posiciones_validas)
                posiciones_validas.remove(pos)
                enemigos.append(Enemigo(pos[0], pos[1], velocidad=velocidad_enemigos))
            else:
                enemigos.append(Enemigo(
                    random.randint(1, mapa.filas - 2),
                    random.randint(1, mapa.columnas - 2),
                    velocidad=velocidad_enemigos
                ))
        
        # Variables de juego
        tiempo_inicio = time.time()
        puntaje = 0
        enemigos_atrapados = 0
        enemigos_escapados = 0
        
        print("\n" + "="*50)
        print(f"{'MODO CAZADOR':^50}")
        print("="*50)
        print(f"Dificultad: {self.dificultad.upper()}")
        print(f"Enemigos iniciales: {num_enemigos_iniciales}")
        print(f"Tiempo límite: {tiempo_limite} segundos")
        print("\nObjetivo: Atrapa a todos los enemigos antes de que escapen")
        print("\nControles:")
        print("  - Movimiento: arriba, abajo, izquierda, derecha")
        print("  - Correr: 'correr' (consume energía)")
        print("\nSistema de puntos:")
        print("  - Atrapar enemigo: +100 puntos")
        print("  - Enemigo llega a salida: -50 puntos")
        print("  - Si atrapas antes que llegue a salida: +200 puntos")
        print("\nTips:")
        print("  - Los enemigos HUYEN de ti")
        print("  - Intenta bloquear su camino a las salidas")
        print("  - Usa túneles para recuperar energía")
        print("="*50 + "\n")
        
        input("Presiona ENTER para comenzar...")
        
        # Loop principal del juego
        ultimo_spawn = time.time()
        
        while True:
            tiempo_actual = time.time()
            tiempo_transcurrido = int(tiempo_actual - tiempo_inicio)
            tiempo_restante = tiempo_limite - tiempo_transcurrido
            
            if tiempo_restante <= 0:
                print("\n" + "="*50)
                print(f"{'⏰ TIEMPO AGOTADO ⏰':^50}")
                print("="*50)
                print(f"🎯 Enemigos atrapados: {enemigos_atrapados}")
                print(f"🏃 Enemigos escapados: {enemigos_escapados}")
                print(f"🏆 Puntaje final: {int(puntaje * multiplicador_puntos)}")
                print("="*50)
                
                for enemigo in enemigos:
                    enemigo.activo = False
                
                self.sistema_puntuacion.guardar_puntaje(
                    self.nombre_jugador, 
                    int(puntaje * multiplicador_puntos), 
                    "cazador"
                )
                break
            
            # Limpiar pantalla (simulado)
            print("\n" * 2)
            
            # Mostrar mapa
            mapa.mostrar_con_multiples_enemigos(jugador, enemigos)
            
            # Mostrar estadísticas
            print(f"\n{'─'*50}")
            print(f"⏱️  Tiempo restante: {tiempo_restante}s | ⚡ Energía: {jugador.energia}/100")
            print(f"🎯 Atrapados: {enemigos_atrapados} | 🏃 Escapados: {enemigos_escapados} | 💰 Puntos: {int(puntaje)}")
            print(f"👾 Enemigos activos: {len([e for e in enemigos if not e.eliminado])}")
            print(f"{'─'*50}")
            
            if tiempo_actual - ultimo_spawn >= 15 and len(enemigos) < num_enemigos_iniciales + 3:
                posiciones_disponibles = mapa.obtener_posiciones_validas_enemigo()
                if posiciones_disponibles:
                    pos = random.choice(posiciones_disponibles)
                    nuevo_enemigo = Enemigo(pos[0], pos[1], velocidad=velocidad_enemigos)
                    enemigos.append(nuevo_enemigo)
                    print("⚠️  ¡Nuevo enemigo apareció!")
                    ultimo_spawn = tiempo_actual
            
            # Input del jugador
            accion = input("\n➤ Acción: ").lower().strip()
            
            # Procesar acción
            if accion == "correr":
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
                    enemigo.huir_de(jugador, mapa)
            
            enemigos_a_eliminar = []
            for i, enemigo in enumerate(enemigos):
                if not enemigo.eliminado and jugador.obtener_posicion() == enemigo.obtener_posicion():
                    dist_salida = abs(enemigo.fila - mapa.pos_salida[0]) + abs(enemigo.columna - mapa.pos_salida[1])
                    
                    if dist_salida <= 2:
                        puntaje += 200
                        print(f"💎 ¡Enemigo atrapado cerca de la salida! +200 puntos (BONUS)")
                    else:
                        puntaje += 100
                        print(f"✅ Enemigo atrapado. +100 puntos")
                    
                    enemigos_atrapados += 1
                    enemigos_a_eliminar.append(i)
            
            for i in reversed(enemigos_a_eliminar):
                enemigos.pop(i)
            
            enemigos_que_escaparon = []
            for i, enemigo in enumerate(enemigos):
                if not enemigo.eliminado and enemigo.obtener_posicion() == mapa.pos_salida:
                    puntaje -= 50
                    enemigos_escapados += 1
                    print(f"❌ ¡Un enemigo escapó por la salida! -50 puntos")
                    enemigos_que_escaparon.append(i)
            
            for i in reversed(enemigos_que_escaparon):
                enemigos.pop(i)
            
            if len(enemigos) == 0 and tiempo_actual - ultimo_spawn >= 15:
                print("\n" + "="*50)
                print(f"{'🏆 ¡VICTORIA PERFECTA! 🏆':^50}")
                print("="*50)
                print("¡Atrapaste a todos los enemigos!")
                print(f"⏱️  Tiempo usado: {tiempo_transcurrido}/{tiempo_limite} segundos")
                print(f"🎯 Enemigos atrapados: {enemigos_atrapados}")
                print(f"🏃 Enemigos escapados: {enemigos_escapados}")
                
                bonus_tiempo = (tiempo_restante * 5)
                puntaje += bonus_tiempo
                print(f"⏰ Bonus por tiempo sobrante: +{int(bonus_tiempo)}")
                print(f"🏆 Puntaje final: {int(puntaje * multiplicador_puntos)}")
                print("="*50)
                
                self.sistema_puntuacion.guardar_puntaje(
                    self.nombre_jugador, 
                    int(puntaje * multiplicador_puntos), 
                    "cazador"
                )
                break
        
        for enemigo in enemigos:
            enemigo.activo = False
