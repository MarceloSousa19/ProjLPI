import cv2
import mediapipe as mp
import numpy as np

# Inicializar MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Simulação de poses armazenadas (depois será substituído por base de dados)
POSES_ARMAZENADAS = {
    "Tree Pose": np.array([[0.5, 0.8], [0.4, 0.6], [0.6, 0.6], [0.5, 0.4]]),  # Exemplo fictício
    "Warrior Pose": np.array([[0.5, 0.9], [0.3, 0.6], [0.7, 0.6], [0.5, 0.3]])  # Exemplo fictício
}

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

        # Comparar com poses armazenadas
        best_match = None
        best_similarity = 0

        for pose_name, stored_pose in POSES_ARMAZENADAS.items():
            similarity = calculate_similarity(user_pose[:len(stored_pose)], stored_pose)
            if similarity > best_similarity:
                best_similarity = similarity
                best_match = pose_name

        # Exibir a melhor correspondência
        if best_similarity >= 90:
            cv2.putText(frame, f"Pose Identificada: {best_match} ({best_similarity:.2f}%)",
                        (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Desenhar os pontos do corpo
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # Mostrar o vídeo
    cv2.imshow("Identificação de Pose", frame)

    # Pressiona 'Q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
