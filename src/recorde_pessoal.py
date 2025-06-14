
import json
import os

def atualizar_recorde_pessoal(nome_pose, precisao, caminho_ficheiro="recordes_pessoais.json"):
   
    if os.path.exists(caminho_ficheiro):
        with open(caminho_ficheiro, 'r', encoding='utf-8') as f:
            recordes = json.load(f)
    else:
        recordes = {}


    recorde_atual = recordes.get(nome_pose, 0)

    # Atualizar só se a nova precisão for superior
    if precisao > recorde_atual:
        recordes[nome_pose] = round(precisao, 2)
        print(f"🏆 Novo recorde para {nome_pose}: {precisao}%")
    else:
        print(f"ℹ️ Mantido recorde anterior para {nome_pose}: {recorde_atual}%")

    # Guardar atualizado
    with open(caminho_ficheiro, 'w', encoding='utf-8') as f:
        json.dump(recordes, f, ensure_ascii=False, indent=4)
