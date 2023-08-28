import sys
import os
import configparser
from dotenv import load_dotenv

# Añadir el directorio que contiene el paquete
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Obtén la ruta completa al archivo .env dentro de la carpeta config
dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'config', '.env')

# Carga las variables de entorno desde el archivo .env
load_dotenv(dotenv_path)

# Configuración inicial
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '..', 'config', '.config'))

# Obtiene la ruta de ASSETS_DIR
ASSETS_DIR = config['PATHS']['ASSETS_DIR']
