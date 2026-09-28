import random
from tabuleiro import Tabuleiro
from navios import Navio
from utils import converter_coordenada


class Jogador:
    def __init__(self, nome):
        self.nome = nome
        self.tabuleiro = Tabuleiro()
        self.navios = []
        self.frota_ativa = 0
        self.tentativas = 0
        self.acertos = 0
        self.criar_frota()

    def criar_frota(self):
        navio_grande1 = Navio("Grande", 4)
        navio_grande2 = Navio("Grande", 4)
        navio_pequeno1 = Navio("Pequeno", 2)
        navio_pequeno2 = Navio("Pequeno", 2)
        navio_pequeno3 = Navio("Pequeno", 2)

        self.navios.append(navio_grande1)
        self.navios.append(navio_grande2)
        self.navios.append(navio_pequeno1)
        self.navios.append(navio_pequeno2)
        self.navios.append(navio_pequeno3)

        self.frota_ativa = 5

    def posicionar_navios_automaticamente(self, navios=None):
        lista_navios = navios if navios is not None else self.navios

        for navio in lista_navios:
            posicionado = False
            while not posicionado:
                linha = random.randint(0, 9)
                coluna = random.randint(0, 9)
                direcao = random.randint(0, 1)

                if self.pode_posicionar(navio.tamanho, linha, coluna, direcao):
                    self.colocar_navio(navio, linha, coluna, direcao)
                    posicionado = True

    def posicionar_navios_manualmente(self):
        print(f"\n--- Posicionamento de frota: {self.nome} ---")
        self.tabuleiro.exibir()

        for navio in self.navios:
            posicionado = False

            while not posicionado:
                print(f"\nA posicionar navio {navio.tipo} (Tamanho: {navio.tamanho})")
                entrada = input("Digite a coordenada inicial (ex: C5): ")
                linha, coluna = converter_coordenada(entrada)

                if linha is None:
                    print("Coordenada invalida! Use Letra e Numero.")
                    continue

                orientacao_str = input("Digite a orientacao (H - Horizontal, V - Vertical): ")
                orientacao_str = orientacao_str.upper().strip()

                if orientacao_str == "H":
                    direcao = 0
                elif orientacao_str == "V":
                    direcao = 1
                else:
                    print("Orientacao invalida!")
                    continue

                if self.pode_posicionar(navio.tamanho, linha, coluna, direcao):
                    self.colocar_navio(navio, linha, coluna, direcao)
                    posicionado = True
                    print(f"Navio {navio.tipo} posicionado com sucesso!")
                    self.tabuleiro.exibir()
                else:
                    print("Posicao invalida!")

    def pode_posicionar(self, tamanho, linha, coluna, direcao):
        for i in range(tamanho):
            if direcao == 0:
                l = linha
                c = coluna + i
            else:
                l = linha + i
                c = coluna

            if l > 9:
                return False
            if c > 9:
                return False
            if self.tabuleiro.matriz[l][c] == "N":
                return False
        return True

    def colocar_navio(self, navio, linha, coluna, direcao):
        for i in range(navio.tamanho):
            if direcao == 0:
                l = linha
                c = coluna + i
            else:
                l = linha + i
                c = coluna

            self.tabuleiro.matriz[l][c] = "N"
            navio.coordenadas.append((l, c))