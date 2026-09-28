# Batalha Naval — GPTech Games

Sistema de Batalha Naval em modo texto, desenvolvido em Python 3.10+, para a
disciplina de Programação em Python (CEFET-MG, Campus Divinópolis).

## Como executar

Requisitos: Python 3.10 ou superior (o projeto usa `match/case`). Nenhuma
biblioteca externa é necessária, apenas a biblioteca padrão do Python
(`tkinter` já vem incluído no Python padrão; em algumas distros Linux é
preciso instalar o pacote `python3-tk` separadamente, ex.:
`sudo apt install python3-tk`).

### Modo texto

```bash
python3 main.py
```

### Interface gráfica (bônus — RNF08)

Duas versões de interface gráfica estão disponíveis; escolha uma delas
(não é preciso rodar as duas):

**Versão Tkinter** (não precisa instalar nada além do Python):

```bash
python3 interface_grafica.py
```

**Versão Pygame** (estilo arcade retro, com sprites de navio/explosão em
`assets/`):

```bash
pip install -r requirements.txt
python3 interface_grafica_pygame.py
```

Ambas reaproveitam exatamente a mesma lógica de jogo do modo texto
(`Jogador`, `Computador`, `Tabuleiro`, `estatisticas.py`, `replay.py`) —
elas só desenham as telas e chamam essas mesmas funções nos cliques do
usuário. Cobrem todo o escopo obrigatório: menu principal, seleção de
modo, posicionamento manual (clique na célula + escolha de orientação
H/V) ou automático, tabuleiro próprio e radar de ataque (que esconde os
navios do adversário até serem atingidos), tela de fim de jogo com
estatísticas, tela de estatísticas acumuladas e um visualizador de
replay com navegação "Anterior/Próxima".

O jogo abre o menu principal descrito no enunciado:

```
1. Nova partida
2. Ver estatisticas
3. Assistir replay da ultima partida
4. Creditos
5. Sair
```

## Estrutura do projeto

```
BatalhaNaval/
├── main.py           # Loop principal, menu e regras de uma partida (modo texto)
├── interface_grafica.py        # Interface grafica em Tkinter (bonus RNF08)
├── interface_grafica_pygame.py # Interface grafica em Pygame, estilo arcade retro (bonus RNF08)
├── assets/           # Sprites usados pela interface Pygame (ship.png, explosion.png)
├── menu.py           # Telas de menu (principal e seleção de modo) do modo texto
├── tabuleiro.py       # Classe Tabuleiro (matriz 10x10, exibição normal e de ataque)
├── navios.py          # Classe Navio (posições, acertos, afundamento)
├── jogador.py         # Classe Jogador (frota, posicionamento, tentativas/acertos)
├── computador.py       # Classe Computador (herda de Jogador, joga sozinho)
├── estatisticas.py     # Grava e exibe estatísticas de desempenho
├── replay.py          # Grava e reproduz o histórico da última partida
├── utils.py           # Conversão e validação de coordenadas (ex.: C5)
├── data/              # Arquivos gerados em tempo de execução (estatisticas.txt, replay.txt)
└── docs/              # Documentação complementar (ex.: diário de desenvolvimento)
```

## Como jogar

1. No menu principal, escolha **1. Nova partida**.
2. Escolha o modo de jogo: **Jogador x Computador** ou **Dois Jogadores**.
3. Posicione sua frota manualmente (informando coordenada inicial + orientação
   H/V) ou automaticamente. A frota de cada jogador é composta por 1 navio
   grande (4 posições) e 2 navios pequenos (2 posições cada).
4. A cada turno, informe a coordenada do ataque no formato `Letra+Número`
   (ex.: `C5`, colunas de A a J, linhas de 1 a 10).
5. O jogo mostra `~` para água não jogada, `X` para acerto e `O` para água
   jogada. **Os navios do adversário que ainda não foram atingidos nunca são
   mostrados** — essa é a visão de ataque, para não revelar a posição da
   frota inimiga antes da hora.
6. A partida termina quando um jogador afunda todos os navios do adversário.
   O resultado (vencedor, número de jogadas, tempo, acertos e aproveitamento
   de cada jogador) é exibido na tela e salvo em `data/estatisticas.txt`.

## Decisões de projeto

- **Visão de ataque separada da visão da própria frota**: o `Tabuleiro` tem
  dois métodos de exibição — `exibir()` (mostra a própria frota, usado ao
  posicionar navios e conferir o próprio tabuleiro) e `exibir_ataque()`
  (esconde os navios ainda não atingidos, usado quando um jogador está
  escolhendo onde atacar). Isso garante que nenhum jogador veja a frota do
  adversário antes de acertá-la.
- **Persistência**: `estatisticas.txt` e `replay.txt` ficam em `data/`,
  conforme a arquitetura de pastas definida no enunciado. São recriados
  automaticamente na primeira execução, caso não existam.
- **Estatísticas de desempenho (RF12)**: cada jogador acumula `tentativas`
  (tiros dados) e `acertos` (tiros que atingiram um navio) durante a
  partida. Ao final, calcula-se o aproveitamento (`acertos / tentativas`)
  de cada jogador e tudo é salvo junto do resultado da partida.
- **IA do computador com 3 níveis (RN05)**: *fácil* (tiros aleatórios sem
  repetir), *médio* (após um acerto, testa as casas vizinhas até afundar o
  navio) e *difícil* (busca por paridade/xadrez e, com 2 acertos alinhados,
  atira só nas pontas da linha). O computador é informado do resultado de
  cada tiro por `registar_resultado()`. Nas simulações, o nível difícil
  afunda a frota com bem menos tiros que o fácil.
- **Frota**: 5 navios (2 grandes de 4 posições e 3 pequenos de 2),
  usando só os dois tipos exigidos em RF03.
- **Replay em formato de vídeo (Pygame)**: o histórico salvo em
  `data/replay.txt` é usado para reconstruir dois radares (um por jogador)
  com os tiros aparecendo jogada a jogada, com Play/Pausa e Anterior/Próxima.
- **Interface gráfica separada do modo texto**: tanto `interface_grafica.py`
  (Tkinter) quanto `interface_grafica_pygame.py` (Pygame) não duplicam
  nenhuma regra de negócio — ambas importam as mesmas classes e funções
  usadas no `main.py` e só cuidam da apresentação. Isso evita divergência
  de comportamento entre as versões e mantém a lógica principal nas
  funções originais, como pede o enunciado.
- **Perspectiva fixa no modo Jogador x Computador (Pygame)**: durante o
  pequeno atraso em que o computador "pensa" antes de atirar, a tela
  continua fixada na perspectiva do jogador humano (mesmo tabuleiro e
  radar de ataque) — isso evita que os navios do computador apareçam
  na tela nesse intervalo, e cliques feitos nesse momento são ignorados.

## Autor

Anthony — Engenharia de Computação, CEFET-MG Campus Divinópolis.
