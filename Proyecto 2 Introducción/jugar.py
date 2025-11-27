#Jugar

from Sistema.controlador import ControladorJuego

if __name__ == "__main__":
    controlador = ControladorJuego()
    controlador.iniciar_sesion()
    controlador.seleccionar_modo()
    controlador.mostrar_resultados()

#estoy editando el archivo jugar.py?