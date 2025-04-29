import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.avaliar_pose import avaliar_pose

angulos_referencia = {
    'elbow_right': 160,
    'elbow_left': 160,
    'shoulder_right': 90,
    'shoulder_left': 90,
    'hip_right': 170,
    'hip_left': 170,
    'knee_right': 170,
    'knee_left': 170
}

angulos_utilizador = {
    'elbow_right': 140,
    'elbow_left': 170,
    'shoulder_right': 85,
    'shoulder_left': 70,
    'hip_right': 160,
    'hip_left': 160,
    'knee_right': 150,
    'knee_left': 180
}

precisao, feedback = avaliar_pose(angulos_referencia, angulos_utilizador, nome_pose="Adho_Mukha_Svanasana")

print(f"Precisão da pose: {precisao}%")
print("Correções sugeridas:")
for mensagem in feedback:
    print(f"• {mensagem}")
