from Sistema.puntuacion import Puntuacion
from Modos.modo_escapa import ModoEscapa
from Modos.modo_cazador import ModoCazador

class ControladorJuego:
    def __init__(self):
        self.sistema_puntuacion = Puntuacion()
        self.nombre_jugador = None
        self.dificultad = "normal"

    def mostrar_banner(self):
        """Muestra el banner de bienvenida"""
        print("\n" + "="*60)
        print(f"{'ESCAPA DEL LABERINTO':^60}")
        print("="*60)
        print(f"{'Proyecto 2 - Introduccion a la Programacion':^60}")
        print(f"{'Instituto Tecnologico de Costa Rica':^60}")
        print("="*60 + "\n")

    def iniciar_sesion(self):
        """Solicita el nombre del jugador y lo registra"""
        self.mostrar_banner()
        
        print("REGISTRO DE JUGADOR")
        print("-" * 60)
        
        while True:
            nombre = input("Ingrese su nombre (min. 3 caracteres): ").strip()
            
            if len(nombre) >= 3:
                self.nombre_jugador = nombre
                self.sistema_puntuacion.registrar_jugador(nombre)
                print(f"Bienvenido, {nombre}!\n")
                break
            else:
                print("El nombre debe tener al menos 3 caracteres.\n")

    def seleccionar_dificultad(self):
        """Permite al jugador seleccionar la dificultad"""
        print("\n" + "="*60)
        print("SELECCION DE DIFICULTAD")
        print("="*60)
        print("\n1. FACIL")
        print("   - Menos enemigos")
        print("   - Enemigos mas lentos")
        print("   - Mas tiempo (solo en modo Cazador)")
        print("   - Multiplicador: x1.0")
        
        print("\n2. NORMAL (Recomendado)")
        print("   - Balance de enemigos")
        print("   - Velocidad normal")
        print("   - Tiempo estandar")
        print("   - Multiplicador: x1.5")
        
        print("\n3. DIFICIL")
        print("   - Mas enemigos")
        print("   - Enemigos mas rapidos")
        print("   - Menos tiempo (solo en modo Cazador)")
        print("   - Multiplicador: x2.0")
        
        print("\n" + "-"*60)
        
        while True:
            opcion = input("Selecciona dificultad (1-3): ").strip()
            
            if opcion == "1":
                self.dificultad = "facil"
                print("Dificultad seleccionada: FACIL\n")
                break
            elif opcion == "2":
                self.dificultad = "normal"
                print("Dificultad seleccionada: NORMAL\n")
                break
            elif opcion == "3":
                self.dificultad = "dificil"
                print("Dificultad seleccionada: DIFICIL\n")
                break
            else:
                print("Opcion invalida. Ingresa 1, 2 o 3.\n")

    def seleccionar_modo(self):
        """Permite al jugador seleccionar el modo de juego"""
        while True:
            print("\n" + "="*60)
            print("SELECCION DE MODO DE JUEGO")
            print("="*60)
            
            print("\n1. MODO ESCAPA")
            print("   Objetivo: Huye de los cazadores y llega a la salida")
            print("   - Multiples enemigos que te persiguen")
            print("   - Coloca trampas para eliminarlos")
            print("   - A menor tiempo, mayor puntaje")
            print("   - Usa tuneles para recuperar energia")
            
            print("\n2. MODO CAZADOR")
            print("   Objetivo: Atrapa enemigos antes de que escapen")
            print("   - Los enemigos huyen de ti")
            print("   - Nuevos enemigos aparecen cada 15 segundos")
            print("   - Si llegan a la salida, pierdes puntos")
            print("   - Bonus por atrapar cerca de la salida")
            
            print("\n3. VER TABLA DE PUNTAJES")
            print("   Muestra los mejores 5 jugadores de cada modo")
            
            print("\n4. SALIR")
            
            print("\n" + "-"*60)
            opcion = input("Selecciona una opcion (1-4): ").strip()
            
            if opcion == "1":
                self.seleccionar_dificultad()
                modo = ModoEscapa(self.sistema_puntuacion, self.nombre_jugador, self.dificultad)
                modo.jugar()
                
                # Preguntar si quiere jugar otra vez
                if not self.quiere_continuar():
                    break
                    
            elif opcion == "2":
                self.seleccionar_dificultad()
                modo = ModoCazador(self.sistema_puntuacion, self.nombre_jugador, self.dificultad)
                modo.jugar()
                
                # Preguntar si quiere jugar otra vez
                if not self.quiere_continuar():
                    break
                    
            elif opcion == "3":
                self.mostrar_resultados()
                input("\nPresiona ENTER para continuar...")
                
            elif opcion == "4":
                print("\n" + "="*60)
                print(f"{'Gracias por jugar!':^60}")
                print("="*60 + "\n")
                break
                
            else:
                print("Opcion invalida. Ingresa un numero del 1 al 4.\n")
                input("Presiona ENTER para continuar...")

    def quiere_continuar(self):
        """Pregunta si el jugador quiere seguir jugando"""
        print("\n" + "-"*60)
        respuesta = input("Quieres jugar otra partida? (s/n): ").lower().strip()
        return respuesta in ['s', 'si', 'sí', 'y', 'yes']

    def mostrar_resultados(self):
        """Muestra las tablas de puntajes de ambos modos"""
        print("\n" + "="*60)
        print(f"{'TABLA DE PUNTAJES':^60}")
        print("="*60)
        
        # Top 5 Modo Escapa
        print("\nTOP 5 - MODO ESCAPA")
        print("-"*60)
        top_escapa = self.sistema_puntuacion.obtener_top("escapa")
        
        if top_escapa:
            print(f"{'#':<5} {'Jugador':<20} {'Puntaje':<15} {'Fecha':<20}")
            print("-"*60)
            for i, p in enumerate(top_escapa, 1):
                print(f"{i:<5} {p['nombre']:<20} {p['puntaje']:<15} {p['fecha']:<20}")
        else:
            print("  (No hay puntajes registrados aun)")
        
        # Top 5 Modo Cazador
        print("\nTOP 5 - MODO CAZADOR")
        print("-"*60)
        top_cazador = self.sistema_puntuacion.obtener_top("cazador")
        
        if top_cazador:
            print(f"{'#':<5} {'Jugador':<20} {'Puntaje':<15} {'Fecha':<20}")
            print("-"*60)
            for i, p in enumerate(top_cazador, 1):
                print(f"{i:<5} {p['nombre']:<20} {p['puntaje']:<15} {p['fecha']:<20}")
        else:
            print("  (No hay puntajes registrados aun)")
        
        print("\n" + "="*60)

    def iniciar(self):
        """Método principal que inicia el juego"""
        self.iniciar_sesion()
        self.seleccionar_modo()
        self.mostrar_resultados()
