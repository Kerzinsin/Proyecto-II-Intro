#Jugar - Archivo principal del juego

from Sistema.controlador import ControladorJuego

if __name__ == "__main__":
    try:
        controlador = ControladorJuego()
        controlador.iniciar()
    except KeyboardInterrupt:
        print("\n\n" + "="*60)
        print(f"{'Juego interrumpido por el usuario':^60}")
        print(f"{'Gracias por jugar!':^60}")
        print("="*60 + "\n")
    except Exception as e:
        print("\n\n" + "="*60)
        print(f"{'ERROR INESPERADO':^60}")
        print("="*60)
        print(f"Se produjo un error: {e}")
        print("Por favor, reporta este error al desarrollador.")
        print("="*60 + "\n")