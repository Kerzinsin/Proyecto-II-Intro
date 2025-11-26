from puntuacion import registrar_jugador, guardar_puntaje, obtener_top

def pedir_nombre_jugador():
    nombre = input("Ingrese su nombre: ").strip()
    registrar_jugador(nombre)
    return nombre

def elegir_modo():
    print("\nSeleccione el modo de juego:")
    print("1. Escapa")
    print("2. Cazador")
    
    opcion = input("Modo: ")

    if opcion == "1":
        return "escapa"
    elif opcion == "2":
        return "cazador"
    else:
        print("Opción inválida, se selecciona Escapa por defecto.")
        return "escapa"

def registrar_puntaje(nombre, modo):
    try:
        puntaje = int(input("\nDigite su puntaje obtenido: "))
        guardar_puntaje(nombre, puntaje, modo)
        print("Puntaje guardado correctamente.\n")
    except ValueError:
        print("Error: Debe ingresar un número entero para el puntaje.")

def mostrar_top(modo):
    print(f"\nTop 5 del modo {modo.capitalize()}:")
    lista = obtener_top(modo)
    if not lista:
        print("No hay registros aún.")
    else:
        for i, jugador in enumerate(lista, start=1):
            print(f"{i}. {jugador['nombre']} - {jugador['puntaje']} pts - {jugador['fecha']}")

def main():
    print("=== Registro de jugador ===")
    nombre = pedir_nombre_jugador()

    print("\n=== Selección de modo ===")
    modo = elegir_modo()

    registrar_puntaje(nombre, modo)

    mostrar_top(modo)

if __name__ == "__main__":
    main()
