import pandas as pd
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import joblib
import os

# Paths
BASE_DIR = 'ProjLPI'
TRAIN_CSV = os.path.join(BASE_DIR, 'shared_data/features_train_angulos.csv')
TEST_CSV = os.path.join(BASE_DIR, 'shared_data/features_test_angulos.csv')

# Carregar datasets
train_df = pd.read_csv(TRAIN_CSV)
test_df = pd.read_csv(TEST_CSV)

# Selecionar colunas dos ângulos
angle_cols = [f'ang_{i+1}' for i in range(8)]

X_train = train_df[angle_cols].values
y_train = train_df['classe'].values

X_test = test_df[angle_cols].values
y_test = test_df['classe'].values

# Codificar labels
label_encoder = LabelEncoder()
y_train_encoded = label_encoder.fit_transform(y_train)
y_test_encoded = label_encoder.transform(y_test)

# MLP
mlp = MLPClassifier(
    hidden_layer_sizes=(256, 128, 64),
    activation='relu',
    solver='adam',
    max_iter=1000,
    random_state=42
)

# Treinar
print("🧠 A treinar o MLP (só com ângulos)...")
mlp.fit(X_train, y_train_encoded)

# Avaliar
y_pred = mlp.predict(X_test)
accuracy = accuracy_score(y_test_encoded, y_pred)
print(f"\n🎯 Accuracy (só ângulos): {accuracy * 100:.2f}%")

print("\n📊 Classification Report:")
print(classification_report(y_test_encoded, y_pred, target_names=label_encoder.classes_))

print("\n🧩 Confusion Matrix:")
print(confusion_matrix(y_test_encoded, y_pred))

# Guardar modelo
joblib.dump(mlp, os.path.join(BASE_DIR, 'mlp_angles.joblib'))
joblib.dump(label_encoder, os.path.join(BASE_DIR, 'label_encoder_angles.joblib'))
print("💾 Modelo só ângulos guardado com sucesso.")
