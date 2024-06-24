# app.py
from flask import Flask,jsonify, request
import os
import shutil
import base64

MODEL_G_PATH = '/model_g'
app = Flask(__name__)

@app.route('/user')
def hello_world():
    return 'Hello, User!'

@app.route('/sync', methods=['POST'])
def sync():
    global MODEL_G_PATH
    try:
        source_dir = "/clasify_model"
        dest_dir = MODEL_G_PATH  # Cambia esto a la ubicación deseada dentro del contenedor

        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        for filename in os.listdir(source_dir):
            source_file = os.path.join(source_dir, filename)
            dest_file = os.path.join(dest_dir, filename)
            if os.path.isfile(source_file):
                shutil.copy2(source_file, dest_file)
                
        return jsonify({"sync": "success"})
    except Exception as e:
        return jsonify({"sync": "failed", "error": str(e)}), 500

@app.route('/user/check_sync')  
def check_sync():
    global MODEL_G_PATH
    try:
        # Listar todos los elementos en el directorio
        files = os.listdir(MODEL_G_PATH)
        str_return_files = ""

        # Filtrar solo los archivos
        for file in files:
            file_path = os.path.join(MODEL_G_PATH, file)
            if os.path.isfile(file_path):
                with open(file_path, 'r') as read_file:
                    str_return_files += f"{file}: {read_file.readline()}\n"
        
        return jsonify({"sync": str_return_files})
    
    except FileNotFoundError:
        return jsonify({"error": f"Directory {MODEL_G_PATH} does not exist."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

    
@app.route('/user/taxonomic_routes', methods=['POST'])
def chek_taxonomic_routes():
    try:
        # Obtener los datos del JSON
        data = request.get_json()
        images = data['images']
        
        saved_files = []

        # Procesar cada imagen codificada en base64
        for idx, image_data in enumerate(images):
            image_base64 = image_data['image']
            image_bytes = base64.b64decode(image_base64)
            saved_files.append(idx)

        return jsonify({'status': 'success', 'saved_files': saved_files})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
   
@app.route('/user/taxonomic_route', methods=['POST'])
def chek_taxonomic_route():
    try:
        # Obtener los datos del JSON
        data = request.get_json()
        image = data['image']

        # Decodificar la imagen base64
        image_bytes = base64.b64decode(image)
        
        return jsonify({'status': 'success', 'message': 'Image uploaded successfully'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
