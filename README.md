 Pac-Man Evolution 

O Pac-Man Evolution é uma aplicação desktop escrita em Python que recria a experiência clássica do arcade com funcionalidades modernas. O projeto foca em uma implementação limpa de Orientação a Objetos (POO) e manipulação de gráficos vetoriais em tempo real com tkinter.

 

🛠️ Arquitetura do Sistema 

O código é estruturado em uma arquitetura de Máquina de Estados de Interface, onde a classe principal gerencia a transição entre diferentes "frames" (telas) sem fechar a janela. 

1. Núcleo (App Class) 

Gerenciador de Telas: Controla o ciclo de vida dos componentes (Menu -> Seleção -> Jogo -> Game Over). 

Persistent Data: Gerencia o carregamento e salvamento do arquivo pacman_save.json para manter o progresso do usuário. 

Full-Screen Engine: Implementa suporte nativo para tela cheia com redimensionamento lógico centralizado. 

2. Motor de Jogo (JogoFrame) 

Grid System: O mapa é gerado a partir de uma matriz numérica onde: 

1: Parede | 0: Pastilha | 3: Super Pastilha | 2: Vazio. 

Game Loop: Um loop recursivo baseado no método .after() do tkinter, onde o tempo de atualização ($dt$) diminui conforme o nível aumenta, elevando a dificuldade. 

Renderização Otimizada: Em vez de redesenhar o Canvas inteiro, o código manipula os IDs dos objetos existentes (coords e itemconfig), garantindo performance mesmo em hardware modesto. 

3. Inteligência Artificial (Ghost Class) 

Cada fantasma possui uma personalidade de movimento simulada: 

Blinky (Vermelho): Perseguição direta (alvo é a posição exata do jogador). 

Pinky (Rosa): Emboscada (tenta prever onde o jogador estará). 

Inky (Ciano): Comportamento errático (misto de perseguição e retorno à base). 

Clyde (Laranja): Covardia (persegue se longe, foge se estiver muito perto). 

 

📋 Especificações Técnicas 

Algoritmos Principais 

Pathfinding Simplificado: Os fantasmas calculam a distância Euclidiana ou Manhattan para decidir a próxima direção em cada interseção: 

$$d = \sqrt{(x_1 - x_2)^2 + (y_1 - y_2)^2}$$ 

Sistema de Áudio: Utiliza winsound no Windows e threading para evitar o "jitter" (travamentos) durante o gameplay enquanto os sons de 8-bits são reproduzidos. 

Variáveis de Design 

Constante 

Valor / Descrição 

CELL 

26 pixels (tamanho da grade) 

TICK_BASE 

90ms (velocidade inicial) 

MIN_TICK 

38ms (limite de velocidade máxima) 

INTEL 

Aumenta $2\%$ por nível a precisão dos fantasmas 

 

🎮 Como Jogar 

Instalação 

Não são necessárias bibliotecas externas. Apenas o Python padrão: 

Bash 

cd pacman-evolution 
python pacman_evolution.py 
 

Mecânicas 

Pastilhas: 10 pontos. 

Super Pastilhas: 50 pontos + Vulnerabilidade dos fantasmas por 7 segundos. 

Combo de Fantasmas: Comer um fantasma vulnerável concede 200 pontos extras. 

Vidas: Você começa com 3 vidas. O jogo termina ao zerar ou ao completar todos os níveis disponíveis. 

 

🛠️ Próximos Passos (Roadmap) 

[ ] Implementar animação de morte do Pac-Man. 

[ ] Adicionar suporte a Joysticks via pygame.joy. 

[ ] Interface Customizada: Migrar os botões e labels para CustomTkinter para um visual Dark Mode moderno. 

[ ] Sistema de partículas ao comer as pastilhas. 
