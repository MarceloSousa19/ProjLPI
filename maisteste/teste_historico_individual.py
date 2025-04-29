import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.historico_individual import guardar_historico_individual

# Exemplo de guardar a precisão de uma pose
guardar_historico_individual("Adho_Mukha_Svanasana", 85.0)
guardar_historico_individual("Virabhadrasana_One", 78.5)
