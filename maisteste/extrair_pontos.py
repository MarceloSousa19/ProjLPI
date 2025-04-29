

import os
import csv
import cv2
import mediapipe as mp
import numpy as np

# Função para calcular ângulo entre três pontos
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = abs(radians * 180.0 / np.pi)
    return 360 - angle if angle > 180.0 else angle

# Função para normalizar landmarks
def normalize_landmarks(landmarks):
    landmarks = np.array([[lm.x, lm.y, lm.z] for lm in landmarks])

    # Center: ponto médio entre ancas
    center = (landmarks[23] + landmarks[24]) / 2
    landmarks -= center

    # Scale: distância entre ombros
    shoulder_dist = np.linalg.norm(landmarks[11] - landmarks[12])
    if shoulder_dist > 0:
        landmarks /= shoulder_dist

    # Rotation: alinhar linha ombro-ombro na horizontal
    delta = landmarks[12] - landmarks[11]
    angle = np.arctan2(delta[1], delta[0])
    rotation_matrix = np.array([
        [np.cos(-angle), -np.sin(-angle), 0],
        [np.sin(-angle), np.cos(-angle), 0],
        [0, 0, 1]
    ])
    landmarks = landmarks.dot(rotation_matrix)

    return landmarks

# Configura MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True)

# Diretórios
BASE_DIR = 'poses_dataset'
SPLITS = ['training', 'testing']

# Cabeçalhos
landmark_headers = []
for i in range(33):
    landmark_headers += [f'lm{i}_x', f'lm{i}_y', f'lm{i}_z']

angle_names = [
    'elbow_right', 'elbow_left',
    'shoulder_right', 'shoulder_left',
    'hip_right', 'hip_left',
    'knee_right', 'knee_left'
]
header = ['image', 'label'] + landmark_headers + angle_names

# Garante que a pasta existe
os.makedirs(BASE_DIR, exist_ok=True)

# Processa datasets
for split in SPLITS:
    input_dir = os.path.join(BASE_DIR, split)
    output_csv = os.path.join(BASE_DIR, f'features_{split}.csv')

    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)

        for label in os.listdir(input_dir):
            class_dir = os.path.join(input_dir, label)
            if not os.path.isdir(class_dir):
                continue

            for img_name in os.listdir(class_dir):
                print(f"[{split}] {label} → {img_name}")
                img_path = os.path.join(class_dir, img_name)
                img = cv2.imread(img_path)
                if img is None:
                    continue

                results = pose.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                if not results.pose_landmarks:
                    continue

                landmarks = normalize_landmarks(results.pose_landmarks.landmark)

                # Define pontos de interesse normalizados
                r_shoulder = landmarks[12][:2]
                r_elbow = landmarks[14][:2]
                r_wrist = landmarks[16][:2]
                l_shoulder = landmarks[11][:2]
                l_elbow = landmarks[13][:2]
                l_wrist = landmarks[15][:2]
                r_hip = landmarks[24][:2]
                r_knee = landmarks[26][:2]
                r_ankle = landmarks[28][:2]
                l_hip = landmarks[23][:2]
                l_knee = landmarks[25][:2]
                l_ankle = landmarks[27][:2]

                # Calcula ângulos
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

                # Prepara linha do CSV
                row = [img_name, label]
                row += [round(coord, 5) for point in landmarks for coord in point]
                row += [round(a, 2) for a in angles]

                writer.writerow(row)

    print(f"✓ {split}: features extraídas e gravadas em {output_csv}")
