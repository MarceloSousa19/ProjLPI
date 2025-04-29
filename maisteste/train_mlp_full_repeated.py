

import pandas as pd
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score
import joblib

# Carregar CSV
df = pd.read_csv('poses_dataset/features_training.csv')

# Features = landmarks + ângulos
X = df.drop(columns=['image', 'label']).values
y = df['label'].values

# Codificar labels
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Definir MLP
def build_model():
    return MLPClassifier(
        hidden_layer_sizes=(256, 128, 64),
        activation='relu',
        solver='adam',
        max_iter=1000,
        random_state=None
    )

# Repetir treino 100 vezes com splits diferentes
kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
accuracies = []

print("🧠 A treinar o MLP 100 vezes...")

for i in range(100):
    model = build_model()
    scores = []

    for train_idx, test_idx in kfold.split(X, y_encoded):
        X_train, X_test = X[train_idx], X[test_idx]
        y_train, y_test = y_encoded[train_idx], y_encoded[test_idx]

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        scores.append(acc)

    avg_acc = np.mean(scores)
    accuracies.append(avg_acc)
    print(f"🏁 Execução {i+1:03}: Accuracy média dos 5 folds = {avg_acc*100:.2f}%")

# Resultados finais
print("\n📊 Estatísticas após 100 execuções:")
print(f"→ Accuracy média: {np.mean(accuracies)*100:.2f}%")
print(f"→ Desvio padrão:  {np.std(accuracies)*100:.2f}%")

# Treinar um último modelo final com todos os dados
final_model = build_model()
final_model.fit(X, y_encoded)
joblib.dump(final_model, 'poses_dataset/mlp_pose_classifier_final.joblib')
joblib.dump(label_encoder, 'poses_dataset/label_encoder_final.joblib')
print("✓ Modelo final treinado com todos os dados e guardado.")
