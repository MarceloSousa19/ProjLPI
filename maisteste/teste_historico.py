import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.gerar_historico import gerar_historico_participacao, guardar_historico_json
from src.avaliar_nivel import avaliar_nivel

# Dados fictícios
nivel = "Principiante"
precisoes_poses = [82, 85, 90, 88, 79, 83, 86, 81, 84, 80]
nomes_poses = [
    "Adho_Mukha_Svanasana",
    "Virabhadrasana_One",
    "Trikonasana",
    "Padmasana",
    "Bakasana",
    "Utkatasana",
    "Vrksasana",
    "Malasana",
    "Dhanurasana",
    "Ustrasana"
]
media, passou, _ = avaliar_nivel(precisoes_poses)

# Criar histórico
historico = gerar_historico_participacao(nivel, precisoes_poses, nomes_poses, passou, media)

# Guardar em JSON
guardar_historico_json(historico)
