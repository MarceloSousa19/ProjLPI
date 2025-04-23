# src/extract_angles.py

import os
import csv
import cv2
import mediapipe as mp
import numpy as np

# Função para calcular o ângulo entre três pontos
# pontos a, b, c: cada um [x, y]
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = abs(radians * 180.0 / np.pi)
    return 360 - angle if angle > 180.0 else angle

# Configura MediaPipe Pose em modo estático (imagens)
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True)

# Diretório base do dataset
BASE_DIR = 'poses_dataset'  # alterar se o nome for outro
SPLITS = ['training', 'testing']

# Nomes das colunas de ângulos (8 articulações)
angle_names = [
    'elbow_right', 'elbow_left',
    'shoulder_right', 'shoulder_left',
    'hip_right', 'hip_left',
    'knee_right', 'knee_left'
]
header = ['image', 'label'] + angle_names

for split in SPLITS:
    input_dir = os.path.join(BASE_DIR, split)  
    output_csv = os.path.join(BASE_DIR, f'angles_{split}.csv')

    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)

        # Percorre cada classe (pose)
        for label in os.listdir(input_dir):
            class_dir = os.path.join(input_dir, label)
            if not os.path.isdir(class_dir):
                continue

            # Processa cada imagem
            for img_name in os.listdir(class_dir):
                print(f"[{split}] {label} → {img_name}")
                img_path = os.path.join(class_dir, img_name)
                img = cv2.imread(img_path)
                if img is None:
                    continue

                # Extrai landmarks
                results = pose.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                if not results.pose_landmarks:
                    continue

                lm = results.pose_landmarks.landmark
                # Define pontos de interesse
                r_shoulder = [lm[12].x, lm[12].y]
                r_elbow = [lm[14].x, lm[14].y]
                r_wrist = [lm[16].x, lm[16].y]
                l_shoulder = [lm[11].x, lm[11].y]
                l_elbow = [lm[13].x, lm[13].y]
                l_wrist = [lm[15].x, lm[15].y]
                r_hip = [lm[24].x, lm[24].y]
                r_knee = [lm[26].x, lm[26].y]
                r_ankle = [lm[28].x, lm[28].y]
                l_hip = [lm[23].x, lm[23].y]
                l_knee = [lm[25].x, lm[25].y]
                l_ankle = [lm[27].x, lm[27].y]

                # Calcula os ângulos
                angles = [
                    calculate_angle(r_shoulder, r_elbow, r_wrist),
                    calculate_angle(l_shoulder, l_elbow, l_wrist),
                    calculate_angle(r_elbow, r_shoulder, r_hip),
                    calculate_angle(l_elbow, l_shoulder, l_hip),
                    calculate_angle(r_shoulder, r_hip, r_knee),
                    calculate_angle(l_shoulder, l_hip, l_knee),
                    calculate_angle(r_hip, r_knee, r_ankle),
                    calculate_angle(l_hip, l_knee, l_ankle)
                ]

                # Grava a linha no CSV
                writer.writerow([img_name, label] + [round(a, 2) for a in angles])

    print(f"✓ {split}: ângulos extraídos e gravados em {output_csv}")
