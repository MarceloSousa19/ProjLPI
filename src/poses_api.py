from flask import Flask, jsonify, send_from_directory, request
import json
import os
from historico_individual import guardar_historico_individual
from gerar_historico import gerar_historico_participacao, guardar_historico_json


app = Flask(__name__)

# Caminho correto: ../shared_data
POSES_JSON_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "shared_data", "poses_por_dificuldade.json"))

@app.route("/poses_por_nivel", methods=["GET"])
def get_poses_por_nivel():
    with open(POSES_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return jsonify(data)


@app.route('/images_test/<path:subpath>')
def servir_imagem(subpath):
    imagens_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "images_test"))
    return send_from_directory(imagens_dir, subpath)

@app.route("/imagem_pose/<pose>")
def imagem_pose(pose):
    # Caminho absoluto para: ../images_test/<pose>
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "images_test"))
    pasta_pose = os.path.join(base_dir, pose)

    if not os.path.exists(pasta_pose):
        print(f"[404] Pasta não encontrada: {pasta_pose}")
        return jsonify({"erro": "Pasta da pose não encontrada"}), 404

    imagens_validas = sorted([
        f for f in os.listdir(pasta_pose)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ])

    if not imagens_validas:
        print(f"[404] Sem imagens válidas em: {pasta_pose}")
        return jsonify({"erro": "Nenhuma imagem válida encontrada"}), 404

    print(f"[200] Enviar imagem: {imagens_validas[0]} de {pose}")
    return jsonify({
        "pasta": pose,
        "ficheiro": imagens_validas[0]
    })


@app.route('/guardar_historico_individual', methods=['POST'])
def api_guardar_individual():
    data = request.get_json()
    guardar_historico_individual(data['nome_pose'], data['precisao'])
    return jsonify({'status': 'ok'})

@app.route('/guardar_historico_participacao', methods=['POST'])
def api_guardar_participacao():
    data = request.get_json()
    historico = gerar_historico_participacao(
        data['nivel'],
        data['precisoes_poses'],
        data['nomes_poses'],
        data['passou'],
        data['media_final']
    )
    guardar_historico_json(historico)
    return jsonify({'status': 'ok'})

@app.route('/classificacao_pessoal', methods=['GET'])
def classificacao_pessoal():
    caminho_ficheiro = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "shared_data", "historico_individual_poses.json"))

    if not os.path.exists(caminho_ficheiro):
        return jsonify({})  # ou [] se preferires uma lista

    with open(caminho_ficheiro, 'r', encoding='utf-8') as f:
        dados = json.load(f)

    return jsonify(dados)
@app.route('/progresso', methods=['GET'])
def get_progresso():
    caminho = os.path.join(os.path.dirname(__file__), "..", "shared_data", "progresso_utilizador.json")
    if not os.path.exists(caminho):
        return jsonify({
            "nivel_maximo_desbloqueado": "Principiante",
            "concluidos": []
        })
    with open(caminho, 'r', encoding='utf-8') as f:
        return jsonify(json.load(f))


@app.route('/atualizar_progresso', methods=['POST'])
def atualizar_progresso():
    data = request.get_json()
    caminho = os.path.join(os.path.dirname(__file__), "..", "shared_data", "progresso_utilizador.json")

    if os.path.exists(caminho):
        with open(caminho, 'r', encoding='utf-8') as f:
            progresso = json.load(f)
    else:
        progresso = {
            "nivel_maximo_desbloqueado": "Principiante",
            "concluidos": []
        }

    nivel_concluido = data.get("nivel")
    mapa = {
    "Intermédio": "Intermedio",
    "Avançado": "Avancado",
    "Mestre": "Mestre",
    "Principiante": "Principiante"
    }
    nivel_concluido = mapa.get(nivel_concluido, nivel_concluido)
    if nivel_concluido and nivel_concluido not in progresso["concluidos"]:
        progresso["concluidos"].append(nivel_concluido)

    # desbloquear próximo nível se existir
    ordem = ["Principiante", "Intermedio", "Avancado", "Mestre"]
    idx_atual = ordem.index(nivel_concluido)
    if idx_atual + 1 < len(ordem):
        progresso["nivel_maximo_desbloqueado"] = ordem[idx_atual + 1]

    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump(progresso, f, ensure_ascii=False, indent=4)

    return jsonify({"status": "ok", "progresso": progresso})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
