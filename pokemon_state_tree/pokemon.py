from enum import Enum
from typing import Optional


class MajorStatus(Enum):
    """Representação de status principal de um Pokémon."""
    NONE = "None"
    BURN = "Burn"
    FREEZE = "Freeze"
    PARALYSIS = "Paralysis"
    POISON = "Poison"
    BADLY_POISONED = "Badly poisoned"
    SLEEP = "Sleep"


class MinorStatus(Enum):
    """Representação de status secundário de um Pokémon."""
    NONE = "None"
    CONFUSED = "Confused"
    INFATUATION = "Infatuation"


class Pokemon:
    """Classe que representa um Pokémon com seus atributos e status."""

    STAT_NAMES = ["HP", "ATK", "DEF", "SATK", "SDEF", "SPE", "ACC", "EVA"]
    STAT_MIN = -6
    STAT_MAX = 6

    def __init__(self, name: str, item: Optional[str] = None, is_mega: bool = False):
        """
        Inicializa um Pokémon.
        
        Args:
            name: Nome do Pokémon
            item: Item segurando (ex: "Black Sludge", "Lum Berry")
            is_mega: Se o Pokémon é uma Mega Evolução
        """
        self.name = name
        self.item = item  # Item que o Pokémon segura
        self.is_mega = is_mega  # Status de Mega Evolução
        self.hp_min_percent = 100  # Vida mínima em percentual
        self.hp_max_percent = 100  # Vida máxima em percentual
        self.major_status = MajorStatus.NONE
        self.minor_status = MinorStatus.NONE
        
        # Stats inicializados em 0 (sem modificação)
        self.stats = {
            "HP": 0,
            "ATK": 0,
            "DEF": 0,
            "SATK": 0,
            "SDEF": 0,
            "SPE": 0,
            "ACC": 0,
            "EVA": 0
        }

    def set_hp_range(self, min_percent: int, max_percent: int) -> None:
        """
        Define o intervalo de vida percentual.
        
        Args:
            min_percent: Vida mínima em percentual (0-100)
            max_percent: Vida máxima em percentual (0-100)
        """
        self.hp_min_percent = int(max(0, min(100, min_percent)))
        self.hp_max_percent = int(max(0, min(100, max_percent)))
        
        # Garantir que min <= max
        if self.hp_min_percent > self.hp_max_percent:
            self.hp_min_percent, self.hp_max_percent = self.hp_max_percent, self.hp_min_percent

    def set_major_status(self, status: MajorStatus) -> None:
        """Define o status principal."""
        self.major_status = status

    def set_minor_status(self, status: MinorStatus) -> None:
        """Define o status secundário."""
        self.minor_status = status

    def set_stat(self, stat_name: str, value: int) -> bool:
        """
        Define o valor de um stat.
        
        Args:
            stat_name: Nome do stat (HP, ATK, DEF, SATK, SDEF, SPE, ACC, EVA)
            value: Valor do stat (-6 a 6)
            
        Returns:
            True se o stat foi definido com sucesso, False caso contrário
        """
        if stat_name not in self.stats:
            return False
        
        value = max(self.STAT_MIN, min(self.STAT_MAX, value))
        self.stats[stat_name] = value
        return True

    def get_stat(self, stat_name: str) -> Optional[int]:
        """Obtém o valor de um stat."""
        return self.stats.get(stat_name)

    def reset_stats(self) -> None:
        """Reseta todos os stats para 0."""
        for stat in self.stats:
            self.stats[stat] = 0

    def reset_status(self) -> None:
        """Reseta todos os status."""
        self.major_status = MajorStatus.NONE
        self.minor_status = MinorStatus.NONE

    def reset_hp(self) -> None:
        """Reseta a vida para 100%."""
        self.hp_min_percent = 100
        self.hp_max_percent = 100

    def set_item(self, item: Optional[str]) -> None:
        """Define o item que o Pokémon segura."""
        self.item = item

    def set_mega_evolution(self, is_mega: bool) -> None:
        """Define o status de Mega Evolução."""
        self.is_mega = is_mega

    def __repr__(self) -> str:
        mega_text = " (Mega)" if self.is_mega else ""
        item_text = f" @ {self.item}" if self.item else ""
        return f"Pokemon(name='{self.name}{mega_text}{item_text}', hp={self.hp_min_percent}-{self.hp_max_percent}%, major_status={self.major_status.value}, minor_status={self.minor_status.value})"

    def copy(self) -> "Pokemon":
        """Cria uma cópia do Pokémon."""
        new_pokemon = Pokemon(self.name, item=self.item, is_mega=self.is_mega)
        new_pokemon.hp_min_percent = self.hp_min_percent
        new_pokemon.hp_max_percent = self.hp_max_percent
        new_pokemon.major_status = self.major_status
        new_pokemon.minor_status = self.minor_status
        new_pokemon.stats = self.stats.copy()
        return new_pokemon
