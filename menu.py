def exibir_menu_principal():
    print("\n=== BATALHA NAVAL - GPTECH GAMES ===")
    print("1. Nova partida")
    print("2. Ver estatisticas")
    print("3. Assistir replay da ultima partida")
    print("4. Creditos")
    print("5. Sair")
    opcao = input("Escolha uma opcao: ")
    return opcao

def exibir_menu_modos():
    print("\nSelecione o modo de jogo:")
    print("[1] Jogador vs Computador")
    print("[2] Dois Jogadores")
    print("[0] Voltar ao menu")
    opcao = input("Escolha uma opcao: ")
    return opcao