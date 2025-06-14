import json
import os
from collections import defaultdict

caminho_json = "shared_data/recordes_pessoais.json"

try:
    with open(caminho_json, "r", encoding="utf-8") as f:
        dados = json.load(f)

    # Contar poses acima de 90% por utilizador
    contagem = defaultdict(set)  

    for entry in dados:
        nome = entry.get("nome_utilizador")
        pose = entry.get("nome_pose")
        precisao = entry.get("precisao", 0)
        if nome and pose and precisao >= 90:
            contagem[nome].add(pose)

    resultados = []
    for nome, poses in contagem.items():
        pontuacao = len(poses)
        medalha = pontuacao == 82  # Medalha de ouro se tiver 82 poses acima de 90%  
        resultados.append({"nome": nome, "pontuacao": pontuacao, "medalha": medalha})

    resultados.sort(key=lambda x: x["pontuacao"], reverse=True)

    path_saida = "shared_data/classificacao_individual.json"
    with open(path_saida, "w", encoding="utf-8") as f_out:
        json.dump(resultados, f_out, ensure_ascii=False, indent=4)

    print("✓ Classificação individual gerada com sucesso!")
    print("📁 Guardado em:", os.path.abspath(path_saida))

except Exception as e:
    print(f"Erro ao gerar classificação: {e}")
