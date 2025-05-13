import pandas as pd
import os

BASE_DIR = 'ProjLPI'

# Caminhos dos ficheiros de entrada
TRAIN_LM = os.path.join(BASE_DIR, 'shared_data/features_train_normalized.csv')
TEST_LM = os.path.join(BASE_DIR, 'shared_data/features_test_normalized.csv')
TRAIN_ANG = os.path.join(BASE_DIR, 'shared_data/features_train_angulos.csv')
TEST_ANG = os.path.join(BASE_DIR, 'shared_data/features_test_angulos.csv')

# Caminhos de saída
TRAIN_OUT = os.path.join(BASE_DIR, 'shared_data/features_train_completo.csv')
TEST_OUT = os.path.join(BASE_DIR, 'shared_data/features_test_completo.csv')

# Função para juntar por 'imagem' e 'classe'
def juntar_csvs(ficheiro_lm, ficheiro_ang, ficheiro_saida):
    df_lm = pd.read_csv(ficheiro_lm)
    df_ang = pd.read_csv(ficheiro_ang)

    # Confirmar que ambas têm imagem e classe como chaves
    df_final = pd.merge(df_lm, df_ang, on=['imagem', 'classe'], how='inner')

    df_final.to_csv(ficheiro_saida, index=False)
    print(f"✅ Ficheiro completo guardado: {ficheiro_saida} ({len(df_final)} linhas)")

# Executar junções
juntar_csvs(TRAIN_LM, TRAIN_ANG, TRAIN_OUT)
juntar_csvs(TEST_LM, TEST_ANG, TEST_OUT)
