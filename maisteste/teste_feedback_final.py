import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.feedback_final import mostrar_feedback_final
from src.gerar_historico import gerar_historico_participacao, guardar_historico_json
from src.avaliar_nivel import avaliar_nivel

# Dados de exemplo
nivel = "Principiante"
nomes_poses = [
    "Adho_Mukha_Svanasana", "Virabhadrasana_One", "Utkatasana",
    "Trikonasana", "Padmasana", "Bakasana", "Navasana",
    "Dhanurasana", "Balasana", "Bitilasana"
]
precisoes_poses = [88, 82, 91, 85, 90, 80, 87, 84, 86, 83]

# Avaliar o nível (calcula média, passa/falha)
media_final, passou, _ = avaliar_nivel(precisoes_poses)

# Mostrar feedback no terminal
mostrar_feedback_final(nivel, nomes_poses, precisoes_poses, media_final, passou)

# Gerar histórico e guardar no ficheiro JSON
historico = gerar_historico_participacao(nivel, precisoes_poses, nomes_poses, passou, media_final)
guardar_historico_json(historico)
