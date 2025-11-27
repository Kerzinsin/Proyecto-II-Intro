#Terreno

class Casilla:
    def __init__(self, codigo, simbolo):
        self.codigo = codigo
        self.simbolo = simbolo

    def puede_pasar_jugador(self):
        return False

    def puede_pasar_enemigo(self):
        return False

class Camino(Casilla):
    def __init__(self):
        super().__init__(0, " ")

    def puede_pasar_jugador(self):
        return True

    def puede_pasar_enemigo(self):
        return True

class Muro(Casilla):
    def __init__(self):
        super().__init__(1, "#")

class Tunel(Casilla):
    def __init__(self):
        super().__init__(2, "T")

    def puede_pasar_jugador(self):
        return True

    def puede_pasar_enemigo(self):
        return False

class Liana(Casilla):
    def __init__(self):
        super().__init__(3, "L")

    def puede_pasar_jugador(self):
        return False

    def puede_pasar_enemigo(self):
        return True

