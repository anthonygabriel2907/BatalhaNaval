def exibir_menu():
    while True:
        print("\nBATALHA NAVAL - GPTECH GAMES")
        print("1. Nova partida")
        print("2. Ver estatisticas")
        print("3. Assistir replay da ultima partida")
        print("4. Creditos")
        print("5. Sair")

        opcao = input("Escolha uma opcao: ")

        match opcao:
            case "1":
                print("\nIniciando nova partida...")
                # A lógica de instanciar jogadores e tabuleiro entrará aqui
            case "2":
                print("\nEstatisticas em desenvolvimento...")
            case "3":
                print("\nReplay em desenvolvimento...")
            case "4":
                print("\nAnthony Gabriel Sotto Mayor Silva - GPTech Games")
            case "5":
                print("\nSaindo do jogo...")
                break
            case _:
                print("\nOpcao invalida! Tente novamente.")