#Puntuación

import json
from datetime import datetime
import os

class Puntuacion:
    def __init__(self, carpeta_info="Info"):
        self.carpeta_info = carpeta_info

        if not os.path.exists(carpeta_info):
            os.makedirs(carpeta_info)

        self.ruta_escapa = os.path.join(carpeta_info, "top5_escapa.json")
        self.ruta_cazador = os.path.join(carpeta_info, "top5_cazador.json")
        self.ruta_historial = os.path.join(carpeta_info, "historial.json")

        self._asegurar_archivo(self.ruta_escapa)
        self._asegurar_archivo(self.ruta_cazador)
        self._asegurar_archivo(self.ruta_historial)

    def _asegurar_archivo(self, ruta):
        if not os.path.exists(ruta):
            with open(ruta, "w") as f:
                f.write("[]")

    def _cargar_json(self, ruta):
        with open(ruta, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    def _guardar_json(self, ruta, datos):
        with open(ruta, "w") as f:
            json.dump(datos, f, indent=4)

    def registrar_jugador(self, nombre):
        historial = self._cargar_json(self.ruta_historial)

        for jugador in historial:
            if jugador["nombre"] == nombre:
                return

        historial.append({
            "nombre": nombre,
            "fecha_registro": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        self._guardar_json(self.ruta_historial, historial)

    def guardar_puntaje(self, nombre, puntaje, modo):
        if modo == "escapa":
            ruta = self.ruta_escapa
        elif modo == "cazador":
            ruta = self.ruta_cazador
        else:
            return

        lista = self._cargar_json(ruta)
        lista.append({
            "nombre": nombre,
            "puntaje": puntaje,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M")
        })

        lista = sorted(lista, key=lambda x: x["puntaje"], reverse=True)[:5]
        self._guardar_json(ruta, lista)

    def obtener_top(self, modo):
        if modo == "escapa":
            return self._cargar_json(self.ruta_escapa)
        elif modo == "cazador":
            return self._cargar_json(self.ruta_cazador)
        return []


if __name__ == "__main__":
    sistema = Puntuacion()
    sistema.registrar_jugador("Juan")
    sistema.guardar_puntaje("Juan", 350, "escapa")
    sistema.guardar_puntaje("Pedro", 400, "escapa")
    sistema.guardar_puntaje("Ana", 500, "cazador")

    print("Top Escapa:")
    for p in sistema.obtener_top("escapa"):
        print(p)

    print("\nTop Cazador:")
    for p in sistema.obtener_top("cazador"):
        print(p)
