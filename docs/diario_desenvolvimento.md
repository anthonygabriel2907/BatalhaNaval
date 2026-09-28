## 22/09/2026 (estrutura e modo texto)

- O que foi implementado: arquitetura de pastas do projeto, separando a
  lógica do jogo (Jogador, Tabuleiro, Navio) da apresentação. Modo texto
  completo: menu, posicionamento manual/automático, validação de
  coordenadas, tabuleiro 10x10 e o loop de uma partida (RF01–RF11).
- Dificuldades encontradas: percebi um bug crítico — o jogador que
  atacava conseguia ver o tabuleiro completo do adversário, inclusive os
  navios ainda não atingidos.
- Como foram superadas: criei um método separado `exibir_ataque()` no
  Tabuleiro, que esconde os navios não descobertos, usado sempre que o
  jogador escolhe onde atacar.

## 24/09/2026 (estatísticas, replay e interface gráfica)

- O que foi implementado: RF12 (estatísticas de acertos/aproveitamento) e
  RF13 (histórico de jogadas em `data/replay.txt`). README com
  instruções e decisões de projeto. Interface gráfica completa em
  Pygame (RNF08), estilo arcade retro, com sprites próprios de navio e
  explosão, cobrindo o mesmo fluxo do modo texto.
- Dificuldades encontradas: o tempo de partida estava formatado errado;
  e, na interface gráfica, a tela chegava a mostrar rapidamente os
  navios do computador antes dele atirar — mesmo tipo de vazamento do
  bug do modo texto, só que na versão gráfica.
- Como foram superadas: corrigi o cálculo de horas/minutos/segundos; e
  fixei a tela sempre na perspectiva do jogador humano no modo Jogador x
  Computador, então os navios do computador nunca aparecem.

## 28/09/2026 (ajustes finais e IA com níveis de dificuldade)

- O que foi implementado: correção de um bug em que posicionar um navio
  manualmente e depois clicar em "automático" fazia o jogo esquecer os
  navios já colocados; aumento da frota para 5 navios (2 grandes + 3
  pequenos); 3 níveis de dificuldade pra IA (fácil, médio, difícil); e
  replay gráfico em formato de "vídeo" da partida, com Play/Pausa.
- Dificuldades encontradas: fazer a IA do nível difícil identificar a
  orientação do navio após dois acertos alinhados, e focar só nas
  pontas dessa linha.
- Como foram superadas: usei uma fila de "próximos alvos" que a IA
  consulta antes de sortear uma jogada aleatória, atualizada a cada
  resultado de tiro.
- Outras anotações: testei os 3 níveis simulando partidas automáticas e
  comparando a média de tiros até afundar a frota — o difícil precisa
  de bem menos tiros que o fácil.
