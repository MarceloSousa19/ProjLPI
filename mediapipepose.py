import cv2
import mediapipe as mp
import numpy as np

# Inicializar MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

pose = mp_pose.Pose()

# Carregar a pose de referência (valores pré-definidos para comparação)
# Exemplo: {ponto_id: (x, y, z)}
pose_referencia = {
    0: (0.5, 0.5, 0),  # Exemplo: Nariz no centro da imagem
    11: (0.4, 0.6, 0), # Ombro esquerdo
    12: (0.6, 0.6, 0), # Ombro direito
    # Adicionar mais pontos conforme necessário
}

def calcular_similaridade(landmarks):
    """Compara os pontos do corpo detectados com a pose de referência."""
    if not landmarks:
        return 0  # Nenhum ponto detectado

    erro_total = 0
    pontos_validos = 0

    for id, ref_point in pose_referencia.items():
        if id in landmarks:
            ponto_user = landmarks[id]
            erro = np.linalg.norm(np.array(ref_point) - np.array(ponto_user))
            erro_total += erro
            pontos_validos += 1

    if pontos_validos == 0:
        return 0

    # Normalizar para uma escala de 0 a 100%
    score = max(0, 100 - (erro_total / pontos_validos) * 100)
    return round(score, 2)

# Capturar vídeo da webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb_frame)

    landmarks_dict = {}

    if results.pose_landmarks:
        for id, lm in enumerate(results.pose_landmarks.landmark):
            landmarks_dict[id] = (lm.x, lm.y, lm.z)

        # Calcular similaridade
        score = calcular_similaridade(landmarks_dict)
        cv2.putText(frame, f"Score: {score}%", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        # Desenhar pontos no corpo
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    cv2.imshow("Pose Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
