import cv2
import mediapipe as mp
import numpy as np
import json
import os

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

def guardar_pose(nome_pose, angulos, ficheiro='poses.json'):
    if os.path.exists(ficheiro):
        try:
            with open(ficheiro, 'r') as f:
                poses = json.load(f)
        except json.decoder.JSONDecodeError:
            poses = {}
    else:
        poses = {}
    poses[nome_pose] = angulos
    with open(ficheiro, 'w') as f:
        json.dump(poses, f, indent=4)
    print(f"Pose '{nome_pose}' guardada com sucesso em {ficheiro}.")

# === INÍCIO ===

# Caminho da imagem
caminho_imagem = input("Caminho da imagem: ").strip()

# Carregar imagem
imagem = cv2.imread(caminho_imagem)
if imagem is None:
    print("Caminho inválido ou imagem não encontrada.")
    exit()

imagem_rgb = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)

with mp_pose.Pose(static_image_mode=True) as pose:
    resultado = pose.process(imagem_rgb)

    if not resultado.pose_landmarks:
        print("Nenhuma pose detetada na imagem.")
        exit()

    lm = resultado.pose_landmarks.landmark

    pontos = {
        "r_shoulder": [lm[12].x, lm[12].y],
        "r_elbow":    [lm[14].x, lm[14].y],
        "r_wrist":    [lm[16].x, lm[16].y],
        "l_shoulder": [lm[11].x, lm[11].y],
        "l_elbow":    [lm[13].x, lm[13].y],
        "l_wrist":    [lm[15].x, lm[15].y],
        "r_hip":      [lm[24].x, lm[24].y],
        "r_knee":     [lm[26].x, lm[26].y],
        "r_ankle":    [lm[28].x, lm[28].y],
        "l_hip":      [lm[23].x, lm[23].y],
        "l_knee":     [lm[25].x, lm[25].y],
        "l_ankle":    [lm[27].x, lm[27].y]
    }

    angulos = [
        calculate_angle(pontos["r_shoulder"], pontos["r_elbow"], pontos["r_wrist"]),
        calculate_angle(pontos["l_shoulder"], pontos["l_elbow"], pontos["l_wrist"]),
        calculate_angle(pontos["r_elbow"], pontos["r_shoulder"], pontos["r_hip"]),
        calculate_angle(pontos["l_elbow"], pontos["l_shoulder"], pontos["l_hip"]),
        calculate_angle(pontos["r_shoulder"], pontos["r_hip"], pontos["r_knee"]),
        calculate_angle(pontos["l_shoulder"], pontos["l_hip"], pontos["l_knee"]),
        calculate_angle(pontos["r_hip"], pontos["r_knee"], pontos["r_ankle"]),
        calculate_angle(pontos["l_hip"], pontos["l_knee"], pontos["l_ankle"])
    ]

    espelhado = [
        angulos[1], angulos[0],
        angulos[3], angulos[2],
        angulos[5], angulos[4],
        angulos[7], angulos[6]
    ]

    # Mostrar imagem com landmarks
    mp_drawing.draw_landmarks(imagem, resultado.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    cv2.imshow("Pose Detetada", imagem)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print("Ângulos (direita):", [int(a) for a in angulos])
    print("Angulos (esquerda):", [int(a) for a in espelhado])

    guardar = input("Queres guardar esta pose no JSON? (s/n): ").strip().lower()
    if guardar == 's':
        nome = input("Nome base da pose (ex: Tree Pose): ").strip()
        guardar_pose(f"{nome} (direita)", [int(a) for a in angulos])
        guardar_pose(f"{nome} (esquerda)", [int(a) for a in espelhado])