import os

PASTA_DADOS = "data"
CAMINHO_ESTATISTICAS = os.path.join(PASTA_DADOS, "estatisticas.txt")


def calcular_aproveitamento(jogador):
    if jogador.tentativas == 0:
        return 0.0
    return (jogador.acertos / jogador.tentativas) * 100


def gravar_resultado(nome_vencedor, total_jogadas, tempo_em_segundos, jogador1, jogador2):
    horas = int(tempo_em_segundos // 3600)
    minutos = int((tempo_em_segundos % 3600) // 60)
    segundos = int(tempo_em_segundos % 60)
    tempo_formatado = f"{horas:02d}:{minutos:02d}:{segundos:02d}"

    aproveitamento1 = calcular_aproveitamento(jogador1)
    aproveitamento2 = calcular_aproveitamento(jogador2)

    linha = (
        f"Vencedor: {nome_vencedor} | Jogadas: {total_jogadas} | Tempo: {tempo_formatado} | "
        f"{jogador1.nome} - Acertos: {jogador1.acertos}/{jogador1.tentativas} ({aproveitamento1:.1f}%) | "
        f"{jogador2.nome} - Acertos: {jogador2.acertos}/{jogador2.tentativas} ({aproveitamento2:.1f}%)\n"
    )

    os.makedirs(PASTA_DADOS, exist_ok=True)
    ficheiro = open(CAMINHO_ESTATISTICAS, "a")
    ficheiro.write(linha)
    ficheiro.close()

    print("\n" + "=" * 20)
    print("FIM DE JOGO")
    print(f"Vencedor: {nome_vencedor}")
    print(f"Total de jogadas: {total_jogadas}")
    print(f"Tempo de partida: {tempo_formatado}")
    print("-" * 20)
    print(f"{jogador1.nome} - Acertos: {jogador1.acertos}/{jogador1.tentativas} ({aproveitamento1:.1f}% de aproveitamento)")
    print(f"{jogador2.nome} - Acertos: {jogador2.acertos}/{jogador2.tentativas} ({aproveitamento2:.1f}% de aproveitamento)")
    print("=" * 20)


def exibir_estatisticas():
    print("\n=== ESTATISTICAS DE DESEMPENHO ===")
    try:
        ficheiro = open(CAMINHO_ESTATISTICAS, "r")
        linhas = ficheiro.readlines()
        ficheiro.close()

        if len(linhas) == 0:
            print("Nenhuma partida registada ainda.")
        else:
            print(f"Total de partidas jogadas: {len(linhas)}\n")
            for linha in linhas:
                print(linha.strip())

    except FileNotFoundError:
        print("Nenhuma partida registada ainda.")