from enum import Enum
from typing import Optional, Dict
from pokemon import Pokemon


class Weather(Enum):
    """Representação das condições de clima."""
    NONE = "None"
    SUNNY = "Sunny"
    RAIN = "Rain"
    SANDSTORM = "Sandstorm"


class State:
    """Classe que representa um estado na árvore de estados."""

    _id_counter = 0
    _turn_counter = 0  # Contador global de turnos para geração de nomes

    def __init__(self, name: str = None, turn: int = None, battle_type: str = "single"):
        """
        Inicializa um estado.
        
        Args:
            name: Nome/descrição do estado. Se None, será gerado automaticamente baseado no turno.
            turn: Número do turno. Se None, será incrementado automaticamente.
            battle_type: Tipo de batalha - "single" (1x1) ou "double" (2x2)
        """
        self.id = State._id_counter
        State._id_counter += 1
        
        # Se turno não foi especificado, usar contador global
        if turn is None:
            turn = State._turn_counter
        
        self.turn = turn
        
        # Se nome não foi especificado, gerar automaticamente
        if name is None:
            name = f"Turn {turn}"
        
        self.name = name
        self.weather = Weather.NONE
        self.battle_type = battle_type  # "single" ou "double"
        
        # Até 4 Pokémon: Self, Enemy, Self2, Enemy2
        self.pokemons: Dict[str, Optional[Pokemon]] = {
            "Self": None,
            "Enemy": None,
            "Self2": None,
            "Enemy2": None
        }
    
    @staticmethod
    def reset_turn_counter() -> None:
        """Reseta o contador de turnos global."""
        State._turn_counter = 0

    def add_pokemon(self, slot: str, pokemon: Pokemon) -> bool:
        """
        Adiciona um Pokémon a um slot do estado.
        
        Args:
            slot: Slot do Pokémon (Self, Enemy, Self2, Enemy2)
            pokemon: Pokémon a ser adicionado
            
        Returns:
            True se adicionado com sucesso, False caso contrário
        """
        if slot not in self.pokemons:
            return False
        
        self.pokemons[slot] = pokemon.copy() if pokemon else None
        return True

    def get_pokemon(self, slot: str) -> Optional[Pokemon]:
        """Obtém um Pokémon de um slot específico."""
        return self.pokemons.get(slot)

    def remove_pokemon(self, slot: str) -> bool:
        """Remove um Pokémon de um slot."""
        if slot not in self.pokemons:
            return False
        self.pokemons[slot] = None
        return True

    def set_weather(self, weather: Weather) -> None:
        """Define a condição de clima."""
        self.weather = weather

    def get_active_pokemons(self) -> Dict[str, Pokemon]:
        """Retorna um dicionário dos Pokémon ativos (não None)."""
        return {slot: pokemon for slot, pokemon in self.pokemons.items() if pokemon is not None}

    def __repr__(self) -> str:
        active_pokes = len(self.get_active_pokemons())
        return f"State(id={self.id}, name='{self.name}', weather={self.weather.value}, pokemons={active_pokes})"

    def reset_id_counter() -> None:
        """Reseta o contador de IDs (usado para testes)."""
        State._id_counter = 0
