import os

PASTA_DADOS = "data"
CAMINHO_REPLAY = os.path.join(PASTA_DADOS, "replay.txt")


def limpar_historico():
    os.makedirs(PASTA_DADOS, exist_ok=True)
    ficheiro = open(CAMINHO_REPLAY, "w")
    ficheiro.write("")
    ficheiro.close()


def registar_jogada(numero_jogada, nome_jogador, coordenada_letra, coordenada_numero, resultado):
    os.makedirs(PASTA_DADOS, exist_ok=True)
    ficheiro = open(CAMINHO_REPLAY, "a")

    numero_formatado = f"{numero_jogada:02d}"
    linha = f"Jogada {numero_formatado} - {nome_jogador} - {coordenada_letra}{coordenada_numero} - {resultado}\n"

    ficheiro.write(linha)
    ficheiro.close()


def reproduzir_replay():
    print("\nReproduzindo replay da ultima partida...")

    try:
        ficheiro = open(CAMINHO_REPLAY, "r")
        linhas = ficheiro.readlines()
        ficheiro.close()

        if len(linhas) == 0:
            print("O historico de jogadas esta vazio.")
        else:
            for linha in linhas:
                print(linha.strip())
                input("[ENTER] Proxima jogada")

        print("\nFim do replay.")

    except FileNotFoundError:
        print("Nenhum ficheiro de replay encontrado. Jogue uma partida primeiro.")