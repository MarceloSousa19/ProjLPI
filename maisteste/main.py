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

# Carregar poses armazqadas (JSON)
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

def guardar_pose(nome_pose, angulos, landmarks, ficheiro='poses.json'):
    if os.path.exists(ficheiro):
        with open(ficheiro, 'r') as f:
            poses = json.load(f)
    else:
        poses = {}
    poses[nome_pose] = {
        "angles": angulos,
        "landmarks": landmarks
    }
    with open(ficheiro, 'w') as f:
        json.dump(poses, f, indent=4)
    print(f"Pose '{nome_pose}' guardada com sucesso.")

def calcular_precisao_landmarks(landmarks_user, landmarks_ref, tolerancia=0.05):
    erros = [
        np.linalg.norm(np.array(user) - np.array(ref))
        for user, ref in zip(landmarks_user, landmarks_ref)
    ]
    precisao = sum(1 for erro in erros if erro < tolerancia) / len(erros) * 100
    return precisao

def calcular_precisao_angulos(angles_user, angles_ref, tolerancia=tolerancia_angular):
    erros = [abs(a - b) for a, b in zip(angles_user, angles_ref)]
    precisao = sum(1 for erro in erros if erro < tolerancia) / len(erros) * 100
    return precisao

def calcular_precisao_combinada(landmarks_user, landmarks_ref, angles_user, angles_ref, peso_landmarks=0.5):
    precisao_landmarks = calcular_precisao_landmarks(landmarks_user, landmarks_ref)
    precisao_angulos = calcular_precisao_angulos(angles_user, angles_ref)
    precisao_combinada = (peso_landmarks * precisao_landmarks) + ((1 - peso_landmarks) * precisao_angulos)
    return precisao_combinada

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
            landmarks = [[lm.x, lm.y, lm.z] for lm in results.pose_landmarks.landmark]

            # Extrair pontos-chave
            r_shoulder = [landmarks[12][0], landmarks[12][1]]
            r_elbow = [landmarks[14][0], landmarks[14][1]]
            r_wrist = [landmarks[16][0], landmarks[16][1]]

            l_shoulder = [landmarks[11][0], landmarks[11][1]]
            l_elbow = [landmarks[13][0], landmarks[13][1]]
            l_wrist = [landmarks[15][0], landmarks[15][1]]

            r_hip = [landmarks[24][0], landmarks[24][1]]
            r_knee = [landmarks[26][0], landmarks[26][1]]
            r_ankle = [landmarks[28][0], landmarks[28][1]]

            l_hip = [landmarks[23][0], landmarks[23][1]]
            l_knee = [landmarks[25][0], landmarks[25][1]]
            l_ankle = [landmarks[27][0], landmarks[27][1]]

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

            # Calcular precisão
            if POSES_ARMAZENADAS:
                for nome, dados_ref in POSES_ARMAZENADAS.items():
                    landmarks_ref = dados_ref["landmarks"]
                    angles_ref = dados_ref["angles"]

                    precisao_landmarks = calcular_precisao_landmarks(landmarks, landmarks_ref)
                    precisao_angulos = calcular_precisao_angulos(angle, angles_ref)
                    precisao_combinada = calcular_precisao_combinada(landmarks, landmarks_ref, angle, angles_ref)

                    print(f"Pose: {nome}")
                    print(f"  Precisão (landmarks): {precisao_landmarks:.2f}%")
                    print(f"  Precisão (ângulos): {precisao_angulos:.2f}%")
                    print(f"  Precisão combinada: {precisao_combinada:.2f}%")

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
                guardar_pose(nome, angle, landmarks)

            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        cv2.imshow('Pose Detector', image)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()