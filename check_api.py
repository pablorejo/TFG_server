import base64
import requests

# Función para codificar una imagen en base64
def encode_image(image_path):
    with open(image_path, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

# Ruta de la imagen a enviar
image_path = '350564589.webp'

# Preparar los datos para enviar
data = {
    'image': encode_image(image_path)
}

# Enviar la imagen codificada en un JSON
response = requests.post('http://localhost/user/taxonomic_route', json=data)
print(response.json())

# Enviar la imagen codificada en un JSON
image_paths = []
for i in range(5):
    image_paths.append(image_path)
    
images = [encode_image(path) for path in image_paths]
data = {
    'images': images
}
response = requests.post('http://localhost/user/taxonomic_routes', json=data)

# Intentar decodificar la respuesta JSON
try:
    print(response.json())
except requests.exceptions.JSONDecodeError as e:
    print("Error decoding JSON:", e)

