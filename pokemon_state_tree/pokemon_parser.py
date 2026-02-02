"""
Parser para importar Pokémon no formato Showdown/Smogon.

Formato suportado:
    Mareanie @ Black Sludge
    Level: 16
    Calm Nature
    Ability: Merciless
    - Venoshock
    - Toxic
    - Soak
    - Baneful Bunker
"""

from typing import Optional, List, Dict
from dataclasses import dataclass
from pokemon import Pokemon


@dataclass
class PokemonRaw:
    """Classe intermediária para armazenar dados Showdown antes de processar."""
    name: str
    item: Optional[str] = None
    level: Optional[int] = None
    nature: Optional[str] = None
    ability: Optional[str] = None
    moves: List[str] = None
    evs: Optional[Dict[str, int]] = None
    ivs: Optional[Dict[str, int]] = None
    is_mega: bool = False
    
    def __post_init__(self):
        """Inicializa valores padrão."""
        if self.moves is None:
            self.moves = []
        if self.evs is None:
            self.evs = {}
        if self.ivs is None:
            self.ivs = {}


class PokemonParser:
    """Parser para formato Showdown de Pokémon."""

    @staticmethod
    def parse_block(block: str) -> Optional[PokemonRaw]:
        """
        Parse um bloco de texto contendo um Pokémon em formato Showdown.
        
        Args:
            block: String contendo as informações do Pokémon
            
        Returns:
            PokemonRaw com os dados parseados, ou None se inválido
        """
        lines = [line.strip() for line in block.strip().split('\n') if line.strip()]
        
        if not lines:
            return None
        
        # Primeira linha contém o nome e possivelmente o item
        first_line = lines[0]
        name, item = PokemonParser._parse_name_and_item(first_line)
        
        if not name:
            return None
        
        # Verificar se é Mega
        is_mega = " Mega" in name or "-Mega" in name
        
        raw_pokemon = PokemonRaw(
            name=name,
            item=item,
            is_mega=is_mega
        )
        
        # Parse demais informações
        for line in lines[1:]:
            if line.startswith('-'):
                # Move
                move = line.lstrip('- ').strip()
                if move:
                    raw_pokemon.moves.append(move)
            elif ':' in line:
                # Atributo com valor
                key, value = line.split(':', 1)
                key = key.strip().lower()
                value = value.strip()
                
                if key == 'level':
                    try:
                        raw_pokemon.level = int(value)
                    except ValueError:
                        pass
                elif key == 'nature':
                    raw_pokemon.nature = value
                elif key == 'ability':
                    raw_pokemon.ability = value
                elif key == 'evs':
                    raw_pokemon.evs = PokemonParser._parse_stats(value)
                elif key == 'ivs':
                    raw_pokemon.ivs = PokemonParser._parse_stats(value)
        
        return raw_pokemon

    @staticmethod
    def parse_multiple(text: str) -> List[PokemonRaw]:
        """
        Parse múltiplos Pokémon separados por linhas em branco.
        
        Args:
            text: String contendo múltiplos Pokémon
            
        Returns:
            Lista de PokemonRaw parseados
        """
        blocks = text.split('\n\n')
        pokemons = []
        
        for block in blocks:
            pokemon = PokemonParser.parse_block(block)
            if pokemon:
                pokemons.append(pokemon)
        
        return pokemons

    @staticmethod
    def to_pokemon(raw_pokemon: PokemonRaw) -> Pokemon:
        """
        Converte PokemonRaw para Pokemon.
        
        Args:
            raw_pokemon: Dados intermediários
            
        Returns:
            Pokemon configurado
        """
        pokemon = Pokemon(
            name=raw_pokemon.name,
            item=raw_pokemon.item,
            is_mega=raw_pokemon.is_mega
        )
        
        # Adicionar outras informações se necessário no futuro
        # (level, nature, ability, moves, EVs, IVs)
        
        return pokemon

    @staticmethod
    def _parse_name_and_item(line: str) -> tuple:
        """
        Parse a primeira linha para extrair nome e item.
        
        Formatos suportados:
            - Mareanie
            - Mareanie @ Black Sludge
            - Mareanie-Galar @ Black Sludge
        
        Args:
            line: Primeira linha
            
        Returns:
            Tupla (nome, item) onde item pode ser None
        """
        if '@' in line:
            name_part, item_part = line.split('@', 1)
            name = name_part.strip()
            item = item_part.strip() if item_part.strip() else None
            return name, item
        else:
            return line.strip(), None

    @staticmethod
    def _parse_stats(stats_str: str) -> Dict[str, int]:
        """
        Parse a linha de stats (EVs ou IVs).
        
        Formato: "4 HP / 252 SpA / 252 Spe"
        
        Args:
            stats_str: String contendo stats
            
        Returns:
            Dicionário com os valores dos stats
        """
        stats_map = {
            'hp': 'HP', 'atk': 'ATK', 'def': 'DEF',
            'spa': 'SATK', 'spd': 'SDEF', 'spe': 'SPE'
        }
        
        stats = {}
        parts = stats_str.split('/')
        
        for part in parts:
            part = part.strip()
            if not part:
                continue
            
            tokens = part.split()
            if len(tokens) >= 2:
                try:
                    value = int(tokens[0])
                    stat_name = tokens[1].lower()
                    
                    if stat_name in stats_map:
                        stats[stats_map[stat_name]] = value
                except ValueError:
                    pass
        
        return stats
