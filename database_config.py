"""
Configuración y gestión de la base de datos PostgreSQL
Proporciona un gestor de base de datos para conexiones directas con PostgreSQL
"""

import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()


class DatabaseManager:
    """Gestor de conexiones y operaciones con PostgreSQL"""
    
    def __init__(self):
        # Cargar configuración desde variables de entorno o usar valores por defecto
        self.host = os.environ.get('POSTGRES_HOST') or 'localhost'
        self.port = int(os.environ.get('POSTGRES_PORT') or 5432)
        self.user = os.environ.get('POSTGRES_USER') or 'postgres'
        self.password = os.environ.get('POSTGRES_PASSWORD') or 'postgres'
        self.database = os.environ.get('POSTGRES_DB') or 'medisoft_db'
        self.connection = None
        self.cursor = None
    
    def connect(self, database=None):
        """
        Conectar a la base de datos PostgreSQL
        
        Args:
            database: Nombre de la base de datos a conectar (opcional, usa self.database por defecto)
        
        Returns:
            bool: True si la conexión fue exitosa, False en caso contrario
        """
        try:
            db_name = database or self.database
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=db_name
            )
            self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            return True
        except psycopg2.Error as e:
            print(f"Error al conectar a PostgreSQL: {e}")
            self.connection = None
            self.cursor = None
            return False
    
    def disconnect(self):
        """Cerrar la conexión a la base de datos"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        self.connection = None
        self.cursor = None
    
    def execute_query(self, query, params=None, fetch=True):
        """
        Ejecutar una consulta SQL
        
        Args:
            query: Consulta SQL con placeholders %s
            params: Tupla o lista de parámetros para la consulta
            fetch: Si es True, retorna los resultados. Si es False, solo ejecuta (para INSERT/UPDATE/DELETE)
        
        Returns:
            Lista de diccionarios con los resultados si fetch=True, None si fetch=False
        """
        if not self.connection or self.connection.closed:
            if not self.connect():
                return None
        
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            if fetch:
                if query.strip().upper().startswith(('SELECT', 'WITH')):
                    return self.cursor.fetchall()
                else:
                    self.connection.commit()
                    return None
            else:
                self.connection.commit()
                return None
        except psycopg2.Error as e:
            self.connection.rollback()
            print(f"Error al ejecutar consulta: {e}")
            print(f"Consulta: {query}")
            print(f"Parámetros: {params}")
            raise e
    
    def create_database(self):
        """
        Crear la base de datos si no existe
        
        Returns:
            bool: True si la base de datos fue creada o ya existe, False en caso contrario
        """
        try:
            # Conectar a la base de datos 'postgres' por defecto para crear la nueva BD
            temp_conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database='postgres'
            )
            temp_conn.autocommit = True
            temp_cursor = temp_conn.cursor()
            
            # Verificar si la base de datos ya existe
            temp_cursor.execute(
                "SELECT 1 FROM pg_database WHERE datname = %s",
                (self.database,)
            )
            exists = temp_cursor.fetchone()
            
            if not exists:
                # Crear la base de datos
                temp_cursor.execute(
                    sql.SQL("CREATE DATABASE {}").format(
                        sql.Identifier(self.database)
                    )
                )
                print(f"Base de datos '{self.database}' creada exitosamente")
            else:
                print(f"La base de datos '{self.database}' ya existe")
            
            temp_cursor.close()
            temp_conn.close()
            return True
        except psycopg2.Error as e:
            print(f"Error al crear la base de datos: {e}")
            return False
    
    def create_tables(self):
        """
        Crear las tablas necesarias en la base de datos
        Nota: Esta función crea tablas básicas. Las tablas complejas se crean mediante Flask-SQLAlchemy
        """
        if not self.connect():
            print("No se pudo conectar a la base de datos para crear tablas")
            return False
        
        try:
            # Crear tabla de usuarios si no existe (para login_flet.py)
            create_usuario_table = """
            CREATE TABLE IF NOT EXISTS usuario (
                id SERIAL PRIMARY KEY,
                username VARCHAR(80) UNIQUE NOT NULL,
                email VARCHAR(120) UNIQUE NOT NULL,
                password_hash VARCHAR(256) NOT NULL,
                rol VARCHAR(20),
                nombre_completo VARCHAR(100),
                activo BOOLEAN DEFAULT TRUE,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ultimo_acceso TIMESTAMP
            );
            """
            
            self.cursor.execute(create_usuario_table)
            self.connection.commit()
            print("Tablas básicas creadas exitosamente")
            return True
        except psycopg2.Error as e:
            self.connection.rollback()
            print(f"Error al crear tablas: {e}")
            return False
        finally:
            self.disconnect()
    
    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disconnect()


# Instancia global del gestor de base de datos
db_manager = DatabaseManager()

