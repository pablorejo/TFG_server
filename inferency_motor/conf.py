import os


def chek_folder(folder: str):
    if not os.path.exists(folder):
        os.makedirs(folder)
    return folder

TAXONOMIC_RANKS = [
    'class',
    'order',
    'family',
    'genus',
    'acceptedScientificName'
]
PATH_MODELS = chek_folder('runs')
PATH_MODELS_TRAINED = chek_folder(os.path.join(PATH_MODELS,'classify'))

PATH_MODEL_CROP = os.path.join(PATH_MODELS,'yolo_detect.pt')
PATH_MODEL_DISCART = os.path.join(PATH_MODELS,'yolo_discard.pt')

VERBOSE = True  # If you want text to appear during executions
# Example of ANSI escape sequences for different colors
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m WARNING: '
    FAIL = '\033[91m ERROR: '
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
def warning(text: str):
    if VERBOSE:
        print(Colors.WARNING, text, Colors.ENDC)

def fail(text: str):
    print(Colors.FAIL, text, Colors.ENDC)

def info(text: str):
    if VERBOSE:
        print(Colors.OKGREEN, text, Colors.ENDC)
        
MAX_NUM_OF_CROPS = 20 # In a image only crop 5 times
types = {
    'good': 'buenas',
    'bad': 'malas'
}