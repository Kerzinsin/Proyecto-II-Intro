import json
from datetime import datetime
import os

# Crear carpeta Info si no existe
if not os.path.exists("Info"):
    os.makedirs("Info")

# Rutas de los archivos JSON
RUTA_ESCAPA = "Info/top5_escapa.json"
RUTA_CAZADOR = "Info/top5_cazador.json"
RUTA_HISTORIAL = "Info/historial.json"


# Función para cargar JSON
def cargar_json(ruta):
    if not os.path.exists(ruta):
        with open(ruta, "w") as f:
            f.write("[]")  # Crear JSON vacío si no existe

    with open(ruta, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []  # Si está vacío o da error, devolver lista vacía



# Función para guardar JSON
def guardar_json(ruta, datos):
    with open(ruta, "w") as f:
        json.dump(datos, f, indent=4)


# Registrar jugador en historial (solo nombre y fecha)
def registrar_jugador(nombre):
    historial = cargar_json(RUTA_HISTORIAL)

    # Evitar nombres duplicados
    for jugador in historial:
        if jugador["nombre"] == nombre:
            return  # No lo agrega si ya existe

    historial.append({
        "nombre": nombre,
        "fecha_registro": datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    guardar_json(RUTA_HISTORIAL, historial)


# Guardar puntaje en el modo correcto (Escapa o Cazador)
def guardar_puntaje(nombre, puntaje, modo):
    if modo == "escapa":
        ruta = RUTA_ESCAPA
    elif modo == "cazador":
        ruta = RUTA_CAZADOR
    else:
        return

    lista = cargar_json(ruta)

    # Agregar nuevo puntaje
    lista.append({
        "nombre": nombre,
        "puntaje": puntaje,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M")
    })

    # Ordenar de mayor a menor y dejar solo Top 5
    lista = sorted(lista, key=lambda x: x["puntaje"], reverse=True)[:5]

    guardar_json(ruta, lista)


# Obtener lista de puntajes
def obtener_top(modo):
    if modo == "escapa":
        return cargar_json(RUTA_ESCAPA)
    elif modo == "cazador":
        return cargar_json(RUTA_CAZADOR)
    return []


# Prueba rápida (solo para consola)
if __name__ == "__main__":
    registrar_jugador("Juan")
    guardar_puntaje("Juan", 350, "escapa")
    guardar_puntaje("Pedro", 400, "escapa")
    guardar_puntaje("Ana", 500, "cazador")

    print("Top Escapa:")
    for p in obtener_top("escapa"):
        print(p)

    print("\nTop Cazador:")
    for p in obtener_top("cazador"):
        print(p)
