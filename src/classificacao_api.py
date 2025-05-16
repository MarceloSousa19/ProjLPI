from flask import Flask, jsonify, request, send_from_directory
import json
import os
import tempfile
from datetime import datetime
from predict_pose import classificar_pose  # Esta função deve aceitar o caminho da imagem e devolver {"pose": ..., "precisao": ...}

app = Flask(__name__)

# Caminhos dos ficheiros
MAPA_PASTAS_PATH = os.path.join("ProjLPI", "shared_data", "mapa_pose_para_pasta.json")
POSES_PATH = os.path.join("ProjLPI", "shared_data", "poses_por_dificuldade.json")
HISTORICO_PATH = os.path.join("ProjLPI", "shared_data", "historico_individual_poses.json")
IMAGES_BASE_PATH = os.path.join("ProjLPI", "images_test")

# 🧩 Utilitários
def carregar_json(caminho):
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def carregar_mapa_pastas():
    return carregar_json(MAPA_PASTAS_PATH)

# ✅ Classificação pessoal por nível
@app.route("/classificacao_pessoal", methods=["GET"])
def classificacao_pessoal():
    poses_por_nivel = carregar_json(POSES_PATH)
    historico = carregar_json(HISTORICO_PATH)

    resultado = {}
    desbloqueia_mestre = True

    for nivel, poses in poses_por_nivel.items():
        if nivel == "Mestre":
            continue

        resultado[nivel] = []
        for pose in poses:
            tentativas = historico.get(pose, {}).get("tentativas", [])
            melhor = max((t["precisao"] for t in tentativas), default=None)

            resultado[nivel].append({
                "pose": pose,
                "precisao": melhor
            })

            if melhor is None or melhor < 90:
                desbloqueia_mestre = False

    if desbloqueia_mestre:
        resultado["Mestre"] = []
        for pose in poses_por_nivel.get("Mestre", []):
            tentativas = historico.get(pose, {}).get("tentativas", [])
            melhor = max((t["precisao"] for t in tentativas), default=None)
            resultado["Mestre"].append({
                "pose": pose,
                "precisao": melhor
            })

    return jsonify(resultado)

# ✅ NOVO: classificar imagem recebida
@app.route("/classificar_pose", methods=["POST"])
def classificar_pose_api():
    if "imagem" not in request.files:
        return jsonify({"erro": "Ficheiro de imagem não fornecido"}), 400

    imagem = request.files["imagem"]

    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
        caminho_temp = temp_file.name
        imagem.save(caminho_temp)

    try:
        resultado = classificar_pose(caminho_temp)  # Deve devolver {"pose": ..., "precisao": ...}
        os.remove(caminho_temp)
        return jsonify(resultado)
    except Exception as e:
        os.remove(caminho_temp)
        return jsonify({"erro": str(e)}), 500

# ✅ NOVO: guardar tentativa no histórico
@app.route("/guardar_tentativa", methods=["POST"])
def guardar_tentativa():
    dados = request.get_json()
    pose = dados.get("pose")
    precisao = dados.get("precisao")

    if not pose or precisao is None:
        return jsonify({"erro": "Dados inválidos"}), 400

    historico = carregar_json(HISTORICO_PATH)
    tentativas = historico.get(pose, {}).get("tentativas", [])

    tentativas.append({
        "precisao": precisao,
        "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    historico[pose] = {"tentativas": tentativas}

    with open(HISTORICO_PATH, "w", encoding="utf-8") as f:
        json.dump(historico, f, indent=2, ensure_ascii=False)

    return jsonify({"sucesso": True})

# ✅ Imagem real de referência da pose
@app.route("/imagem_pose/<pose>", methods=["GET"])
def primeira_imagem_pose(pose):
    mapa = carregar_mapa_pastas()
    pasta_real = mapa.get(pose, pose)
    pasta_pose = os.path.join(IMAGES_BASE_PATH, pasta_real)

    try:
        if not os.path.exists(pasta_pose):
            return jsonify({"erro": f"Pasta não encontrada: {pasta_pose}"}), 404

        ficheiros = sorted(os.listdir(pasta_pose))
        imagem = next((f for f in ficheiros if f.lower().endswith(('.jpg', '.jpeg', '.png'))), None)

        if imagem:
            return jsonify({"ficheiro": imagem, "pasta": pasta_real})
        return jsonify({"erro": "Nenhuma imagem encontrada"}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# ✅ Servir imagens diretamente
@app.route("/images/<pose>/<filename>")
def servir_imagem_pose(pose, filename):
    dir_completo = os.path.abspath(os.path.join(IMAGES_BASE_PATH, pose))
    return send_from_directory(dir_completo, filename)

# ✅ Iniciar servidor
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5002)
