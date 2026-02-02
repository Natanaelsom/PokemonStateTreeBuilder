"""
Script para criar executável (.exe) do Pokémon State Tree Builder
com ícone personalizado
"""

import os
import sys
import subprocess
from pathlib import Path

def create_icon():
    """Criar o ícone se não existir."""
    icon_file = "pokemon_tree.ico"
    if not os.path.exists(icon_file):
        print("Criando ícone...")
        try:
            # Tentar usar PIL se disponível
            from PIL import Image, ImageDraw
            
            img = Image.new('RGBA', (256, 256), (255, 255, 255, 0))
            draw = ImageDraw.Draw(img)
            
            cx, cy = 128, 128
            # Tronco
            draw.rectangle([110, 160, 146, 210], fill=(139, 69, 19, 255))
            # Folhas - círculos concêntricos
            draw.ellipse([60, 80, 196, 180], fill=(34, 139, 34, 255))
            draw.ellipse([45, 70, 211, 190], fill=(50, 205, 50, 255))
            draw.ellipse([85, 30, 171, 130], fill=(144, 238, 144, 255))
            # Berry
            draw.ellipse([110, 110, 146, 146], fill=(220, 20, 60, 255))
            
            img.save(icon_file)
            print(f"✓ Ícone criado: {icon_file}")
        except ImportError:
            print("⚠ Pillow não instalado, pulando criação de ícone customizado")
            print("  Execute: pip install pillow")
            return None
    return icon_file

def build_executable():
    """Criar o executável com PyInstaller."""
    
    # Criar ícone
    icon_file = create_icon()
    
    # Verificar PyInstaller
    try:
        import PyInstaller
    except ImportError:
        print("PyInstaller nao esta instalado")
        print("Execute: pip install pyinstaller")
        sys.exit(1)
    
    # Comando PyInstaller
    output_dir = "Executavel"
    build_dir = "build"

    # Garantir que a pasta de saída exista
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",  # Arquivo único
        "--name", "PokemonStateTreeBuilder",
        "--console",  # Mostrar console (para debug)
    ]
    
    # Adicionar ícone se criado
    if icon_file and os.path.exists(icon_file):
        cmd.extend(["--icon", icon_file])
    
    cmd.extend([
        "--distpath", output_dir,
        "--workpath", build_dir,
        "--specpath", ".",
        "gui.py"
    ])
    
    print("\n" + "="*60)
    print("Criando executavel com PyInstaller...")
    print("="*60 + "\n")
    
    try:
        result = subprocess.run(cmd, check=True)
        
        exe_path = os.path.join(output_dir, "PokemonStateTreeBuilder.exe")
        if os.path.exists(exe_path):
            print("\n" + "="*60)
            print("OK - Executavel criado com sucesso!")
            print(f"Localizacao: {exe_path}")
            print("="*60)
            
            # Informações
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"\nTamanho: {size_mb:.1f} MB")
            print("\nPara distribuir, envie apenas o arquivo .exe")
            
        else:
            print("ERRO: Arquivo .exe nao encontrado apos build")
            
    except subprocess.CalledProcessError as e:
        print(f"ERRO ao criar executavel: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Erro inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("\nPokémon State Tree Builder - Gerador de Executável")
    print("="*60)
    
    # Verificar se está no diretório correto
    if not os.path.exists("gui.py"):
        print("✗ Erro: gui.py não encontrado no diretório atual")
        print("Execute este script no diretório raiz do projeto")
        sys.exit(1)
    
    build_executable()
