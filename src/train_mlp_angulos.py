import pandas as pd
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import joblib
import os


BASE_DIR = 'ProjLPI'
SHARED_DIR = os.path.join(BASE_DIR, 'shared_data')

TRAIN_CSV = os.path.join(SHARED_DIR, 'features_train_angulos.csv')
TEST_CSV = os.path.join(SHARED_DIR, 'features_test_angulos.csv')


train_df = pd.read_csv(TRAIN_CSV)
test_df = pd.read_csv(TEST_CSV)

angle_cols = [f'ang_{i+1}' for i in range(8)]

X_train = train_df[angle_cols].values
y_train = train_df['classe'].values

X_test = test_df[angle_cols].values
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


print(" Trainning MLP model (angles only)...")
mlp.fit(X_train, y_train_encoded)


y_pred = mlp.predict(X_test)
accuracy = accuracy_score(y_test_encoded, y_pred)
print(f"\n Accuracy (só ângulos): {accuracy * 100:.2f}%")

print("\n Classification Report:")
print(classification_report(y_test_encoded, y_pred, target_names=label_encoder.classes_))

print("\n Confusion Matrix:")
print(confusion_matrix(y_test_encoded, y_pred))

# Guardar modelo
MODEL_PATH = os.path.join(SHARED_DIR, 'mlp_angles.joblib')
ENCODER_PATH = os.path.join(SHARED_DIR, 'label_encoder_angles.joblib')

joblib.dump(mlp, MODEL_PATH)
joblib.dump(label_encoder, ENCODER_PATH)

print("💾 Modelo só ângulos guardado com sucesso.")
