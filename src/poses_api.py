from flask import Flask, jsonify, send_from_directory
import json
import os


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

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
