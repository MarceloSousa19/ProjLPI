import os
import cv2
import mediapipe as mp
import math
import csv

# Inicialização do MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True)
LANDMARKS = mp_pose.PoseLandmark

# Diretório base com subpastas por pose
DATASET_PATH = 'images_test'
CSV_OUTPUT = 'shared_data/features.csv'

# Função para calcular ângulo entre 3 pontos
def calcular_angulo(a, b, c):
    ang = math.degrees(
        math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0])
    )
    return abs(ang) if ang >= 0 else abs(360 + ang)

# Define os ângulos a calcular (exemplo)
ANGULOS = [
    (LANDMARKS.LEFT_SHOULDER, LANDMARKS.LEFT_ELBOW, LANDMARKS.LEFT_WRIST),
    (LANDMARKS.RIGHT_SHOULDER, LANDMARKS.RIGHT_ELBOW, LANDMARKS.RIGHT_WRIST),
    (LANDMARKS.LEFT_HIP, LANDMARKS.LEFT_KNEE, LANDMARKS.LEFT_ANKLE),
    (LANDMARKS.RIGHT_HIP, LANDMARKS.RIGHT_KNEE, LANDMARKS.RIGHT_ANKLE),
    (LANDMARKS.LEFT_SHOULDER, LANDMARKS.LEFT_HIP, LANDMARKS.LEFT_KNEE),
    (LANDMARKS.RIGHT_SHOULDER, LANDMARKS.RIGHT_HIP, LANDMARKS.RIGHT_KNEE),
]

# Criação do CSV
with open(CSV_OUTPUT, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Cabeçalho: nome, classe, ang1, ang2, ...
    writer.writerow(['imagem', 'classe'] + [f'ang_{i+1}' for i in range(len(ANGULOS))])

    # Iterar pelas pastas de poses
    for pasta_pose in os.listdir(DATASET_PATH):
        pasta_path = os.path.join(DATASET_PATH, pasta_pose)
        if not os.path.isdir(pasta_path):
            continue

        for imagem_nome in os.listdir(pasta_path):
            imagem_path = os.path.join(pasta_path, imagem_nome)
            imagem = cv2.imread(imagem_path)

            if imagem is None:
                print(f"[AVISO] Imagem inválida: {imagem_path}")
                continue

            try:
                rgb = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
                resultado = pose.process(rgb)

                if not resultado.pose_landmarks:
                    print(f"[ERRO] Sem landmarks: {imagem_path}")
                    continue

                landmarks = resultado.pose_landmarks.landmark
                angulos = []

                for a, b, c in ANGULOS:
                    ponto_a = (landmarks[a].x, landmarks[a].y)
                    ponto_b = (landmarks[b].x, landmarks[b].y)
                    ponto_c = (landmarks[c].x, landmarks[c].y)
                    angulo = calcular_angulo(ponto_a, ponto_b, ponto_c)
                    angulos.append(round(angulo, 2))

                writer.writerow([imagem_nome, pasta_pose] + angulos)

            except Exception as e:
                print(f"[EXCEÇÃO] {imagem_path}: {str(e)}")
                continue
