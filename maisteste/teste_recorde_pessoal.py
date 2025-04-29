import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.recorde_pessoal import atualizar_recorde_pessoal

# Exemplo de atualizar recordes
atualizar_recorde_pessoal("Adho_Mukha_Svanasana", 90.5)
atualizar_recorde_pessoal("Virabhadrasana_One", 85.0)
atualizar_recorde_pessoal("Adho_Mukha_Svanasana", 88.0)  # Não vai atualizar porque é inferior
