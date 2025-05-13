import pandas as pd
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import joblib
import os

# Caminhos dos CSVs
BASE_DIR = 'ProjLPI'
TRAIN_CSV = os.path.join(BASE_DIR, 'shared_data/features_train_completo.csv')
TEST_CSV = os.path.join(BASE_DIR, 'shared_data/features_test_completo.csv')

# Carregar datasets
train_df = pd.read_csv(TRAIN_CSV)
test_df = pd.read_csv(TEST_CSV)

# Separar X (features) e y (labels)
X_train = train_df.drop(columns=['imagem', 'classe']).values
y_train = train_df['classe'].values

X_test = test_df.drop(columns=['imagem', 'classe']).values
y_test = test_df['classe'].values

# Codificar labels (string → número)
label_encoder = LabelEncoder()
y_train_encoded = label_encoder.fit_transform(y_train)
y_test_encoded = label_encoder.transform(y_test)

# Criar o MLP
mlp = MLPClassifier(
    hidden_layer_sizes=(256, 128, 64),  # 3 camadas
    activation='relu',
    solver='adam',
    max_iter=1000,
    random_state=42
)

# Treinar
print("🧠 A treinar o modelo MLP (landmarks + ângulos)...")
mlp.fit(X_train, y_train_encoded)
print("✅ Treino concluído!")

# Avaliar
y_pred = mlp.predict(X_test)

accuracy = accuracy_score(y_test_encoded, y_pred)
print(f"\n🎯 Accuracy (completo): {accuracy * 100:.2f}%")

print("\n📊 Classification Report:")
print(classification_report(y_test_encoded, y_pred, target_names=label_encoder.classes_))

print("\n🧩 Confusion Matrix:")
print(confusion_matrix(y_test_encoded, y_pred))

# Guardar modelo e label encoder
joblib.dump(mlp, os.path.join(BASE_DIR, 'mlp_pose_classifier.joblib'))
joblib.dump(label_encoder, os.path.join(BASE_DIR, 'label_encoder.joblib'))
print(f"\n💾 Modelo guardado em {BASE_DIR}/mlp_pose_classifier.joblib")
print(f"💾 LabelEncoder guardado em {BASE_DIR}/label_encoder.joblib")
