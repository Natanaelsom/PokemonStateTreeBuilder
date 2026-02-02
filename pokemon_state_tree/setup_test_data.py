"""
Script para criar dados de teste: Box de exemplo e Treinadores de exemplo.
"""

from pokemon import Pokemon, MajorStatus, MinorStatus
from library import Box, Trainer, EnemyLibrary
import json


def create_test_box() -> Box:
    """Cria uma Box de exemplo com vários Pokémon."""
    box = Box(name="Caixa de Teste")
    
    # Adicionar alguns Pokémon para teste
    pokemon_list = [
        ("pika_1", Pokemon(name="Pikachu", item="Leftovers")),
        ("char_1", Pokemon(name="Charizard", item="Assault Vest")),
        ("blast_1", Pokemon(name="Blastoise", item="Choice Specs")),
        ("venu_1", Pokemon(name="Venusaur", item="Sitrus Berry")),
        ("arc_1", Pokemon(name="Arcanine", item="Choice Band")),
        ("lap_1", Pokemon(name="Lapras", item="Weakness Policy")),
        ("gen_1", Pokemon(name="Gengar", item="Life Orb")),
        ("alak_1", Pokemon(name="Alakazam", item="Choice Scarf")),
        ("mach_1", Pokemon(name="Machamp", item="Assault Vest")),
        ("golem_1", Pokemon(name="Golem", item="Rockium Z")),
    ]
    
    for name, pokemon in pokemon_list:
        box.add_pokemon(name, pokemon)
    
    return box


def create_test_trainers() -> EnemyLibrary:
    """Cria uma biblioteca de treinadores de teste."""
    library = EnemyLibrary()
    
    # Treinador 1: Campeão Competidor
    trainer1 = Trainer(name="Campeão")
    trainer1.add_pokemon(Pokemon(name="Dragonite", item="Choice Band"))
    trainer1.add_pokemon(Pokemon(name="Landorus", item="Assault Vest"))
    trainer1.add_pokemon(Pokemon(name="Tornadus", item="Choice Scarf"))
    library.add_trainer(trainer1)
    
    # Treinador 2: Especialista em Fogo
    trainer2 = Trainer(name="Especialista em Fogo")
    trainer2.add_pokemon(Pokemon(name="Charizard", item="Life Orb"))
    trainer2.add_pokemon(Pokemon(name="Arcanine", item="Weakness Policy"))
    trainer2.add_pokemon(Pokemon(name="Volcarona", item="Choice Specs"))
    library.add_trainer(trainer2)
    
    # Treinador 3: Estrategista Psíquico
    trainer3 = Trainer(name="Estrategista Psíquico")
    trainer3.add_pokemon(Pokemon(name="Alakazam", item="Choice Scarf"))
    trainer3.add_pokemon(Pokemon(name="Gardevoir", item="Assault Vest"))
    trainer3.add_pokemon(Pokemon(name="Gallade", item="Life Orb"))
    library.add_trainer(trainer3)
    
    return library


def save_test_data():
    """Salva os dados de teste em arquivos JSON."""
    # Criar Box
    box = create_test_box()
    
    # Converter Box para dicionário (simplificado)
    box_data = {
        "name": box.name,
        "pokemons": []
    }
    for name, pokemon in box.pokemons.items():
        box_data["pokemons"].append({
            "name": pokemon.name,
            "item": pokemon.item,
            "is_mega": pokemon.is_mega,
            "hp_min_percent": pokemon.hp_min_percent,
            "hp_max_percent": pokemon.hp_max_percent,
            "major_status": pokemon.major_status.value,
            "minor_status": pokemon.minor_status.value
        })
    
    # Salvar Box
    with open("test_box.json", "w", encoding="utf-8") as f:
        json.dump(box_data, f, ensure_ascii=False, indent=2)
    
    # Criar Biblioteca de Treinadores
    library = create_test_trainers()
    
    # Converter Library para dicionário
    library_data = {
        "trainers": []
    }
    for trainer_name, trainer in library.trainers.items():
        trainer_data = {
            "name": trainer.name,
            "battle_type": trainer.battle_type,
            "pokemons": []
        }
        for pokemon in trainer.pokemons:
            trainer_data["pokemons"].append({
                "name": pokemon.name,
                "item": pokemon.item,
                "is_mega": pokemon.is_mega,
                "hp_min_percent": pokemon.hp_min_percent,
                "hp_max_percent": pokemon.hp_max_percent,
                "major_status": pokemon.major_status.value,
                "minor_status": pokemon.minor_status.value
            })
        library_data["trainers"].append(trainer_data)
    
    # Salvar Biblioteca
    with open("test_enemy_library.json", "w", encoding="utf-8") as f:
        json.dump(library_data, f, ensure_ascii=False, indent=2)
    
    print("✓ Dados de teste criados com sucesso!")
    print(f"  - test_box.json: {len(box.pokemons)} Pokémon")
    print(f"  - test_enemy_library.json: {len(library.trainers)} Treinadores")


if __name__ == "__main__":
    save_test_data()
