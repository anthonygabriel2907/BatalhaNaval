def converter_coordenada(entrada):
    entrada = entrada.upper()
    entrada = entrada.strip()

    if len(entrada) < 2:
        return None, None

    if len(entrada) > 3:
        return None, None

    letra = entrada[0]
    numero_str = entrada[1:]

    if letra < 'A':
        return None, None

    if letra > 'J':
        return None, None

    if not numero_str.isdigit():
        return None, None

    linha = int(numero_str) - 1
    coluna = ord(letra) - ord('A')

    if linha < 0 or linha > 9:
        return None, None

    if coluna < 0 or coluna > 9:
        return None, None

    return linha, coluna