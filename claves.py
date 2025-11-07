import os
from flask import Flask
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
# Usar PostgreSQL en lugar de SQLite
if os.environ.get('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
else:
    # Construir URL desde variables individuales
    db_user = os.environ.get('POSTGRES_USER') or 'postgres'
    db_password = os.environ.get('POSTGRES_PASSWORD') or 'postgres'
    db_host = os.environ.get('POSTGRES_HOST') or 'localhost'
    db_port = os.environ.get('POSTGRES_PORT') or '5432'
    db_name = os.environ.get('POSTGRES_DB') or 'medisoft_db'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar DB
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

# Modelo de ejemplo (ajusta según tu modelo real)
class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(256))
    rol = db.Column(db.String(20))
    nombre_completo = db.Column(db.String(100))
    activo = db.Column(db.Boolean, default=True)
    fecha_registro = db.Column(db.DateTime, default=db.func.current_timestamp())
    ultimo_acceso = db.Column(db.DateTime)

with app.app_context():
    # Generar hash y SQL
    password_hash = generate_password_hash('s1p2t3')
    
    print("Hash generado:")
    print(password_hash)
    
    # Crear usuario directamente en la DB
    try:
        nuevo_usuario = Usuario(
            username='soporte',
            email='soporte@example.com',
            password_hash='s1p2t3',
            rol='full',
            nombre_completo='Usuario de Soporte Técnico',
            activo=True
        )
        
        db.session.add(nuevo_usuario)
        db.session.commit()
        print("\nUsuario 'soporte' creado exitosamente en la base de datos!")
    except Exception as e:
        print(f"\nError al crear usuario: {str(e)}")