# src/predict_video_api.py

from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import cv2
import numpy as np
from joblib import load
from src.extrair_features_todas import extrair_landmarks_angulo
from src.historico_individual import guardar_historico_individual

# Configuração
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Carregar modelos e codificadores
modelo = load('shared_data/mlp_pose_classifier.joblib')
label_encoder = load('shared_data/label_encoder.joblib')

# Inicializar Flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/predict', methods=['POST'])
def predict_pose():
    if 'image' not in request.files:
        return jsonify({'error': 'Nenhuma imagem enviada'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'Nome de ficheiro vazio'}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Carregar imagem
    image = cv2.imread(file_path)

    if image is None:
        return jsonify({'error': 'Erro ao ler a imagem'}), 400

    # Extrair 107 features (landmarks + ângulos)
    features = extrair_landmarks_angulo(image)

    if features is None or len(features) != 107:
        return jsonify({'error': 'Erro ao extrair landmarks ou formato inválido'}), 400

    # Prever
    probs = modelo.predict_proba([features])[0]
    predicted_index = np.argmax(probs)
    predicted_label = label_encoder.inverse_transform([predicted_index])[0]
    confidence = float(probs[predicted_index])

    # Guardar no histórico
    guardar_historico_individual(predicted_label, confidence)

    # Remover imagem após processamento
    os.remove(file_path)

    return jsonify({
        'pose': predicted_label,
        'confidence': round(confidence, 4)
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
