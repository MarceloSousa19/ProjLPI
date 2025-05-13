import pandas as pd
import numpy as np
import os

# Caminhos
BASE_DIR = 'shared_data'
TRAIN_PATH = os.path.join(BASE_DIR, '/home/joaosousa/ProjLPI/ProjLPI/shared_data/features_train.csv')
TEST_PATH = os.path.join(BASE_DIR, '/home/joaosousa/ProjLPI/ProjLPI/shared_data/features_test.csv')
TRAIN_OUT = os.path.join(BASE_DIR, '/home/joaosousa/ProjLPI/ProjLPI/shared_data/features_train_normalized.csv')
TEST_OUT = os.path.join(BASE_DIR, '/home/joaosousa/ProjLPI/ProjLPI/shared_data/features_test_normalized.csv')

# Indices dos landmarks
LANDMARK_COUNT = 33
NOSE_IDX = 0
L_HIP_IDX = 23
R_HIP_IDX = 24

# Função para normalizar um conjunto de landmarks
def normalizar_linha(linha):
    # Extrair coordenadas (ignorando imagem e classe)
    coords = linha[2:]  # x0,y0,z0,v0,...
    coords = np.array(coords, dtype=np.float32).reshape((LANDMARK_COUNT, 4))  # 33x4

    # Calcular ponto central (mid_hip)
    mid_hip = (coords[L_HIP_IDX][:3] + coords[R_HIP_IDX][:3]) / 2  # [x,y,z]

    # Calcular distância para o nariz (altura virtual do corpo)
    nose = coords[NOSE_IDX][:3]
    scale = np.linalg.norm(nose - mid_hip)

    if scale == 0:
        return None  # evitar divisão por zero

    # Normalizar todos os landmarks (x, y, z)
    norm_coords = (coords[:, :3] - mid_hip) / scale
    norm_coords = norm_coords.flatten()  # x0,y0,z0,x1,...

    return [linha[0], linha[1]] + norm_coords.tolist()

# Processar ficheiros
def processar_csv(input_path, output_path):
    df = pd.read_csv(input_path)
    linhas_normalizadas = []

    for _, row in df.iterrows():
        linha_norm = normalizar_linha(row.tolist())
        if linha_norm:
            linhas_normalizadas.append(linha_norm)

    # Cabeçalho
    header = ['imagem', 'classe'] + [f'{coord}{i}' for i in range(LANDMARK_COUNT) for coord in ['x','y','z']]

    # Guardar novo CSV
    df_out = pd.DataFrame(linhas_normalizadas, columns=header)
    df_out.to_csv(output_path, index=False)
    print(f"✅ Guardado: {output_path} ({len(df_out)} linhas)")

# Executar
processar_csv(TRAIN_PATH, TRAIN_OUT)
processar_csv(TEST_PATH, TEST_OUT)
