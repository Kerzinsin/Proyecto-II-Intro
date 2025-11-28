Proyecto-II-Intro
Escapa del Laberinto - Proyecto TEC
Instituto Tecnológico de Costa Rica
Curso: Introducción a la Programación
Realizado por Kerzin Rivera y Angie Alpízar

Descripción del Proyecto:

Escapa del Laberinto es un videojuego desarrollado en Python con POO y Pygame, que combina estrategia, persecución y toma de decisiones.
El jugador debe escapar del laberinto, evitando ser atrapado por enemigos que se mueven inteligentemente y reaparecen con intervalos controlados según la dificultad.
Incluye dos modos de juego con mecánicas distintas, un sistema de puntuación, trampas, energía, vida, túneles y elementos del terreno como muros y lianas.

---------------------------------------Objetivos del juego---------------------------------------
Diferentes Modos de Juego

Modo Escapa: Se trata de intentar evitar ser atrapado por los cazadores siendo el objetivo escapar llegando a la salida. Usa trampas, túneles y energía.

Modo Cazador: Debes	persiguir y atrapar enemigos que huyen e intentan escapar por las salidas.

------------------------------------Funcionalidades principales------------------------------------

- Juego con interfaz gráfica usando Pygame
- Mapa generado visualmente usando clases de terreno
- Implementación de trampas y reaparición de enemigos
- Energía y sistema de correr con túneles
- Sistema de vidas y reinicio de jugador
- Puntuaciones con top 5 por modo
- Enemigos con movimiento automático e inteligente
- Diferentes dificultades que afectan velocidad, enemigos y reaparición
- Menús visuales, HUD, animaciones y sonidos

----------------------------------------Mecánicas del Juego-----------------------------------------
Modo Escapa: No tiene un tiempo límite de juego. Pero, entre mas dure el jugador en salir los puntos irán bajando haciendo así que salir lo más rápido posible sea una regla para conseguir mas puntos. El puntaje inicial siempre es 1500 en cualquier nivel de dificultad.

Nivel Fácil: 
- Se conforma de 3 enemigos
- 1000 puntos por encontrar la salida
- Enemigos se mueven cada un segundo
- Trampa activa otorga 100 puntos adicionales
- Tres vidas

Nivel Intermedio:
- Se conforma de 5 enemigos
- Trampa activa otorga 100 puntos adicionales
- Escapar otorga 2250 puntos
- Tres vidas
- Enemigos se mueven cada 0,75 segundos

Nivel Díficil:
- Se conforma de 6 enemigos
- Trampa activa otorga 100 puntos adicionales
- Escapar otorga 3000 puntos
- Tres vidas
- Enemigos se mueven cada 0,5 segundos

Modo Cazador: Tiene como límite 2 minutos para conseguir la mayor cantidad de puntos, en este modo no se pueden usar trampas. El puntaje inicial es 0.

Nivel Fácil:
- 1 salida
- 5 enemigos
- Mas 100 puntos por atrapar al enemigo
- Menos 50 puntos por enemigo que logre escapar

Nivel Intermedio:
- 2 salidas
- 5 enemigos
- Mas 100 puntos por atrapar al enemigo
- Menos 50 puntos por enemigo que logre escapar

Nivel Díficil:
- 2 salidas
- 4 enemigos
- Mas 100 puntos por atrapar al enemigo
- Menos 50 puntos por enemigo que logre escapar
