#!/usr/bin/env python3
"""
Script para crear tablas en Render
Ejecutar desde el Shell de Render: python crear_tablas_render.py
"""

import os
import sys

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from werkzeug.security import generate_password_hash

def crear_tablas():
    """Crear todas las tablas"""
    print("=" * 60)
    print("CREANDO TABLAS EN LA BASE DE DATOS")
    print("=" * 60)
    print()
    
    try:
        with app.app_context():
            print("Creando tablas...")
            db.create_all()
            print("✅ Tablas creadas exitosamente")
            print()
            
            # Verificar que la tabla usuario existe
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            print(f"Tablas creadas: {len(tables)}")
            for table in sorted(tables):
                print(f"  - {table}")
            print()
            
            return True
    except Exception as e:
        print(f"❌ Error al crear tablas: {e}")
        import traceback
        traceback.print_exc()
        return False

def crear_usuario_admin():
    """Crear usuario administrador"""
    print("=" * 60)
    print("CREANDO USUARIO ADMINISTRADOR")
    print("=" * 60)
    print()
    
    try:
        with app.app_context():
            from app import Usuario
            
            # Verificar si ya existe
            admin = Usuario.query.filter_by(username='admin').first()
            if admin:
                print("⚠️  Usuario 'admin' ya existe")
                print(f"   Email: {admin.email}")
                return True
            
            # Crear usuario admin
            admin = Usuario(
                username='admin',
                email='admin@medisoft.com',
                password_hash=generate_password_hash('admin123'),
                rol='administrador',
                nombre_completo='Administrador del Sistema',
                activo=True
            )
            
            db.session.add(admin)
            db.session.commit()
            
            print("✅ Usuario administrador creado")
            print("   Usuario: admin")
            print("   Contraseña: admin123")
            print("   ⚠️  IMPORTANTE: Cambia la contraseña después del primer acceso")
            print()
            
            return True
    except Exception as e:
        print(f"❌ Error al crear usuario admin: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print()
    print("=" * 60)
    print("INICIALIZACIÓN DE BASE DE DATOS EN RENDER")
    print("=" * 60)
    print()
    
    # Verificar conexión
    try:
        with app.app_context():
            db.engine.connect().close()
            print("✅ Conexión a la base de datos verificada")
            print()
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        print()
        print("Verifica que:")
        print("  1. La base de datos PostgreSQL esté creada en Render")
        print("  2. La variable DATABASE_URL esté configurada correctamente")
        sys.exit(1)
    
    # Crear tablas
    if crear_tablas():
        # Crear usuario admin
        crear_usuario_admin()
        
        print("=" * 60)
        print("✅ INICIALIZACIÓN COMPLETADA")
        print("=" * 60)
        print()
        print("Ahora puedes:")
        print("  1. Acceder a tu aplicación")
        print("  2. Iniciar sesión con: admin / admin123")
        print()
    else:
        print("=" * 60)
        print("❌ ERROR EN LA INICIALIZACIÓN")
        print("=" * 60)
        sys.exit(1)

