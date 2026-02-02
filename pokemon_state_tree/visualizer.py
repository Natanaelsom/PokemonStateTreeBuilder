"""
Módulo de visualização gráfica da árvore de estados com Canvas.
Mostra estados como caixas e transições como setas.
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Tuple, Optional
from state import State
from state_tree import StateTree
from transition import Transition
import math


class StateBoxVisualizer:
    """Visualiza a árvore de estados em um Canvas com caixas e setas."""
    
    # Dimensões das caixas (em pixels) - AUMENTADAS para acomodar Pokémon
    BOX_WIDTH_SINGLE = 180  # Aumentado de 140
    BOX_HEIGHT_SINGLE = 120  # Aumentado de 70
    BOX_WIDTH_DOUBLE = 180
    BOX_HEIGHT_DOUBLE = 200  # Aumentado de 140
    
    # Tamanho do botão +
    BUTTON_SIZE = 80
    
    # Espaçamento
    HORIZONTAL_SPACING = 250  # Aumentado de 200
    VERTICAL_SPACING = 280  # Aumentado de 220
    MARGIN = 50
    
    def __init__(self, canvas: tk.Canvas, state_tree: StateTree):
        """
        Inicializa o visualizador.
        
        Args:
            canvas: Canvas do Tkinter para desenhar
            state_tree: Árvore de estados a visualizar
        """
        self.canvas = canvas
        self.state_tree = state_tree
        self.state_positions: Dict[int, Tuple[float, float]] = {}
        self.state_boxes: Dict[int, int] = {}  # state_id -> canvas rectangle id
        self.state_texts: Dict[int, int] = {}  # state_id -> canvas text id
        self.pokemon_texts: Dict[int, list] = {}  # state_id -> list of text ids
        self.add_state_buttons: Dict[Tuple[int, str], 'AddStateButton'] = {}  # (state_id, type) -> button
        self.arrow_lines: Dict[int, int] = {}  # transition index -> canvas line id
        self.on_add_state_click = None  # Callback para adicionar estado
        self.on_pokemon_edit = None  # Callback para editar pokémon
        
        # Cores
        self.color_single = "#E3F2FD"  # Azul claro
        self.color_double = "#F3E5F5"  # Roxo claro
        self.color_highlight = "#FFD54F"  # Amarelo
        self.color_border = "#1976D2"  # Azul escuro
        self.color_border_double = "#7B1FA2"  # Roxo escuro
        
    def draw(self) -> None:
        """Desenha a árvore completa."""
        self.canvas.delete("all")
        self.state_positions.clear()
        self.state_boxes.clear()
        self.state_texts.clear()
        self.pokemon_texts.clear()
        self.add_state_buttons.clear()
        
        # Organizar estados por turno
        states_by_turn = self._organize_states_by_turn()
        
        # Calcular posições
        self._calculate_positions(states_by_turn)
        
        # Desenhar setas (transições) - primeiro para ficarem atrás
        self._draw_transitions()
        
        # Desenhar boxes de estados
        self._draw_state_boxes()
        
        # Desenhar botões de adicionar estado/turno
        self._draw_add_state_buttons(states_by_turn)
        
        # Atualizar scroll region
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def _organize_states_by_turn(self) -> Dict[int, list]:
        """Organiza os estados por turno."""
        states_by_turn = {}
        
        for state in self.state_tree.get_all_states():
            turn = state.turn
            if turn not in states_by_turn:
                states_by_turn[turn] = []
            states_by_turn[turn].append(state)
        
        # Ordenar estados em cada turno por ID para consistência
        for turn in states_by_turn:
            states_by_turn[turn].sort(key=lambda s: s.id)
        
        return states_by_turn
    
    def _calculate_positions(self, states_by_turn: Dict[int, list]) -> None:
        """Calcula a posição de cada estado no Canvas (layout vertical por turno)."""
        if not states_by_turn:
            return
        
        max_turn = max(states_by_turn.keys())
        
        for turn in sorted(states_by_turn.keys()):
            states = states_by_turn[turn]
            
            # Coordenada X baseada no turno (colunas de esquerda para direita)
            x = self.MARGIN + turn * self.HORIZONTAL_SPACING
            
            # Distribuir estados verticalmente no mesmo turno
            total_height = len(states) * self.BOX_HEIGHT_SINGLE + (len(states) - 1) * self.VERTICAL_SPACING
            start_y = self.MARGIN + (300 - total_height / 2)  # Centrar verticalmente
            
            for i, state in enumerate(states):
                y = start_y + i * (self.BOX_HEIGHT_SINGLE + self.VERTICAL_SPACING)
                self.state_positions[state.id] = (x, y)
    
    def _draw_state_boxes(self) -> None:
        """Desenha os boxes dos estados com informações de Pokémon inline."""
        for state in self.state_tree.get_all_states():
            if state.id not in self.state_positions:
                continue
            
            x, y = self.state_positions[state.id]
            
            # Determinar dimensões baseado no tipo de batalha
            if state.battle_type == "double":
                width = self.BOX_WIDTH_DOUBLE
                height = self.BOX_HEIGHT_DOUBLE
                color = self.color_double
                border_color = self.color_border_double
            else:
                width = self.BOX_WIDTH_SINGLE
                height = self.BOX_HEIGHT_SINGLE
                color = self.color_single
                border_color = self.color_border
            
            # Desenhar retângulo
            x1, y1 = x - width / 2, y - height / 2
            x2, y2 = x + width / 2, y + height / 2
            
            rect_id = self.canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=color,
                outline=border_color,
                width=2
            )
            self.state_boxes[state.id] = rect_id
            
            # Desenhar nome do estado (no topo)
            self.canvas.create_text(
                x, y - height / 2.5,
                text=f"{state.name} (Turn {state.turn})",
                font=("Arial", 8, "bold"),
                width=int(width * 0.9),
                fill="#1976D2"
            )
            
            # Desenhar Pokémon Self (acima do centro)
            self_pokemon = state.get_pokemon("Self")
            if self_pokemon:
                self_text = f"✓ {self_pokemon.name} ({self_pokemon.hp_min_percent}-{self_pokemon.hp_max_percent}%)"
                if self_pokemon.major_status.value != "NONE":
                    self_text += f" [{self_pokemon.major_status.value}]"
                
                text_id = self.canvas.create_text(
                    x, y - height / 6,
                    text=self_text,
                    font=("Arial", 7),
                    width=int(width * 0.85),
                    fill="#1976D2",
                    tags=f"pokemon_self_{state.id}"
                )
                if state.id not in self.pokemon_texts:
                    self.pokemon_texts[state.id] = []
                self.pokemon_texts[state.id].append(text_id)
                
                # Bind para editar ao clicar
                self.canvas.tag_bind(text_id, "<Button-1>",
                    lambda e, sid=state.id, slot="Self": self._on_pokemon_click(sid, slot))
            
            # Desenhar Pokémon Enemy (abaixo do centro)
            enemy_pokemon = state.get_pokemon("Enemy")
            if enemy_pokemon:
                enemy_text = f"✗ {enemy_pokemon.name} ({enemy_pokemon.hp_min_percent}-{enemy_pokemon.hp_max_percent}%)"
                if enemy_pokemon.major_status.value != "NONE":
                    enemy_text += f" [{enemy_pokemon.major_status.value}]"
                
                text_id = self.canvas.create_text(
                    x, y + height / 6,
                    text=enemy_text,
                    font=("Arial", 7),
                    width=int(width * 0.85),
                    fill="#C62828",
                    tags=f"pokemon_enemy_{state.id}"
                )
                if state.id not in self.pokemon_texts:
                    self.pokemon_texts[state.id] = []
                self.pokemon_texts[state.id].append(text_id)
                
                # Bind para editar ao clicar
                self.canvas.tag_bind(text_id, "<Button-1>",
                    lambda e, sid=state.id, slot="Enemy": self._on_pokemon_click(sid, slot))
            
            # Bind para clique no box
            self.canvas.tag_bind(rect_id, "<Button-1>", 
                                lambda e, sid=state.id: self._on_state_click(sid))
    
    def _draw_transitions(self) -> None:
        """Desenha as setas de transição."""
        for i, transition in enumerate(self.state_tree.get_all_transitions()):
            from_id = transition.from_state.id
            to_id = transition.to_state.id
            
            if from_id not in self.state_positions or to_id not in self.state_positions:
                continue
            
            from_x, from_y = self.state_positions[from_id]
            to_x, to_y = self.state_positions[to_id]
            
            # Desenhar linha com seta
            self._draw_arrow(from_x, from_y, to_x, to_y, transition.probability)
    
    def _draw_arrow(self, x1: float, y1: float, x2: float, y2: float, probability: float) -> None:
        """Desenha uma seta com rótulo de probabilidade."""
        # Calcular vetor de deslocamento perpendicular
        dx = x2 - x1
        dy = y2 - y1
        dist = math.sqrt(dx*dx + dy*dy)
        
        if dist == 0:
            return
        
        # Vetor perpendicular normalizado (para desviar de múltiplas setas)
        perp_x = -dy / dist
        perp_y = dx / dist
        offset = 8  # Pixels de desvio
        
        # Desenhar linha com seta
        line_id = self.canvas.create_line(
            x1 + perp_x * offset, y1 + perp_y * offset,
            x2 + perp_x * offset, y2 + perp_y * offset,
            fill="#424242",
            width=2,
            arrow=tk.LAST,
            arrowshape=(12, 12, 6)
        )
        
        # Desenhar probabilidade no meio da linha
        mid_x = (x1 + x2) / 2 + perp_x * (offset + 15)
        mid_y = (y1 + y2) / 2 + perp_y * (offset + 15)
        self.canvas.create_text(
            mid_x, mid_y,
            text=f"{probability:.0%}",
            font=("Arial", 8),
            fill="#424242",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="none")
        )
    
    def _draw_add_state_buttons(self, states_by_turn: Dict[int, list]) -> None:
        """Desenha botões para adicionar novos estados/turnos."""
        if not states_by_turn:
            return
        
        max_turn = max(states_by_turn.keys())
        
        for turn in sorted(states_by_turn.keys()):
            states = states_by_turn[turn]
            
            # Posição X do turno
            turn_x = self.MARGIN + turn * self.HORIZONTAL_SPACING
            
            # 1. Botão para adicionar novo estado no MESMO turno (ao lado direito)
            # Exceto para turno 0
            if turn > 0 and len(states) > 0:
                last_state = states[-1]
                _, last_y = self.state_positions[last_state.id]
                
                button_x = turn_x + self.BOX_WIDTH_SINGLE / 2 + 60
                button_y = last_y
                
                button = AddStateButton(
                    self.canvas, button_x, button_y,
                    on_click=lambda btn_type, t=turn, lx=button_x, ly=button_y: 
                        self._on_add_state_button_click(t, lx, ly, "possibility"),
                    button_type="possibility"
                )
                self.add_state_buttons[(turn, "possibility")] = button
            
            # 2. Botão para criar novo turno (abaixo, se não houver turno seguinte)
            if turn == max_turn:  # Último turno
                last_state = states[-1]
                _, last_y = self.state_positions[last_state.id]
                
                button_x = turn_x
                button_y = last_y + self.BOX_HEIGHT_SINGLE / 2 + 100
                
                button = AddStateButton(
                    self.canvas, button_x, button_y,
                    on_click=lambda btn_type, t=turn, bx=button_x, by=button_y: 
                        self._on_add_state_button_click(t, bx, by, "new_turn"),
                    button_type="new_turn"
                )
                self.add_state_buttons[(turn, "new_turn")] = button
    
    def _on_add_state_button_click(self, turn: int, x: float, y: float, button_type: str) -> None:
        """Callback quando um botão de adicionar estado é clicado."""
        if self.on_add_state_click:
            self.on_add_state_click(turn, button_type)
    
    def _on_state_click(self, state_id: int) -> None:
        """Callback quando um estado é clicado."""
        rect_id = self.state_boxes.get(state_id)
        if rect_id:
            self.canvas.itemconfig(rect_id, outline=self.color_highlight, width=3)
    
    def _on_pokemon_click(self, state_id: int, slot: str) -> None:
        """Callback quando um pokémon é clicado para editar."""
        if self.on_pokemon_edit:
            self.on_pokemon_edit(state_id, slot)
    
    def highlight_state(self, state_id: int) -> None:
        """Destaca um estado."""
        if state_id in self.state_boxes:
            rect_id = self.state_boxes[state_id]
            state = self.state_tree.get_state(state_id)
            border_color = self.color_border_double if state.battle_type == "double" else self.color_border
            self.canvas.itemconfig(rect_id, outline=self.color_highlight, width=3)
    
    def unhighlight_state(self, state_id: int) -> None:
        """Remove highlight de um estado."""
        if state_id in self.state_boxes:
            rect_id = self.state_boxes[state_id]
            state = self.state_tree.get_state(state_id)
            border_color = self.color_border_double if state.battle_type == "double" else self.color_border
            self.canvas.itemconfig(rect_id, outline=border_color, width=2)


class AddStateButton:
    """Botão especial para adicionar novo estado (box pontilhada com +)."""
    
    def __init__(self, canvas: tk.Canvas, x: float, y: float, on_click=None, button_type: str = "turn"):
        """
        Inicializa o botão.
        
        Args:
            canvas: Canvas para desenhar
            x, y: Posição central
            on_click: Callback quando clicado
            button_type: "turn" para próximo turno, "possibility" para possibilidade
        """
        self.canvas = canvas
        self.x = x
        self.y = y
        self.on_click = on_click
        self.button_type = button_type
        self.width = 80
        self.height = 80
        
        # Desenhar box pontilhada
        x1 = x - self.width / 2
        y1 = y - self.height / 2
        x2 = x + self.width / 2
        y2 = y + self.height / 2
        
        self.rect_id = canvas.create_rectangle(
            x1, y1, x2, y2,
            fill="#FAFAFA",
            outline="#BDBDBD",
            width=2,
            dash=(5, 5)  # Pontilhada
        )
        
        # Desenhar +
        self.text_id = canvas.create_text(
            x, y,
            text="+",
            font=("Arial", 32, "bold"),
            fill="#757575"
        )
        
        # Bind
        canvas.tag_bind(self.rect_id, "<Button-1>", self._on_click)
        canvas.tag_bind(self.text_id, "<Button-1>", self._on_click)
    
    def _on_click(self, event):
        """Callback de clique."""
        if self.on_click:
            self.on_click(self.button_type)
