class Terreno:
    def __init__(self, codigo, simbolo):
        self.codigo = codigo          # Número que identifica el tipo de casilla
        self.simbolo = simbolo        # Carácter para mostrar en consola

    def puede_pasar_jugador(self):
        return False

    def puede_pasar_enemigo(self):
        return False


class Camino(Terreno):
    def __init__(self):
        super().__init__(0, " ")

    def puede_pasar_jugador(self):
        return True

    def puede_pasar_enemigo(self):
        return True


class Muro(Terreno):
    def __init__(self):
        super().__init__(1, "#")  # Pared

    # Nadie puede pasar (ambos retornan False)


class Tunel(Terreno):
    def __init__(self):
        super().__init__(2, "T")

    def puede_pasar_jugador(self):
        return True

    def puede_pasar_enemigo(self):
        return False


class Liana(Terreno):
    def __init__(self):
        super().__init__(3, "L")

    def puede_pasar_jugador(self):
        return False

    def puede_pasar_enemigo(self):
        return True
    
if __name__ == "__main__":
    casillas = [Camino(), Muro(), Tunel(), Liana()]
    for c in casillas:
        print(type(c).__name__, "| Jugador:", c.puede_pasar_jugador(), "| Enemigo:", c.puede_pasar_enemigo())
