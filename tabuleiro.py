class Tabuleiro:
    def __init__(self):
        self.tamanho = 10
        self.matriz = []

        for i in range(self.tamanho):
            nova_linha = []
            for j in range(self.tamanho):
                nova_linha.append("~")
            self.matriz.append(nova_linha)

    def exibir(self):
        letras = "ABCDEFGHIJ"
        print("   " + " ".join(letras))

        for i in range(self.tamanho):
            numero_linha = i + 1

            if numero_linha < 10:
                espaco = " "
            else:
                espaco = ""

            linha_formatada = " ".join(self.matriz[i])
            print(f"{espaco}{numero_linha} {linha_formatada}")