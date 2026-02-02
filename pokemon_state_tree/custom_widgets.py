"""
Widgets customizados para a GUI do Pokémon State Tree Builder.
"""

import tkinter as tk
from tkinter import ttk
from typing import List, Callable, Optional
from pokemon_data import get_pokemon_list, search_pokemon


class SearchableCombobox(ttk.Frame):
    """Combobox com busca em tempo real para selecionar Pokémon."""
    
    def __init__(self, parent, on_select: Callable = None, pokemon_list: List[str] = None, **kwargs):
        """
        Inicializa o widget.
        
        Args:
            parent: Widget pai
            on_select: Callback chamado quando um Pokémon é selecionado
            pokemon_list: Lista customizada de Pokémon (se None, usa lista completa)
        """
        super().__init__(parent, **kwargs)
        
        self.on_select = on_select
        # Se pokemon_list estiver vazio, usar lista completa
        if pokemon_list is None or len(pokemon_list) == 0:
            self.pokemon_list = get_pokemon_list()
        else:
            self.pokemon_list = pokemon_list
        
        # Frame para entrada
        entry_frame = ttk.Frame(self)
        entry_frame.pack(fill=tk.X, pady=5)
        
        # Entrada de busca
        ttk.Label(entry_frame, text="Pokémon:").pack(side=tk.LEFT, padx=5)
        
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self._on_search_change)
        
        self.entry = ttk.Entry(entry_frame, textvariable=self.search_var, width=25)
        self.entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Listbox com resultados
        listbox_frame = ttk.Frame(self)
        listbox_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        scrollbar = ttk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set, height=8)
        scrollbar.config(command=self.listbox.yview)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.listbox.bind('<<ListboxSelect>>', self._on_listbox_select)
        self.listbox.bind('<Double-Button-1>', self._on_listbox_double_click)
        
        # Preencher lista inicial com todos os Pokémon
        self._update_list(self.pokemon_list)
    
    def _on_search_change(self, *args):
        """Callback quando o texto de busca muda."""
        query = self.search_var.get()
        if query:
            # Buscar na lista filtrada
            results = [p for p in self.pokemon_list if query.lower() in p.lower()]
        else:
            results = self.pokemon_list
        self._update_list(results)
    
    def _update_list(self, pokemon_names: List[str]):
        """Atualiza a listbox com os nomes."""
        self.listbox.delete(0, tk.END)
        for name in pokemon_names[:100]:  # Limitar a 100 resultados
            self.listbox.insert(tk.END, name)
    
    def _on_listbox_select(self, event):
        """Callback quando um item é selecionado na listbox."""
        selection = self.listbox.curselection()
        if selection:
            pokemon_name = self.listbox.get(selection[0])
            self.search_var.set(pokemon_name)
            if self.on_select:
                self.on_select(pokemon_name)
    
    def _on_listbox_double_click(self, event):
        """Callback quando um item é clicado duas vezes na listbox."""
        selection = self.listbox.curselection()
        if selection:
            pokemon_name = self.listbox.get(selection[0])
            self.search_var.set(pokemon_name)
            if self.on_select:
                self.on_select(pokemon_name)
    
    def _show_full_list(self):
        """Mostra uma janela com a lista completa."""
        dialog = tk.Toplevel(self)
        dialog.title("Select Pokémon")
        dialog.geometry("300x400")
        
        # Entrada de busca no diálogo
        ttk.Label(dialog, text="Search:").pack(padx=5, pady=5)
        search_var = tk.StringVar()
        search_entry = ttk.Entry(dialog, textvariable=search_var, width=30)
        search_entry.pack(padx=5, pady=5, fill=tk.X)
        
        # Listbox
        listbox_frame = ttk.Frame(dialog)
        listbox_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        def on_search(*args):
            query = search_var.get()
            if query:
                results = search_pokemon(query)
            else:
                results = self.pokemon_list
            listbox.delete(0, tk.END)
            for name in results:
                listbox.insert(tk.END, name)
        
        search_var.trace("w", on_search)
        
        def select_pokemon():
            selection = listbox.curselection()
            if selection:
                pokemon_name = listbox.get(selection[0])
                self.search_var.set(pokemon_name)
                if self.on_select:
                    self.on_select(pokemon_name)
                dialog.destroy()
        
        ttk.Button(dialog, text="Select", command=select_pokemon).pack(pady=5)
        
        # Populate with all pokemon initially
        for name in self.pokemon_list:
            listbox.insert(tk.END, name)
    
    def get(self) -> str:
        """Retorna o Pokémon selecionado."""
        return self.search_var.get()
    
    def set(self, value: str):
        """Define o Pokémon selecionado."""
        self.search_var.set(value)
    
    def update_pokemon_list(self, pokemon_list: List[str]):
        """Atualiza a lista de Pokémon disponíveis."""
        self.pokemon_list = pokemon_list if pokemon_list else []
        self._update_list(self.pokemon_list)
        self.search_var.set("")


class PokemonStatusFrame(ttk.Frame):
    """Frame para exibir e editar informações de status de um Pokémon."""
    
    def __init__(self, parent, pokemon=None, **kwargs):
        """
        Inicializa o frame.
        
        Args:
            parent: Widget pai
            pokemon: Pokémon a exibir (opcional)
        """
        super().__init__(parent, **kwargs)
        
        self.pokemon = pokemon
        self.on_change = None  # Callback para mudanças
        self._create_widgets()
    
    def _create_widgets(self):
        """Cria os widgets para exibir e editar status."""
        # Frame para status principal (editável)
        major_frame = ttk.LabelFrame(self, text="Major Status", padding=5)
        major_frame.pack(fill=tk.X, padx=5, pady=2)
        
        self.major_var = tk.StringVar()
        major_combo = ttk.Combobox(major_frame, textvariable=self.major_var,
                                  values=["NONE", "BURN", "FREEZE", "PARALYSIS", "POISON", "BADLY_POISONED", "SLEEP"],
                                  state="readonly", width=15)
        major_combo.pack(side=tk.LEFT, padx=5)
        major_combo.bind("<<ComboboxSelected>>", lambda e: self._on_status_changed())
        
        # Frame para status secundário (editável)
        minor_frame = ttk.LabelFrame(self, text="Minor Status", padding=5)
        minor_frame.pack(fill=tk.X, padx=5, pady=2)
        
        self.minor_var = tk.StringVar()
        minor_combo = ttk.Combobox(minor_frame, textvariable=self.minor_var,
                                  values=["NONE", "CURSE", "LEECH_SEED", "SUBSTITUTE", "ENTRY_HAZARD"],
                                  state="readonly", width=15)
        minor_combo.pack(side=tk.LEFT, padx=5)
        minor_combo.bind("<<ComboboxSelected>>", lambda e: self._on_status_changed())
        
        # Frame para HP (editável)
        hp_frame = ttk.LabelFrame(self, text="HP %", padding=5)
        hp_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(hp_frame, text="Min:").pack(side=tk.LEFT, padx=2)
        self.hp_min_var = tk.IntVar(value=100)
        ttk.Spinbox(hp_frame, from_=0, to=100, textvariable=self.hp_min_var, width=5).pack(side=tk.LEFT, padx=2)
        
        ttk.Label(hp_frame, text="Max:").pack(side=tk.LEFT, padx=2)
        self.hp_max_var = tk.IntVar(value=100)
        ttk.Spinbox(hp_frame, from_=0, to=100, textvariable=self.hp_max_var, width=5).pack(side=tk.LEFT, padx=2)
        
        # Frame para stats (editável)
        stats_frame = ttk.LabelFrame(self, text="Stats", padding=5)
        stats_frame.pack(fill=tk.X, padx=5, pady=2)
        
        self.stats_vars = {}
        for stat in ["ATK", "DEF", "SATK", "SDEF", "SPE"]:
            ttk.Label(stats_frame, text=f"{stat}:").pack(side=tk.LEFT, padx=2)
            var = tk.IntVar(value=0)
            self.stats_vars[stat] = var
            ttk.Spinbox(stats_frame, from_=-6, to=6, textvariable=var, width=3).pack(side=tk.LEFT, padx=1)
        
        self.update_display()
    
    def update_display(self):
        """Atualiza a exibição com os dados do Pokémon."""
        if not self.pokemon:
            self.major_var.set("NONE")
            self.minor_var.set("NONE")
            self.hp_min_var.set(100.0)
            self.hp_max_var.set(100.0)
            for stat in ["ATK", "DEF", "SATK", "SDEF", "SPE"]:
                self.stats_vars[stat].set(0)
            return
        
        self.major_var.set(self.pokemon.major_status.value)
        self.minor_var.set(self.pokemon.minor_status.value)
        self.hp_min_var.set(self.pokemon.hp_min_percent)
        self.hp_max_var.set(self.pokemon.hp_max_percent)
        
        for stat in ["ATK", "DEF", "SATK", "SDEF", "SPE"]:
            self.stats_vars[stat].set(self.pokemon.get_stat(stat))
    
    def set_pokemon(self, pokemon):
        """Define o Pokémon a exibir."""
        self.pokemon = pokemon
        self.update_display()
    
    def get_pokemon_data(self):
        """Retorna os dados editados do Pokémon."""
        if not self.pokemon:
            return None
        
        # Atualizar dados do pokémon com valores editados
        from pokemon import MajorStatus, MinorStatus
        
        # Atualizar status
        major_str = self.major_var.get()
        minor_str = self.minor_var.get()
        
        if major_str != "NONE":
            self.pokemon.major_status = MajorStatus[major_str]
        else:
            self.pokemon.major_status = MajorStatus.NONE
        
        if minor_str != "NONE":
            self.pokemon.minor_status = MinorStatus[minor_str]
        else:
            self.pokemon.minor_status = MinorStatus.NONE
        
        # Atualizar HP
        self.pokemon.set_hp_range(self.hp_min_var.get(), self.hp_max_var.get())
        
        # Atualizar stats
        for stat in ["ATK", "DEF", "SATK", "SDEF", "SPE"]:
            self.pokemon.set_stat(stat, self.stats_vars[stat].get())
        
        return self.pokemon
    
    def _on_status_changed(self):
        """Callback quando status é alterado."""
        if self.on_change:
            self.on_change()
