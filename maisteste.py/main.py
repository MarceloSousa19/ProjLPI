import cv2
import mediapipe as mp
import numpy as np
import json
import os
import time

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Tolerância para comparação dos ângulos
tolerancia_angular = 15

# Carregar poses armazenadas (JSON)
if os.path.exists('poses.json'):
    with open('poses.json', 'r') as f:
        POSES_ARMAZENADAS = json.load(f)
else:
    POSES_ARMAZENADAS = {}

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

def identificar_pose(angle_user, poses_ref, tolerancia=tolerancia_angular):
    melhor_match = "Pose desconhecida"
    menor_erro_total = float("inf")
    tipo_match = "nenhuma"

    espelhado = [
        angle_user[1], angle_user[0],
        angle_user[3], angle_user[2],
        angle_user[5], angle_user[4],
        angle_user[7], angle_user[6]
    ]

    for nome, angles_ref in poses_ref.items():
        erro_normal = sum([abs(a - b) for a, b in zip(angle_user, angles_ref)])
        erro_espelhado = sum([abs(a - b) for a, b in zip(espelhado, angles_ref)])

        if erro_normal < menor_erro_total and all(abs(a - b) < tolerancia for a, b in zip(angle_user, angles_ref)):
            menor_erro_total = erro_normal
            melhor_match = nome
            tipo_match = "direta"

        if erro_espelhado < menor_erro_total and all(abs(a - b) < tolerancia for a, b in zip(espelhado, angles_ref)):
            menor_erro_total = erro_espelhado
            melhor_match = nome
            tipo_match = "espelhada"

    return melhor_match, tipo_match

def guardar_pose(nome_pose, angulos, ficheiro='poses.json'):
    if os.path.exists(ficheiro):
        with open(ficheiro, 'r') as f:
            poses = json.load(f)
    else:
        poses = {}
    poses[nome_pose] = angulos
    with open(ficheiro, 'w') as f:
        json.dump(poses, f, indent=4)
    print(f"Pose '{nome_pose}' guardada com sucesso.")

cap = cv2.VideoCapture(0)
print("Iniciando deteção de pose... Pressiona 'q' para sair ou 'g' para guardar pose.")

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    ultimo_print = time.time()
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = pose.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            # Extrair pontos-chave
            r_shoulder = [landmarks[12].x, landmarks[12].y]
            r_elbow = [landmarks[14].x, landmarks[14].y]
            r_wrist = [landmarks[16].x, landmarks[16].y]

            l_shoulder = [landmarks[11].x, landmarks[11].y]
            l_elbow = [landmarks[13].x, landmarks[13].y]
            l_wrist = [landmarks[15].x, landmarks[15].y]

            r_hip = [landmarks[24].x, landmarks[24].y]
            r_knee = [landmarks[26].x, landmarks[26].y]
            r_ankle = [landmarks[28].x, landmarks[28].y]

            l_hip = [landmarks[23].x, landmarks[23].y]
            l_knee = [landmarks[25].x, landmarks[25].y]
            l_ankle = [landmarks[27].x, landmarks[27].y]

            # Calcular ângulos
            angle = [
                calculate_angle(r_shoulder, r_elbow, r_wrist),
                calculate_angle(l_shoulder, l_elbow, l_wrist),
                calculate_angle(r_elbow, r_shoulder, r_hip),
                calculate_angle(l_elbow, l_shoulder, l_hip),
                calculate_angle(r_shoulder, r_hip, r_knee),
                calculate_angle(l_shoulder, l_hip, l_knee),
                calculate_angle(r_hip, r_knee, r_ankle),
                calculate_angle(l_hip, l_knee, l_ankle)
            ]

            if time.time() - ultimo_print >= 10:
                print("Ângulos atuais:", [int(a) for a in angle])
                ultimo_print = time.time()

            # Identificar pose
            nome_pose, tipo = identificar_pose(angle, POSES_ARMAZENADAS)
            texto = f"{nome_pose} ({tipo})" if nome_pose != "Pose desconhecida" else nome_pose
            cv2.putText(image, texto, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

            # Guardar pose se pressionar 'g'
            if cv2.waitKey(10) & 0xFF == ord('g'):
                nome = input("Nome da nova pose: ")
                guardar_pose(nome, angle)

            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        cv2.imshow('Pose Detector', image)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()