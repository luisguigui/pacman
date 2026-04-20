# 🟡 PAC-MAN EVOLUTION

> Uma reimaginação moderna do clássico arcade Pac-Man, desenvolvida em Python com Tkinter. Apresenta sistema de níveis progressivos, inteligência artificial sofisticada para fantasmas, persistência de progresso e uma experiência nostálgica com visual retro-futurista.

[![Python](https://img.shields.io/badge/python-3.6+-3776ab.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Tkinter](https://img.shields.io/badge/Tkinter-Nativo-blue.svg)](https://docs.python.org/3/library/tkinter.html)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-Active-brightgreen.svg)]()

<div align="center">

**[🚀 Instalação](#-instalação-e-execução) • [📖 Documentação](#-arquitetura-e-estrutura) • [🎮 Como Jogar](#-como-jogar) • [🛠️ Tecnologias](#️-tecnologias-utilizadas) • [🧠 IA](#-sistema-de-ia-dos-fantasmas)**

</div>

---

## 🌟 Visão Geral

**PAC-MAN EVOLUTION** é uma reimaginação fidedigna do clássico arcade Pac-Man (1980), desenvolvida em **Python puro** usando apenas a biblioteca **Tkinter** nativa. O projeto demonstra conhecimento profundo sobre:

- 🎮 **Mecânicas de Jogo Clássicas**: Grid-based movement, collision detection, score system
- 🧠 **Inteligência Artificial Emergente**: Cada fantasma tem sua própria personalidade e estratégia
- 📊 **Matemática de Jogos**: Pathfinding, distância Manhattan, comportamentos aleatórios
- 💾 **Persistência de Dados**: High scores e progressão de níveis em JSON
- 🎨 **Rendering 2D Otimizado**: Atualização seletiva de objetos Canvas para melhor performance
- 🔊 **Áudio Nativo**: Efeitos sonoros via winsound (Windows) com threading

### ✨ Destaques Principais

- 🗺️ **Mapas Procedurais**: Cada nível tem um mapa único gerado dinamicamente
- 👻 **4 Fantasmas com IA Distinta**: Blinky (persegue), Pinky (embosca), Inky (errático), Clyde (covarde)
- ⚡ **Dificuldade Escalável**: Velocidade aumenta 2% por nível, IA melhora progressivamente
- 🛡️ **Super Pastilhas**: Tornam fantasmas vulneráveis por 7 segundos
- 💾 **Sistema de Save**: High score e último nível desbloqueado salvos automaticamente
- 🎯 **3 Vidas**: Você recomeça com 3 vidas; perder todas = Game Over
- 🖥️ **Tela Cheia**: Suporte nativo com F11 (multiplataforma)
- 📱 **Interface Responsiva**: Controla com WASD/Setas + Mouse

---

## 🎮 Como Jogar

### 🎯 Objetivo
Comer todas as pastilhas no mapa sem ser pego pelos fantasmas. Cada nível oferece 20 fases (mapas) progressivamente mais desafiadoras.

### 📋 Controles

| Entrada | Ação |
|---------|------|
| ⬆️ **W / UP** | Mover para cima |
| ⬇️ **S / DOWN** | Mover para baixo |
| ⬅️ **A / LEFT** | Mover para esquerda |
| ➡️ **D / RIGHT** | Mover para direita |
| **ESC** | Pausar / Despausar |
| **F11** | Alternar tela cheia |

### 🎮 Menu Principal

```
┌─────────────────────┐
│    PAC-MAN EVOLUTION│
│     ♦ ♦ ♦ ♦         │
│                     │
│  RECORDE: 12,450    │
│  FASE: 5            │
│                     │
│ [▶ JOGAR]           │
│ [☰ FASES]           │
│ [✕ SAIR]            │
└─────────────────────┘
```

**Opções**:
- **▶ JOGAR**: Inicia do último nível desbloqueado
- **☰ FASES**: Seleciona qual nível/fase jogar
- **✕ SAIR**: Fecha o jogo

---

### 📊 Sistema de Pontos

| Item | Pontos | Descrição |
|------|--------|-----------|
| 🟡 Pastilha Normal | 10 pts | Pequeno ponto |
| 🔘 Super Pastilha | 50 pts | Grande ponto (vulnerabilidade) |
| 👻 Fantasma Comido | 200 pts | Bonus ao comer vulnerável |

**Pontuação Total por Nível**: 1540 pontos (248×10 pastilhas normais + 4×50 super pastilhas)

---

### 👻 Os 4 Fantasmas

Cada fantasma tem uma **cor, base e estratégia únicos**:

#### 🔴 **BLINKY** (Vermelho) — O Perseguidor

```
📍 Base: Canto Superior Direito
```

**Estratégia**: Persegue **diretamente você**

```python
alvo = (pacman_x, pacman_y)  # Seu localização exata
```

**Dificuldade**: ⭐⭐⭐⭐  
**Comportamento**: Agressivo, imprevisível  
**Fraqueza**: Sem estratégia especial

---

#### 🩷 **PINKY** (Rosa) — O Emboscador

```
📍 Base: Canto Superior Esquerdo
```

**Estratégia**: Tenta **prever seu movimento** (+3 tiles à frente)

```python
alvo = (pacman_x + 3, pacman_y + 3)  # Onde você SERÁ
```

**Dificuldade**: ⭐⭐⭐⭐⭐  
**Comportamento**: Tenta te cercear pela frente  
**Fraqueza**: Previsível se você mudar direção rapidamente

---

#### 🔷 **INKY** (Ciano) — O Errático

```
📍 Base: Canto Inferior Esquerdo
```

**Estratégia**: **Alternância aleatória** entre perseguição e retorno à base

```python
alvo = (pacman_x, pacman_y)  if random.random() < 0.5 else (base_x, base_y)
```

**Dificuldade**: ⭐⭐⭐  
**Comportamento**: Impredizível, às vezes te persegue, às vezes volta  
**Fraqueza**: Use isso a seu favor!

---

#### 🟠 **CLYDE** (Laranja) — O Covarde

```
📍 Base: Centro do Mapa
```

**Estratégia**: **Covardia tática** - persegue se longe, foge se perto

```python
dist = manhattan_distance(clyde, pacman)
alvo = (pacman_x, pacman_y) if dist > 6 else (base_x, base_y)
```

**Dificuldade**: ⭐⭐  
**Comportamento**: Menos ameaçador que outros, fácil de explorar  
**Fraqueza**: Sempre volta perto da base quando assustado

---

### 🛡️ Super Pastilhas

Quando você come uma super pastilha (4 no mapa):

1. **Todos os fantasmas ficam vulneráveis por 7 segundos**
2. Fantasmas mudam de cor (azul piscante)
3. Você pode comê-los e ganhar **200 pontos**
4. Fantasmas comidos retornam à base como "olhos"

```
Normal:       🟠🔴🩷🔷 (agressivo)
Vulnerável:   🔵🔵🔵🔵 (assustado)
Invulnerável: 🔵🔵🔵🔵 (piscando - quase de volta)
```

**Estratégia**: Use as super pastilhas para ganhar pontos extras!

---

### 📈 Progressão de Dificuldade

| Nível | Velocidade Base | Precisão IA | Fases | Observação |
|-------|-----------------|------------|-------|-----------|
| 1 | 90ms | 15% | 1-20 | Fácil - aprender mecânicas |
| 2 | 88ms | 17% | 21-40 | Médio - fantasmas mais rápidos |
| 3 | 86ms | 19% | 41-60 | Difícil - IA mais inteligente |
| 5+ | 70ms+ | 40%+ | Infinitas | Muito Difícil - Hardcore |

**Fórmula de Dificuldade**:
- **Velocidade**: `TICK_BASE - (nivel × 2)` ms/move (mín 38ms)
- **IA**: `min(0.15 + nivel×0.02, 0.92)` (mín 15%, máx 92%)

---

## 🛠️ Tecnologias Utilizadas

| Componente | Tecnologia | Versão | Propósito |
|-----------|-----------|--------|----------|
| **Linguagem** | Python | 3.6+ | Lógica e estrutura |
| **GUI** | Tkinter | Nativo | Renderização e eventos |
| **Áudio** | winsound | Windows | Efeitos sonoros (8-bit) |
| **Threading** | threading | Nativo | Sons assincronos |
| **Persistência** | JSON | Nativo | Salvar progresso |
| **Matemática** | Pathfinding | Nativo | IA dos fantasmas |

### Por que apenas Tkinter?

- ✅ **Zero dependências externas**: Funciona "out of the box"
- ✅ **Multiplataforma**: Windows, macOS, Linux
- ✅ **Renderização eficiente**: Canvas com ID-based updates
- ✅ **Suporte nativo a eventos**: Teclado, mouse, timer
- ✅ **Leve**: ~15MB vs 500MB+ de alternativas

---

## 🏗️ Arquitetura e Estrutura

### 📊 Fluxo de Dados

```
┌──────────────────────┐
│   App (Main Window)  │
│   - Frame Manager    │
│   - Transition Logic │
└─────────┬────────────┘
          │
    ┌─────┴─────┐
    │           │
┌───▼──┐    ┌──▼────┐
│Menu  │    │Jogo   │
│Frame │    │Frame  │
└──────┘    └───┬───┘
                │
        ┌───────┴────────┐
        │                │
    ┌───▼──┐        ┌───▼──┐
    │Ghost │        │Mapa  │
    │IA    │        │Grid  │
    └──────┘        └──────┘
```

### 🧩 Componentes Principais

```
pacman.py
│
├── 🎵 ÁUDIO
│   ├── som(freq, ms) ........... Toca bip via winsound
│   └── _beep() ............... Helper de som
│
├── 💾 PERSISTÊNCIA
│   ├── salvar(nivel, score) ... Grava JSON
│   ├── load_save() ........... Carrega progress
│   └── pacman_save.json ..... Arquivo de save
│
├── 🗺️ GERAÇÃO DE MAPA
│   ├── gerar_mapa() ......... Cria maze procedural
│   └── Constantes:
│       ├── COLS, ROWS = 23, 23 (grid size)
│       ├── CELL = 26 ........... pixels/célula
│       ├── W, H = 598, 598 .... dimensões
│       ├── TICK_BASE = 90 .... delay base (ms)
│       └── MIN_TICK = 38 ..... limite velocidade
│
├── 🎨 CORES
│   ├── BG ................... Background preto
│   ├── WALL_C/WALL_G ....... Azul (parede)
│   ├── PILL_C .............. Rosa (pastilha)
│   ├── PAC_C ............... Amarelo (você)
│   ├── GHOST_C ............ Cores dos fantasmas
│   └── ... (10+ cores)
│
├── 📐 HELPERS
│   ├── cx(grid_x) .......... Converte grid X → pixel
│   ├── cy(grid_y) .......... Converte grid Y → pixel
│   ├── pode(mapa, x, y) .... Verifica se passável
│   └── dirs_livres(mapa, x, y) Retorna direções válidas
│
├── 👻 CLASSE: Ghost (IA)
│   ├── __init__(tipo) ...... Inicializa fantasma
│   ├── BASES .............. Posições iniciais
│   ├── x, y ............... Posição atual
│   ├── vul ............... Vulnerável? (bool)
│   ├── morto ............ Morto (olhos)? (bool)
│   ├── reset() ........... Reseta ao estado inicial
│   ├── set_vul(ms) ...... Torna vulnerável por X ms
│   ├── tick(dt) ......... Atualiza timer vulnerabilidade
│   ├── piscando ........ Property: pisca quando vul+2s
│   └── mover(mapa, px, py, nivel, tick)
│       └── IA PATH FINDING
│           ├── Calcula direções válidas
│           ├── Se vulnerável: FOGE
│           ├── Se inteligente: PERSEGUE/EMBOSCA
│           └── Senão: ALEATÓRIO
│
├── 🎮 CLASSE: MenuFrame
│   ├── __init__(app) ........... Menu principal
│   ├── Mostra recordes
│   ├── Opções: JOGAR, FASES, SAIR
│   └── _ghost_icon() ......... Desenha icon
│
├── 📋 CLASSE: SelecaoFrame
│   ├── __init__(app) .... Seletor de fases
│   ├── Grid 5×4 com 20 fases
│   ├── Desbloqueadas progressivamente
│   └── _render() ....... Renderiza grid
│
├── 🎮 CLASSE: JogoFrame (Principal)
│   │
│   ├── INICIALIZAÇÃO
│   │   ├── __init__(app, nivel) ... Setup
│   │   ├── Gera mapa
│   │   ├── Cria fantasmas
│   │   └── Desenha HUD
│   │
│   ├── RENDERIZAÇÃO
│   │   ├── _draw_walls() ... Desenha paredes
│   │   ├── _draw_pills() .. Desenha pastilhas
│   │   ├── _make_pac() ... Cria Pac-Man (2 arcos)
│   │   ├── _make_ghosts() . Cria sprites dos fantasmas
│   │   ├── _update_pac() .. Atualiza posição
│   │   ├── _update_ghost(g) Atualiza ghost
│   │   └── _draw_hud() ... Renderiza HUD
│   │
│   ├── LÓGICA (Game Loop)
│   │   ├── _loop() ......... Loop principal (recursivo)
│   │   ├── _tick .......... Contador de frames
│   │   ├── dt ........... Delay (escala com nível)
│   │   └── Fluxo:
│   │       ├── Anima Pac-Man (boca abre/fecha)
│   │       ├── Tenta mover Pac-Man
│   │       ├── Verifica colisão com pastilha
│   │       ├── Atualiza timers dos fantasmas
│   │       ├── Move fantasmas (IA)
│   │       ├── Verifica colisão Pac ↔ fantasma
│   │       └── Se todo comido/morre: fim
│   │
│   ├── IA & COLISÕES
│   │   ├── _fim(venceu) ... Encerra nível
│   │   └── Detecção:
│   │       ├── Grid-based (sem float)
│   │       └── Check: x == x && y == y
│   │
│   └── INPUT
│       └── _key(event) ... Processa teclado
│           ├── WASD / Arrows
│           ├── Muda próximo movimento (_nx, _ny)
│           └── ESC = Pausa
│
└── 🎮 CLASSE: GameOverFrame
    ├── __init__(...) ..... Tela final
    ├── Exibe score
    ├── "VITÓRIA!" ou "GAME OVER"
    └── Botão: MENU PRINCIPAL
```

---

## 📚 Documentação das Classes Principais

### 1️⃣ `Ghost` — Inteligência Artificial

**Responsabilidade**: Implementar 4 personalidades de fantasmas com comportamento único

**Atributos**:

```python
class Ghost:
    tipo: str              # "blinky", "pinky", "inky", "clyde"
    x: int, y: int         # Posição atual (grid)
    bx: int, by: int       # Posição base (saída)
    vul: bool              # Vulnerável aos tiros?
    vt: int                # Timer de vulnerabilidade (ms)
    morto: bool            # É apenas olhos?
    dir: tuple             # Última direção (dx, dy)
```

**Método: `mover(mapa, px, py, nivel, tick)`**

```python
def mover(self, mapa, px, py, nivel, tick):
    # 1. Se morto: retorna à base com Manhattan distance
    if self.morto:
        melhor = min(livres, key=lambda d: 
            abs(self.x+d[0]-self.bx) + abs(self.y+d[1]-self.by)
        )
        self.x += melhor[0]
        self.y += melhor[1]
        if self.x == self.bx and self.y == self.by:
            self.morto = False
        return
    
    # 2. Se vulnerável: FOGE do Pac-Man
    if self.vul:
        melhor = max(candidatos, key=lambda d:
            (self.x+d[0]-px)**2 + (self.y+d[1]-py)**2
        )  # Maximiza distância
    
    # 3. Se inteligente (baseado em nível):
    elif random.random() < intel:
        # Cada fantasma tem estratégia:
        if self.tipo == "blinky":
            alvo = (px, py)  # Persegue direto
        elif self.tipo == "pinky":
            alvo = (min(px+3, COLS-1), min(py+3, ROWS-1))  # Embosca
        elif self.tipo == "inky":
            alvo = (px, py) if random.random() < 0.5 else (self.bx, self.by)  # Aleatório
        elif self.tipo == "clyde":
            dist = abs(self.x-px) + abs(self.y-py)
            alvo = (px, py) if dist > 6 else (self.bx, self.by)  # Covarde
        
        # Usa Manhattan distance para encontrar melhor direção
        melhor = min(candidatos, key=lambda d:
            abs(self.x+d[0]-alvo[0]) + abs(self.y+d[1]-alvo[1])
        )
    
    # 4. Senão: escolhe aleatoriamente
    else:
        melhor = random.choice(candidatos)
    
    self.dir = melhor
    self.x += melhor[0]
    self.y += melhor[1]
```

**Lógica da IA**:

```
┌─────────────────┐
│ Calcular IA %   │
│ intel = 0.15+   │
│ nivel*0.02      │
└────────┬────────┘
         │
    ┌────▼─────┐
    │           │
┌───▼──┐   ┌──▼────┐
│ if   │   │ if    │
│ vul? │   │ intel?│
└──┬───┘   └───┬───┘
   │           │
FOGE       PERSEGUE
(max)      (min)
   │           │
   └───────┬───┘
           │
      MOVE
```

---

### 2️⃣ `JogoFrame` — Loop Principal do Jogo

**Responsabilidade**: Gerenciar lógica de jogo, renderização e interação

**Game Loop**:

```python
def _loop(self):
    if self.pausa:
        self._job = self.after(80, self._loop)
        return
    
    # 1. Delta Time (escala com nível)
    dt = max(TICK_BASE - self.nivel*2, MIN_TICK)
    self._tick += 1
    
    # 2. Animação do Pac-Man (abre/fecha boca)
    self._ang += self._ang_d * 4
    if self._ang <= 2 or self._ang >= 38:
        self._ang_d *= -1
    
    # 3. Entrada do Jogador (next move)
    if pode(self.mapa, self.px+self._nx, self.py+self._ny):
        self.dx, self.dy = self._nx, self._ny
    
    # 4. Movimento do Pac-Man
    if pode(self.mapa, self.px+self.dx, self.py+self.dy):
        self.px += self.dx
        self.py += self.dy
    
    # 5. Colisão com Pastilha?
    v = self.mapa[self.py][self.px]
    if v in (0, 3):
        self.mapa[self.py][self.px] = 2
        self._comidos += 1
        pid = self._pills.pop((self.px, self.py), None)
        if pid:
            self.cv.delete(pid)
        
        if v == 3:  # Super pastilha
            self.score += 50
            som(1100, 80)
            [g.set_vul(7000) for g in self.ghosts]
        else:  # Pastilha normal
            self.score += 10
            som(880, 15)
    
    # 6. Atualizar Fantasmas
    [g.tick(dt) for g in self.ghosts]
    [g.mover(self.mapa, self.px, self.py, self.nivel, self._tick) for g in self.ghosts]
    
    # 7. Colisão Pac-Man ↔ Fantasma?
    for g in self.ghosts:
        if g.x == self.px and g.y == self.py and not g.morto:
            if g.vul:
                g.morto = True
                self.score += 200
                som(1500, 100)
            else:
                self.vidas -= 1
                som(280, 450)
                self.px, self.py = 1, 1
                if self.vidas <= 0:
                    self._fim(False)
                    return
    
    # 8. Verificar Se Venceu
    if self._comidos >= self._total:
        self._fim(True)
        return
    
    # 9. Renderizar
    self._update_pac()
    [self._update_ghost(g) for g in self.ghosts]
    self._draw_hud()
    
    # 10. Re-schedule loop
    self._job = self.after(dt, self._loop)
```

---

## 🎯 Conceitos-Chave Explicados

### 1️⃣ **Grid-Based Movement** — Maze em Células

O mapa é representado como uma **matriz 23×23** onde cada célula pode ser:

```python
# Tipos de célula:
0 = Pastilha normal
1 = Parede
2 = Vazio
3 = Super Pastilha

# Exemplo:
mapa = [
    [1, 1, 1, 1, 1, ...],
    [1, 0, 0, 0, 1, ...],
    [1, 0, 1, 0, 1, ...],
    [1, 3, 0, 0, 1, ...],
    [1, 1, 1, 1, 1, ...],
    ...
]

# Você está na célula (1, 1)
px, py = 1, 1
```

**Conversão Grid → Pixel**:

```python
pixel_x = px * CELL + CELL//2  # 1 * 26 + 13 = 39 pixels
pixel_y = py * CELL + CELL//2  # Centraliza na célula
```

---

### 2️⃣ **Distância Manhattan** — Pathfinding Simples

Para calcular quão perto um fantasma está de você:

```python
# Distância euclidiana (reta):
dist_euclidiana = sqrt((x1-x2)^2 + (y1-y2)^2)

# Distância Manhattan (grid):
dist_manhattan = abs(x1-x2) + abs(y1-y2)

# Exemplo:
# Você: (5, 5), Blinky: (7, 3)
# Manhattan = |5-7| + |5-3| = 2 + 2 = 4 passos
```

**Por que Manhattan?** Porque Pac-Man se move em **grade**, não na diagonal!

---

### 3️⃣ **Sistema de IA com 4 Personalidades**

```
BLINKY        PINKY         INKY          CLYDE
(Vermelho)    (Rosa)        (Ciano)       (Laranja)

Alvo = Você   Alvo = Você   Alvo = RANDOM ALVO = Você se
              +3            ou Base       distante > 6
                                         Senão = Base

RESULTADO:
Persegue     Embosca      Impredizível   Covarde
direto       pela frente                 tático
```

---

### 4️⃣ **Animação do Pac-Man** — Boca Dinâmica

O Pac-Man é desenhado usando **2 arcos (wedges)** que se sobrepõem:

```
Ângulo = 30°
┌────────────┐
│    Pac     │  Exterior: boca de 0°
│   (😊)     │  Interior: boca de 2°
└────────────┘

Quando _ang = 38°:
┌────────────┐
│    Pac     │  Boca abre
│   (◯)      │
└────────────┘
```

**Animação**:
```python
self._ang += self._ang_d * 4  # Aumenta ângulo
if self._ang <= 2 or self._ang >= 38:  # Inverte direção
    self._ang_d *= -1
```

**Resultado**: Boca abre/fecha suavemente

---

### 5️⃣ **Persistência de Dados em JSON**

Salva seu progresso automaticamente:

```json
{
    "level": 5,
    "highscore": 12450
}
```

**Carregamento**:
```python
def load_save():
    if os.path.exists("pacman_save.json"):
        with open("pacman_save.json") as f:
            return json.load(f)
    return {"level": 1, "highscore": 0}
```

**Salva quando**:
- Completa um nível (nível aumenta)
- Novo high score

---

### 6️⃣ **Vulnerabilidade e Timer** — Duração de Efeitos

Quando come super pastilha:

```python
# Todos os fantasmas ficam vulneráveis por 7 segundos
[g.set_vul(7000) for g in self.ghosts]

# No update, countdown:
def tick(self, dt):
    if self.vul:
        self.vt -= dt  # Reduz timer
        if self.vt <= 0:
            self.vul = False  # Volta ao normal
```

**Piscada**: Quando `vt < 2000` (últimos 2 segundos):
```python
@property
def piscando(self):
    return self.vul and self.vt < 2000

# Na renderização:
if self.piscando and (self._tick//3) % 2 == 0:
    cor = VUL_END  # Azul claro
else:
    cor = VUL_C    # Azul escuro (pisca)
```

---

## 📊 Fluxo Completo de Jogo

```
1. Inicializa aplicação
   App()
   ↓
2. Mostra Menu Principal
   MenuFrame
   ├─ Recordes carregados
   └─ Opções: JOGAR, FASES, SAIR
   ↓
3. Usuário clica JOGAR
   ir_jogo(nivel)
   ↓
4. Gera Mapa Procedural
   gerar_mapa()
   ├─ Cria maze 23×23
   ├─ Coloca 4 super pastilhas
   └─ Retorna 1540 pastilhas
   ↓
5. Inicializa Entidades
   JogoFrame.__init__()
   ├─ Cria 4 fantasmas em bases
   ├─ Pac-Man em (1, 1)
   ├─ Desenha paredes
   └─ Desenha pastilhas
   ↓
6. GAME LOOP (recursivo, ~50 FPS)
   ┌──────────────────────┐
   │ 1. Anima Pac-Man     │
   │ 2. Lê input (WASD)   │
   │ 3. Move Pac-Man      │
   │ 4. Colisão pastilha? │
   │ 5. Move fantasmas    │
   │ 6. Colisão ghost?    │
   │ 7. Renderiza         │
   │ 8. after(dt, _loop)  │
   └──────────────────────┘
          ↓ (Enquanto jogo)
   ↓
7. Condição de Vitória?
   ├─ Todos as pastilhas comidas?
   │  SIM → ir_gameover(venceu=True)
   │        Próximo nível desbloqueado
   │        Score salvo
   └─ Pac-Man atingido por fantasma não-vulnerável?
      SIM → Perde vida
           Se vidas = 0 → ir_gameover(venceu=False)
           Senão → Reseta Pac-Man em (1, 1)
   ↓
8. Tela de GameOver
   GameOverFrame
   ├─ Exibe "VITÓRIA!" ou "GAME OVER"
   ├─ Score final
   └─ Botão: MENU PRINCIPAL
   ↓
9. Volta ao passo 2
```

---

## 🎨 Sistema de Cores e Sprites

### Paleta de Cores

```python
BG = "#000011"                    # Fundo preto/azul escuro
WALL_C = "#0033cc"               # Azul vibrante (parede)
WALL_G = "#002299"               # Azul escuro (sombra)

PILL_C = "#ffaaaa"               # Rosa claro (pastilha)
POWER_C = "#ffffff"              # Branco (super pastilha)

PAC_C = "#ffee00"                # Amarelo brilhante
PAC_EDGE = "#ffaa00"             # Laranja (borda)

GHOST_C = {
    "blinky": "#ff2222",         # Vermelho
    "pinky": "#ff99ff",          # Rosa/Magenta
    "inky": "#22ffff",           # Ciano
    "clyde": "#ffaa22"           # Laranja
}

VUL_C = "#1133ff"                # Azul (vulnerável)
VUL_END = "#aaaaff"              # Azul claro (piscando)
EYE_W = "#ffffff"                # Branco (olho)
EYE_B = "#0000ff"                # Azul (pupila)
```

### Renderização

**Paredes**: Duplo retângulo (sombra + cor)
**Pastilhas**: Óval pequeno (3px)
**Super Pastilhas**: Óval com borda (9px exterior, 6px interior)
**Pac-Man**: 2 arcos sobrepostos (animação)
**Fantasmas**: Corpo + saia + olhos

---

## 🔊 Sistema de Áudio

Sons via **winsound** (Windows) com threading:

```python
def som(freq, ms):
    threading.Thread(
        target=_beep,
        args=(freq, ms),
        daemon=True
    ).start()
```

**Sons do Jogo**:

| Som | Frequência | Duração | Evento |
|-----|-----------|---------|--------|
| 🍴 Pastilha | 880 Hz | 15 ms | Comeu pastilha |
| ⚡ Super | 1100 Hz | 80 ms | Comeu super pastilha |
| 💥 Morte | 280 Hz | 450 ms | Levou tiro |
| 👻 Comeu | 1500 Hz | 100 ms | Comeu fantasma |

---

## 💾 Sistema de Save

Arquivo: `pacman_save.json`

**Quando salva**:
- ✅ Completa um nível (nível += 1)
- ✅ Novo high score

**Estrutura**:
```json
{
    "level": 5,
    "highscore": 12450
}
```

**Carregamento**:
- Menu mostra nível desbloqueado e recorde
- Botão "JOGAR" começa do nível mais alto
- "FASES" mostra apenas fases desbloqueadas

---

## 🚀 Possíveis Melhorias Futuras

- [ ] **Animação de Morte**: Pac-Man desaparecendo
- [ ] **Suporte a Joystick**: Via pygame.joy
- [ ] **Dark Mode**: CustomTkinter para interface
- [ ] **Efeitos de Partículas**: Explosões ao comer fantasma
- [ ] **Sons Melhorados**: Arquivos .wav ao invés de bips
- [ ] **Leaderboard**: Top 10 scores
- [ ] **Skins Customizáveis**: Cores diferentes para Pac-Man
- [ ] **Modos Alternativos**: Survival, Time Attack
- [ ] **Inteligência IA Mais Sofisticada**: A* pathfinding
- [ ] **Multiplayer Local**: Dois Pac-Mans

---

## 📋 Instalação e Execução

### ✅ Pré-requisitos

- Python 3.6+
- Tkinter (geralmente incluído)

### 🔧 Passos

1. **Clone o repositório**:
```bash
git clone https://github.com/luisguigui/pacman.git
cd pacman
```

2. **Execute diretamente** (sem dependências externas!):
```bash
python pacman.py
```

3. **Menu deve aparecer**:
   - Escolha [▶ JOGAR] ou [☰ FASES]
   - Use WASD ou Setas para mover
   - ESC para pausar
   - F11 para tela cheia

---

## 🐛 Troubleshooting

### ❌ Problema: Tkinter não encontrado
**Solução**:
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# macOS (Homebrew)
brew install python-tk
```

### ❌ Problema: Som não funciona
**Causa**: winsound é apenas Windows  
**Solução**: Funciona normalmente em Windows. Em Linux/Mac, sons são ignorados gracefully.

### ❌ Problema: Programa trava
**Causa**: Muitos clientes Canvas  
**Solução**: Verificar que `coords()` é chamado, não `delete()`+`create_*()`.

### ❌ Problema: Fantasmas se comportam estranho
**Causa**: IA depende de nível  
**Verificação**: Em nível 1, IA é menos inteligente (15%). Aumenta com níveis.

---

## ⚙️ Configuração Avançada

**Modificar Dificuldade**:
```python
# Aumentar velocidade dos fantasmas
TICK_BASE = 80  # Era 90 (mais rápido)

# Aumentar inteligência IA
# Na classe Ghost.mover(), linha com:
intel = min(0.25 + nivel*0.03, 0.95)  # Aumentar inicialmente
```

**Modificar Tamanho do Mapa**:
```python
COLS, ROWS = 27, 27  # Era 23, 23
CELL = 26  # Deixar igual para manter proporção
```

**Modificar Cores**:
```python
GHOST_C = {
    "blinky": "#ff0000",   # Vermelho mais brilhante
    "pinky": "#ff00ff",    # Magenta puro
    "inky": "#00ffff",     # Ciano puro
    "clyde": "#ffff00"     # Amarelo
}
```

---

## ✒️ Autor

**Luis Guilherme G.B.**

- 🐙 GitHub: [@luisguigui](https://github.com/luisguigui)
- 💼 Portfólio: Desenvolvedor Python Full-Stack
- 📧 Contato: Abra uma issue no repositório

---

## 🙏 Créditos

- Inspirado no clássico **Pac-Man (1980)** da Namco
- Desenvolvido com ❤️ em Python puro
- Sem dependências externas além de Tkinter nativo

---

## 📄 Licença

Este projeto está sob a licença **MIT**. Use, modifique e distribua livremente!

---

## 🌟 Se gostou, considere dar uma ⭐!

```
   👻👻👻👻
   
   🟡 PAC-MAN
   
   OBRIGADO!
```

---

**Última atualização**: 2026-04-20  
**Versão**: 1.0 — Stable Release  
**Status**: ✅ Totalmente funcional e jogável  
**Dependências**: Apenas Tkinter (incluído no Python!)
```

---
