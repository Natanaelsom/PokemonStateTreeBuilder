from typing import Callable, Optional, List
from state import State, Weather
from pokemon import Pokemon, MajorStatus, MinorStatus


class Action:
    """Classe que representa uma ação que afeta o estado ou Pokémon."""

    def __init__(self):
        """Inicializa uma ação."""
        self.effects: List[Callable[[State], None]] = []

    def add_pokemon_status_change(self, slot: str, major_status: Optional[MajorStatus] = None, minor_status: Optional[MinorStatus] = None) -> None:
        """
        Adiciona um efeito que muda o status de um Pokémon.
        
        Args:
            slot: Slot do Pokémon (Self, Enemy, Self2, Enemy2)
            major_status: Status principal a ser aplicado
            minor_status: Status secundário a ser aplicado
        """
        def effect(state: State):
            pokemon = state.get_pokemon(slot)
            if pokemon:
                if major_status:
                    pokemon.set_major_status(major_status)
                if minor_status:
                    pokemon.set_minor_status(minor_status)
        
        self.effects.append(effect)

    def add_pokemon_hp_change(self, slot: str, hp_min_delta: float = 0, hp_max_delta: float = 0) -> None:
        """
        Adiciona um efeito que modifica a vida de um Pokémon.
        
        Args:
            slot: Slot do Pokémon
            hp_min_delta: Mudança na vida mínima (em percentual)
            hp_max_delta: Mudança na vida máxima (em percentual)
        """
        def effect(state: State):
            pokemon = state.get_pokemon(slot)
            if pokemon:
                new_min = pokemon.hp_min_percent + hp_min_delta
                new_max = pokemon.hp_max_percent + hp_max_delta
                pokemon.set_hp_range(new_min, new_max)
        
        self.effects.append(effect)

    def add_pokemon_stat_change(self, slot: str, stat_name: str, value_delta: int) -> None:
        """
        Adiciona um efeito que modifica um stat de um Pokémon.
        
        Args:
            slot: Slot do Pokémon
            stat_name: Nome do stat (HP, ATK, DEF, SATK, SDEF, SPE, ACC, EVA)
            value_delta: Mudança no valor do stat
        """
        def effect(state: State):
            pokemon = state.get_pokemon(slot)
            if pokemon:
                current_value = pokemon.get_stat(stat_name) or 0
                new_value = current_value + value_delta
                pokemon.set_stat(stat_name, new_value)
        
        self.effects.append(effect)

    def add_weather_change(self, weather: Weather) -> None:
        """
        Adiciona um efeito que muda o clima.
        
        Args:
            weather: Nova condição de clima
        """
        def effect(state: State):
            state.set_weather(weather)
        
        self.effects.append(effect)

    def execute(self, state: State) -> None:
        """
        Executa todos os efeitos da ação.
        
        Args:
            state: Estado a ser modificado
        """
        for effect in self.effects:
            effect(state)

    def __repr__(self) -> str:
        return f"Action(effects={len(self.effects)})"


class Transition:
    """Classe que representa uma transição entre estados."""

    def __init__(self, from_state: State, to_state: State, probability: float):
        """
        Inicializa uma transição.
        
        Args:
            from_state: Estado de origem
            to_state: Estado de destino
            probability: Probabilidade da transição (0.0 a 1.0)
        """
        self.from_state = from_state
        self.to_state = to_state
        self.probability = max(0.0, min(1.0, probability))  # Garantir intervalo 0-1
        self.action = Action()

    def set_probability(self, probability: float) -> None:
        """Define a probabilidade da transição."""
        self.probability = max(0.0, min(1.0, probability))

    def get_action(self) -> Action:
        """Retorna a ação associada a esta transição."""
        return self.action

    def execute_transition(self, state: State) -> State:
        """
        Executa a transição, aplicando a ação e retornando o novo estado.
        
        Args:
            state: Estado atual
            
        Returns:
            O estado de destino com a ação aplicada
        """
        # Aplicar a ação ao estado de destino
        self.action.execute(self.to_state)
        return self.to_state

    def __repr__(self) -> str:
        return f"Transition({self.from_state.name} -> {self.to_state.name}, probability={self.probability:.2f})"
