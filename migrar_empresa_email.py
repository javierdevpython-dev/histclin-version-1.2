"""
Script de migración para agregar columnas de email a la tabla empresa
Usa Flask-SQLAlchemy para compatibilidad con PostgreSQL
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from sqlalchemy import text

def migrar_empresa_email():
    """Agregar columnas de email a la tabla empresa si no existen"""
    with app.app_context():
        try:
            # Verificar si la tabla empresa existe
            inspector = db.inspect(db.engine)
            if 'empresa' not in inspector.get_table_names():
                print("⚠️ La tabla 'empresa' no existe. Creándola primero...")
                # La tabla se creará automáticamente si está definida en los modelos
                db.create_all()
            
            # Agregar columnas si no existen (PostgreSQL)
            columnas_a_agregar = [
                ('correo_emisor', 'VARCHAR(120)'),
                ('correo_password', 'VARCHAR(120)'),
                ('smtp_server', 'VARCHAR(120)'),
                ('smtp_port', 'VARCHAR(10)')
            ]
            
            for col_name, col_type in columnas_a_agregar:
                try:
                    # Verificar si la columna ya existe
                    result = db.session.execute(text(f"""
                        SELECT column_name 
                        FROM information_schema.columns 
                        WHERE table_name='empresa' AND column_name='{col_name}'
                    """))
                    if result.fetchone():
                        print(f"✓ La columna '{col_name}' ya existe")
                    else:
                        # Agregar la columna
                        db.session.execute(text(f"""
                            ALTER TABLE empresa ADD COLUMN {col_name} {col_type}
                        """))
                        db.session.commit()
                        print(f"✓ Columna '{col_name}' agregada exitosamente")
                except Exception as e:
                    db.session.rollback()
                    print(f"⚠️ Error al agregar columna '{col_name}': {e}")
            
            print('\n✅ Migración completada.')
            
        except Exception as e:
            db.session.rollback()
            print(f'❌ Error durante la migración: {e}')
            sys.exit(1)

if __name__ == '__main__':
    migrar_empresa_email()
