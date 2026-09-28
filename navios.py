class Navio:
    def __init__(self, tipo, tamanho):
        self.tipo = tipo
        self.tamanho = tamanho
        self.coordenadas = []
        self.acertos = 0

    def registar_acerto(self):
        self.acertos = self.acertos + 1

    def afundou(self):

        if self.acertos >= self.tamanho:
            return True
        else:
            return False