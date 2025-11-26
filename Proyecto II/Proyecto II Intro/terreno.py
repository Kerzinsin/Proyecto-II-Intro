#Terreno

class Terreno:
    def __init__(self, codigo, simbolo):
        self.codigo = codigo
        self.simbolo = simbolo

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
        super().__init__(1, "#")

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
