import random
from jogador import Jogador


class Computador(Jogador):

    NIVEIS_VALIDOS = ("facil", "medio", "dificil")

    def __init__(self, nome="Computador", dificuldade="facil"):
        super().__init__(nome)
        self.jogadas_feitas = []

        if dificuldade not in self.NIVEIS_VALIDOS:
            dificuldade = "facil"
        self.dificuldade = dificuldade

        self.fila_alvos = []
        self.acertos_navio_atual = []

    def gerar_jogada(self):
        if self.dificuldade in ("medio", "dificil"):
            jogada = self._proxima_da_fila_alvos()
            if jogada is not None:
                self.jogadas_feitas.append(jogada)
                return jogada

        if self.dificuldade == "dificil":
            candidatos = self._celulas_disponiveis_por_paridade()
            if candidatos:
                jogada = random.choice(candidatos)
                self.jogadas_feitas.append(jogada)
                return jogada

        return self._jogada_aleatoria()

    def _jogada_aleatoria(self):
        while True:
            linha = random.randint(0, 9)
            coluna = random.randint(0, 9)
            if (linha, coluna) not in self.jogadas_feitas:
                self.jogadas_feitas.append((linha, coluna))
                return (linha, coluna)

    def _proxima_da_fila_alvos(self):
        while self.fila_alvos:
            candidato = self.fila_alvos.pop(0)
            linha, coluna = candidato
            if (0 <= linha <= 9 and 0 <= coluna <= 9
                    and candidato not in self.jogadas_feitas):
                return candidato
        return None

    def _celulas_disponiveis_por_paridade(self):

        candidatos = []
        for linha in range(10):
            for coluna in range(10):
                if (linha + coluna) % 2 == 0 and (linha, coluna) not in self.jogadas_feitas:
                    candidatos.append((linha, coluna))
        return candidatos

    def registar_resultado(self, linha, coluna, resultado):

        if self.dificuldade == "facil":
            return

        if resultado == "Navio afundado":
            self.fila_alvos = []
            self.acertos_navio_atual = []
            return

        if resultado != "Acerto":
            return

        self.acertos_navio_atual.append((linha, coluna))

        if self.dificuldade == "dificil" and len(self.acertos_navio_atual) >= 2:

            linhas = [c[0] for c in self.acertos_navio_atual]
            colunas = [c[1] for c in self.acertos_navio_atual]

            if len(set(linhas)) == 1:
                linha_fixa = linhas[0]
                coluna_min, coluna_max = min(colunas), max(colunas)
                self.fila_alvos = [
                    (linha_fixa, coluna_min - 1),
                    (linha_fixa, coluna_max + 1),
                ]
            elif len(set(colunas)) == 1:
                coluna_fixa = colunas[0]
                linha_min, linha_max = min(linhas), max(linhas)
                self.fila_alvos = [
                    (linha_min - 1, coluna_fixa),
                    (linha_max + 1, coluna_fixa),
                ]
            self.fila_alvos = [
                (l, c) for (l, c) in self.fila_alvos
                if 0 <= l <= 9 and 0 <= c <= 9 and (l, c) not in self.jogadas_feitas
            ]
        else:

            linha_alvo, coluna_alvo = linha, coluna
            vizinhos = [
                (linha_alvo - 1, coluna_alvo), (linha_alvo + 1, coluna_alvo),
                (linha_alvo, coluna_alvo - 1), (linha_alvo, coluna_alvo + 1),
            ]
            for vizinho in vizinhos:
                l, c = vizinho
                if (0 <= l <= 9 and 0 <= c <= 9
                        and vizinho not in self.jogadas_feitas
                        and vizinho not in self.fila_alvos):
                    self.fila_alvos.append(vizinho)