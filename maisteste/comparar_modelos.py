import pandas as pd
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import joblib
import os

BASE_DIR = 'ProjLPI'
SHARED = os.path.join(BASE_DIR, 'shared_data')

# Caminhos
paths = {
    "angulos": {
        "train": os.path.join(SHARED, "features_train_angulos.csv"),
        "test": os.path.join(SHARED, "features_test_angulos.csv")
    },
    "landmarks": {
        "train": os.path.join(SHARED, "features_train_normalized.csv"),
        "test": os.path.join(SHARED, "features_test_normalized.csv")
    },
    "completo": {
        "train": os.path.join(SHARED, "features_train_completo.csv"),
        "test": os.path.join(SHARED, "features_test_completo.csv")
    }
}

# Função para treinar e avaliar
def treinar_avaliar(nome, train_path, test_path, drop_cols):
    print(f"\n===== MODELO: {nome.upper()} =====")

    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)

    X_train = train_df.drop(columns=drop_cols).values
    y_train = train_df['classe'].values

    X_test = test_df.drop(columns=drop_cols).values
    y_test = test_df['classe'].values

    label_encoder = LabelEncoder()
    y_train_encoded = label_encoder.fit_transform(y_train)
    y_test_encoded = label_encoder.transform(y_test)

    mlp = MLPClassifier(
        hidden_layer_sizes=(256, 128, 64),
        activation='relu',
        solver='adam',
        max_iter=1000,
        random_state=42
    )

    mlp.fit(X_train, y_train_encoded)
    y_pred = mlp.predict(X_test)
    accuracy = accuracy_score(y_test_encoded, y_pred)

    print(f"✅ Accuracy: {accuracy * 100:.2f}%")
    return accuracy * 100

# Comparar os 3 modelos
acc_angulos = treinar_avaliar("angulos", paths["angulos"]["train"], paths["angulos"]["test"], ['imagem', 'classe'])
acc_landmarks = treinar_avaliar("landmarks", paths["landmarks"]["train"], paths["landmarks"]["test"], ['imagem', 'classe'])
acc_completo = treinar_avaliar("completo", paths["completo"]["train"], paths["completo"]["test"], ['imagem', 'classe'])

# Resultados finais
print("\n=== Comparação Final ===")
print(f"🔹 Só Ângulos:           {acc_angulos:.2f}%")
print(f"🔹 Só Landmarks:         {acc_landmarks:.2f}%")
print(f"🔹 Completo (107 feats): {acc_completo:.2f}%")

# (Opcional) Plot com matplotlib
try:
    import matplotlib.pyplot as plt
    plt.bar(['Ângulos', 'Landmarks', 'Completo'], [acc_angulos, acc_landmarks, acc_completo], color=['#f39c12', '#3498db', '#2ecc71'])
    plt.ylabel('Accuracy (%)')
    plt.title('Comparação de Modelos MLP')
    plt.ylim(0, 100)
    plt.grid(True, axis='y')
    plt.show()
except ImportError:
    print("\nℹ️ matplotlib não está instalado. Corre `pip install matplotlib` para ver gráfico.")
