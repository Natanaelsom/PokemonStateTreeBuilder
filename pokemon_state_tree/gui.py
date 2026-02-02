"""
Interface gráfica melhorada para o Pokémon State Tree Builder.
Versão 2.0 com suporte a bibliotecas dual, busca de Pokémon e layout moderno.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from typing import Dict, Optional, List
from state import State, Weather
from version import VERSION
from pokemon import Pokemon, MajorStatus, MinorStatus
from transition import Transition, Action
from state_tree import StateTree
from library import Box, Trainer, EnemyLibrary
from pokemon_parser import PokemonParser
from custom_widgets import SearchableCombobox, PokemonStatusFrame
from visualizer import StateBoxVisualizer, AddStateButton


class PokemonStateTreeGUI:
    """Interface gráfica para criar e editar uma árvore de estados com Pokémon - v2.0."""

    def __init__(self, root: tk.Tk):
        """
        Inicializa a interface gráfica.
        
        Args:
            root: Janela raiz do Tkinter
        """
        self.root = root
        self.root.title(f"Pokémon State Tree Builder v{VERSION}")
        self.root.geometry("1400x900")
        
        # Configurar estilo moderno
        self._setup_theme()
        
        # Estrutura de dados
        initial_state = State()  # Turn 0 por padrão
        self.tree = StateTree(initial_state)
        self.selected_state: Optional[State] = initial_state
        
        # Bibliotecas
        self.box = Box("Main Box")  # Aliados
        self.enemy_library = EnemyLibrary()  # Inimigos
        self.selected_library = "box"  # Qual biblioteca está aberta
        self.selected_trainer: Optional[Trainer] = None  # Treinador atual
        
        self.setup_ui()
        
        # Carregar dados de teste se existirem
        self._load_test_data_if_available()
    
    def _setup_theme(self) -> None:
        """Configura um tema moderno."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Cores personalizadas
        style.configure('Treeview', font=('Arial', 10))
        style.configure('TLabel', font=('Arial', 9))
        style.configure('TButton', font=('Arial', 9))
        style.configure('Header.TLabel', font=('Arial', 11, 'bold'))
    
    def setup_ui(self) -> None:
        """Configura a interface do usuário."""
        # Menu bar
        self._setup_menubar()
        
        # Main layout com Notebook (abas)
        main_notebook = ttk.Notebook(self.root)
        main_notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Aba 1: Editor de Árvore
        tree_tab = ttk.Frame(main_notebook)
        main_notebook.add(tree_tab, text="Tree Editor")
        self._setup_tree_editor_tab(tree_tab)
        
        # Aba 2: Biblioteca de Aliados
        box_tab = ttk.Frame(main_notebook)
        main_notebook.add(box_tab, text="Box (Allies)")
        self._setup_box_tab(box_tab)
        
        # Aba 3: Biblioteca de Inimigos
        enemy_tab = ttk.Frame(main_notebook)
        main_notebook.add(enemy_tab, text="Enemy Library")
        self._setup_enemy_library_tab(enemy_tab)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
    
    def _load_test_data_if_available(self) -> None:
        """Carrega dados de teste se os arquivos JSON existirem."""
        import os
        
        test_box_file = "test_box.json"
        test_enemy_file = "test_enemy_library.json"
        
        if not (os.path.exists(test_box_file) and os.path.exists(test_enemy_file)):
            return
        
        try:
            # Carregar Box
            with open(test_box_file, "r", encoding="utf-8") as f:
                box_data = json.load(f)
            
            # Iterar sobre a lista de Pokémon
            for idx, poke_info in enumerate(box_data.get("pokemons", [])):
                pokemon = Pokemon(
                    poke_info["name"],
                    item=poke_info.get("item"),
                    is_mega=poke_info.get("is_mega", False)
                )
                pokemon.set_hp_range(
                    int(poke_info.get("hp_min_percent", 100)),
                    int(poke_info.get("hp_max_percent", 100))
                )
                # Usar um ID único para cada pokémon
                pokemon_id = f"{poke_info['name']}_{idx}"
                self.box.add_pokemon(pokemon_id, pokemon)
            
            # Carregar Enemy Library
            with open(test_enemy_file, "r", encoding="utf-8") as f:
                enemy_data = json.load(f)
            
            # Iterar sobre a lista de treinadores
            for trainer_info in enemy_data.get("trainers", []):
                trainer = Trainer(
                    trainer_info["name"],
                    battle_type=trainer_info.get("battle_type", "single")
                )
                
                for poke_info in trainer_info.get("pokemons", []):
                    pokemon = Pokemon(
                        poke_info["name"],
                        item=poke_info.get("item"),
                        is_mega=poke_info.get("is_mega", False)
                    )
                    pokemon.set_hp_range(
                        int(poke_info.get("hp_min_percent", 100)),
                        int(poke_info.get("hp_max_percent", 100))
                    )
                    trainer.add_pokemon(pokemon)
                
                self.enemy_library.add_trainer(trainer)
            
            # Atualizar UI
            if hasattr(self, 'refresh_box_list'):
                self.refresh_box_list()
            if hasattr(self, 'refresh_trainers_list'):
                self.refresh_trainers_list()
            
            self.status_var.set(f"✓ Dados de teste carregados! ({len(self.box.pokemons)} Pokémon, {len(self.enemy_library.trainers)} Treinadores)")
        except Exception as e:
            # Log do erro para debug
            print(f"Erro ao carregar dados de teste: {e}")
            import traceback
            traceback.print_exc()
    
    def _setup_menubar(self) -> None:
        """Configura o menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save Project", command=self.save_project)
        file_menu.add_command(label="Load Project", command=self.load_project)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        import_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Import", menu=import_menu)
        import_menu.add_command(label="Import Pokémon (Showdown)", command=self.import_showdown_dialog)
    
    def _setup_tree_editor_tab(self, parent: ttk.Frame) -> None:
        """Configura a aba do editor de árvore com visualização gráfica (novo layout com tree flutuante)."""
        # Combobox de seleção de treinador no topo (barra de ferramentas)
        toolbar_frame = ttk.Frame(parent)
        toolbar_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(toolbar_frame, text="Trainer:", style='Header.TLabel').pack(side=tk.LEFT, padx=5)
        self.trainer_var = tk.StringVar()
        self.trainer_combo = ttk.Combobox(toolbar_frame, textvariable=self.trainer_var,
                                         state="readonly", width=40)
        self.trainer_combo.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.trainer_combo.bind("<<ComboboxSelected>>", self._on_trainer_selected)
        
        ttk.Button(toolbar_frame, text="Next Trainer", command=self.go_to_next_trainer).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar_frame, text="Mark Defeated", command=self.mark_trainer_defeated).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar_frame, text="Mark Skipped", command=self.mark_trainer_skipped).pack(side=tk.LEFT, padx=2)
        
        # Inicializar combobox de treinadores
        self._refresh_trainer_combobox()
        
        # Main container - Canvas no centro com botões nos cantos
        main_container = ttk.Frame(parent)
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Top buttons (canto superior)
        top_button_frame = ttk.Frame(main_container)
        top_button_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(top_button_frame, text="Next Turn", command=self.add_next_turn_state).pack(side=tk.LEFT, padx=2)
        ttk.Button(top_button_frame, text="Add Possibility", command=self.add_possibility_dialog).pack(side=tk.LEFT, padx=2)
        ttk.Button(top_button_frame, text="Remove", command=self.remove_state).pack(side=tk.LEFT, padx=2)
        
        # Canvas no centro (flutuante)
        canvas_frame = ttk.Frame(main_container)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scrollbars
        h_scroll = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL)
        v_scroll = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Canvas
        self.canvas = tk.Canvas(canvas_frame, bg="#FAFAFA", 
                               xscrollcommand=h_scroll.set,
                               yscrollcommand=v_scroll.set)
        h_scroll.config(command=self.canvas.xview)
        v_scroll.config(command=self.canvas.yview)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Visualizador
        self.visualizer = StateBoxVisualizer(self.canvas, self.tree)
        
        # Callbacks para o visualizador
        self.visualizer.on_pokemon_edit = self._on_pokemon_inline_edit
        self.visualizer.on_add_state_click = self._on_add_state_from_button
        
        # Bind de clique no canvas
        self.canvas.bind("<Button-1>", self._on_canvas_click)
        
        # Bottom buttons (canto inferior) - Editor rápido
        bottom_frame = ttk.Frame(main_container)
        bottom_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # State name editor
        ttk.Label(bottom_frame, text="Name:", style='Header.TLabel').pack(side=tk.LEFT, padx=5)
        self.state_name_var = tk.StringVar()
        name_entry = ttk.Entry(bottom_frame, textvariable=self.state_name_var, width=20)
        name_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom_frame, text="Update", command=self.update_state_name).pack(side=tk.LEFT, padx=2)
        
        # Battle type
        ttk.Label(bottom_frame, text="Type:").pack(side=tk.LEFT, padx=5)
        self.battle_type_var = tk.StringVar(value="single")
        battle_combo = ttk.Combobox(bottom_frame, textvariable=self.battle_type_var,
                                    values=["single", "double"], state="readonly", width=10)
        battle_combo.pack(side=tk.LEFT, padx=2)
        battle_combo.bind("<<ComboboxSelected>>", lambda e: self.update_battle_type())
        
        # Weather (compacto)
        ttk.Label(bottom_frame, text="Weather:").pack(side=tk.LEFT, padx=5)
        self.weather_var = tk.StringVar(value=Weather.NONE.value)
        weather_combo = ttk.Combobox(bottom_frame, textvariable=self.weather_var,
                                     values=[w.value for w in Weather], state="readonly", width=12)
        weather_combo.pack(side=tk.LEFT, padx=2)
        weather_combo.bind("<<ComboboxSelected>>", lambda e: self.update_weather())
        
        # Pokémon slots with notebook - em um painel separado (lado direito, compacto)
        right_panel_frame = ttk.LabelFrame(main_container, text="Pokémon Editor", width=300)
        right_panel_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        pokemon_notebook = ttk.Notebook(right_panel_frame)
        pokemon_notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.pokemon_notebook = pokemon_notebook
        
        self.pokemon_frames = {}
        self.pokemon_tabs = {}
        for slot in ["Self", "Enemy", "Self2", "Enemy2"]:
            slot_frame = ttk.Frame(pokemon_notebook)
            tab_id = pokemon_notebook.add(slot_frame, text=slot)
            self.pokemon_tabs[slot] = (tab_id, slot_frame)
            
            self.pokemon_frames[slot] = self._create_pokemon_slot_editor(slot_frame, slot)
        
        # Transições
        transition_frame = ttk.LabelFrame(main_container, text="Transitions from this State")
        transition_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self._setup_transitions_panel(transition_frame)
    
    def _create_pokemon_slot_editor(self, parent: ttk.Frame, slot: str) -> Dict:
        """Cria o editor para um slot de Pokémon."""
        info_dict = {
            "var": tk.StringVar(value="None"),
            "item_var": tk.StringVar(value="None"),
            "mega_var": tk.BooleanVar(value=False),
            "hp_min_var": tk.DoubleVar(value=100.0),
            "hp_max_var": tk.DoubleVar(value=100.0),
            "parent": parent
        }
        
        # Nome do Pokémon (buscável)
        ttk.Label(parent, text="Pokémon:", style='Header.TLabel').pack(anchor=tk.W, padx=5, pady=5)
        
        search_frame = ttk.Frame(parent)
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Determinar lista de Pokémon baseado no slot (Self/Self2 = Box, Enemy/Enemy2 = Trainer)
        if slot in ["Self", "Self2"]:
            available_pokemon = self.box.list_pokemons()
        else:  # Enemy, Enemy2
            if self.selected_trainer:
                available_pokemon = self.selected_trainer.list_pokemons()
            else:
                available_pokemon = []
        
        search_combo = SearchableCombobox(search_frame, 
                                         on_select=lambda p: self._on_pokemon_selected(slot, p),
                                         pokemon_list=available_pokemon)
        search_combo.pack(fill=tk.X, expand=True)
        info_dict["search_combo"] = search_combo
        
        # Item
        item_frame = ttk.Frame(parent)
        item_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(item_frame, text="Item:").pack(side=tk.LEFT, padx=5)
        item_entry = ttk.Entry(item_frame, textvariable=info_dict["item_var"], width=20)
        item_entry.pack(side=tk.LEFT, padx=5)
        
        # Mega Evolution
        mega_check = ttk.Checkbutton(item_frame, text="Mega Evolution", variable=info_dict["mega_var"])
        mega_check.pack(side=tk.LEFT, padx=5)
        
        # HP Range
        hp_frame = ttk.Frame(parent)
        hp_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(hp_frame, text="HP Min %:").pack(side=tk.LEFT, padx=5)
        ttk.Spinbox(hp_frame, from_=0, to=100, textvariable=info_dict["hp_min_var"], width=8).pack(side=tk.LEFT, padx=2)
        ttk.Label(hp_frame, text="HP Max %:").pack(side=tk.LEFT, padx=5)
        ttk.Spinbox(hp_frame, from_=0, to=100, textvariable=info_dict["hp_max_var"], width=8).pack(side=tk.LEFT, padx=2)
        
        # Status display
        status_display = PokemonStatusFrame(parent)
        status_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        info_dict["status_display"] = status_display
        
        # Buttons
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(button_frame, text="Apply", command=lambda: self._apply_pokemon_changes(slot)).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Remove", command=lambda: self.remove_pokemon_from_slot(slot)).pack(side=tk.LEFT, padx=2)
        
        return info_dict
    
    def _setup_transitions_panel(self, parent: ttk.Frame) -> None:
        """Configura o painel de transições."""
        # Listbox para transições
        list_frame = ttk.Frame(parent)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scroll = ttk.Scrollbar(list_frame)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.transitions_listbox = tk.Listbox(list_frame, yscrollcommand=scroll.set)
        scroll.config(command=self.transitions_listbox.yview)
        self.transitions_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Botões
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(button_frame, text="Add Transition", command=self.add_transition_dialog).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Remove", command=self.remove_transition).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Edit", command=self.edit_transition_dialog).pack(side=tk.LEFT, padx=2)
    
    def _setup_box_tab(self, parent: ttk.Frame) -> None:
        """Configura a aba Box (Aliados)."""
        # Botões de gerenciamento
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(button_frame, text="Add Pokémon", command=self.add_pokemon_to_box_dialog).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Remove", command=self.remove_pokemon_from_box).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Clear All", command=self.clear_box).pack(side=tk.LEFT, padx=2)
        
        # Lista de Pokémon
        list_frame = ttk.Frame(parent)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scroll = ttk.Scrollbar(list_frame)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.box_listbox = tk.Listbox(list_frame, yscrollcommand=scroll.set, font=('Arial', 10))
        scroll.config(command=self.box_listbox.yview)
        self.box_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.box_listbox.bind('<<ListboxSelect>>', self.show_pokemon_details)
        
        # Details frame
        details_frame = ttk.LabelFrame(parent, text="Details")
        details_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.box_details_label = ttk.Label(details_frame, text="Select a Pokémon")
        self.box_details_label.pack(fill=tk.BOTH, padx=5, pady=5)
        
        self.refresh_box_list()
    
    def _setup_enemy_library_tab(self, parent: ttk.Frame) -> None:
        """Configura a aba Enemy Library."""
        # Painel de treinadores (esquerda)
        trainer_frame = ttk.LabelFrame(parent, text="Trainers", width=200)
        trainer_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=5, pady=5)
        
        trainer_buttons = ttk.Frame(trainer_frame)
        trainer_buttons.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(trainer_buttons, text="Add Trainer", command=self.add_trainer_dialog).pack(side=tk.LEFT, padx=2)
        ttk.Button(trainer_buttons, text="Remove", command=self.remove_trainer).pack(side=tk.LEFT, padx=2)
        
        trainer_scroll = ttk.Scrollbar(trainer_frame)
        trainer_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.trainers_listbox = tk.Listbox(trainer_frame, yscrollcommand=trainer_scroll.set)
        trainer_scroll.config(command=self.trainers_listbox.yview)
        self.trainers_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.trainers_listbox.bind('<<ListboxSelect>>', self.show_trainer_pokemons)
        
        # Painel de Pokémon do treinador (direita)
        pokemon_frame = ttk.LabelFrame(parent, text="Trainer's Pokémon")
        pokemon_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        pokemon_buttons = ttk.Frame(pokemon_frame)
        pokemon_buttons.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(pokemon_buttons, text="Add to Team", command=self.add_pokemon_to_trainer_dialog).pack(side=tk.LEFT, padx=2)
        ttk.Button(pokemon_buttons, text="Remove", command=self.remove_pokemon_from_trainer).pack(side=tk.LEFT, padx=2)
        
        scroll = ttk.Scrollbar(pokemon_frame)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.trainer_pokemons_listbox = tk.Listbox(pokemon_frame, yscrollcommand=scroll.set)
        scroll.config(command=self.trainer_pokemons_listbox.yview)
        self.trainer_pokemons_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.refresh_trainers_list()
    
    # ==================== TREE EDITOR METHODS ====================
    
    def refresh_tree_view(self) -> None:
        """Atualiza a visualização da árvore."""
        if hasattr(self, 'visualizer'):
            self.visualizer.draw()
            if self.selected_state:
                self.visualizer.highlight_state(self.selected_state.id)
    
    def _on_canvas_click(self, event) -> None:
        """Callback quando clica no canvas."""
        # Encontrar se clicou em algum estado
        item = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
        
        # Procurar pela state box que foi clicada
        for item_id in item:
            for state_id, box_id in self.visualizer.state_boxes.items():
                if box_id == item_id:
                    self.selected_state = self.tree.get_state(state_id)
                    # Unhighlight anterior
                    for sid in self.visualizer.state_boxes.keys():
                        self.visualizer.unhighlight_state(sid)
                    # Highlight novo
                    self.visualizer.highlight_state(state_id)
                    self.refresh_state_editor()
                    return
    
    def _on_pokemon_inline_edit(self, state_id: int, slot: str) -> None:
        """Callback quando um pokémon é clicado para editar inline."""
        # Selecionar o estado
        self.selected_state = self.tree.get_state(state_id)
        self.selected_slot = slot
        
        # Atualizar o editor
        self.refresh_state_editor()
        
        # Focar no campo do pokémon selecionado
        if slot in self.pokemon_frames:
            pokemon_frame = self.pokemon_frames[slot]
            # Focar no campo de pesquisa de pokémon
            if "search" in pokemon_frame:
                pokemon_frame["search"].focus()
    
    def _on_add_state_from_button(self, turn: int, button_type: str) -> None:
        """Callback quando botão de adicionar estado é clicado."""
        if button_type == "possibility":
            # Adicionar novo estado no mesmo turno
            self._add_new_state_in_turn(turn)
        elif button_type == "new_turn":
            # Adicionar novo turno
            self._add_new_state_in_turn(turn + 1)
    
    def _add_new_state_in_turn(self, turn: int) -> None:
        """Adiciona um novo estado em um turno específico."""
        from tkinter import simpledialog
        
        # Perguntar nome do novo estado
        new_name = simpledialog.askstring(
            "Novo Estado",
            f"Nome do novo estado no Turno {turn}:"
        )
        
        if new_name:
            try:
                # Determinar o próximo ID
                all_states = self.tree.get_all_states()
                new_id = max([s.id for s in all_states], default=0) + 1
                
                # Criar novo estado
                new_state = State(
                    id=new_id,
                    name=new_name,
                    turn=turn,
                    battle_type="single"
                )
                
                # Adicionar à árvore
                self.tree.add_state(new_state)
                
                # Atualizar visualização
                self.visualizer.draw()
                
                # Selecionar o novo estado
                self.selected_state = new_state
                self.refresh_state_editor()
                
                # Feedback
                self.status_label.config(text=f"Estado '{new_name}' criado no Turno {turn}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao criar estado: {e}")
    

    def refresh_state_editor(self) -> None:
        """Atualiza o editor de estados."""
        if not self.selected_state:
            return
        
        self.state_name_var.set(self.selected_state.name)
        self.battle_type_var.set(self.selected_state.battle_type)
        self.weather_var.set(self.selected_state.weather.value)
        
        # Mostrar/esconder tabs baseado no battle type
        self._update_pokemon_tabs()
        
        # Atualizar slots
        for slot in ["Self", "Enemy", "Self2", "Enemy2"]:
            pokemon = self.selected_state.get_pokemon(slot)
            if pokemon:
                self.pokemon_frames[slot]["search_combo"].set(pokemon.name)
                self.pokemon_frames[slot]["item_var"].set(pokemon.item or "None")
                self.pokemon_frames[slot]["mega_var"].set(pokemon.is_mega)
                self.pokemon_frames[slot]["hp_min_var"].set(pokemon.hp_min_percent)
                self.pokemon_frames[slot]["hp_max_var"].set(pokemon.hp_max_percent)
                self.pokemon_frames[slot]["status_display"].set_pokemon(pokemon)
            else:
                self.pokemon_frames[slot]["search_combo"].set("")
                self.pokemon_frames[slot]["status_display"].set_pokemon(None)
        
        # Atualizar transições
        self.refresh_transitions_list()
    
    def _update_pokemon_tabs(self) -> None:
        """Mostra/esconde tabs de Pokémon baseado no battle type."""
        battle_type = self.selected_state.battle_type
        
        if battle_type == "single":
            # Mostrar apenas Self e Enemy
            self._show_tab("Self")
            self._show_tab("Enemy")
            self._hide_tab("Self2")
            self._hide_tab("Enemy2")
        elif battle_type == "double":
            # Mostrar todos os 4
            self._show_tab("Self")
            self._show_tab("Enemy")
            self._show_tab("Self2")
            self._show_tab("Enemy2")
    
    def _show_tab(self, slot: str) -> None:
        """Mostra a tab de um slot."""
        if slot in self.pokemon_tabs:
            tab_id, _ = self.pokemon_tabs[slot]
            try:
                self.pokemon_notebook.tab(tab_id, state="normal")
            except:
                pass
    
    def _hide_tab(self, slot: str) -> None:
        """Esconde a tab de um slot."""
        if slot in self.pokemon_tabs:
            tab_id, _ = self.pokemon_tabs[slot]
            try:
                self.pokemon_notebook.tab(tab_id, state="disabled")
            except:
                pass
    
    def update_battle_type(self) -> None:
        """Atualiza o tipo de batalha do estado."""
        if not self.selected_state:
            return
        
        new_battle_type = self.battle_type_var.get()
        self.selected_state.battle_type = new_battle_type
        self._update_pokemon_tabs()
        self.status_var.set(f"Battle type updated to {new_battle_type}")
    
    
    def add_next_turn_state(self) -> None:
        """Adiciona um novo estado para o próximo turno com preenchimento automático."""
        if not self.selected_state:
            messagebox.showwarning("Warning", "No state selected")
            return
        
        next_turn = self.selected_state.turn + 1
        # Herdar battle_type do estado anterior
        new_state = State(turn=next_turn, battle_type=self.selected_state.battle_type)
        
        # Copiar Pokémon do estado anterior como ponto de partida (default)
        for slot in ["Self", "Enemy", "Self2", "Enemy2"]:
            pokemon = self.selected_state.get_pokemon(slot)
            if pokemon:
                new_state.add_pokemon(slot, pokemon)
        
        if self.tree.add_state(new_state):
            # Criar transição automática
            transition = Transition(self.selected_state, new_state, 1.0)
            self.tree.add_transition(transition)
            self.tree.auto_adjust_probabilities(self.selected_state.id)
            
            self.selected_state = new_state
            self.refresh_tree_view()
            self.refresh_state_editor()
            self.status_var.set(f"Created Turn {next_turn}")
        else:
            messagebox.showerror("Error", "Could not add state")
    
    def add_possibility_dialog(self) -> None:
        """Abre diálogo para adicionar uma possibilidade (outro desfecho do mesmo turno)."""
        if not self.selected_state:
            messagebox.showwarning("Warning", "No state selected")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Possibility")
        dialog.geometry("400x300")
        
        ttk.Label(dialog, text="New State Name:").pack(padx=10, pady=5)
        name_entry = ttk.Entry(dialog, width=30)
        name_entry.pack(padx=10, pady=5)
        
        ttk.Label(dialog, text="Battle Type:").pack(padx=10, pady=5)
        battle_type_var = tk.StringVar(value=self.selected_state.battle_type)
        battle_combo = ttk.Combobox(dialog, textvariable=battle_type_var,
                                    values=["single", "double"], state="readonly")
        battle_combo.pack(padx=10, pady=5)
        
        ttk.Label(dialog, text="Probability (leave empty for auto):").pack(padx=10, pady=5)
        prob_entry = ttk.Entry(dialog)
        prob_entry.pack(padx=10, pady=5)
        
        def add_possibility():
            state_name = name_entry.get().strip()
            if not state_name:
                messagebox.showerror("Error", "State name cannot be empty")
                return
            
            # Criar novo estado com o mesmo turno (mesma possibilidade)
            new_state = State(name=state_name, turn=self.selected_state.turn, 
                            battle_type=battle_type_var.get())
            
            # Copiar Pokémon do estado atual como default
            for slot in ["Self", "Enemy", "Self2", "Enemy2"]:
                pokemon = self.selected_state.get_pokemon(slot)
                if pokemon:
                    new_state.add_pokemon(slot, pokemon)
            
            if not self.tree.add_state(new_state):
                messagebox.showerror("Error", "Could not add state")
                return
            
            prob_str = prob_entry.get().strip()
            if prob_str:
                try:
                    prob = float(prob_str)
                except ValueError:
                    messagebox.showerror("Error", "Invalid probability")
                    return
            else:
                prob = 1.0  # Default value
            
            transition = Transition(self.selected_state, new_state, prob)
            self.tree.add_transition(transition)
            self.tree.auto_adjust_probabilities(self.selected_state.id)
            
            self.refresh_tree_view()
            self.selected_state = new_state
            self.refresh_state_editor()
            self.status_var.set(f"Possibility added")
            dialog.destroy()
        
        ttk.Button(dialog, text="Add", command=add_possibility).pack(pady=10)
    
    def remove_state(self) -> None:
        """Remove o estado selecionado."""
        if not self.selected_state:
            messagebox.showwarning("Warning", "No state selected")
            return
        
        if self.selected_state == self.tree.root_state:
            messagebox.showerror("Error", "Cannot remove root state")
            return
        
        if messagebox.askyesno("Confirm", f"Remove '{self.selected_state.name}'?"):
            state_id = self.selected_state.id
            self.tree.remove_state(state_id)
            self.selected_state = self.tree.root_state
            self.refresh_tree_view()
            self.refresh_state_editor()
            self.status_var.set("State removed")
    
    def update_state_name(self) -> None:
        """Atualiza o nome do estado."""
        if not self.selected_state:
            return
        
        new_name = self.state_name_var.get().strip()
        if not new_name:
            messagebox.showerror("Error", "Name cannot be empty")
            return
        
        self.selected_state.name = new_name
        self.refresh_tree_view()
        self.status_var.set("State name updated")
    
    def update_weather(self) -> None:
        """Atualiza o clima do estado."""
        if not self.selected_state:
            return
        
        weather_name = self.weather_var.get()
        weather = Weather[weather_name.upper().replace(" ", "_")]
        self.selected_state.set_weather(weather)
        self.status_var.set(f"Weather updated")
    
    def go_to_next_trainer(self) -> None:
        """Vai para o próximo treinador não derrotado."""
        trainers_list = self.enemy_library.list_trainers()
        if not trainers_list:
            messagebox.showwarning("Warning", "No trainers available")
            return
        
        # Encontrar próximo não derrotado/não pulado
        start_idx = 0
        if self.selected_trainer:
            try:
                start_idx = trainers_list.index(self.selected_trainer.name) + 1
            except ValueError:
                start_idx = 0
        
        next_trainer = None
        for i in range(start_idx, len(trainers_list)):
            trainer = self.enemy_library.get_trainer(trainers_list[i])
            if not trainer.defeated and not trainer.skipped:
                next_trainer = trainer
                break
        
        if not next_trainer:
            messagebox.showinfo("Info", "All trainers defeated or skipped!")
            return
        
        # Definir como treinador atual
        self.selected_trainer = next_trainer
        self._on_trainer_changed()
    
    def _on_trainer_selected(self, event) -> None:
        """Callback quando treinador é selecionado na combobox."""
        trainer_name = self.trainer_var.get()
        if trainer_name:
            # Remover sufixo de status se existir
            if " [" in trainer_name:
                trainer_name = trainer_name.split(" [")[0]
            
            trainer = self.enemy_library.get_trainer(trainer_name)
            if trainer:
                self.selected_trainer = trainer
                self._on_trainer_changed()
    
    def _on_trainer_changed(self) -> None:
        """Chamado quando o treinador selecionado muda."""
        if not self.selected_trainer:
            return
        
        # Reset da árvore
        State.reset_turn_counter()
        State.reset_id_counter()
        
        initial_state = State(battle_type=self.selected_trainer.battle_type)
        self.tree = StateTree(initial_state)
        self.selected_state = initial_state
        
        # Atualizar combobox
        self._refresh_trainer_combobox()
        
        # Atualizar listas de Pokémon dos slots Enemy
        self._refresh_enemy_pokemon_lists()
        
        # Atualizar visualização
        self.refresh_tree_view()
        self.refresh_state_editor()
        self.status_var.set(f"Trainer: {self.selected_trainer.name} ({self.selected_trainer.battle_type})")
    
    def _refresh_enemy_pokemon_lists(self) -> None:
        """Atualiza a lista de Pokémon disponíveis para os slots inimigos."""
        if not self.selected_trainer:
            return
        
        enemy_pokemon = self.selected_trainer.list_pokemons()
        
        # Atualizar combobox dos slots Enemy e Enemy2
        for slot in ["Enemy", "Enemy2"]:
            if slot in self.pokemon_frames:
                search_combo = self.pokemon_frames[slot].get("search_combo")
                if search_combo:
                    search_combo.update_pokemon_list(enemy_pokemon)
    
    def _refresh_trainer_combobox(self) -> None:
        """Atualiza a combobox de treinadores."""
        trainers_list = []
        for name in self.enemy_library.list_trainers():
            trainer = self.enemy_library.get_trainer(name)
            if trainer.defeated:
                status = "[DEFEATED]"
            elif trainer.skipped:
                status = "[SKIPPED]"
            else:
                status = ""
            
            display_name = f"{name} {status}".strip()
            trainers_list.append(display_name)
        
        self.trainer_combo['values'] = trainers_list
        
        if self.selected_trainer:
            display_name = self.selected_trainer.name
            if self.selected_trainer.defeated:
                display_name += " [DEFEATED]"
            elif self.selected_trainer.skipped:
                display_name += " [SKIPPED]"
            self.trainer_var.set(display_name)
    
    def mark_trainer_defeated(self) -> None:
        """Marca o treinador atual como derrotado."""
        if not self.selected_trainer:
            messagebox.showwarning("Warning", "No trainer selected")
            return
        
        self.selected_trainer.defeated = True
        self._refresh_trainer_combobox()
        self.status_var.set(f"{self.selected_trainer.name} marked as DEFEATED")
    
    def mark_trainer_skipped(self) -> None:
        """Marca o treinador atual como pulado."""
        if not self.selected_trainer:
            messagebox.showwarning("Warning", "No trainer selected")
            return
        
        self.selected_trainer.skipped = True
        self._refresh_trainer_combobox()
        self.status_var.set(f"{self.selected_trainer.name} marked as SKIPPED")
    
    def next_trainer(self) -> None:
        """Alias para go_to_next_trainer (para compatibilidade)."""
        self.go_to_next_trainer()
    
    
    def _on_pokemon_selected(self, slot: str, pokemon_name: str) -> None:
        """Callback quando um Pokémon é selecionado na busca."""
        pokemon = None
        
        # Determinar de onde pegar o pokémon baseado no slot
        if slot in ["Self", "Self2"]:
            pokemon = self.box.get_pokemon(pokemon_name)
        else:  # Enemy, Enemy2
            if self.selected_trainer:
                # Buscar na lista do treinador
                for p in self.selected_trainer.pokemons:
                    if p.name == pokemon_name:
                        pokemon = p
                        break
        
        if pokemon:
            # Atualizar o campo de seleção no combobox
            self.pokemon_frames[slot]["search_combo"].set(pokemon_name)
            # Exibir na status display
            self.pokemon_frames[slot]["status_display"].set_pokemon(pokemon)
    
    def _apply_pokemon_changes(self, slot: str) -> None:
        """Aplica as mudanças do Pokémon."""
        if not self.selected_state:
            return
        
        pokemon_name = self.pokemon_frames[slot]["search_combo"].get().strip()
        if not pokemon_name:
            self.selected_state.remove_pokemon(slot)
            self.refresh_state_editor()
            return
        
        # Obter pokémon da fonte correta
        pokemon = None
        if slot in ["Self", "Self2"]:
            pokemon = self.box.get_pokemon(pokemon_name)
        else:  # Enemy, Enemy2
            if self.selected_trainer:
                for p in self.selected_trainer.pokemons:
                    if p.name == pokemon_name:
                        pokemon = p
                        break
        
        if not pokemon:
            messagebox.showerror("Error", f"Pokémon '{pokemon_name}' not found")
            return
        
        # Atualizar informações
        pokemon = pokemon.copy()
        item = self.pokemon_frames[slot]["item_var"].get()
        pokemon.set_item(item if item != "None" else None)
        pokemon.set_mega_evolution(self.pokemon_frames[slot]["mega_var"].get())
        
        hp_min = self.pokemon_frames[slot]["hp_min_var"].get()
        hp_max = self.pokemon_frames[slot]["hp_max_var"].get()
        pokemon.set_hp_range(hp_min, hp_max)
        
        # Aplicar status e stats editados
        status_frame = self.pokemon_frames[slot]["status_display"]
        pokemon = status_frame.get_pokemon_data()
        
        self.selected_state.add_pokemon(slot, pokemon)
        self.status_var.set(f"{pokemon_name} added to {slot}")
    
    def remove_pokemon_from_slot(self, slot: str) -> None:
        """Remove Pokémon do slot."""
        if not self.selected_state:
            return
        
        self.selected_state.remove_pokemon(slot)
        self.refresh_state_editor()
        self.status_var.set(f"Pokémon removed from {slot}")
    
    def refresh_transitions_list(self) -> None:
        """Atualiza a lista de transições."""
        self.transitions_listbox.delete(0, tk.END)
        
        if not self.selected_state:
            return
        
        transitions = self.tree.get_transitions_from(self.selected_state.id)
        for trans in transitions:
            text = f"{trans.to_state.name} (prob: {trans.probability:.1%})"
            self.transitions_listbox.insert(tk.END, text)
    
    def add_transition_dialog(self) -> None:
        """Abre diálogo para adicionar transição."""
        if not self.selected_state:
            messagebox.showwarning("Warning", "No state selected")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Transition")
        dialog.geometry("400x200")
        
        ttk.Label(dialog, text="To State:").pack(padx=10, pady=5)
        to_states = [s.name for s in self.tree.get_all_states() if s.id != self.selected_state.id]
        to_var = tk.StringVar()
        ttk.Combobox(dialog, textvariable=to_var, values=to_states, state="readonly").pack(padx=10, pady=5)
        
        ttk.Label(dialog, text="Probability:").pack(padx=10, pady=5)
        prob_entry = ttk.Entry(dialog)
        prob_entry.insert(0, "1.0")
        prob_entry.pack(padx=10, pady=5)
        
        def add():
            to_state_name = to_var.get()
            to_state = next((s for s in self.tree.get_all_states() if s.name == to_state_name), None)
            
            if not to_state:
                messagebox.showerror("Error", "Select a target state")
                return
            
            try:
                prob = float(prob_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Invalid probability")
                return
            
            transition = Transition(self.selected_state, to_state, prob)
            self.tree.add_transition(transition)
            self.tree.auto_adjust_probabilities(self.selected_state.id)
            
            self.refresh_state_editor()
            self.status_var.set("Transition added")
            dialog.destroy()
        
        ttk.Button(dialog, text="Add", command=add).pack(pady=10)
    
    def remove_transition(self) -> None:
        """Remove a transição selecionada."""
        selection = self.transitions_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Select a transition")
            return
        
        transitions = self.tree.get_transitions_from(self.selected_state.id)
        trans_to_remove = transitions[selection[0]]
        
        self.tree.remove_transition(trans_to_remove)
        self.refresh_state_editor()
        self.status_var.set("Transition removed")
    
    def edit_transition_dialog(self) -> None:
        """Abre diálogo para editar transição."""
        selection = self.transitions_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Select a transition")
            return
        
        transitions = self.tree.get_transitions_from(self.selected_state.id)
        trans = transitions[selection[0]]
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Transition")
        dialog.geometry("300x150")
        
        ttk.Label(dialog, text=f"From: {trans.from_state.name}").pack(padx=10, pady=5)
        ttk.Label(dialog, text=f"To: {trans.to_state.name}").pack(padx=10, pady=5)
        
        ttk.Label(dialog, text="Probability:").pack(padx=10, pady=5)
        prob_entry = ttk.Entry(dialog)
        prob_entry.insert(0, str(trans.probability))
        prob_entry.pack(padx=10, pady=5)
        
        def update():
            try:
                trans.probability = float(prob_entry.get())
                self.tree.auto_adjust_probabilities(self.selected_state.id)
                self.refresh_state_editor()
                self.status_var.set("Transition updated")
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Error", "Invalid probability")
        
        ttk.Button(dialog, text="Update", command=update).pack(pady=10)
    
    # ==================== BOX METHODS ====================
    
    def refresh_box_list(self) -> None:
        """Atualiza a lista de Pokémon no Box."""
        self.box_listbox.delete(0, tk.END)
        for name in self.box.list_pokemons():
            self.box_listbox.insert(tk.END, name)
    
    def add_pokemon_to_box_dialog(self) -> None:
        """Abre diálogo para adicionar Pokémon ao Box."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Pokémon to Box")
        dialog.geometry("500x400")
        
        # Usar SearchableCombobox
        search = SearchableCombobox(dialog, on_select=lambda p: name_entry.delete(0, tk.END) or name_entry.insert(0, p))
        search.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(dialog, text="Name:").pack(padx=10, pady=5)
        name_entry = ttk.Entry(dialog, width=30)
        name_entry.pack(padx=10, pady=5)
        
        ttk.Label(dialog, text="Item:").pack(padx=10, pady=5)
        item_entry = ttk.Entry(dialog, width=30)
        item_entry.pack(padx=10, pady=5)
        
        mega_var = tk.BooleanVar()
        ttk.Checkbutton(dialog, text="Mega Evolution", variable=mega_var).pack(padx=10, pady=5)
        
        ttk.Label(dialog, text="HP Min % (0-100):").pack(padx=10, pady=5)
        hp_min_spin = ttk.Spinbox(dialog, from_=0, to=100, width=10)
        hp_min_spin.set(100)
        hp_min_spin.pack(padx=10, pady=5)
        
        ttk.Label(dialog, text="HP Max % (0-100):").pack(padx=10, pady=5)
        hp_max_spin = ttk.Spinbox(dialog, from_=0, to=100, width=10)
        hp_max_spin.set(100)
        hp_max_spin.pack(padx=10, pady=5)
        
        def add():
            poke_name = name_entry.get().strip()
            if not poke_name:
                messagebox.showerror("Error", "Name cannot be empty")
                return
            
            pokemon = Pokemon(poke_name, item=item_entry.get() or None, is_mega=mega_var.get())
            pokemon.set_hp_range(float(hp_min_spin.get()), float(hp_max_spin.get()))
            
            self.box.add_pokemon(poke_name, pokemon)
            self.refresh_box_list()
            self.status_var.set(f"Added {poke_name} to Box")
            dialog.destroy()
        
        ttk.Button(dialog, text="Add", command=add).pack(pady=10)
    
    def remove_pokemon_from_box(self) -> None:
        """Remove Pokémon do Box."""
        selection = self.box_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Select a Pokémon")
            return
        
        name = self.box_listbox.get(selection[0])
        self.box.remove_pokemon(name)
        self.refresh_box_list()
        self.status_var.set(f"Removed {name} from Box")
    
    def clear_box(self) -> None:
        """Limpa o Box."""
        if messagebox.askyesno("Confirm", "Clear all Pokémon from Box?"):
            self.box.clear()
            self.refresh_box_list()
            self.status_var.set("Box cleared")
    
    def show_pokemon_details(self, event) -> None:
        """Mostra detalhes do Pokémon selecionado."""
        selection = self.box_listbox.curselection()
        if not selection:
            return
        
        name = self.box_listbox.get(selection[0])
        pokemon = self.box.get_pokemon(name)
        
        if pokemon:
            details = f"Name: {pokemon.name}\nItem: {pokemon.item or 'None'}\nMega: {pokemon.is_mega}\nHP: {pokemon.hp_min_percent}-{pokemon.hp_max_percent}%"
            self.box_details_label.config(text=details)
    
    # ==================== ENEMY LIBRARY METHODS ====================
    
    def refresh_trainers_list(self) -> None:
        """Atualiza a lista de treinadores."""
        self.trainers_listbox.delete(0, tk.END)
        for name in self.enemy_library.list_trainers():
            self.trainers_listbox.insert(tk.END, name)
    
    def add_trainer_dialog(self) -> None:
        """Abre diálogo para adicionar treinador."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Trainer")
        dialog.geometry("300x100")
        
        ttk.Label(dialog, text="Trainer Name:").pack(padx=10, pady=5)
        name_entry = ttk.Entry(dialog, width=30)
        name_entry.pack(padx=10, pady=5)
        
        def add():
            name = name_entry.get().strip()
            if not name:
                messagebox.showerror("Error", "Name cannot be empty")
                return
            
            trainer = Trainer(name)
            self.enemy_library.add_trainer(trainer)
            self.refresh_trainers_list()
            self.status_var.set(f"Trainer {name} added")
            dialog.destroy()
        
        ttk.Button(dialog, text="Add", command=add).pack(pady=10)
    
    def remove_trainer(self) -> None:
        """Remove treinador."""
        selection = self.trainers_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Select a trainer")
            return
        
        name = self.trainers_listbox.get(selection[0])
        self.enemy_library.remove_trainer(name)
        self.refresh_trainers_list()
        self.trainer_pokemons_listbox.delete(0, tk.END)
        self.status_var.set(f"Trainer {name} removed")
    
    def show_trainer_pokemons(self, event) -> None:
        """Mostra Pokémon do treinador selecionado."""
        selection = self.trainers_listbox.curselection()
        if not selection:
            return
        
        trainer_name = self.trainers_listbox.get(selection[0])
        trainer = self.enemy_library.get_trainer(trainer_name)
        
        self.trainer_pokemons_listbox.delete(0, tk.END)
        if trainer:
            for pokemon in trainer.pokemons:
                self.trainer_pokemons_listbox.insert(tk.END, pokemon.name)
    
    def add_pokemon_to_trainer_dialog(self) -> None:
        """Abre diálogo para adicionar Pokémon ao treinador."""
        trainer_selection = self.trainers_listbox.curselection()
        if not trainer_selection:
            messagebox.showwarning("Warning", "Select a trainer")
            return
        
        trainer_name = self.trainers_listbox.get(trainer_selection[0])
        
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Add Pokémon to {trainer_name}")
        dialog.geometry("500x400")
        
        search = SearchableCombobox(dialog, on_select=lambda p: name_entry.delete(0, tk.END) or name_entry.insert(0, p))
        search.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(dialog, text="Name:").pack(padx=10, pady=5)
        name_entry = ttk.Entry(dialog, width=30)
        name_entry.pack(padx=10, pady=5)
        
        ttk.Label(dialog, text="Item:").pack(padx=10, pady=5)
        item_entry = ttk.Entry(dialog, width=30)
        item_entry.pack(padx=10, pady=5)
        
        mega_var = tk.BooleanVar()
        ttk.Checkbutton(dialog, text="Mega Evolution", variable=mega_var).pack(padx=10, pady=5)
        
        ttk.Label(dialog, text="HP Range:").pack(padx=10, pady=5)
        hp_frame = ttk.Frame(dialog)
        hp_frame.pack(padx=10, pady=5)
        ttk.Spinbox(hp_frame, from_=0, to=100, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Label(hp_frame, text="-").pack(side=tk.LEFT)
        ttk.Spinbox(hp_frame, from_=0, to=100, width=10).pack(side=tk.LEFT, padx=5)
        
        def add():
            poke_name = name_entry.get().strip()
            if not poke_name:
                messagebox.showerror("Error", "Name cannot be empty")
                return
            
            pokemon = Pokemon(poke_name, item=item_entry.get() or None, is_mega=mega_var.get())
            self.enemy_library.add_pokemon_to_trainer(trainer_name, pokemon)
            self.show_trainer_pokemons(None)
            self.status_var.set(f"Added {poke_name} to {trainer_name}")
            dialog.destroy()
        
        ttk.Button(dialog, text="Add", command=add).pack(pady=10)
    
    def remove_pokemon_from_trainer(self) -> None:
        """Remove Pokémon do treinador."""
        trainer_selection = self.trainers_listbox.curselection()
        pokemon_selection = self.trainer_pokemons_listbox.curselection()
        
        if not trainer_selection or not pokemon_selection:
            messagebox.showwarning("Warning", "Select trainer and Pokémon")
            return
        
        trainer_name = self.trainers_listbox.get(trainer_selection[0])
        trainer = self.enemy_library.get_trainer(trainer_name)
        
        trainer.remove_pokemon(pokemon_selection[0])
        self.show_trainer_pokemons(None)
        self.status_var.set("Pokémon removed from trainer")
    
    # ==================== FILE OPERATIONS ====================
    
    def import_showdown_dialog(self) -> None:
        """Abre diálogo para importar Pokémon em formato Showdown."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Import Pokémon (Showdown Format)")
        dialog.geometry("600x400")
        
        ttk.Label(dialog, text="Paste Showdown format:").pack(padx=10, pady=5)
        
        text_widget = tk.Text(dialog, height=15, width=70)
        text_widget.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        def import_pokemon():
            content = text_widget.get("1.0", tk.END)
            if not content.strip():
                messagebox.showerror("Error", "Paste some Pokémon first")
                return
            
            try:
                pokemons = PokemonParser.parse_multiple(content)
                
                for raw_poke in pokemons:
                    pokemon = PokemonParser.to_pokemon(raw_poke)
                    self.box.add_pokemon(pokemon.name, pokemon)
                
                self.refresh_box_list()
                self.status_var.set(f"Imported {len(pokemons)} Pokémon")
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to parse: {str(e)}")
        
        ttk.Button(dialog, text="Import", command=import_pokemon).pack(pady=10)
    
    def save_project(self) -> None:
        """Salva o projeto."""
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if not filename:
            return
        
        try:
            data = {
                "states": [],
                "transitions": [],
                "box": {},
                "enemy_library": {}
            }
            
            # Salvar estados
            for state in self.tree.get_all_states():
                state_data = {
                    "id": state.id,
                    "name": state.name,
                    "turn": state.turn,
                    "weather": state.weather.value,
                    "pokemons": {}
                }
                for slot, pokemon in state.pokemons.items():
                    if pokemon:
                        state_data["pokemons"][slot] = pokemon.name
                data["states"].append(state_data)
            
            # Salvar transições
            for trans in self.tree.get_all_transitions():
                data["transitions"].append({
                    "from": trans.from_state.id,
                    "to": trans.to_state.id,
                    "probability": trans.probability
                })
            
            # Salvar Box
            for name, pokemon in self.box.pokemons.items():
                data["box"][name] = {
                    "name": pokemon.name,
                    "item": pokemon.item,
                    "is_mega": pokemon.is_mega,
                    "hp_min": pokemon.hp_min_percent,
                    "hp_max": pokemon.hp_max_percent,
                    "major_status": pokemon.major_status.value,
                    "minor_status": pokemon.minor_status.value,
                    "stats": pokemon.stats
                }
            
            # Salvar Enemy Library
            for trainer_name, trainer in self.enemy_library.trainers.items():
                data["enemy_library"][trainer_name] = [
                    {
                        "name": p.name,
                        "item": p.item,
                        "is_mega": p.is_mega
                    } for p in trainer.pokemons
                ]
            
            with open(filename, "w") as f:
                json.dump(data, f, indent=2)
            
            messagebox.showinfo("Success", "Project saved")
            self.status_var.set(f"Saved to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {str(e)}")
    
    def load_project(self) -> None:
        """Carrega um projeto."""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if not filename:
            return
        
        try:
            with open(filename, "r") as f:
                data = json.load(f)
            
            # Limpar estruturas
            State.reset_id_counter()
            State.reset_turn_counter()
            self.tree = StateTree(State())
            self.box = Box("Main Box")
            self.enemy_library = EnemyLibrary()
            
            # Carregar Box
            for name, poke_data in data.get("box", {}).items():
                pokemon = Pokemon(poke_data["name"], item=poke_data.get("item"), is_mega=poke_data.get("is_mega", False))
                pokemon.set_hp_range(poke_data.get("hp_min", 100), poke_data.get("hp_max", 100))
                pokemon.set_major_status(MajorStatus[poke_data.get("major_status", "NONE").upper().replace(" ", "_")])
                pokemon.set_minor_status(MinorStatus[poke_data.get("minor_status", "NONE").upper().replace(" ", "_")])
                for stat, value in poke_data.get("stats", {}).items():
                    pokemon.set_stat(stat, value)
                self.box.add_pokemon(name, pokemon)
            
            # Carregar Estados
            state_map = {}
            for state_data in data.get("states", []):
                if state_data["id"] == 0:
                    state = self.tree.root_state
                else:
                    state = State(name=state_data.get("name"), turn=state_data.get("turn", 0))
                    self.tree.add_state(state)
                
                state.set_weather(Weather[state_data.get("weather", "NONE").upper().replace(" ", "_")])
                state_map[state_data["id"]] = state
            
            # Carregar Transições
            for trans_data in data.get("transitions", []):
                from_state = state_map.get(trans_data["from"])
                to_state = state_map.get(trans_data["to"])
                if from_state and to_state:
                    trans = Transition(from_state, to_state, trans_data.get("probability", 1.0))
                    self.tree.add_transition(trans)
            
            # Carregar Enemy Library
            for trainer_name, pokemons_data in data.get("enemy_library", {}).items():
                trainer = Trainer(trainer_name)
                for poke_data in pokemons_data:
                    pokemon = Pokemon(poke_data["name"], item=poke_data.get("item"), is_mega=poke_data.get("is_mega", False))
                    trainer.add_pokemon(pokemon)
                self.enemy_library.add_trainer(trainer)
            
            self.selected_state = self.tree.root_state
            self.refresh_tree_view()
            self.refresh_state_editor()
            self.refresh_box_list()
            self.refresh_trainers_list()
            
            messagebox.showinfo("Success", "Project loaded")
            self.status_var.set(f"Loaded from {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load: {str(e)}")


def main():
    """Função principal."""
    root = tk.Tk()
    app = PokemonStateTreeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
