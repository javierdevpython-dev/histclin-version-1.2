import os
from dotenv import load_dotenv

load_dotenv()

# Detectar si estamos en Render (Render establece RENDER_EXTERNAL_URL)
IS_RENDER = os.environ.get('RENDER') == 'true' or os.environ.get('RENDER_EXTERNAL_URL') is not None
IS_PRODUCTION = os.environ.get('FLASK_ENV') == 'production' or IS_RENDER

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    # PostgreSQL configuration
    # Render proporciona DATABASE_URL automáticamente
    # Si DATABASE_URL está definida, la usa; si no, construye la URL desde variables individuales
    if os.environ.get('DATABASE_URL'):
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    else:
        # Construir URL desde variables individuales
        db_user = os.environ.get('POSTGRES_USER') or 'postgres'
        db_password = os.environ.get('POSTGRES_PASSWORD') or 'postgres'
        db_host = os.environ.get('POSTGRES_HOST') or 'localhost'
        db_port = os.environ.get('POSTGRES_PORT') or '5432'
        db_name = os.environ.get('POSTGRES_DB') or 'medisoft_db'
        SQLALCHEMY_DATABASE_URI = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuración del pool de conexiones para producción
    # Maneja reconexiones automáticas y timeouts
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 5,
        'pool_recycle': 300,  # Reciclar conexiones cada 5 minutos
        'pool_pre_ping': True,  # Verificar conexiones antes de usarlas
        'max_overflow': 10,
        'connect_args': {
            'connect_timeout': 10,
            'sslmode': 'prefer'  # Usar SSL si está disponible
        }
    }
    
    # Network configuration
    # Render usa la variable PORT automáticamente
    HOST = os.environ.get('HOST') or '0.0.0.0'
    PORT = int(os.environ.get('PORT') or 5000)
    DEBUG = os.environ.get('DEBUG', 'False' if IS_PRODUCTION else 'True').lower() == 'true'

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    HOST = os.environ.get('HOST') or '0.0.0.0'  # Render necesita 0.0.0.0

# Seleccionar configuración automáticamente
if IS_PRODUCTION:
    config = ProductionConfig
else:
    config = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'default': DevelopmentConfig
    }
