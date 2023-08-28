import sys
import os
from dotenv import load_dotenv

# Añadir el directorio que contiene el paquete api-gateway al sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Obtén la ruta completa al archivo .env dentro de la carpeta config
dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'config', '.env')

# Carga las variables de entorno desde el archivo .env
load_dotenv(dotenv_path)
