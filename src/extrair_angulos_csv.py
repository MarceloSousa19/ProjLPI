import pandas as pd
import numpy as np
import os
import math

BASE_DIR = 'ProjLPI'
TRAIN_PATH = os.path.join(BASE_DIR, 'shared_data/features_train_normalized.csv')
TEST_PATH = os.path.join(BASE_DIR, 'shared_data/features_test_normalized.csv')
TRAIN_OUT = os.path.join(BASE_DIR, 'shared_data/features_train_angulos.csv')
TEST_OUT = os.path.join(BASE_DIR, 'shared_data/features_test_angulos.csv')

# Índices dos landmarks
indices = {
    'R_SHOULDER': 12, 'R_ELBOW': 14, 'R_WRIST': 16,
    'L_SHOULDER': 11, 'L_ELBOW': 13, 'L_WRIST': 15,
    'R_HIP': 24, 'R_KNEE': 26, 'R_ANKLE': 28,
    'L_HIP': 23, 'L_KNEE': 25, 'L_ANKLE': 27
}

# Função para obter ponto (x,y,z) normalizado
def get_ponto(row, idx):
    return np.array([row[f'x{idx}'], row[f'y{idx}'], row[f'z{idx}']])

# Função para calcular ângulo entre três pontos
def calcular_angulo(a, b, c):
    ba = a - b
    bc = c - b
    cos_angulo = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    cos_angulo = np.clip(cos_angulo, -1.0, 1.0)
    return round(np.degrees(np.arccos(cos_angulo)), 2)

# Função para processar um CSV e gerar outro com ângulos
def gerar_csv_angulos(ficheiro_entrada, ficheiro_saida):
    df = pd.read_csv(ficheiro_entrada)
    novas_linhas = []

    for _, row in df.iterrows():
        linha = [row['imagem'], row['classe']]

        # Ângulos conforme lista definida
        angulos = [
            calcular_angulo(get_ponto(row, indices['R_SHOULDER']), get_ponto(row, indices['R_ELBOW']), get_ponto(row, indices['R_WRIST'])),
            calcular_angulo(get_ponto(row, indices['L_SHOULDER']), get_ponto(row, indices['L_ELBOW']), get_ponto(row, indices['L_WRIST'])),

            calcular_angulo(get_ponto(row, indices['R_ELBOW']), get_ponto(row, indices['R_SHOULDER']), get_ponto(row, indices['R_HIP'])),
            calcular_angulo(get_ponto(row, indices['L_ELBOW']), get_ponto(row, indices['L_SHOULDER']), get_ponto(row, indices['L_HIP'])),

            calcular_angulo(get_ponto(row, indices['R_SHOULDER']), get_ponto(row, indices['R_HIP']), get_ponto(row, indices['R_KNEE'])),
            calcular_angulo(get_ponto(row, indices['L_SHOULDER']), get_ponto(row, indices['L_HIP']), get_ponto(row, indices['L_KNEE'])),

            calcular_angulo(get_ponto(row, indices['R_HIP']), get_ponto(row, indices['R_KNEE']), get_ponto(row, indices['R_ANKLE'])),
            calcular_angulo(get_ponto(row, indices['L_HIP']), get_ponto(row, indices['L_KNEE']), get_ponto(row, indices['L_ANKLE'])),
        ]

        linha += angulos
        novas_linhas.append(linha)

    colunas = ['imagem', 'classe'] + [f'ang_{i+1}' for i in range(8)]
    pd.DataFrame(novas_linhas, columns=colunas).to_csv(ficheiro_saida, index=False)
    print(f"✅ Guardado: {ficheiro_saida} ({len(novas_linhas)} linhas)")

# Executar
gerar_csv_angulos(TRAIN_PATH, TRAIN_OUT)
gerar_csv_angulos(TEST_PATH, TEST_OUT)
