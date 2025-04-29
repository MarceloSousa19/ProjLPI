# src/train_mlp.py

import pandas as pd
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import joblib  # Para guardar o modelo

# Paths dos CSVs
BASE_DIR = 'poses_dataset'
TRAIN_CSV = f'{BASE_DIR}/features_training.csv'
TEST_CSV = f'{BASE_DIR}/features_testing.csv'

# Carregar datasets
train_df = pd.read_csv(TRAIN_CSV)
test_df = pd.read_csv(TEST_CSV)

# Separar X (features) e y (labels)
X_train = train_df.drop(columns=['image', 'label']).values
y_train = train_df['label'].values

X_test = test_df.drop(columns=['image', 'label']).values
y_test = test_df['label'].values

# Codificar labels (string → número)
label_encoder = LabelEncoder()
y_train_encoded = label_encoder.fit_transform(y_train)
y_test_encoded = label_encoder.transform(y_test)

# Criar o MLP
mlp = MLPClassifier(
    hidden_layer_sizes=(128, 64),  # 2 camadas escondidas
    activation='relu',
    solver='adam',
    max_iter=500,
    random_state=42
)

# Treinar
print("A treinar o modelo MLP...")
mlp.fit(X_train, y_train_encoded)
print("Treino concluído!")

# Avaliar
y_pred = mlp.predict(X_test)

accuracy = accuracy_score(y_test_encoded, y_pred)
print(f"Accuracy: {accuracy*100:.2f}%")

print("\nClassification Report:")
print(classification_report(y_test_encoded, y_pred, target_names=label_encoder.classes_))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test_encoded, y_pred))

# Guardar modelo e label encoder
joblib.dump(mlp, f'{BASE_DIR}/mlp_pose_classifier.joblib')
joblib.dump(label_encoder, f'{BASE_DIR}/label_encoder.joblib')
print(f"✓ Modelo guardado em {BASE_DIR}/mlp_pose_classifier.joblib")
print(f"✓ LabelEncoder guardado em {BASE_DIR}/label_encoder.joblib")
