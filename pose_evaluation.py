import cv2
import mediapipe as mp
import numpy as np
import random

# Inicializar MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Poses pré-definidas organizadas por nível (depois será ligado a uma base de dados)
POSES_POR_NIVEL = {
    "Principiante": {
        "Tree Pose": np.array([[0.5, 0.8], [0.4, 0.6], [0.6, 0.6], [0.5, 0.4]]),
        "Mountain Pose": np.array([[0.5, 0.9], [0.5, 0.7], [0.5, 0.5], [0.5, 0.3]]),
        "Pose 3": np.array([[0.6, 0.85], [0.5, 0.65], [0.7, 0.55], [0.6, 0.4]]),
        "Pose 4": np.array([[0.4, 0.8], [0.3, 0.6], [0.5, 0.5], [0.4, 0.3]])
    },
    "Intermédio": {
        "Warrior Pose": np.array([[0.5, 0.9], [0.3, 0.6], [0.7, 0.6], [0.5, 0.3]]),
        "Pose 6": np.array([[0.4, 0.85], [0.3, 0.65], [0.6, 0.55], [0.5, 0.4]])
    },
    "Experiente": {
        "Dancer Pose": np.array([[0.5, 0.85], [0.4, 0.5], [0.6, 0.4], [0.5, 0.2]]),
        "Pose 8": np.array([[0.6, 0.9], [0.5, 0.7], [0.7, 0.6], [0.6, 0.35]])
    }
}

# Inicializar nível e seleção de poses
nivel_atual = "Principiante"
poses_aleatorias = random.sample(list(POSES_POR_NIVEL[nivel_atual].keys()), 10)
indice_pose_atual = 0
aprovacoes = 0  # Contador de poses com ≥ 95%

def extract_keypoints(landmarks):
    """Extrai os pontos (x, y) normalizados da pose detectada."""
    keypoints = []
    for landmark in landmarks.landmark:
        keypoints.append([landmark.x, landmark.y])
    return np.array(keypoints)

def calculate_similarity(pose1, pose2):
    """Calcula a similaridade entre duas poses usando a distância euclidiana."""
    if pose1.shape != pose2.shape:
        return 0  # Formatos incompatíveis
    
    distances = np.linalg.norm(pose1 - pose2, axis=1)
    similarity = 100 - (np.mean(distances) * 100)  # Normaliza para 0-100%
    return max(0, similarity)

# Inicializar captura de vídeo
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Converter para RGB e processar a pose
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb_frame)

    if results.pose_landmarks:
        # Extrair pontos da pose capturada
        user_pose = extract_keypoints(results.pose_landmarks)

        # Comparar com a pose da tentativa atual
        pose_nome = poses_aleatorias[indice_pose_atual]
        stored_pose = POSES_POR_NIVEL[nivel_atual][pose_nome]
        similarity = calculate_similarity(user_pose[:len(stored_pose)], stored_pose)

        # Definir feedback de avaliação
        if similarity >= 95:
            feedback = f"✅ Excelente! {pose_nome} ({similarity:.2f}%)"
            aprovacoes += 1
        elif similarity >= 70:
            feedback = f"👌 Bom! {pose_nome} ({similarity:.2f}%) - Tente melhorar!"
        else:
            feedback = f"❌ Fraco! {pose_nome} ({similarity:.2f}%) - Repita ou Pule ('S')"

        # Exibir feedback na tela
        cv2.putText(frame, feedback, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Desenhar os pontos do corpo
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # Mostrar o vídeo
    cv2.imshow("Sistema de Avaliação de Poses", frame)

    # Teclas para interação
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):  # Skip
        indice_pose_atual += 1
    
    # Se completou as 10 poses
    if indice_pose_atual >= 10:
        feedback = f"🏁 Fim da tentativa! {aprovacoes}/10 ≥ 95%."
        print(feedback)

        # Se todas as 10 foram bem avaliadas (≥ 95%), sobe de nível
        if aprovacoes >= 10:
            if nivel_atual == "Principiante":
                nivel_atual = "Intermédio"
            elif nivel_atual == "Intermédio":
                nivel_atual = "Experiente"
            
            print(f"🎉 Parabéns! Subiu para o nível {nivel_atual}!")
        
        break  # Termina a avaliação

cap.release()
cv2.destroyAllWindows()
