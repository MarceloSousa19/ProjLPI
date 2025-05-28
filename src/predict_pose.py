
import cv2
import numpy as np
import mediapipe as mp
from joblib import load
from historico_individual import guardar_historico_individual
from feedback_pose import gerar_correcoes

LANDMARK_INDEXES = {
    'R_SHOULDER': 12, 'R_ELBOW': 14, 'R_WRIST': 16,
    'L_SHOULDER': 11, 'L_ELBOW': 13, 'L_WRIST': 15,
    'R_HIP': 24, 'R_KNEE': 26, 'R_ANKLE': 28,
    'L_HIP': 23, 'L_KNEE': 25, 'L_ANKLE': 27,
    'NOSE': 0
}

import os
path_modelo = os.path.join(os.path.dirname(__file__), "..", "shared_data", "mlp_pose_classifier.joblib")
modelo = load(path_modelo)

label_encoder = load("../shared_data/label_encoder.joblib")

def calcular_angulo(a, b, c):
    ba = a - b
    bc = c - b
    cos_angulo = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    cos_angulo = np.clip(cos_angulo, -1.0, 1.0)
    angulo = np.degrees(np.arccos(cos_angulo))
    return round(angulo / 180.0, 5)

def extrair_features(caminho_imagem):
    imagem = cv2.imread(caminho_imagem)
    if imagem is None:
        raise ValueError(f"Erro ao abrir a imagem: {caminho_imagem}")

    mp_pose = mp.solutions.pose
    with mp_pose.Pose(static_image_mode=True) as pose:
        results = pose.process(cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB))

    if not results.pose_landmarks:
        raise ValueError("Landmarks não encontrados na imagem.")

    pontos = results.pose_landmarks.landmark
    coord = np.array([[lm.x, lm.y, lm.z] for lm in pontos])
    mid_hip = (coord[LANDMARK_INDEXES['L_HIP']] + coord[LANDMARK_INDEXES['R_HIP']]) / 2
    scale = np.linalg.norm(coord[LANDMARK_INDEXES['NOSE']] - mid_hip)
    if scale == 0:
        raise ValueError("Erro na normalização: escala nula.")

    norm_coords = (coord - mid_hip) / scale
    flatten = norm_coords.flatten().tolist()

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

    return np.array(flatten + angulos).reshape(1, -1), angulos

def classificar_pose(caminho_imagem):
    try:
        X, angulos = extrair_features(caminho_imagem)
        probs = modelo.predict_proba(X)[0]
        pred_index = np.argmax(probs)
        classe = label_encoder.inverse_transform([pred_index])[0]
        precisao = float(probs[pred_index])

        guardar_historico_individual(classe, precisao)

        correcoes = gerar_correcoes(classe, angulos)

        return {
            "pose": classe,
            "precisao": round(precisao * 100, 1),
            "correcoes": correcoes
        }

    except Exception as e:
        raise RuntimeError(f"Erro na classificação: {str(e)}")

if __name__ == "__main__":
    imagem_path = input("🖼️ Caminho da imagem: ").strip()
    try:
        resultado = classificar_pose(imagem_path)
        print(f"🧘 Pose prevista: {resultado['pose']}")
        print(f"🎯 Precisão: {resultado['precisao']}%")
        print("🛠️ Correções:")
        for c in resultado["correcoes"]:
            print(f" - {c}")
    except Exception as e:
        print(f"❌ Erro: {e}")
