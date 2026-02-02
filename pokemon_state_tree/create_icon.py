"""
Criar um ícone de uma árvore berry em formato .ico
"""

from PIL import Image, ImageDraw
import os

def create_tree_icon(filename="pokemon_tree.ico", size=256):
    """Criar ícone de uma árvore berry."""
    
    # Criar imagem com fundo transparente
    img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Dimensões
    cx, cy = size // 2, size // 2
    
    # Tronco (marrom)
    trunk_width = size // 8
    trunk_height = size // 4
    draw.rectangle(
        [cx - trunk_width//2, cy + size//5, cx + trunk_width//2, cy + size//5 + trunk_height],
        fill=(139, 69, 19, 255)
    )
    
    # Folhas/Berry (verde com detalhes)
    # Camada 1 (base - grande)
    draw.ellipse(
        [cx - size//3, cy - size//6, cx + size//3, cy + size//4],
        fill=(34, 139, 34, 255),  # Verde escuro
        outline=(0, 100, 0, 255),
        width=2
    )
    
    # Camada 2 (meio)
    draw.ellipse(
        [cx - size//2.5, cy - size//5, cx + size//2.5, cy + size//5],
        fill=(50, 205, 50, 255),  # Verde claro
        outline=(34, 139, 34, 255),
        width=2
    )
    
    # Camada 3 (topo)
    draw.ellipse(
        [cx - size//4, cy - size//3, cx + size//4, cy - size//10],
        fill=(144, 238, 144, 255),  # Verde bem claro
        outline=(50, 205, 50, 255),
        width=2
    )
    
    # Berry (círculo vermelho no centro)
    berry_size = size // 12
    draw.ellipse(
        [cx - berry_size, cy - berry_size//2, cx + berry_size, cy + berry_size//2],
        fill=(220, 20, 60, 255),  # Crimson
        outline=(139, 0, 0, 255),
        width=1
    )
    
    # Salvar como ICO
    # Criar múltiplos tamanhos para o ícone
    img.save(filename, format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
    print(f"✓ Ícone criado: {filename}")
    
    # Também salvar como PNG para referência
    png_filename = filename.replace('.ico', '.png')
    img.save(png_filename, 'PNG')
    print(f"✓ PNG criado para referência: {png_filename}")

if __name__ == "__main__":
    try:
        create_tree_icon()
    except ImportError:
        print("⚠ Pillow não está instalado. Execute: pip install pillow")
        print("Criando ícone simples alternativo...")
        # Fallback: criar um ícone simples em ICO padrão
        from PIL import Image
        img = Image.new('RGB', (256, 256), color='white')
        img.save("pokemon_tree.ico")
        print("✓ Ícone padrão criado (branco)")
