#Puntuación
import json
from datetime import datetime
from pathlib import Path

class Puntuacion:
    def __init__(self):
        base_dir = Path(__file__).parent.parent
        self.carpeta_info = base_dir / "Info"
        
        # Crear carpeta Info si no existe
        self.carpeta_info.mkdir(exist_ok=True)
        
        self.ruta_escapa = self.carpeta_info / "top5_escapa.json"
        self.ruta_cazador = self.carpeta_info / "top5_cazador.json"
        self.ruta_historial = self.carpeta_info / "historial.json"
        
        self._asegurar_archivo(self.ruta_escapa)
        self._asegurar_archivo(self.ruta_cazador)
        self._asegurar_archivo(self.ruta_historial)
    
    def _asegurar_archivo(self, ruta):
        """Crea el archivo JSON si no existe"""
        if not ruta.exists():
            ruta.write_text("[]")
    
    def _cargar_json(self, ruta):
        """Carga datos desde un archivo JSON"""
        try:
            return json.loads(ruta.read_text())
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _guardar_json(self, ruta, datos):
        """Guarda datos en un archivo JSON"""
        ruta.write_text(json.dumps(datos, indent=4, ensure_ascii=False))
    
    def registrar_jugador(self, nombre):
        """Registra un nuevo jugador en el historial"""
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
        """Guarda un puntaje en el top 5 del modo correspondiente"""
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
        """Obtiene el top 5 de puntajes del modo especificado"""
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
