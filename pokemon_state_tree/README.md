# Pokémon State Tree Builder v4.0

Um programa Python com interface gráfica para criar e editar árvores de estados com Pokémon, com visualização gráfica de estados como caixas e transições como setas.

## ✨ Características

### Visualização
- **Visualizador Gráfico**: Estados representados como caixas coloridas (azul para simples, roxo para duplas)
- **Transições com Setas**: Setas conectando estados com probabilidades
- **Alinhamento Automático**: Estados no mesmo turno alinhados horizontalmente
- **Canvas Interativo**: Clique em qualquer estado para selecioná-lo e editá-lo

### Gerenciamento de Batalhas
- **Batalhas Simples (1x1)**: Self vs Enemy
- **Batalhas Duplas (2x2)**: Self1 & Self2 vs Enemy1 & Enemy2
- **Próximo Treinador**: Botão para resetar e começar novo treinador

### Pokémon e Estados
- **Classes de Domínio:**
  - `Pokemon`: Nome, item, Mega Evolução, vida (min/max %), status, stats
  - `State`: Até 4 Pokémon, clima, tipo de batalha (simples/dupla)
  - `Transition`: Probabilidade, ações associadas
  - `StateTree`: Gerencia estados e transições

- **Stats de Pokémon:**
  - HP, ATK, DEF, SATK, SDEF, SPE, ACC, EVA

- **Status de Pokémon:**
  - Major: Burn, Freeze, Paralysis, Poison, Badly poisoned, Sleep
  - Minor: Confused, Infatuation

- **Condições de Clima:**
  - Sunny, Rain, Sandstorm

## Requisitos

- Python 3.7+
- tkinter (geralmente incluído com Python)

## Como Executar

```bash
python main.py
```

## Estrutura do Projeto

```
pokemon_state_tree/
├── main.py              # Arquivo principal executável
├── gui.py               # Interface gráfica (abas e editor)
├── visualizer.py        # Visualizador gráfico com Canvas
├── custom_widgets.py    # Widgets personalizados
├── pokemon.py           # Classe Pokemon
├── state.py             # Classe State com battle_type
├── transition.py        # Classes Transition e Action
├── state_tree.py        # Classe StateTree
├── library.py           # Box, Trainer, EnemyLibrary
├── pokemon_parser.py    # Parser de Pokémon
├── pokemon_data.py      # Dados de Pokémon
├── setup_test_data.py   # Gerador de dados de teste
├── test_box.json        # Dados de teste (Box)
├── test_enemy_library.json # Dados de teste (Treinadores)
└── requirements.txt     # Dependências
```

## Como Usar

### 1. Preparar Pokémon (Aba "Box")
- Clique em "Add Pokémon"
- Selecione ou digite o nome do Pokémon
- Defina item, Mega Evolução, vida (%)
- Clique "Add"

### 2. Preparar Treinadores (Aba "Enemy Library")
- Clique em "Add Trainer"
- Defina o nome do treinador
- Selecione o treinador e clique "Add to Team"
- Adicione Pokémon ao time

### 3. Criar Árvore de Estados (Aba "Tree Editor")
- **Visualizar**: Veja a árvore graficamente no Canvas
- **Clique em Estado**: Selecione um estado para editá-lo
- **Next Turn**: Cria novo turno com Pokémon herdados
- **Add Possibility**: Cria alternativa no mesmo turno
- **Next Trainer**: Inicia novo treinador com reset da árvore

### 4. Editar Estado (Painel Direito)
- Altere nome, tipo de batalha (single/double)
- Defina clima
- Configure Pokémon para cada slot
- Edite transições

### 5. Salvar/Carregar
- File > Save: Salva em JSON
- File > Load: Carrega projeto anterior
3. Adicionar Pokémon aos estados
4. Criar transições com probabilidades
5. Salvar o projeto
