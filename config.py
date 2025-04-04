import os
from dotenv import load_dotenv
from pathlib import Path

# Obtener la ruta del directorio actual
current_dir = Path(__file__).parent

# Cargar variables de entorno desde el archivo .env
load_dotenv(current_dir / '.env')

# Configuración de la aplicación
class Config:
    # Azure configuration
    CLIENT_ID = os.getenv('CLIENT_ID')
    REDIRECT_URI = os.getenv('REDIRECT_URI')
    TENANT_ID = os.getenv('TENANT_ID')
    KEY = os.getenv('KEY')

    @classmethod
    def validate(cls):
        """Validar que todas las variables requeridas estén presentes"""
        required_vars = ['CLIENT_ID', 'TENANT_ID', 'KEY', 'REDIRECT_URI']
        missing_vars = [var for var in required_vars if not getattr(cls, var)]
        
        if missing_vars:
            raise ValueError(
                f"Faltan las siguientes variables de entorno: {', '.join(missing_vars)}\n"
                "Por favor, asegúrate de que estén definidas en el archivo .env"
            )

# Validar la configuración al importar el módulo
Config.validate() 