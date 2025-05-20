
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from src.predict_pose import classificar_pose

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/classificar_pose', methods=['POST'])
def classificar_pose_api():
    if 'imagem' not in request.files:
        return jsonify({'erro': 'Nenhuma imagem enviada'}), 400

    file = request.files['imagem']
    if file.filename == '':
        return jsonify({'erro': 'Nome de ficheiro vazio'}), 400

    filename = secure_filename(file.filename)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{timestamp}_{filename}")
    file.save(filepath)

    try:
        resultado = classificar_pose(filepath)
    except Exception as e:
        os.remove(filepath)
        return jsonify({'erro': str(e)}), 500

    # Opcional: manter a imagem ou remover
    # os.remove(filepath)

    return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True, port=5002, host="0.0.0.0")
