from marshmallow import Schema, fields
import base64
from ultralytics import YOLO
from conf import *
import cv2

class TaxonomicRoute:
    clase = None
    conf_clase = None

    orden = None
    conf_orden = None

    familia = None
    conf_familia = None

    genero = None
    conf_genero = None

    especie = None
    conf_especie = None
    
    def __init__(
        self, 
        clase=None,
        conf_clase=None,
        orden=None,
        conf_orden=None,
        familia=None,
        conf_familia=None,
        genero=None,
        conf_genero=None,
        especie=None,
        conf_especie=None,
    ):
        self.clase = clase 
        self.conf_clase = conf_clase 

        self.orden = orden 
        self.conf_orden = conf_orden 

        self.familia = familia 
        self.conf_familia = conf_familia 

        self.genero = genero 
        self.conf_genero = conf_genero 

        self.especie = especie 
        self.conf_especie = conf_especie 
    
    def set_taxon(self,taxon_name,name, conf):
        if taxon_name == TAXONOMIC_RANKS[0]:
            self.clase = name
            self.conf_clase = conf
        elif taxon_name == TAXONOMIC_RANKS[1]:
            self.orden = name
            self.conf_orden = conf
        elif taxon_name == TAXONOMIC_RANKS[2]:
            self.familia = name
            self.conf_familia = conf
        elif taxon_name == TAXONOMIC_RANKS[3]:
            self.genero = name
            self.conf_genero = conf
        elif taxon_name == TAXONOMIC_RANKS[4]:
            self.especie = name
            self.conf_especie = conf
            
    def get_global_conf(self):
        return self.conf_clase*self.conf_orden*self.conf_familia*self.conf_genero*self.conf_especie    
    
    def merge_taxonomic_route(self,taxonomic_route):
        taxonomic_route = TaxonomicRoute(taxonomic_route)
        self.conf_clase = (self.conf_clase+taxonomic_route.conf_clase)/2
        self.conf_orden = (self.conf_orden+taxonomic_route.conf_orden)/2
        self.conf_familia = (self.conf_familia+taxonomic_route.conf_familia)/2
        self.conf_genero = (self.conf_genero+taxonomic_route.conf_genero)/2
        self.conf_especie = (self.conf_especie+taxonomic_route.conf_especie)/2
        
class Image:
    def __init__(self,
            images= [],
            taxonomic_rank_top1 = None,
            taxonomic_rank_top2 = None,
            taxonomic_rank_top3 = None,
            taxonomic_rank_top4 = None,
            taxonomic_rank_top5 = None
        ):
        self.images = images
        self.taxonomic_rank_top1 = taxonomic_rank_top1
        self.taxonomic_rank_top2 = taxonomic_rank_top2
        self.taxonomic_rank_top3 = taxonomic_rank_top3
        self.taxonomic_rank_top4 = taxonomic_rank_top4
        self.taxonomic_rank_top5 = taxonomic_rank_top5
        
    def set_taxonomic_routes(self, taxonomic_routes):
        self.taxonomic_rank_top1 = taxonomic_routes[0]
        self.taxonomic_rank_top2 = taxonomic_routes[1]
        self.taxonomic_rank_top3 = taxonomic_routes[2]
        self.taxonomic_rank_top4 = taxonomic_routes[3]
        self.taxonomic_rank_top5 = taxonomic_routes[4]
         
# Definir los esquemas de marshmallow
class TaxonomicRouteSchema(Schema):
    clase = fields.Str()
    conf_clase = fields.Float()
    orden = fields.Str()
    conf_orden = fields.Float()
    familia = fields.Str()
    conf_familia = fields.Float()
    genero = fields.Str()
    conf_genero = fields.Float()
    especie = fields.Str()
    conf_especie = fields.Float()

class ImageSchema(Schema):
    images = fields.List(fields.Str())
    taxonomic_rank_top1 = fields.Nested(TaxonomicRouteSchema)
    taxonomic_rank_top2 = fields.Nested(TaxonomicRouteSchema)
    taxonomic_rank_top3 = fields.Nested(TaxonomicRouteSchema)
    taxonomic_rank_top4 = fields.Nested(TaxonomicRouteSchema)
    taxonomic_rank_top5 = fields.Nested(TaxonomicRouteSchema)
# Fin Definir los esquemas de marshmallow 

def preditc_taxon(image,model,taxonomic_routes,taxon_name, one_taxonomic_route = False):
    results = model.predict(image,verbose=False,device='cpu')
    
    # Assuming `results` is a list of `Results` objects
    for result in results:
        # Access bounding boxes, confidences, and classes
        probs = result.probs  # Probs object for classification outputs

        top5_confs = probs.top5conf
        top5_class_indexs = probs.top5
        names = result.names
        
            
        if one_taxonomic_route:
            taxon = names[top5_class_indexs[0]]
            taxonomic_routes[0].set_taxon(taxon_name,taxon,float(top5_confs[0]))
        else:
            index_route = 0
            for conf,index in zip(top5_confs,top5_class_indexs):
                taxon = names[index]
                taxonomic_routes[index_route].set_taxon(taxon_name,taxon,float(conf))
                index_route += 1
            
        return names[probs.top1]

def predict_image(image, one_taxonomic_route = False):
    if one_taxonomic_route:
        taxonomic_route_top1 = TaxonomicRoute()
        taxonomic_routes = [taxonomic_route_top1]
    else:
        taxonomic_route_top1 = TaxonomicRoute()
        taxonomic_route_top2 = TaxonomicRoute()
        taxonomic_route_top3 = TaxonomicRoute()
        taxonomic_route_top4 = TaxonomicRoute()
        taxonomic_route_top5 = TaxonomicRoute()
        taxonomic_routes = [taxonomic_route_top1,
                            taxonomic_route_top2,
                            taxonomic_route_top3,
                            taxonomic_route_top4,
                            taxonomic_route_top5]
        
        
    folder = os.path.join(PATH_MODELS_TRAINED,"model_g")
    model = YOLO(os.path.join(folder,"model_g","weights",'best.pt'))
    
    init = True
    for index,taxon_name in enumerate(TAXONOMIC_RANKS):
        taxon = preditc_taxon(image,model,taxonomic_routes,taxon_name,one_taxonomic_route)
        init = False
        if not init and index < len(TAXONOMIC_RANKS):
            name_model = f"{taxon_name}_{taxon}"
            folder = os.path.join(folder,name_model)
            
            yolo_model = os.path.join(folder,name_model,"weights",'best.pt')
            if os.path.exists(yolo_model):
                model = YOLO(yolo_model)
            else:
                break
            
    return taxonomic_routes

def predic_image_mode_precision(imgages):
    def calc_global_conf(routes):
        conf = 0
        for route in routes:
            conf += route.get_global_conf()
            
    def merge_taxonomic_routes(routes):
        new_routes = []
        for route in routes:
            for route_2 in route[1:]:
                route[0].merge_taxonomic_route(route_2)
            new_routes.append(route[0])
        return new_routes
                
    predicted_images = {}
    for image in imgages:
        predict_image_routes = predict_image(image,one_taxonomic_route=True)
        route_top1 = predict_image_routes[0]
        if route_top1.especie in predicted_images:
            
            predicted_images[route_top1.especie].apend(route_top1) 
        else:
            predicted_images[route_top1.especie] = [route_top1]
    
    sorted_routes = sorted(predicted_images.items(), key=lambda routes: calc_global_conf(routes), reverse=True)
    routes = merge_taxonomic_routes(sorted_routes)
    return routes
    
def image_to_base64(image_path):
    # Abre la imagen en modo binario
    with open(image_path, "rb") as image_file:
        # Lee el contenido de la imagen
        image_data = image_file.read()
        # Codifica el contenido de la imagen en base64
        encoded_image = base64.b64encode(image_data)
        # Convierte el resultado a una cadena de texto
        base64_string = encoded_image.decode("utf-8")
    return base64_string

def base64_to_image(base64_string, output_path):
    # Decodifica la cadena base64 a datos binarios
    image_data = base64.b64decode(base64_string)
    # Escribe los datos binarios en un archivo
    with open(output_path, "wb") as image_file:
        image_file.write(image_data)

def crop_images(src_img: str, model_to_crop: YOLO , model_to_discard: YOLO, delete_original: bool = True):
    """
    This function crops images based on an AI model.
    
    Args:
    src_img: Path to the image.
    model: Model for detection.
    
    Returns: An array with the paths of the cropped images.
    """
    # from conf import DETECT_MODEL_PATH,chek_model, info, warning, fail,VERBOSE
    image = cv2.imread(src_img)
    if image is None:
        info(f"Error reading image: {src_img}")
        return []

    try:
        results = model_to_crop(image, verbose=VERBOSE, device='cpu')
        base_name, _ = os.path.splitext(src_img)
        number = 0
        paths = []
        final = False
        for result in results:
            # Get all bounding boxes
            boxes = result.boxes

            for box in boxes:
                if bool(box.conf > 0.6):
                    # Extract the bounding box coordinates, converted to integers
                    x_min, y_min, x_max, y_max = map(int, box.xyxy[0])
                    
                    # Crop the image using the coordinates
                    cropped_img = image[y_min:y_max, x_min:x_max]

                    # Save the cropped image
                    cropped_img_path = f'{base_name}_cropped_{number}.jpg'
                    cv2.imwrite(cropped_img_path, cropped_img)

                    
                    if discard_bad_image(cropped_img_path, model_to_discard):
                        number += 1
                        
                        paths.append(cropped_img_path)
                        if (len(paths) == MAX_NUM_OF_CROPS):
                            final = True
                            break
                        info(f'Cropped image saved at: {cropped_img_path}')
                    else:
                        os.remove(cropped_img_path)
            if final:
                break

    except Exception as e:
        warning(f"Error processing image {src_img}: {str(e)}")
        return []

    finally:
        del image
        if delete_original:
            os.remove(src_img)
        else:
            paths.append(src_img)
        return paths

def discard_bad_image(img_path,model_to_discard, ask=False, confidence=0.90):
    """Discards images that are not useful for the project according to the model already trained by YOLO
    
    Args:
    img_path: The path to the image to predict
    ask: Whether to ask if confidence is less than 85%, default is False
    confidence: The confidence level you want the model to have between (0,1), default is 0.85
    
    Returns: True if the image is good, False if it is bad or not a file"""
    # from conf import types, info, warning, fail, VERBOSE
    try:
        # Make a prediction on the image
        results = model_to_discard.predict(img_path, verbose=VERBOSE, device='cpu')
        
        for result in results:
            probs = result.probs  # Probs object for classification outputs
            top1_class_index = probs.top1
            top1_confidence = probs.top1conf

            if result.names[top1_class_index] == types['bad']:
                if os.path.isfile(img_path) or os.path.islink(img_path):
                    if top1_confidence < confidence and ask:
                        with Image.open(img_path) as image:
                            image.show()
                            print(f"Most probable class: {result.names[top1_class_index]} with confidence {top1_confidence}\n")
                            response = input('Do you want to delete the image? (y/n)\n')
                            if response.lower() == 'y':
                                os.remove(img_path)
                                info("You indicated the image is bad")
                                return False
                            else: 
                                info("You indicated the image is good")
                                return True
                    else: 
                        os.remove(img_path)
                        warning("The image is bad")
                        return False
                else:
                    fail("The image is not a file") 
                    return False
            else: 
                info("The image is good")
                return True
    except NameError as e:
        warning(f"The discard model does not exist, so return true: {e}")
        return True
    except Exception as e:
        warning(f"{e}")
        return True
    
def mode_hight_velocity(image64):
    """This is funtion tu use mode hight precision in one image
    this funtion is used check all routes of all organism in one image  

    Args:
        image (base64): this is a image in base 64
    """
    # Convert base 64 to jpg image
    image_path = 'image.jpg'
    base64_to_image(image64,image_path)
    
    # here we will check if the image is good.
    model_to_discard = YOLO(PATH_MODEL_DISCART)
    if discard_bad_image(image_path,model_to_discard=model_to_discard):
        
        # Now we will go to detect more animals in the image
        model_to_crop = YOLO(PATH_MODEL_CROP)
        paths = crop_images(src_img=image_path,model_to_crop=model_to_crop,model_to_discard=model_to_discard)

        images_predicted = []
        # Analize image per image independent
        for path_image in paths:
            image = Image()
            taxonomic_routes = predict_image(path_image)
            image.set_taxonomic_routes(taxonomic_routes)
            image.images = [image_to_base64(path_image)]
            images_predicted.append(image)
        paths.append(image_path)
        for path in paths:
            if os.path.exists(path):
                os.remove(path)
        del paths
        return images_predicted
    else:
        return None
    
def mode_hight_precision(images):
    """This is the funtion to use in server to use mode precision 

    Args:
        images (list(image64)): a list in array that contains image64.
    """
    
    # change to norma image
    images_path = []
    for i,image in enumerate(images):
        image_path = f"image_{i}.jpg"
        base64_to_image(image,image_path)
        images_path.append(images_path)
    
    # now check all images
    correct_images_path = []
    model_to_discard = YOLO(PATH_MODEL_DISCART)
    for image_path in images_path:
        if discard_bad_image(image_path,model_to_discard):
            correct_images_path.append(image_path)
    del images_path
    
    # Use funtion mode hight precision
    routes = predic_image_mode_precision(correct_images_path)
    
    image = Image()
    image.set_taxonomic_routes(routes)
    for image_path in images_path:
        image_64 = image_to_base64(image_path)
        image.images.append(image_64)
    
    return image    
        
    
    
    
if __name__ == "__main__":
    images_rapid = ['350564589_2.webp','image copy.png']
    image_path_1 = 'image_2.png'
    image_path_2 = 'image.png'
    
    image_64 = image_to_base64(image_path_1)
    
    json =  mode_hight_velocity(image64=image_64)
    print('fin')
    