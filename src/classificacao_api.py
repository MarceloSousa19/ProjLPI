from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
import traceback
from datetime import datetime
from predict_pose import classificar_pose


UPLOAD_FOLDER = 'uploads'
IMAGE_FOLDER = 'images_test'
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
        os.remove(filepath)  # só apaga se a classificação for bem-sucedida
        return jsonify(resultado)
    except Exception as e:
        print(" Erro ao classificar imagem:", e)
        traceback.print_exc()
        return jsonify({'erro': str(e)}), 500


@app.route('/images/<pose>/<image>')
def serve_pose_image(pose, image):
    folder = os.path.join(IMAGE_FOLDER, pose)
    return send_from_directory(folder, image)



if __name__ == '__main__':
    app.run(debug=True, port=5002, host="192.168.1.64")
