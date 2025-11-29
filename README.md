# Proyecto-II-Intro

**Escapa del Laberinto - Proyecto TEC**

---

## 📋 Información del Proyecto

**Instituto:** Tecnológico de Costa Rica  
**Curso:** Introducción a la Programación  
**Realizado por:** Kerzin Rivera y Angie Alpízar

---

## 🎮 Descripción del Proyecto

**Escapa del Laberinto** es un videojuego desarrollado en Python utilizando Programación Orientada a Objetos (POO) y Pygame. Combina estrategia, persecución y toma de decisiones en tiempo real.

El jugador debe navegar por un laberinto generado aleatoriamente, evitando ser atrapado por enemigos que se mueven inteligentemente y reaparecen con intervalos controlados según la dificultad seleccionada.

El juego incluye dos modos con mecánicas distintas, un sistema de puntuación, trampas estratégicas, gestión de energía y vida, túneles exclusivos para el jugador, y diversos elementos del terreno como muros y lianas.

---

## 🎯 Objetivos del Juego

### Diferentes Modos de Juego

**Modo Escapa:**  
Evita ser atrapado por los cazadores mientras buscas la salida del laberinto. Utiliza trampas, túneles y gestiona tu energía para sobrevivir.

**Modo Cazador:**  
Invierte los roles: persigue y atrapa a los enemigos que intentan huir y escapar por las salidas antes de que se agote el tiempo.

---

## ⚙️ Funcionalidades Principales

- ✅ Interfaz gráfica desarrollada con Pygame
- ✅ Mapa generado aleatoriamente usando clases de terreno
- ✅ Sistema de trampas y reaparición controlada de enemigos
- ✅ Gestión de energía y habilidad de correr
- ✅ Túneles exclusivos para el jugador
- ✅ Sistema de vidas y reinicio automático del jugador
- ✅ Sistema de puntuaciones con Top 5 por modo de juego
- ✅ Enemigos con movimiento automático e inteligente
- ✅ Diferentes niveles de dificultad (Fácil, Intermedio, Difícil)
- ✅ Menús visuales, HUD informativo, animaciones y efectos de sonido

---

## 🕹️ Mecánicas del Juego

### **Modo Escapa**

**Objetivo:** Llegar a la salida lo más rápido posible.  
**Puntuación inicial:** 1500 puntos (todos los niveles)  
**Nota:** No hay límite de tiempo, pero la puntuación disminuye gradualmente, incentivando la velocidad.

| Dificultad | Enemigos | Puntos por Escapar | Velocidad Enemigos | Puntos por Trampa | Vidas |
|------------|----------|--------------------|--------------------|-------------------|-------|
| **Fácil** | 3 | 1000 | 1 seg | 100 | 3 |
| **Intermedio** | 5 | 2250 | 0.75 seg | 100 | 3 |
| **Difícil** | 6 | 3000 | 0.5 seg | 100 | 3 |

---

### **Modo Cazador**

**Objetivo:** Atrapar la mayor cantidad de enemigos en 2 minutos.  
**Puntuación inicial:** 0 puntos  
**Nota:** No se pueden usar trampas en este modo.

| Dificultad | Salidas | Enemigos | Puntos por Captura | Puntos por Escape | Velocidad Enemigos |
|------------|---------|----------|--------------------|--------------------|-------------------|
| **Fácil** | 1 | 5 | +100 | -50 | 1 seg |
| **Intermedio** | 2 | 5 | +100 | -50 | 0.75 seg |
| **Difícil** | 2 | 4 | +100 | -50 | 0.5 seg |

---

## 📦 Estructura del Repositorio
```
Proyecto-II-Intro/
├── src/                    # Código fuente del juego
├── assets/                 # Recursos (sprites, sonidos, fuentes)
├── docs/                   # Documentación del proyecto
├── README.md              # Este archivo
└── requirements.txt       # Dependencias del proyecto
```

---

## 🚀 Instalación y Ejecución

### Requisitos
- Python 3.8 o superior
- Pygame

### Instrucciones

1. Clonar el repositorio:
```bash
git clone https://github.com/usuario/Proyecto-II-Intro.git
cd Proyecto-II-Intro
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Ejecutar el juego:
```bash
python main.py
```

---

## 👥 Autores

- **Kerzin Rivera**
- **Angie Alpízar**

---

## 📄 Licencia

Este proyecto fue desarrollado con fines académicos para el curso de Introducción a la Programación del Instituto Tecnológico de Costa Rica.

---

## 🎓 Agradecimientos

Agradecemos al Instituto Tecnológico de Costa Rica y al equipo docente del curso por su guía durante el desarrollo de este proyecto.
