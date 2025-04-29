

import pandas as pd
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import joblib

# Paths
BASE_DIR = 'poses_dataset'
TRAIN_CSV = f'{BASE_DIR}/features_training.csv'
TEST_CSV = f'{BASE_DIR}/features_testing.csv'

# Carregar datasets
train_df = pd.read_csv(TRAIN_CSV)
test_df = pd.read_csv(TEST_CSV)

# Selecionar apenas as colunas dos ângulos
angle_cols = [
    'elbow_right', 'elbow_left',
    'shoulder_right', 'shoulder_left',
    'hip_right', 'hip_left',
    'knee_right', 'knee_left'
]

X_train = train_df[angle_cols].values
y_train = train_df['label'].values

X_test = test_df[angle_cols].values
y_test = test_df['label'].values

# Codificar labels
label_encoder = LabelEncoder()
y_train_encoded = label_encoder.fit_transform(y_train)
y_test_encoded = label_encoder.transform(y_test)

# MLP
mlp = MLPClassifier(
    hidden_layer_sizes=(256, 128, 64),  # um pouco mais pequeno (menos features)
    activation='relu',
    solver='adam',
    max_iter=1000,
    random_state=42
)

# Treinar
print("Treinar MLP (só ângulos)...")
mlp.fit(X_train, y_train_encoded)

# Avaliar
y_pred = mlp.predict(X_test)
accuracy = accuracy_score(y_test_encoded, y_pred)
print(f"Accuracy (só ângulos): {accuracy*100:.2f}%")

print("\nClassification Report:")
print(classification_report(y_test_encoded, y_pred, target_names=label_encoder.classes_))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test_encoded, y_pred))

# Guardar modelo
joblib.dump(mlp, f'{BASE_DIR}/mlp_angles.joblib')
joblib.dump(label_encoder, f'{BASE_DIR}/label_encoder_angles.joblib')
print("✓ Modelo só ângulos guardado.")
