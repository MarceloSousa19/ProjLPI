from flask import Flask, request, jsonify
import cv2
import numpy as np
import mediapipe as mp
import joblib
import tempfile
import os

# Inicializar Flask
app = Flask(__name__)

# Carregar modelo e encoder
MODEL_PATH = "ProjLPI/shared_data/mlp_pose_classifier.joblib"
ENCODER_PATH = "ProjLPI/shared_data/label_encoder.joblib"

modelo = joblib.load(MODEL_PATH)
label_encoder = joblib.load(ENCODER_PATH)

# Índices dos landmarks
LANDMARK_INDEXES = {
    'R_SHOULDER': 12, 'R_ELBOW': 14, 'R_WRIST': 16,
    'L_SHOULDER': 11, 'L_ELBOW': 13, 'L_WRIST': 15,
    'R_HIP': 24, 'R_KNEE': 26, 'R_ANKLE': 28,
    'L_HIP': 23, 'L_KNEE': 25, 'L_ANKLE': 27,
    'NOSE': 0
}

def calcular_angulo(a, b, c):
    ba = a - b
    bc = c - b
    cos_ang = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    cos_ang = np.clip(cos_ang, -1.0, 1.0)
    return round(np.degrees(np.arccos(cos_ang)) / 180.0, 5)

def extrair_features(imagem_cv):
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=True)
    results = pose.process(cv2.cvtColor(imagem_cv, cv2.COLOR_BGR2RGB))

    if not results.pose_landmarks:
        return None

    pontos = results.pose_landmarks.landmark
    coord = np.array([[lm.x, lm.y, lm.z] for lm in pontos])
    mid_hip = (coord[LANDMARK_INDEXES['L_HIP']] + coord[LANDMARK_INDEXES['R_HIP']]) / 2
    scale = np.linalg.norm(coord[LANDMARK_INDEXES['NOSE']] - mid_hip)
    if scale == 0:
        return None

    norm_coords = (coord - mid_hip) / scale
    flattened = norm_coords.flatten().tolist()

    def p(idx): return norm_coords[idx]
    angulos = [
        calcular_angulo(p(12), p(14), p(16)),
        calcular_angulo(p(11), p(13), p(15)),
        calcular_angulo(p(14), p(12), p(24)),
        calcular_angulo(p(13), p(11), p(23)),
        calcular_angulo(p(12), p(24), p(26)),
        calcular_angulo(p(11), p(23), p(25)),
        calcular_angulo(p(24), p(26), p(28)),
        calcular_angulo(p(23), p(25), p(27))
    ]

    return np.array(flattened + angulos).reshape(1, -1)

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({"error": "No image file uploaded"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp:
        file.save(temp.name)
        imagem = cv2.imread(temp.name)
        os.unlink(temp.name)

    try:
        X = extrair_features(imagem)
        if X is None:
            return jsonify({"error": "Pose não detectada na imagem."}), 422

        pred = modelo.predict(X)[0]
        proba = np.max(modelo.predict_proba(X))
        pose = label_encoder.inverse_transform([pred])[0]

        return jsonify({
            "pose": pose,
            "confidence": round(proba * 100, 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
