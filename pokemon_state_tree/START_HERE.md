╔════════════════════════════════════════════════════════════════════════════╗
║                                                                                ║
║    🎮 POKÉMON STATE TREE BUILDER v4.0 - PRONTO PARA USAR 🎮                  ║
║                                                                                ║
║  Interface gráfica moderna para criar árvores de estados com Pokémon,        ║
║  com visualização gráfica, batalhas simples/duplas e transições.             ║
║                                                                                ║
╚════════════════════════════════════════════════════════════════════════════╝


⚡ INICIAR AGORA
════════════════════════════════════════════════════════════════════════════════

Linha de comando (qualquer sistema):
  python main.py

O programa abrirá com dados de teste já carregados:
  • Box com 10 Pokémon de teste
  • 4 Treinadores (2 simples, 2 duplos)


📚 LEIA PRIMEIRO
════════════════════════════════════════════════════════════════════════════════

👉 README.md          - Informações principais
📖 ARCHITECTURE.md    - Como o programa funciona
🆕 setup_test_data.py - Gerar novos dados de teste


🎯 O QUE MUDOU NA v4.0
════════════════════════════════════════════════════════════════════════════════

✨ VISUALIZAÇÃO GRÁFICA:
   • Canvas interativo com estados como caixas coloridas
   • Azul para batalhas simples (1x1)
   • Roxo para batalhas duplas (2x2)
   • Setas conectando estados com probabilidades
   • Alinhamento automático de turnos

🎮 GERENCIAMENTO DE BATALHAS:
   • Suporte explícito a batalhas simples E duplas
   • Alternar entre tipos na interface
   • Configuração automática de slots

🚀 FUNCIONALIDADES NOVAS:
   • Botão "Next Trainer" para começar novo combate
   • Preenchimento automático ao criar novo turno/possibilidade
   • Seleção de Pokémon restrita ao Box/Biblioteca
   • Dados de teste gerados (JSON)


📋 ARQUIVOS PRINCIPAIS
════════════════════════════════════════════════════════════════════════════════

EXECUTAR:
  main.py                    ← Programa principal
  setup_test_data.py         ← Gerar dados de teste

CÓDIGO CORE:
  gui.py                     - Interface gráfica (abas)
  visualizer.py              - Visualização gráfica (Canvas)
  custom_widgets.py          - Widgets personalizados
  pokemon.py                 - Classe Pokemon
  state.py                   - Classe State
  transition.py              - Classes Transition e Action
  state_tree.py              - Classe StateTree
  library.py                 - Box, Trainer, EnemyLibrary

SUPORTE:
  pokemon_data.py            - Lista de Pokémon
  pokemon_parser.py          - Parser Showdown

DADOS:
  test_box.json              - Pokémon de teste
  test_enemy_library.json    - Treinadores de teste

DOCUMENTAÇÃO:
  README.md                  - Guia de uso
  ARCHITECTURE.md            - Documentação técnica
  PROJECT_SUMMARY.md         - Resumo do projeto


🧪 COMEÇAR AGORA
════════════════════════════════════════════════════════════════════════════════

1. Execute o programa:
   python main.py
   
2. Você verá 3 abas:
   • Tree Editor: Crie e edite a árvore visualmente
   • Box (Allies): Gerencie Pokémon aliados
   • Enemy Library: Gerencie treinadores inimigos

3. Na aba "Tree Editor":
   • Visualize a árvore no Canvas (esquerda)
   • Clique em um estado para selecioná-lo
   • Use botões para: Next Turn, Add Possibility, Remove, Next Trainer
   • Edite no painel direito

4. Dados de teste já estão carregados!
   • 10 Pokémon no Box
   • 4 Treinadores (Brock, Misty, Cynthia, Lance)
   ✓ TODOS OS EXEMPLOS EXECUTADOS COM SUCESSO!

3. Criar arquivo de exemplo:
   python setup_sample.py
   
   Resultado esperado:
   ✓ Projeto de exemplo criado: 'sample_project.json'


💻 REQUISITOS
════════════════════════════════════════════════════════════════════════════════

✓ Python 3.7 ou superior
✓ tkinter (geralmente já vem com Python)

Verificar:
  python --version
  python -m tkinter


🚀 COMEÇAR EM 5 MINUTOS
════════════════════════════════════════════════════════════════════════════════

1. Execute:
   python main.py

2. Clique "New Pokémon" e crie "Pikachu"

3. Clique "Add State" e crie "State 1" e "State 2"

4. Selecione State 1 e clique "Select" no slot "Self"

5. Escolha Pikachu

6. Clique "Add Transition"

7. Escolha State 2 e probabilidade 1.0

8. Salve em File > Save

Pronto! Você criou sua primeira árvore! 🎉


📖 PRÓXIMAS LEITURAS
════════════════════════════════════════════════════════════════════════════════

Iniciante?          → QUICKSTART.md
Usando o programa?  → GUIDE.md
Entender o código?  → ARCHITECTURE.md
Exemplos práticos?  → python examples.py
Validação?          → python test.py


🎓 APRENDER MAIS
════════════════════════════════════════════════════════════════════════════════

Exemplos de uso (sem GUI):
  python examples.py

Testes com resultado esperado:
  python test.py

Criar projeto pré-configurado:
  python setup_sample.py
  (depois abra em File > Load)


⚙️ ESTRUTURA DO CÓDIGO
════════════════════════════════════════════════════════════════════════════════

pokemon.py
  ├─ Pokemon          - Pokémon com atributos
  ├─ MajorStatus      - Enum de status principal
  └─ MinorStatus      - Enum de status secundário

state.py
  ├─ State            - Estado com Pokémon
  └─ Weather          - Enum de clima

transition.py
  ├─ Transition       - Transição entre estados
  └─ Action           - Ações que modificam estados

state_tree.py
  └─ StateTree        - Árvore que gerencia tudo

gui.py
  └─ PokemonStateTreeGUI  - Interface gráfica


🎯 FUNCIONALIDADES PRINCIPAIS
════════════════════════════════════════════════════════════════════════════════

[✓] Criar e editar Pokémon
[✓] Criar e editar Estados
[✓] Adicionar Pokémon a estados
[✓] Criar transições com probabilidades
[✓] Adicionar ações a transições
[✓] Validar integridade da árvore
[✓] Salvar em JSON
[✓] Carregar de JSON
[✓] Interface gráfica completa
[✓] Testes unitários


💾 SALVAMENTO
════════════════════════════════════════════════════════════════════════════════

Seus projetos são salvos em formato JSON puro, compatível com qualquer editor:

  {
    "states": [...],
    "transitions": [...],
    "pokemon_library": {...}
  }

Você pode editar manualmente se quiser!


❓ DÚVIDAS?
════════════════════════════════════════════════════════════════════════════════

Qual é o primeiro passo?
  → Leia QUICKSTART.md (2 minutos)

Como uso a interface?
  → Leia GUIDE.md (10 minutos)

Como funciona o código?
  → Leia ARCHITECTURE.md e execute python examples.py

O programa está funcionando?
  → Execute python test.py


═════════════════════════════════════════════════════════════════════════════════

👉 Seu próximo passo: python main.py

Aproveite! 🎮

═════════════════════════════════════════════════════════════════════════════════
