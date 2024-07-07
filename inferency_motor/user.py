# app.py
from flask import Flask,jsonify, request
import os
import shutil
import base64
from image import Image, TaxonomicRoute, ImageSchema, mode_hight_velocity, mode_hight_precision
import logging

MODEL_G_PATH = '/model_g'
app = Flask(__name__)

@app.route('/user')
def hello_world():
    return 'Hello, User!'

@app.route('/sync', methods=['POST'])
def sync():
    global MODEL_G_PATH
    try:
        source_dir = "/runs"
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
    """This is the route to use hight precision mode

    Returns:
        json: json with a class Image
    """
    try:
        # Obtener los datos del JSON
        data = request.get_json()
        images = data['images']
        
        image = mode_hight_precision(images)
        
        
    
        image_schema = ImageSchema()
        image_data = image_schema.dump(image)
        response = {
                'status': 'success', 
                'message': 'Image uploaded successfully',
                'image': image_data
            }

        return jsonify(response)
    except Exception as e:
        logging.error(f'ha ocurrido un error en check taxonomic routes\nError: {str(e)}')
        return jsonify({'status': 'error', 'message': str(e)}), 500
    
   
@app.route('/user/taxonomic_route', methods=['POST'])
def chek_taxonomic_route():
    """This is the route to use hight velocity mode

    Returns:
        json: json who contains a list o class Image
    """
    try:
        # Obtener los datos del JSON
        data = request.get_json()
        image = data['image']

        # Use mode hight velocity
        results = mode_hight_velocity(image)
        
        
        if results == None:
            return jsonify({'status': 'success', 'message': 'there is no organism in the image'}), 200 
        
        # Change to json all images
        results_json = []
        image_schema = ImageSchema()
        for result in results:
            json_image = {
                'status': 'success', 
                'message': 'Image uploaded successfully',
                'image': image_schema.dump(result)
            }
            results_json.append(json_image)
        
        # create the return array
        response_array = {
            "responseImages": results_json,
            'message': 'Image uploaded successfully',
            'status': 'success'
        }
        
        return jsonify(response_array)
    except Exception as e:
        logging.error(f'ha ocurrido un error en check taxonomic route\nError: {str(e)}')
        return jsonify({'status': 'error', 'message': str(e)}), 500 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
