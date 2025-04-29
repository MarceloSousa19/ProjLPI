import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.avaliar_nivel import avaliar_nivel

# Exemplo de precisões simuladas para 10 poses
precisoes_poses = [82, 85, 90, 88, 79, 83, 86, 81, 84, 80]

media, passou, feedback = avaliar_nivel(precisoes_poses)

print(f"Média final: {media}%")
print(feedback)
