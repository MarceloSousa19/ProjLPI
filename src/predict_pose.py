import cv2
import numpy as np
import mediapipe as mp
import joblib

# --- Constantes dos landmarks ---
LANDMARK_COUNT = 33
LANDMARK_INDEXES = {
    'R_SHOULDER': 12, 'R_ELBOW': 14, 'R_WRIST': 16,
    'L_SHOULDER': 11, 'L_ELBOW': 13, 'L_WRIST': 15,
    'R_HIP': 24, 'R_KNEE': 26, 'R_ANKLE': 28,
    'L_HIP': 23, 'L_KNEE': 25, 'L_ANKLE': 27,
    'NOSE': 0
}

# --- Função para calcular ângulo ---
def calcular_angulo(a, b, c):
    ba = a - b
    bc = c - b
    cos_angulo = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    cos_angulo = np.clip(cos_angulo, -1.0, 1.0)
    angulo = np.degrees(np.arccos(cos_angulo))
    return round(angulo / 180.0, 5)  # normalizado para [0, 1]

# --- Função para extrair os 107 features ---
def extrair_features(imagem_path):
    imagem = cv2.imread(imagem_path)
    if imagem is None:
        raise Exception(f"Erro ao abrir a imagem: {imagem_path}")

    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=True)
    results = pose.process(cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB))

    if not results.pose_landmarks:
        raise Exception("Landmarks não encontrados na imagem.")

    pontos = results.pose_landmarks.landmark

    # --- Normalizar landmarks ---
    coord = np.array([[lm.x, lm.y, lm.z] for lm in pontos])
    mid_hip = (coord[LANDMARK_INDEXES['L_HIP']] + coord[LANDMARK_INDEXES['R_HIP']]) / 2
    scale = np.linalg.norm(coord[LANDMARK_INDEXES['NOSE']] - mid_hip)
    if scale == 0:
        raise Exception("Erro na normalização dos landmarks.")
    norm_coords = (coord - mid_hip) / scale
    features_landmarks = norm_coords.flatten().tolist()  # 99

    # --- Calcular 8 ângulos normalizados ---
    def p(idx): return norm_coords[idx]
    angulos = [
        calcular_angulo(p(LANDMARK_INDEXES['R_SHOULDER']), p(LANDMARK_INDEXES['R_ELBOW']), p(LANDMARK_INDEXES['R_WRIST'])),
        calcular_angulo(p(LANDMARK_INDEXES['L_SHOULDER']), p(LANDMARK_INDEXES['L_ELBOW']), p(LANDMARK_INDEXES['L_WRIST'])),

        calcular_angulo(p(LANDMARK_INDEXES['R_ELBOW']), p(LANDMARK_INDEXES['R_SHOULDER']), p(LANDMARK_INDEXES['R_HIP'])),
        calcular_angulo(p(LANDMARK_INDEXES['L_ELBOW']), p(LANDMARK_INDEXES['L_SHOULDER']), p(LANDMARK_INDEXES['L_HIP'])),

        calcular_angulo(p(LANDMARK_INDEXES['R_SHOULDER']), p(LANDMARK_INDEXES['R_HIP']), p(LANDMARK_INDEXES['R_KNEE'])),
        calcular_angulo(p(LANDMARK_INDEXES['L_SHOULDER']), p(LANDMARK_INDEXES['L_HIP']), p(LANDMARK_INDEXES['L_KNEE'])),

        calcular_angulo(p(LANDMARK_INDEXES['R_HIP']), p(LANDMARK_INDEXES['R_KNEE']), p(LANDMARK_INDEXES['R_ANKLE'])),
        calcular_angulo(p(LANDMARK_INDEXES['L_HIP']), p(LANDMARK_INDEXES['L_KNEE']), p(LANDMARK_INDEXES['L_ANKLE']))
    ]

    return np.array(features_landmarks + angulos).reshape(1, -1)

# --- Carregar modelo e label encoder ---
modelo = joblib.load("ProjLPI/shared_data/mlp_pose_classifier.joblib")
label_encoder = joblib.load("ProjLPI/shared_data/label_encoder.joblib")

# --- Função reutilizável para usar no Flask ---
def classificar_pose(caminho_imagem):
    X = extrair_features(caminho_imagem)
    y_pred = modelo.predict(X)[0]
    y_proba = modelo.predict_proba(X)[0]
    classe = label_encoder.inverse_transform([y_pred])[0]
    probabilidade = float(np.max(y_proba))  # converter para float nativo

    return {
        "pose": classe,
        "precisao": round(probabilidade, 4)
    }

# --- Execução manual opcional (para testes) ---
if __name__ == "__main__":
    imagem_path = input("🖼️ Caminho da imagem para prever a pose: ").strip()

    try:
        resultado = classificar_pose(imagem_path)
        print(f"\n🧘 Pose prevista: {resultado['pose']}")
        print(f"🎯 Confiança: {resultado['precisao'] * 100:.2f}%")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
