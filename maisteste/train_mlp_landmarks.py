

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

# Selecionar apenas as colunas dos landmarks (x, y, z)
landmark_cols = [col for col in train_df.columns if col.startswith('lm')]

X_train = train_df[landmark_cols].values
y_train = train_df['label'].values

X_test = test_df[landmark_cols].values
y_test = test_df['label'].values

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
print("Treinar MLP (só landmarks)...")
mlp.fit(X_train, y_train_encoded)

# Avaliar
y_pred = mlp.predict(X_test)
accuracy = accuracy_score(y_test_encoded, y_pred)
print(f"Accuracy (só landmarks): {accuracy*100:.2f}%")

print("\nClassification Report:")
print(classification_report(y_test_encoded, y_pred, target_names=label_encoder.classes_))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test_encoded, y_pred))

# Guardar modelo
joblib.dump(mlp, f'{BASE_DIR}/mlp_landmarks.joblib')
joblib.dump(label_encoder, f'{BASE_DIR}/label_encoder_landmarks.joblib')
print("✓ Modelo só landmarks guardado.")
