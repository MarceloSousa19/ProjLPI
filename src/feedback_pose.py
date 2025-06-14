
import json

import os
path = os.path.join(os.path.dirname(__file__), "..", "shared_data", "angulos_ideais.json")
with open(path, "r", encoding="utf-8") as f:
    angulos_ideais_data = json.load(f)

def gerar_correcoes(pose_nome: str, angulos_utilizador: list[float], tolerancia: float = 0.25) -> list[str]:
   
    correcoes = []
    angulos_ideais = angulos_ideais_data.get(pose_nome)

    if not angulos_ideais:
        return [" Pose não encontrada nos ângulos ideais."]

    nomes_angulos = [
        "Braço direito (ombro-cotovelo-pulso)",
        "Braço esquerdo (ombro-cotovelo-pulso)",
        "Ombro direito (cotovelo-ombro-anca)",
        "Ombro esquerdo (cotovelo-ombro-anca)",
        "Anca direita (ombro-anca-joelho)",
        "Anca esquerda (ombro-anca-joelho)",
        "Perna direita (anca-joelho-tornozelo)",
        "Perna esquerda (anca-joelho-tornozelo)"
    ]

    for i, angulo_user in enumerate(angulos_utilizador):
        angulo_ideal = angulos_ideais.get(f"ang_{i+1}")
        if angulo_ideal is None:
            continue
        diff = angulo_user - angulo_ideal

        if abs(diff) > tolerancia:
            direcao = "demasiado dobrado" if diff < 0 else "demasiado estendido"
            correcoes.append(f"{nomes_angulos[i]} está {direcao}")

    return correcoes
