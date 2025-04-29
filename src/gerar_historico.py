import json
from datetime import datetime
import os

def gerar_historico_participacao(nivel, precisoes_poses, nomes_poses, passou, media_final):
    """
    Gera o dicionário do histórico de uma participação.

    Args:
        nivel (str): Nome do nível ("Principiante", "Intermédio", etc).
        precisoes_poses (list of float): Lista com as precisões individuais.
        nomes_poses (list of str): Lista com os nomes das poses.
        passou (bool): True se passou o nível, False caso contrário.
        media_final (float): Média final das 10 poses.

    Returns:
        dict: Histórico da participação.
    """

    data_hoje = datetime.now().strftime("%Y-%m-%d")

    poses_info = []
    for nome, precisao in zip(nomes_poses, precisoes_poses):
        poses_info.append({
            "nome": nome,
            "precisao": round(precisao, 2)
        })

    historico = {
        "nivel": nivel,
        "data": data_hoje,
        "resultado_nivel": "Passou" if passou else "Falhou",
        "media_final": round(media_final, 2),
        "poses": poses_info
    }

    return historico

def guardar_historico_json(historico, caminho_ficheiro="historico_participacoes.json"):
    """
    Guarda um histórico de participação num ficheiro JSON.

    Args:
        historico (dict): Dicionário do histórico da participação.
        caminho_ficheiro (str, optional): Caminho do ficheiro JSON. Default é 'historico_participacoes.json'.
    """

    # Se já existe, carregar o conteúdo anterior
    if os.path.exists(caminho_ficheiro):
        with open(caminho_ficheiro, 'r', encoding='utf-8') as f:
            historico_total = json.load(f)
    else:
        historico_total = []

    # Adicionar novo histórico
    historico_total.append(historico)

    # Guardar tudo de volta
    with open(caminho_ficheiro, 'w', encoding='utf-8') as f:
        json.dump(historico_total, f, ensure_ascii=False, indent=4)

    print(f"✓ Histórico guardado em {caminho_ficheiro}")
