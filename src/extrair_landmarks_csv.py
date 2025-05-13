import os
import cv2
import mediapipe as mp
import csv
import random

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True)
LANDMARK_COUNT = 33

DATASET_PATH = '/home/joaosousa/ProjLPI/ProjLPI/images_test'
CSV_TRAIN = '/home/joaosousa/ProjLPI/ProjLPI/shared_data/features_train.csv'
CSV_TEST = '/home/joaosousa/ProjLPI/ProjLPI/shared_data/features_test.csv'

# Cabeçalho: imagem, classe, x0, y0, z0, v0, ..., x32, y32, z32, v32
header = ['imagem', 'classe']
for i in range(LANDMARK_COUNT):
    header += [f'x{i}', f'y{i}', f'z{i}', f'v{i}']

dados_train = []
dados_test = []

for pasta_pose in os.listdir(DATASET_PATH):
    pasta_path = os.path.join(DATASET_PATH, pasta_pose)
    if not os.path.isdir(pasta_path):
        continue

    imagens = os.listdir(pasta_path)
    random.shuffle(imagens)

    split_idx = int(len(imagens) * 0.7)
    imagens_train = imagens[:split_idx]
    imagens_test = imagens[split_idx:]

    for grupo, lista in [('train', imagens_train), ('test', imagens_test)]:
        for imagem_nome in lista:
            imagem_path = os.path.join(pasta_path, imagem_nome)
            imagem = cv2.imread(imagem_path)

            if imagem is None:
                print(f"[REMOVIDA] Imagem inválida: {imagem_path}")
                os.remove(imagem_path)
                continue

            try:
                rgb = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
                resultado = pose.process(rgb)

                if not resultado.pose_landmarks:
                    print(f"[REMOVIDA] Sem landmarks: {imagem_path}")
                    os.remove(imagem_path)
                    continue

                linha = [imagem_nome, pasta_pose]
                for lm in resultado.pose_landmarks.landmark:
                    linha += [round(lm.x, 5), round(lm.y, 5), round(lm.z, 5), round(lm.visibility, 5)]

                if len(linha) != 1 + 1 + LANDMARK_COUNT * 4:
                    print(f"[AVISO] Incompleto: {imagem_path}")
                    continue

                if grupo == 'train':
                    dados_train.append(linha)
                else:
                    dados_test.append(linha)

            except Exception as e:
                print(f"[REMOVIDA] Exceção em {imagem_path}: {str(e)}")
                os.remove(imagem_path)
                continue

# Guardar CSVs
with open(CSV_TRAIN, mode='w', newline='') as f_train:
    writer = csv.writer(f_train)
    writer.writerow(header)
    writer.writerows(dados_train)

with open(CSV_TEST, mode='w', newline='') as f_test:
    writer = csv.writer(f_test)
    writer.writerow(header)
    writer.writerows(dados_test)

print(f"\n✅ Landmarks completos extraídos e guardados:")
print(f"- {CSV_TRAIN} com {len(dados_train)} amostras")
print(f"- {CSV_TEST} com {len(dados_test)} amostras")
