import json
import os
from collections import defaultdict

# Caminho para o ficheiro JSON com recordes de grupos
caminho_json = "shared_data/recordes_grupos.json"

try:
    with open(caminho_json, "r", encoding="utf-8") as f:
        dados = json.load(f)

    # Contar poses acima de 90% por grupo
    contagem = defaultdict(set)  # grupo -> set de poses com >90%

    for entry in dados:
        grupo = entry.get("nome_grupo")
        pose = entry.get("nome_pose")
        precisao = entry.get("precisao", 0)
        if grupo and pose and precisao >= 90:
            contagem[grupo].add(pose)

    resultados = []
    for grupo, poses in contagem.items():
        pontuacao = len(poses)
        medalha = pontuacao == 50  # assumindo 50 poses totais possíveis
        resultados.append({"grupo": grupo, "pontuacao": pontuacao, "medalha": medalha})

    resultados.sort(key=lambda x: x["pontuacao"], reverse=True)

    path_saida = "shared_data/classificacao_grupos.json"
    with open(path_saida, "w", encoding="utf-8") as f_out:
        json.dump(resultados, f_out, ensure_ascii=False, indent=4)

    print("✓ Classificação de grupos gerada com sucesso!")
    print("📁 Guardado em:", os.path.abspath(path_saida))

except Exception as e:
    print(f"Erro ao gerar classificação de grupos: {e}")
