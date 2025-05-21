# src/historico_individual.py

import json
import os
from datetime import datetime

def guardar_historico_individual(nome_pose, precisao, caminho_ficheiro="../shared_data/historico_individual_poses.json"):
    """
    Guarda a precisão individual de uma pose num histórico geral.

    Args:
        nome_pose (str): Nome da pose.
        precisao (float): Precisão obtida.
        caminho_ficheiro (str, optional): Nome do ficheiro JSON onde guardar. ="../shared_data/historico_individual_poses.json"
    """

    # Carregar histórico atual (se existir)
    if os.path.exists(caminho_ficheiro):
        with open(caminho_ficheiro, 'r', encoding='utf-8') as f:
            historico_total = json.load(f)
    else:
        historico_total = {}

    data_hoje = datetime.now().strftime("%Y-%m-%d")

    # Se a pose ainda não existe no histórico, cria-la
    if nome_pose not in historico_total:
        historico_total[nome_pose] = {
            "nome": nome_pose,
            "tentativas": []
        }

    # Adicionar nova tentativa
    historico_total[nome_pose]["tentativas"].append({
        "data": data_hoje,
        "precisao": round(precisao, 2)
    })

    # Guardar atualizado
    with open(caminho_ficheiro, 'w', encoding='utf-8') as f:
        json.dump(historico_total, f, ensure_ascii=False, indent=4)

    print(f"✓ Histórico individual da pose '{nome_pose}' atualizado.")
