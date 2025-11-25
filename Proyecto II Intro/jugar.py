from mapa import Mapa
from jugador import Jugador

mapa = Mapa(10, 10)
jugador = Jugador(0, 0)

mapa.mostrar_matriz()
print("Posición inicial:", jugador.obtener_posicion())

jugador.mover("abajo", mapa)
jugador.mover("derecha", mapa)
jugador.mover("derecha", mapa)

print("Posición final:", jugador.obtener_posicion())
