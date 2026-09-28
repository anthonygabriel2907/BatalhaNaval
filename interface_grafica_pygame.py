import sys
import time

import pygame

from jogador import Jogador
from computador import Computador
import estatisticas
import replay

pygame.init()

COR_FUNDO = (10, 10, 22)
COR_AGUA_1 = (0, 162, 232)
COR_AGUA_2 = (0, 140, 205)
COR_BORDA = (0, 70, 120)
COR_ERRO = (220, 240, 255)
COR_ERRO_SOMBRA = (140, 190, 220)
COR_TEXTO = (255, 255, 85)
COR_TEXTO_SOMBRA = (90, 70, 0)
COR_TEXTO_SECUNDARIO = (159, 184, 204)
COR_MOLDURA_EXTERNA = (255, 255, 85)
COR_MOLDURA_INTERNA = (0, 70, 120)
COR_BOTAO = (21, 42, 61)
COR_BOTAO_HOVER = (38, 65, 92)
COR_BOTAO_BORDA = (0, 162, 232)
COR_VITORIA = (126, 217, 87)
COR_SELECIONADO = (255, 255, 85)

LARGURA_TELA = 1200
ALTURA_TELA = 780

tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Batalha Naval - GPTech Games")
relogio = pygame.time.Clock()

fonte_titulo = pygame.font.SysFont("courier", 34, bold=True)
fonte_secao = pygame.font.SysFont("courier", 22, bold=True)
fonte_normal = pygame.font.SysFont("courier", 16, bold=True)
fonte_pequena = pygame.font.SysFont("courier", 13, bold=True)

LETRAS = "ABCDEFGHIJ"


def recortar_margem_transparente(imagem):
    caixa = imagem.get_bounding_rect(min_alpha=10)
    return imagem.subsurface(caixa).copy()


IMG_NAVIO_BASE = recortar_margem_transparente(
    pygame.image.load("assets/ship.png").convert_alpha())
IMG_EXPLOSAO_BASE = recortar_margem_transparente(
    pygame.image.load("assets/explosion.png").convert_alpha())

_cache_navios = {}


def obter_imagem_navio(comprimento, horizontal, tamanho_celula):
    chave = (comprimento, horizontal, tamanho_celula)
    if chave in _cache_navios:
        return _cache_navios[chave]

    if horizontal:
        largura = tamanho_celula * comprimento
        altura = tamanho_celula
        imagem = pygame.transform.scale(IMG_NAVIO_BASE, (largura, altura))
    else:
        largura = tamanho_celula
        altura = tamanho_celula * comprimento
        base_rotacionada = pygame.transform.rotate(IMG_NAVIO_BASE, 90)
        imagem = pygame.transform.scale(base_rotacionada, (largura, altura))

    _cache_navios[chave] = imagem
    return imagem


_cache_explosao = {}


def obter_imagem_explosao(tamanho_celula):
    if tamanho_celula in _cache_explosao:
        return _cache_explosao[tamanho_celula]
    lado = int(tamanho_celula * 1.15)
    imagem = pygame.transform.scale(IMG_EXPLOSAO_BASE, (lado, lado))
    _cache_explosao[tamanho_celula] = imagem
    return imagem


def texto_com_sombra(texto, fonte, cor, x, y, cor_sombra=COR_TEXTO_SOMBRA, deslocamento=2, centralizado=False):
    render_principal = fonte.render(texto, True, cor)
    if centralizado:
        x = x - render_principal.get_width() // 2
    render_sombra = fonte.render(texto, True, cor_sombra)
    tela.blit(render_sombra, (x + deslocamento, y + deslocamento))
    tela.blit(render_principal, (x, y))
    return render_principal.get_rect(topleft=(x, y))


def desenhar_moldura():
    externa = pygame.Rect(15, 15, LARGURA_TELA - 30, ALTURA_TELA - 30)
    pygame.draw.rect(tela, COR_MOLDURA_EXTERNA, externa, 4)
    interna = pygame.Rect(25, 25, LARGURA_TELA - 50, ALTURA_TELA - 50)
    pygame.draw.rect(tela, COR_MOLDURA_INTERNA, interna, 2)


def desenhar_scanlines():
    overlay = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
    for y in range(0, ALTURA_TELA, 3):
        pygame.draw.line(overlay, (0, 0, 0, 35), (0, y), (LARGURA_TELA, y))
    tela.blit(overlay, (0, 0))


class Botao:

    def __init__(self, x, y, largura, altura, texto, fonte=None, ativo=True):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.fonte = fonte or fonte_normal
        self.ativo = ativo

    def desenhar(self, superficie):
        pos_mouse = pygame.mouse.get_pos()
        hover = self.ativo and self.rect.collidepoint(pos_mouse)
        cor_fundo = COR_BOTAO_HOVER if hover else COR_BOTAO
        pygame.draw.rect(superficie, cor_fundo, self.rect)
        pygame.draw.rect(superficie, COR_BOTAO_BORDA, self.rect, 2)

        render = self.fonte.render(self.texto, True, COR_TEXTO if self.ativo else COR_TEXTO_SECUNDARIO)
        pos_texto = render.get_rect(center=self.rect.center)
        superficie.blit(render, pos_texto)

    def clicado(self, pos_evento):
        return self.ativo and self.rect.collidepoint(pos_evento)


def desenhar_tabuleiro(origem_x, origem_y, tamanho_celula, tabuleiro, navios, modo):

    rects = {}

    for i in range(10):
        texto_com_sombra(LETRAS[i], fonte_pequena, COR_TEXTO,
                          origem_x + i * tamanho_celula + tamanho_celula // 2, origem_y - 22,
                          centralizado=True)
    for i in range(10):
        texto_com_sombra(str(i + 1), fonte_pequena, COR_TEXTO,
                          origem_x - 22, origem_y + i * tamanho_celula + tamanho_celula // 2 - 8,
                          centralizado=True)

    for linha in range(10):
        for coluna in range(10):
            x = origem_x + coluna * tamanho_celula
            y = origem_y + linha * tamanho_celula
            cor_agua = COR_AGUA_1 if (linha + coluna) % 2 == 0 else COR_AGUA_2
            rect = pygame.Rect(x, y, tamanho_celula, tamanho_celula)
            pygame.draw.rect(tela, cor_agua, rect)
            pygame.draw.rect(tela, COR_BORDA, rect, 2)
            rects[(linha, coluna)] = rect

    for navio in navios:
        if not navio.coordenadas:
            continue
        deve_desenhar = (modo == "proprio") or (modo == "ataque" and navio.afundou())
        if not deve_desenhar:
            continue

        linhas = [c[0] for c in navio.coordenadas]
        colunas = [c[1] for c in navio.coordenadas]
        horizontal = (min(linhas) == max(linhas))
        linha_topo = min(linhas)
        coluna_topo = min(colunas)

        x = origem_x + coluna_topo * tamanho_celula
        y = origem_y + linha_topo * tamanho_celula
        imagem = obter_imagem_navio(navio.tamanho, horizontal, tamanho_celula)
        tela.blit(imagem, (x, y))

    imagem_explosao = obter_imagem_explosao(tamanho_celula)
    offset_explosao = (imagem_explosao.get_width() - tamanho_celula) // 2

    for linha in range(10):
        for coluna in range(10):
            valor = tabuleiro.matriz[linha][coluna]
            x = origem_x + coluna * tamanho_celula
            y = origem_y + linha * tamanho_celula
            if valor == "X":
                tela.blit(imagem_explosao, (x - offset_explosao, y - offset_explosao))
            elif valor == "O":
                pygame.draw.rect(tela, COR_ERRO_SOMBRA,
                                  (x + tamanho_celula * 0.22, y + tamanho_celula * 0.31,
                                   tamanho_celula * 0.56, tamanho_celula * 0.47))
                pygame.draw.rect(tela, COR_ERRO,
                                  (x + tamanho_celula * 0.27, y + tamanho_celula * 0.27,
                                   tamanho_celula * 0.46, tamanho_celula * 0.40))

    return rects


class _TabuleiroReplay:

    def __init__(self, matriz):
        self.matriz = matriz


class BatalhaNavalPygame:
    ESTADOS = ("menu", "modo", "dificuldade", "posicionamento", "transicao", "batalha",
               "fim", "estatisticas", "replay", "creditos")

    def __init__(self):
        self.estado = "menu"
        self.rodando = True

        self.modo_jogo = None
        self.jogador1 = None
        self.jogador2 = None
        self.jogador_atual = None
        self.jogador_adversario = None
        self.numero_jogada_global = 0
        self.tempo_inicio = None
        self.mensagem_status = ""
        self.mensagem_erro_posicionamento = ""

        self.jogador_em_posicionamento = None
        self.navio_atual_index = 0
        self.orientacao_horizontal = True

        self.vencedor = None
        self.tempo_total_partida = 0

        self._replay_jogadas = []
        self._replay_nomes = []
        self._replay_grades = {}
        self._replay_reproduzindo = False
        self._replay_proximo_passo_em = None
        self._indice_replay = 0

        self._transicao_callback = None
        self._transicao_titulo = ""
        self._transicao_mensagem = ""

        self._construir_botoes_estaticos()

        self._proxima_jogada_cpu_em = None

    def _construir_botoes_estaticos(self):
        cx = LARGURA_TELA // 2

        self.botoes_menu = [
            Botao(cx - 160, 260, 320, 46, "Nova partida"),
            Botao(cx - 160, 315, 320, 46, "Ver estatisticas"),
            Botao(cx - 160, 370, 320, 46, "Assistir replay"),
            Botao(cx - 160, 425, 320, 46, "Creditos"),
            Botao(cx - 160, 480, 320, 46, "Sair"),
        ]

        self.botoes_modo = [
            Botao(cx - 170, 280, 340, 50, "Jogador x Computador"),
            Botao(cx - 170, 345, 340, 50, "Dois Jogadores"),
            Botao(cx - 170, 430, 340, 44, "Voltar ao menu", fonte=fonte_pequena),
        ]

        self.botoes_dificuldade = [
            Botao(cx - 170, 280, 340, 50, "Facil"),
            Botao(cx - 170, 345, 340, 50, "Medio"),
            Botao(cx - 170, 410, 340, 50, "Dificil"),
            Botao(cx - 170, 480, 340, 44, "Voltar ao menu", fonte=fonte_pequena),
        ]

        self.botao_voltar_menu = Botao(cx - 110, ALTURA_TELA - 70, 220, 42, "Voltar ao menu", fonte=fonte_pequena)

        self.botao_orientacao = Botao(cx - 170, ALTURA_TELA - 150, 200, 42, "Orientacao: H")
        self.botao_auto = Botao(cx + 10, ALTURA_TELA - 150, 300, 42, "Posicionar automaticamente")

        self.botao_continuar_transicao = Botao(cx - 110, 460, 220, 46, "Continuar")

        self.botoes_fim = [
            Botao(cx - 330, ALTURA_TELA - 110, 200, 44, "Ver replay"),
            Botao(cx - 100, ALTURA_TELA - 110, 200, 44, "Nova partida"),
            Botao(cx + 130, ALTURA_TELA - 110, 200, 44, "Menu principal"),
        ]

        self.botao_replay_anterior = Botao(cx - 330, ALTURA_TELA - 130, 200, 44, "< Anterior")
        self.botao_replay_play = Botao(cx - 100, ALTURA_TELA - 130, 200, 44, "Play")
        self.botao_replay_proximo = Botao(cx + 130, ALTURA_TELA - 130, 200, 44, "Proxima >")


    def rodar(self):
        while self.rodando:
            self._cuidar_eventos()
            self._atualizar_logica_assincrona()
            self._desenhar()
            pygame.display.flip()
            relogio.tick(60)
        pygame.quit()
        sys.exit()

    def _atualizar_logica_assincrona(self):
        if self._proxima_jogada_cpu_em is not None and time.time() >= self._proxima_jogada_cpu_em:
            self._proxima_jogada_cpu_em = None
            self._executar_jogada_computador()

        if self.estado == "replay":
            self._avancar_replay_automatico()

    def _cuidar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                self._cuidar_clique(evento.pos)


    def _cuidar_clique(self, pos):
        if self.estado == "menu":
            self._clique_menu(pos)
        elif self.estado == "modo":
            self._clique_modo(pos)
        elif self.estado == "dificuldade":
            self._clique_dificuldade(pos)
        elif self.estado == "posicionamento":
            self._clique_posicionamento(pos)
        elif self.estado == "transicao":
            if self.botao_continuar_transicao.clicado(pos):
                callback = self._transicao_callback
                self._transicao_callback = None
                if callback:
                    callback()
        elif self.estado == "batalha":
            self._clique_batalha(pos)
        elif self.estado == "fim":
            self._clique_fim(pos)
        elif self.estado == "estatisticas":
            if self.botao_voltar_menu.clicado(pos):
                self.estado = "menu"
        elif self.estado == "replay":
            self._clique_replay(pos)
        elif self.estado == "creditos":
            if self.botao_voltar_menu.clicado(pos):
                self.estado = "menu"

    def _clique_menu(self, pos):
        nomes = ["nova", "estatisticas", "replay", "creditos", "sair"]
        for botao, nome in zip(self.botoes_menu, nomes):
            if botao.clicado(pos):
                if nome == "nova":
                    self.estado = "modo"
                elif nome == "estatisticas":
                    self.estado = "estatisticas"
                elif nome == "replay":
                    self._carregar_replay()
                    self.estado = "replay"
                elif nome == "creditos":
                    self.estado = "creditos"
                elif nome == "sair":
                    self.rodando = False

    def _clique_modo(self, pos):
        if self.botoes_modo[0].clicado(pos):
            self.estado = "dificuldade"
        elif self.botoes_modo[1].clicado(pos):
            self._iniciar_novo_jogo("dois_jogadores")
        elif self.botoes_modo[2].clicado(pos):
            self.estado = "menu"

    def _clique_dificuldade(self, pos):
        niveis = ["facil", "medio", "dificil"]
        for botao, nivel in zip(self.botoes_dificuldade[:3], niveis):
            if botao.clicado(pos):
                self._iniciar_novo_jogo("cpu", dificuldade=nivel)
                return
        if self.botoes_dificuldade[3].clicado(pos):
            self.estado = "modo"


    def _iniciar_novo_jogo(self, modo, dificuldade="facil"):
        self.modo_jogo = modo
        self.jogador1 = Jogador("Jogador 1")
        self.jogador2 = Computador("Computador", dificuldade=dificuldade) if modo == "cpu" else Jogador("Jogador 2")

        replay.limpar_historico()
        self.numero_jogada_global = 0

        self._iniciar_posicionamento(self.jogador1)


    def _iniciar_posicionamento(self, jogador):
        self.jogador_em_posicionamento = jogador
        self.navio_atual_index = 0
        self.orientacao_horizontal = True
        self.mensagem_erro_posicionamento = ""
        self.estado = "posicionamento"

    def _clique_posicionamento(self, pos):
        if self.botao_auto.clicado(pos):
            jogador = self.jogador_em_posicionamento

            navios_restantes = jogador.navios[self.navio_atual_index:]
            jogador.posicionar_navios_automaticamente(navios_restantes)
            self.navio_atual_index = len(jogador.navios)
            self._avancar_apos_posicionamento()
            return

        if self.botao_orientacao.clicado(pos):
            self.orientacao_horizontal = not self.orientacao_horizontal
            return

        for (linha, coluna), rect in self._rects_grade_posicionamento.items():
            if rect.collidepoint(pos):
                self._tentar_posicionar(linha, coluna)
                return

    def _tentar_posicionar(self, linha, coluna):
        jogador = self.jogador_em_posicionamento
        if self.navio_atual_index >= len(jogador.navios):
            return
        navio = jogador.navios[self.navio_atual_index]
        direcao = 0 if self.orientacao_horizontal else 1

        if jogador.pode_posicionar(navio.tamanho, linha, coluna, direcao):
            jogador.colocar_navio(navio, linha, coluna, direcao)
            self.navio_atual_index += 1
            self.mensagem_erro_posicionamento = ""
            if self.navio_atual_index >= len(jogador.navios):
                self._avancar_apos_posicionamento()
        else:
            self.mensagem_erro_posicionamento = "Posicao invalida! O navio sai do tabuleiro ou sobrepoe outro."

    def _avancar_apos_posicionamento(self):
        if self.jogador_em_posicionamento is self.jogador1:
            if self.modo_jogo == "cpu":
                self.jogador2.posicionar_navios_automaticamente()
                self._iniciar_batalha()
            else:
                self._mostrar_transicao(
                    f"Frota do {self.jogador1.nome} pronta!",
                    "Passe o computador para o Jogador 2 e clique em continuar.",
                    lambda: self._iniciar_posicionamento(self.jogador2))
        else:
            self._iniciar_batalha()


    def _mostrar_transicao(self, titulo, mensagem, callback):
        self._transicao_titulo = titulo
        self._transicao_mensagem = mensagem
        self._transicao_callback = callback
        self.estado = "transicao"


    def _iniciar_batalha(self):
        self.tempo_inicio = time.time()
        self.jogador_atual = self.jogador1
        self.jogador_adversario = self.jogador2
        self._ir_para_tela_batalha()

    def _ir_para_tela_batalha(self):
        if self.modo_jogo == "dois_jogadores":
            self._mostrar_transicao(
                f"Vez de {self.jogador_atual.nome}",
                "Passe o computador e clique em continuar para ver seu radar de ataque.",
                self._entrar_tela_batalha)
        else:
            self._entrar_tela_batalha()

    def _entrar_tela_batalha(self):
        self.mensagem_status = "Clique numa celula do radar de ataque."
        self.estado = "batalha"

    def _clique_batalha(self, pos):
        if self.modo_jogo == "cpu" and self.jogador_atual is self.jogador2:
            return
        for (linha, coluna), rect in self._rects_radar_ataque.items():
            if rect.collidepoint(pos):
                self._atacar(linha, coluna)
                return

    def _encontrar_navio(self, jogador, linha, coluna):
        for navio in jogador.navios:
            if (linha, coluna) in navio.coordenadas:
                return navio
        return None

    def _atacar(self, linha, coluna):
        atacante = self.jogador_atual
        defensor = self.jogador_adversario
        casa = defensor.tabuleiro.matriz[linha][coluna]

        if casa in ("X", "O"):
            self.mensagem_status = "Essa posicao ja foi jogada. Escolha outra."
            return

        letra = LETRAS[coluna]
        numero = linha + 1
        self.numero_jogada_global += 1
        atacante.tentativas += 1

        if casa == "N":
            defensor.tabuleiro.matriz[linha][coluna] = "X"
            atacante.acertos += 1
            navio_atingido = self._encontrar_navio(defensor, linha, coluna)
            resultado = "Acerto"
            if navio_atingido is not None:
                navio_atingido.registar_acerto()
                if navio_atingido.afundou():
                    defensor.frota_ativa -= 1
                    resultado = "Navio afundado"
                    self.mensagem_status = (
                        f"Navio afundado! Voce destruiu um navio "
                        f"{navio_atingido.tipo.lower()} do adversario.")
                else:
                    self.mensagem_status = "Acerto! Voce atingiu um navio inimigo."
            replay.registar_jogada(self.numero_jogada_global, atacante.nome, letra, numero, resultado)

            if defensor.frota_ativa == 0:
                self._finalizar_partida(atacante)
                return

            self._passar_turno()
        else:
            defensor.tabuleiro.matriz[linha][coluna] = "O"
            self.mensagem_status = "Agua! Nenhum navio atingido nessa posicao."
            replay.registar_jogada(self.numero_jogada_global, atacante.nome, letra, numero, "Agua")
            self._passar_turno()

    def _passar_turno(self):
        self.jogador_atual, self.jogador_adversario = self.jogador_adversario, self.jogador_atual
        if self.modo_jogo == "cpu" and self.jogador_atual is self.jogador2:
            self._proxima_jogada_cpu_em = time.time() + 1.5
        else:
            self._ir_para_tela_batalha()

    def _executar_jogada_computador(self):
        computador = self.jogador2
        defensor = self.jogador1
        linha, coluna = computador.gerar_jogada()
        letra = LETRAS[coluna]
        numero = linha + 1
        casa = defensor.tabuleiro.matriz[linha][coluna]

        self.numero_jogada_global += 1
        computador.tentativas += 1

        if casa == "N":
            defensor.tabuleiro.matriz[linha][coluna] = "X"
            computador.acertos += 1
            navio_atingido = self._encontrar_navio(defensor, linha, coluna)
            resultado = "Acerto"
            if navio_atingido is not None:
                navio_atingido.registar_acerto()
                if navio_atingido.afundou():
                    defensor.frota_ativa -= 1
                    resultado = "Navio afundado"
                    self.mensagem_status = "O Computador afundou um dos seus navios! Sua vez."
                else:
                    self.mensagem_status = "O Computador acertou um dos seus navios! Sua vez."

            replay.registar_jogada(self.numero_jogada_global, computador.nome, letra, numero, resultado)
            computador.registar_resultado(linha, coluna, resultado)

            if defensor.frota_ativa == 0:
                self._finalizar_partida(computador)
                return

            self.jogador_atual, self.jogador_adversario = self.jogador1, self.jogador2
            self.estado = "batalha"
        else:
            defensor.tabuleiro.matriz[linha][coluna] = "O"
            replay.registar_jogada(self.numero_jogada_global, computador.nome, letra, numero, "Agua")
            computador.registar_resultado(linha, coluna, "Agua")
            self.jogador_atual, self.jogador_adversario = self.jogador1, self.jogador2
            self.mensagem_status = "O computador errou! Sua vez."
            self.estado = "batalha"

    def _finalizar_partida(self, vencedor):
        self.vencedor = vencedor
        self.tempo_total_partida = time.time() - self.tempo_inicio
        estatisticas.gravar_resultado(
            vencedor.nome, self.numero_jogada_global, self.tempo_total_partida,
            self.jogador1, self.jogador2)
        self.estado = "fim"

    def _clique_fim(self, pos):
        if self.botoes_fim[0].clicado(pos):
            self._carregar_replay()
            self.estado = "replay"
        elif self.botoes_fim[1].clicado(pos):
            self.estado = "modo"
        elif self.botoes_fim[2].clicado(pos):
            self.estado = "menu"


    def _carregar_replay(self):
        try:
            with open(replay.CAMINHO_REPLAY, "r") as ficheiro:
                linhas_brutas = [l.strip() for l in ficheiro.readlines() if l.strip()]
        except FileNotFoundError:
            linhas_brutas = []

        self._replay_jogadas = []
        nomes_ordem = []
        for linha in linhas_brutas:
            partes = linha.split(" - ")
            if len(partes) != 4:
                continue
            _, nome, coordenada, resultado = partes
            letra = coordenada[0]
            try:
                numero = int(coordenada[1:])
            except ValueError:
                continue
            if letra not in LETRAS:
                continue
            lin = numero - 1
            col = LETRAS.index(letra)
            self._replay_jogadas.append({
                "texto": linha, "nome": nome, "lin": lin, "col": col, "resultado": resultado,
            })
            if nome not in nomes_ordem:
                nomes_ordem.append(nome)

        self._replay_nomes = nomes_ordem
        self._indice_replay = 0
        self._replay_reproduzindo = False
        self._replay_proximo_passo_em = None
        self._reconstruir_grades_replay()

    def _reconstruir_grades_replay(self):
        # Recria, do zero, uma matriz 10x10 de tiros (por jogador) contendo
        # so o que ja aconteceu ate a jogada atual - e' isso que da o efeito
        # de "video" ao avancar/retroceder ou dar play no replay.
        self._replay_grades = {nome: [["~"] * 10 for _ in range(10)] for nome in self._replay_nomes}
        for indice, jogada in enumerate(self._replay_jogadas):
            if indice > self._indice_replay:
                break
            marca = "X" if jogada["resultado"] in ("Acerto", "Navio afundado") else "O"
            self._replay_grades[jogada["nome"]][jogada["lin"]][jogada["col"]] = marca

    def _replay_ir_para(self, indice):
        total = len(self._replay_jogadas)
        if total == 0:
            return
        self._indice_replay = max(0, min(indice, total - 1))
        self._reconstruir_grades_replay()

    def _clique_replay(self, pos):
        if self.botao_replay_anterior.clicado(pos):
            self._replay_reproduzindo = False
            self._replay_ir_para(self._indice_replay - 1)
        elif self.botao_replay_proximo.clicado(pos):
            self._replay_reproduzindo = False
            self._replay_ir_para(self._indice_replay + 1)
        elif self.botao_replay_play.clicado(pos):
            if self._replay_jogadas:
                self._replay_reproduzindo = not self._replay_reproduzindo
                if self._replay_reproduzindo and self._indice_replay >= len(self._replay_jogadas) - 1:
                    # Se estava no fim, o play recomeca do inicio
                    self._indice_replay = 0
                    self._reconstruir_grades_replay()
                self._replay_proximo_passo_em = time.time() + 0.5
        elif self.botao_voltar_menu.clicado(pos):
            self._replay_reproduzindo = False
            self.estado = "menu"

    def _avancar_replay_automatico(self):
        if not self._replay_reproduzindo:
            return
        if time.time() < self._replay_proximo_passo_em:
            return

        if self._indice_replay >= len(self._replay_jogadas) - 1:
            self._replay_reproduzindo = False
            return

        self._indice_replay += 1
        self._reconstruir_grades_replay()
        self._replay_proximo_passo_em = time.time() + 0.5


    def _desenhar(self):
        tela.fill(COR_FUNDO)

        if self.estado == "menu":
            self._desenhar_menu()
        elif self.estado == "modo":
            self._desenhar_modo()
        elif self.estado == "dificuldade":
            self._desenhar_dificuldade()
        elif self.estado == "posicionamento":
            self._desenhar_posicionamento()
        elif self.estado == "transicao":
            self._desenhar_transicao()
        elif self.estado == "batalha":
            self._desenhar_batalha()
        elif self.estado == "fim":
            self._desenhar_fim()
        elif self.estado == "estatisticas":
            self._desenhar_estatisticas()
        elif self.estado == "replay":
            self._desenhar_replay()
        elif self.estado == "creditos":
            self._desenhar_creditos()

        desenhar_moldura()
        desenhar_scanlines()

    def _desenhar_menu(self):
        texto_com_sombra("BATALHA NAVAL", fonte_titulo, COR_TEXTO, LARGURA_TELA // 2, 110, centralizado=True)
        texto_com_sombra("GPTECH GAMES", fonte_secao, COR_TEXTO_SECUNDARIO, LARGURA_TELA // 2, 160, centralizado=True)
        for botao in self.botoes_menu:
            botao.desenhar(tela)

    def _desenhar_modo(self):
        texto_com_sombra("SELECIONE O MODO DE JOGO", fonte_secao, COR_TEXTO,
                          LARGURA_TELA // 2, 190, centralizado=True)
        for botao in self.botoes_modo:
            botao.desenhar(tela)

    def _desenhar_dificuldade(self):
        texto_com_sombra("SELECIONE A DIFICULDADE DO COMPUTADOR", fonte_secao, COR_TEXTO,
                          LARGURA_TELA // 2, 190, centralizado=True)
        for botao in self.botoes_dificuldade:
            botao.desenhar(tela)

    def _desenhar_posicionamento(self):
        jogador = self.jogador_em_posicionamento
        texto_com_sombra(f"Posicionamento de frota: {jogador.nome}", fonte_secao, COR_TEXTO,
                          LARGURA_TELA // 2, 55, centralizado=True)

        if self.navio_atual_index < len(jogador.navios):
            navio = jogador.navios[self.navio_atual_index]
            msg = f"Clique na celula inicial do navio {navio.tipo} (tamanho {navio.tamanho})"
        else:
            msg = "Frota completa!"
        texto_com_sombra(msg, fonte_normal, COR_TEXTO_SECUNDARIO, LARGURA_TELA // 2, 100, centralizado=True)

        if self.mensagem_erro_posicionamento:
            texto_com_sombra(self.mensagem_erro_posicionamento, fonte_normal, (255, 120, 120),
                              LARGURA_TELA // 2, 128, centralizado=True)

        tamanho_celula = 40
        origem_x = LARGURA_TELA // 2 - 5 * tamanho_celula
        origem_y = 180
        self._rects_grade_posicionamento = desenhar_tabuleiro(
            origem_x, origem_y, tamanho_celula, jogador.tabuleiro, jogador.navios, modo="proprio")

        self.botao_orientacao.texto = f"Orientacao: {'H' if self.orientacao_horizontal else 'V'}"
        self.botao_orientacao.desenhar(tela)
        self.botao_auto.desenhar(tela)

    def _desenhar_transicao(self):
        texto_com_sombra(self._transicao_titulo, fonte_secao, COR_TEXTO,
                          LARGURA_TELA // 2, 300, centralizado=True)
        texto_com_sombra(self._transicao_mensagem, fonte_normal, COR_TEXTO_SECUNDARIO,
                          LARGURA_TELA // 2, 350, centralizado=True)
        self.botao_continuar_transicao.desenhar(tela)

    def _desenhar_batalha(self):
        if self.modo_jogo == "cpu":
            dono, alvo = self.jogador1, self.jogador2
        else:
            dono, alvo = self.jogador_atual, self.jogador_adversario

        texto_com_sombra(f"Turno de {self.jogador_atual.nome}", fonte_secao, COR_TEXTO,
                          LARGURA_TELA // 2, 45, centralizado=True)

        tamanho_celula = 32
        y_topo = 130

        origem_proprio_x = 90
        texto_com_sombra(f"Seu tabuleiro ({dono.nome})", fonte_normal, COR_TEXTO_SECUNDARIO,
                          origem_proprio_x + 5 * tamanho_celula, y_topo - 45, centralizado=True)
        desenhar_tabuleiro(origem_proprio_x, y_topo, tamanho_celula, dono.tabuleiro,
                            dono.navios, modo="proprio")

        origem_ataque_x = LARGURA_TELA - 90 - 10 * tamanho_celula
        texto_com_sombra(f"Radar de ataque ({alvo.nome})", fonte_normal, COR_TEXTO_SECUNDARIO,
                          origem_ataque_x + 5 * tamanho_celula, y_topo - 45, centralizado=True)
        self._rects_radar_ataque = desenhar_tabuleiro(
            origem_ataque_x, y_topo, tamanho_celula, alvo.tabuleiro, alvo.navios, modo="ataque")

        texto_com_sombra(self.mensagem_status, fonte_normal, COR_TEXTO,
                          LARGURA_TELA // 2, ALTURA_TELA - 60, centralizado=True)

    def _desenhar_fim(self):
        aproveitamento1 = estatisticas.calcular_aproveitamento(self.jogador1)
        aproveitamento2 = estatisticas.calcular_aproveitamento(self.jogador2)
        minutos = int(self.tempo_total_partida // 60)
        segundos = int(self.tempo_total_partida % 60)

        texto_com_sombra("FIM DE JOGO", fonte_titulo, COR_TEXTO, LARGURA_TELA // 2, 90, centralizado=True)
        texto_com_sombra(f"Vencedor: {self.vencedor.nome}", fonte_secao, COR_VITORIA,
                          LARGURA_TELA // 2, 150, centralizado=True)
        texto_com_sombra(f"Total de jogadas: {self.numero_jogada_global}", fonte_normal, COR_TEXTO_SECUNDARIO,
                          LARGURA_TELA // 2, 195, centralizado=True)
        texto_com_sombra(f"Tempo de partida: {minutos:02d}:{segundos:02d}", fonte_normal, COR_TEXTO_SECUNDARIO,
                          LARGURA_TELA // 2, 222, centralizado=True)

        texto_com_sombra(
            f"{self.jogador1.nome} - Acertos: {self.jogador1.acertos}/{self.jogador1.tentativas} "
            f"({aproveitamento1:.1f}%)", fonte_normal, COR_TEXTO, LARGURA_TELA // 2, 270, centralizado=True)
        texto_com_sombra(
            f"{self.jogador2.nome} - Acertos: {self.jogador2.acertos}/{self.jogador2.tentativas} "
            f"({aproveitamento2:.1f}%)", fonte_normal, COR_TEXTO, LARGURA_TELA // 2, 297, centralizado=True)

        for botao in self.botoes_fim:
            botao.desenhar(tela)

    def _desenhar_estatisticas(self):
        texto_com_sombra("ESTATISTICAS DE DESEMPENHO", fonte_secao, COR_TEXTO,
                          LARGURA_TELA // 2, 55, centralizado=True)

        try:
            with open(estatisticas.CAMINHO_ESTATISTICAS, "r") as ficheiro:
                linhas = ficheiro.readlines()
        except FileNotFoundError:
            linhas = []

        if not linhas:
            texto_com_sombra("Nenhuma partida registada ainda.", fonte_normal, COR_TEXTO_SECUNDARIO,
                              LARGURA_TELA // 2, 130, centralizado=True)
        else:
            texto_com_sombra(f"Total de partidas jogadas: {len(linhas)}", fonte_normal, COR_TEXTO_SECUNDARIO,
                              LARGURA_TELA // 2, 110, centralizado=True)
            y = 150
            for linha in linhas[-14:]:
                texto_com_sombra(linha.strip(), fonte_pequena, COR_TEXTO_SECUNDARIO, 60, y)
                y += 26

        self.botao_voltar_menu.desenhar(tela)

    def _desenhar_replay(self):
        texto_com_sombra("REPLAY DA ULTIMA PARTIDA", fonte_secao, COR_TEXTO,
                          LARGURA_TELA // 2, 45, centralizado=True)

        if not self._replay_jogadas:
            texto_com_sombra("O historico de jogadas esta vazio.", fonte_normal, COR_TEXTO_SECUNDARIO,
                              LARGURA_TELA // 2, 220, centralizado=True)
            self.botao_voltar_menu.desenhar(tela)
            return

        total = len(self._replay_jogadas)
        jogada_atual = self._replay_jogadas[self._indice_replay]

        texto_com_sombra(f"Jogada {self._indice_replay + 1}/{total}", fonte_normal, COR_TEXTO_SECUNDARIO,
                          LARGURA_TELA // 2, 80, centralizado=True)
        texto_com_sombra(jogada_atual["texto"], fonte_secao, COR_TEXTO,
                          LARGURA_TELA // 2, 105, centralizado=True)

        tamanho_celula = 32
        y_topo = 190
        largura_tabuleiro = 10 * tamanho_celula
        gap = 100
        origem_x_1 = LARGURA_TELA // 2 - largura_tabuleiro - gap // 2
        origem_x_2 = LARGURA_TELA // 2 + gap // 2

        nomes = self._replay_nomes
        origens = [origem_x_1, origem_x_2]

        for nome, origem_x in zip(nomes, origens):
            texto_com_sombra(f"Ataques de {nome}", fonte_normal, COR_TEXTO_SECUNDARIO,
                              origem_x + 5 * tamanho_celula, y_topo - 45, centralizado=True)
            tabuleiro_falso = _TabuleiroReplay(self._replay_grades[nome])
            rects = desenhar_tabuleiro(origem_x, y_topo, tamanho_celula, tabuleiro_falso, [], modo="ataque")

            # Realca a celula da jogada atual, se for deste jogador
            if jogada_atual["nome"] == nome:
                rect_atual = rects[(jogada_atual["lin"], jogada_atual["col"])]
                pygame.draw.rect(tela, COR_SELECIONADO, rect_atual, 3)

        self.botao_replay_play.texto = "Pausar" if self._replay_reproduzindo else "Play"
        self.botao_replay_anterior.desenhar(tela)
        self.botao_replay_play.desenhar(tela)
        self.botao_replay_proximo.desenhar(tela)
        self.botao_voltar_menu.desenhar(tela)

    def _desenhar_creditos(self):
        texto_com_sombra("CRÉDITOS", fonte_titulo, COR_TEXTO, LARGURA_TELA // 2, 160, centralizado=True)
        linhas = [
            "Batalha Naval - GPTech Games",
            "Desenvolvido por Anthony",
        ]
        y = 250
        for linha in linhas:
            texto_com_sombra(linha, fonte_normal, COR_TEXTO_SECUNDARIO, LARGURA_TELA // 2, y, centralizado=True)
            y += 30

        self.botao_voltar_menu.desenhar(tela)


if __name__ == "__main__":
    app = BatalhaNavalPygame()
    app.rodar()
