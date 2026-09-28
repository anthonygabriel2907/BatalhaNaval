from menu import exibir_menu_principal, exibir_menu_modos
from jogador import Jogador
from computador import Computador
from utils import converter_coordenada
from replay import limpar_historico, registar_jogada, reproduzir_replay
import time
from estatisticas import gravar_resultado, exibir_estatisticas


def realizar_jogada_humano(jogador_atacante, jogador_defensor, numero_jogada):
    jogada_valida = False
    letras = "ABCDEFGHIJ"

    while not jogada_valida:
        print(f"\n--- Turno de {jogador_atacante.nome} ---")
        jogador_defensor.tabuleiro.exibir_ataque()

        entrada = input("\nSua jogada (ex.: C5): ")
        linha, coluna = converter_coordenada(entrada)

        if linha is None:
            print("Coordenada invalida!")
            continue

        casa_alvo = jogador_defensor.tabuleiro.matriz[linha][coluna]

        if casa_alvo == "X":
            print("Voce já acertou um navio nesta posicao!")
        elif casa_alvo == "O":
            print("Voce já atirou nesta posicao!")
        else:
            jogada_valida = True
            letra_jogada = letras[coluna]
            numero_jogada_tabuleiro = linha + 1
            jogador_atacante.tentativas = jogador_atacante.tentativas + 1

            if casa_alvo == "N":
                print("Acerto! Você atingiu um navio inimigo.")
                jogador_defensor.tabuleiro.matriz[linha][coluna] = "X"
                jogador_atacante.acertos = jogador_atacante.acertos + 1
                registar_jogada(numero_jogada, jogador_atacante.nome, letra_jogada, numero_jogada_tabuleiro, "Acerto")

                for navio in jogador_defensor.navios:
                    for coordenada in navio.coordenadas:
                        if coordenada[0] == linha:
                            if coordenada[1] == coluna:
                                navio.registar_acerto()
                                if navio.afundou():
                                    print(f"Navio afundado! Voce destruiu um navio {navio.tipo}.")
                                    jogador_defensor.frota_ativa = jogador_defensor.frota_ativa - 1
            else:
                print("Água! Nenhum navio atingido nessa posicao.")
                jogador_defensor.tabuleiro.matriz[linha][coluna] = "O"
                registar_jogada(numero_jogada, jogador_atacante.nome, letra_jogada, numero_jogada_tabuleiro, "Agua")


def realizar_jogada_computador(computador, jogador_defensor, numero_jogada):
    print(f"\n--- Turno do {computador.nome} ---")
    linha, coluna = computador.gerar_jogada()

    letras = "ABCDEFGHIJ"
    letra_jogada = letras[coluna]
    numero_jogada_tabuleiro = linha + 1

    time.sleep(1.5)

    print(f"O computador atirou em: {letra_jogada}{numero_jogada_tabuleiro}")

    casa_alvo = jogador_defensor.tabuleiro.matriz[linha][coluna]
    computador.tentativas = computador.tentativas + 1

    if casa_alvo == "N":
        print("O Computador acertou num dos seus navios!")
        jogador_defensor.tabuleiro.matriz[linha][coluna] = "X"
        computador.acertos = computador.acertos + 1
        registar_jogada(numero_jogada, computador.nome, letra_jogada, numero_jogada_tabuleiro, "Acerto")

        resultado_para_ia = "Acerto"
        for navio in jogador_defensor.navios:
            for coordenada in navio.coordenadas:
                if coordenada[0] == linha:
                    if coordenada[1] == coluna:
                        navio.registar_acerto()
                        if navio.afundou():
                            print(f"O Computador afundou o seu navio {navio.tipo}!")
                            jogador_defensor.frota_ativa = jogador_defensor.frota_ativa - 1
                            resultado_para_ia = "Navio afundado"
        computador.registar_resultado(linha, coluna, resultado_para_ia)
    else:
        print("O Computador atirou na água.")
        jogador_defensor.tabuleiro.matriz[linha][coluna] = "O"
        registar_jogada(numero_jogada, computador.nome, letra_jogada, numero_jogada_tabuleiro, "Agua")
        computador.registar_resultado(linha, coluna, "Agua")


def iniciar_partida(modo):
    limpar_historico()
    jogador1 = Jogador("Jogador 1")

    print("\nComo deseja posicionar os seus navios?")
    print("1. Manualmente")
    print("2. Automaticamente")
    escolha_posicao = input("Escolha (1 ou 2): ")

    if escolha_posicao == "1":
        jogador1.posicionar_navios_manualmente()
    else:
        jogador1.posicionar_navios_automaticamente()
        print(f"\nFrota de {jogador1.nome} posicionada:")
        jogador1.tabuleiro.exibir()

    if modo == "1":
        print("\nEscolha a dificuldade do computador:")
        print("1. Fácil")
        print("2. Médio")
        print("3. Difícil")
        escolha_dificuldade = input("Escolha (1, 2 ou 3): ")
        dificuldade = {"1": "facil", "2": "medio", "3": "dificil"}.get(escolha_dificuldade, "facil")

        jogador2 = Computador("Computador", dificuldade=dificuldade)
        jogador2.posicionar_navios_automaticamente()
    else:
        jogador2 = Jogador("Jogador 2")
        print(f"\n--- Vez do {jogador2.nome} organizar a frota ---")
        escolha_posicao2 = input("1. Manualmente ou 2. Automaticamente: ")

        if escolha_posicao2 == "1":
            jogador2.posicionar_navios_manualmente()
        else:
            jogador2.posicionar_navios_automaticamente()
            print(f"\nFrota de {jogador2.nome} posicionada:")
            jogador2.tabuleiro.exibir()

    fim_de_jogo = False
    turno_jogador1 = True
    numero_jogada_global = 1
    tempo_inicio = time.time()

    while not fim_de_jogo:
        if turno_jogador1:
            realizar_jogada_humano(jogador1, jogador2, numero_jogada_global)
            if jogador2.frota_ativa == 0:
                tempo_fim = time.time()
                tempo_total = tempo_fim - tempo_inicio
                gravar_resultado(jogador1.nome, numero_jogada_global, tempo_total, jogador1, jogador2)
                fim_de_jogo = True
            else:
                turno_jogador1 = False
        else:
            if modo == "1":
                realizar_jogada_computador(jogador2, jogador1, numero_jogada_global)
            else:
                realizar_jogada_humano(jogador2, jogador1, numero_jogada_global)

            if jogador1.frota_ativa == 0:
                tempo_fim = time.time()
                tempo_total = tempo_fim - tempo_inicio
                gravar_resultado(jogador2.nome, numero_jogada_global, tempo_total, jogador1, jogador2)
                fim_de_jogo = True
            else:
                turno_jogador1 = True

        numero_jogada_global = numero_jogada_global + 1


if __name__ == "__main__":
    em_execucao = True

    while em_execucao:
        opcao_principal = exibir_menu_principal()

        match opcao_principal:
            case "1":
                opcao_modo = exibir_menu_modos()
                if opcao_modo == "1" or opcao_modo == "2":
                    iniciar_partida(opcao_modo)
                elif opcao_modo == "0":
                    print("Voltando ao menu principal...")
                else:
                    print("Opcao de modo invalida.")
            case "2":
                exibir_estatisticas()
            case "3":
                reproduzir_replay()
            case "4":
                print("\nAnthony Gabriel - GPTech Games")
            case "5":
                print("\nSaindo do jogo. Ate logo!")
                em_execucao = False
            case _:
                print("\nOpcao invalida! Tente novamente.")