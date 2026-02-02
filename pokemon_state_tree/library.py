"""
Sistemas de bibliotecas de Pokémon: Box (aliados) e EnemyLibrary (inimigos com treinadores).
"""

from typing import Dict, List, Optional
from pokemon import Pokemon


class Box:
    """Biblioteca de Pokémon aliados."""
    
    def __init__(self, name: str = "Box 1"):
        """
        Inicializa um Box.
        
        Args:
            name: Nome do Box
        """
        self.name = name
        self.pokemons: Dict[str, Pokemon] = {}
    
    def add_pokemon(self, name: str, pokemon: Pokemon) -> bool:
        """
        Adiciona um Pokémon ao Box.
        
        Args:
            name: ID/chave para o Pokémon
            pokemon: Pokémon a ser adicionado
            
        Returns:
            True se adicionado com sucesso
        """
        if name in self.pokemons:
            return False
        self.pokemons[name] = pokemon
        return True
    
    def remove_pokemon(self, name: str) -> bool:
        """Remove um Pokémon do Box."""
        if name not in self.pokemons:
            return False
        del self.pokemons[name]
        return True
    
    def get_pokemon(self, name: str) -> Optional[Pokemon]:
        """Obtém um Pokémon do Box."""
        return self.pokemons.get(name)
    
    def list_pokemons(self) -> List[str]:
        """Retorna lista de nomes de Pokémon no Box."""
        return list(self.pokemons.keys())
    
    def clear(self) -> None:
        """Limpa todos os Pokémon do Box."""
        self.pokemons.clear()
    
    def __repr__(self) -> str:
        return f"Box(name='{self.name}', pokemons={len(self.pokemons)})"


class Trainer:
    """Treinador com seus Pokémon em uma ordem específica."""
    
    def __init__(self, name: str, battle_type: str = "single"):
        """
        Inicializa um Treinador.
        
        Args:
            name: Nome do treinador
            battle_type: Tipo de batalha - "single" (1x1) ou "double" (2x2)
        """
        self.name = name
        self.battle_type = battle_type  # "single" ou "double"
        self.pokemons: List[Pokemon] = []  # Lista ordenada de Pokémon
        self.defeated = False  # Se o treinador foi derrotado
        self.skipped = False   # Se o treinador foi pulado
    
    def add_pokemon(self, pokemon: Pokemon) -> None:
        """Adiciona um Pokémon à equipe do treinador (no final)."""
        self.pokemons.append(pokemon)
    
    def remove_pokemon(self, index: int) -> bool:
        """Remove um Pokémon pela posição."""
        if 0 <= index < len(self.pokemons):
            del self.pokemons[index]
            return True
        return False
    
    def get_pokemon(self, index: int) -> Optional[Pokemon]:
        """Obtém um Pokémon pela posição."""
        if 0 <= index < len(self.pokemons):
            return self.pokemons[index]
        return None
    
    def list_pokemons(self) -> List[str]:
        """Retorna lista de nomes de Pokémon na ordem."""
        return [p.name for p in self.pokemons]
    
    def clear(self) -> None:
        """Remove todos os Pokémon da equipe."""
        self.pokemons.clear()
    
    def __repr__(self) -> str:
        return f"Trainer(name='{self.name}', pokemons={len(self.pokemons)})"


class EnemyLibrary:
    """Biblioteca de inimigos organizada por treinadores."""
    
    def __init__(self):
        """Inicializa a biblioteca de inimigos."""
        self.trainers: Dict[str, Trainer] = {}
    
    def add_trainer(self, trainer: Trainer) -> bool:
        """
        Adiciona um novo treinador à biblioteca.
        
        Args:
            trainer: Treinador a ser adicionado
            
        Returns:
            True se adicionado com sucesso
        """
        if trainer.name in self.trainers:
            return False
        self.trainers[trainer.name] = trainer
        return True
    
    def remove_trainer(self, trainer_name: str) -> bool:
        """Remove um treinador da biblioteca."""
        if trainer_name not in self.trainers:
            return False
        del self.trainers[trainer_name]
        return True
    
    def get_trainer(self, trainer_name: str) -> Optional[Trainer]:
        """Obtém um treinador pelo nome."""
        return self.trainers.get(trainer_name)
    
    def list_trainers(self) -> List[str]:
        """Retorna lista de nomes de treinadores."""
        return list(self.trainers.keys())
    
    def add_pokemon_to_trainer(self, trainer_name: str, pokemon: Pokemon) -> bool:
        """
        Adiciona um Pokémon à equipe de um treinador.
        
        Args:
            trainer_name: Nome do treinador
            pokemon: Pokémon a ser adicionado
            
        Returns:
            True se adicionado com sucesso
        """
        trainer = self.trainers.get(trainer_name)
        if trainer:
            trainer.add_pokemon(pokemon)
            return True
        return False
    
    def clear(self) -> None:
        """Limpa todos os treinadores e Pokémon."""
        self.trainers.clear()
    
    def __repr__(self) -> str:
        total_pokemons = sum(len(t.pokemons) for t in self.trainers.values())
        return f"EnemyLibrary(trainers={len(self.trainers)}, pokemons={total_pokemons})"
