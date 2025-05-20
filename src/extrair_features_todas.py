# src/extract_features.py

import mediapipe as mp
import cv2
import numpy as np
from math import acos, degrees

mp_pose = mp.solutions.pose

# Índices de pontos usados para ângulos
def calcular_angulo(v1, v2):
    """Calcula o ângulo entre dois vetores"""
    v1 = np.array(v1)
    v2 = np.array(v2)
    cos_ang = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-8)
    return degrees(acos(np.clip(cos_ang, -1.0, 1.0)))

def extrair_landmarks_angulo(imagem):
    with mp_pose.Pose(static_image_mode=True) as pose:
        imagem_rgb = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
        resultado = pose.process(imagem_rgb)

        if not resultado.pose_landmarks:
            return None

        lm = resultado.pose_landmarks.landmark

        # Normalizar os landmarks por largura e altura da imagem
        altura, largura, _ = imagem.shape
        landmarks = []
        for ponto in lm:
            landmarks.extend([
                ponto.x * largura,
                ponto.y * altura,
                ponto.z * largura
            ])

        # Centrar e normalizar
        landmarks = np.array(landmarks)
        landmarks = landmarks - np.mean(landmarks)
        landmarks = landmarks / (np.std(landmarks) + 1e-8)

        # Extrair 8 ângulos articulares principais
        def ponto(i): return [lm[i].x, lm[i].y, lm[i].z]

        angulos = []
        try:
            # Cotovelo esquerdo
            angulos.append(calcular_angulo(np.subtract(ponto(11), ponto(13)), np.subtract(ponto(15), ponto(13))))
            # Cotovelo direito
            angulos.append(calcular_angulo(np.subtract(ponto(12), ponto(14)), np.subtract(ponto(16), ponto(14))))
            # Ombro esquerdo
            angulos.append(calcular_angulo(np.subtract(ponto(23), ponto(11)), np.subtract(ponto(13), ponto(11))))
            # Ombro direito
            angulos.append(calcular_angulo(np.subtract(ponto(24), ponto(12)), np.subtract(ponto(14), ponto(12))))
            # Anca esquerda
            angulos.append(calcular_angulo(np.subtract(ponto(11), ponto(23)), np.subtract(ponto(25), ponto(23))))
            # Anca direita
            angulos.append(calcular_angulo(np.subtract(ponto(12), ponto(24)), np.subtract(ponto(26), ponto(24))))
            # Joelho esquerdo
            angulos.append(calcular_angulo(np.subtract(ponto(23), ponto(25)), np.subtract(ponto(27), ponto(25))))
            # Joelho direito
            angulos.append(calcular_angulo(np.subtract(ponto(24), ponto(26)), np.subtract(ponto(28), ponto(26))))
        except Exception:
            return None

        # Normalizar ângulos (0 a 180) para 0-1
        angulos = np.array(angulos) / 180.0

        # Concatenar 99 landmarks + 8 ângulos
        features = np.concatenate([landmarks, angulos])
        return features.tolist()
