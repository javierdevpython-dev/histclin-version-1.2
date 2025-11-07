#!/usr/bin/env python3
"""
Script completo para crear y configurar la base de datos PostgreSQL
Este script:
1. Crea la base de datos si no existe
2. Crea todas las tablas necesarias
3. Crea el usuario administrador inicial
4. Opcionalmente crea datos de ejemplo
"""

import os
import sys
from datetime import datetime
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Importar configuración
from database_config import db_manager
from app import app, db, Usuario, Paciente, Medico, Insumo, Medicamento, HonorarioMedico, ServicioClinico, Bioanalista

def print_banner():
    """Imprimir banner"""
    print("=" * 60)
    print("🗄️  CREACIÓN DE BASE DE DATOS POSTGRESQL")
    print("=" * 60)
    print()

def check_postgresql_connection():
    """Verificar conexión básica a PostgreSQL"""
    print("📡 Verificando conexión a PostgreSQL...")
    try:
        # Intentar conectar a la base de datos 'postgres' por defecto
        import psycopg2
        temp_conn = psycopg2.connect(
            host=db_manager.host,
            port=db_manager.port,
            user=db_manager.user,
            password=db_manager.password,
            database='postgres'
        )
        temp_conn.close()
        print("✅ Conexión a PostgreSQL exitosa")
        return True
    except Exception as e:
        print(f"❌ Error al conectar a PostgreSQL: {e}")
        print("\n💡 Soluciones:")
        print("   1. Verifica que PostgreSQL esté instalado y corriendo")
        print("   2. Verifica las credenciales en el archivo .env")
        print("   3. Verifica que el usuario tenga permisos para crear bases de datos")
        return False

def create_database():
    """Crear la base de datos si no existe"""
    print("\n📦 Creando base de datos...")
    try:
        if db_manager.create_database():
            print("✅ Base de datos lista")
            return True
        else:
            print("❌ Error al crear la base de datos")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def create_tables():
    """Crear todas las tablas de la base de datos"""
    print("\n📋 Creando tablas...")
    try:
        with app.app_context():
            db.create_all()
            print("✅ Todas las tablas creadas exitosamente")
            return True
    except Exception as e:
        print(f"❌ Error al crear tablas: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_admin_user():
    """Crear usuario administrador inicial"""
    print("\n👤 Creando usuario administrador...")
    try:
        with app.app_context():
            # Verificar si ya existe un usuario admin
            admin = Usuario.query.filter_by(username='admin').first()
            if admin:
                print("⚠️  Usuario administrador ya existe")
                print(f"   Username: {admin.username}")
                print(f"   Email: {admin.email}")
                return True
            
            # Crear usuario administrador
            admin_user = Usuario(
                username='admin',
                email='admin@medisoft.com',
                password_hash=generate_password_hash('admin123'),
                rol='administrador',
                nombre_completo='Administrador del Sistema',
                activo=True
            )
            
            db.session.add(admin_user)
            db.session.commit()
            print("✅ Usuario administrador creado")
            print("   Usuario: admin")
            print("   Contraseña: admin123")
            print("   ⚠️  IMPORTANTE: Cambia la contraseña después del primer acceso")
            return True
    except Exception as e:
        print(f"❌ Error al crear usuario administrador: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_sample_data():
    """Crear datos de ejemplo"""
    print("\n📊 ¿Deseas crear datos de ejemplo? (s/n): ", end='')
    respuesta = input().lower().strip()
    
    if respuesta != 's':
        print("⏭️  Saltando creación de datos de ejemplo")
        return True
    
    print("\n📝 Creando datos de ejemplo...")
    try:
        with app.app_context():
            # Crear médicos de ejemplo
            medicos_data = [
                {
                    'dni': '12345678',
                    'nombre': 'Dr. Juan',
                    'apellido': 'Pérez',
                    'especialidad': 'Cardiología',
                    'telefono': '+58 212 123-4567',
                    'email': 'juan.perez@medisoft.com'
                },
                {
                    'dni': '23456789',
                    'nombre': 'Dra. María',
                    'apellido': 'González',
                    'especialidad': 'Pediatría',
                    'telefono': '+58 212 234-5678',
                    'email': 'maria.gonzalez@medisoft.com'
                },
                {
                    'dni': '34567890',
                    'nombre': 'Dr. Carlos',
                    'apellido': 'Rodríguez',
                    'especialidad': 'Dermatología',
                    'telefono': '+58 212 345-6789',
                    'email': 'carlos.rodriguez@medisoft.com'
                }
            ]
            
            medicos_creados = 0
            for medico_data in medicos_data:
                medico = Medico.query.filter_by(dni=medico_data['dni']).first()
                if not medico:
                    medico = Medico(**medico_data)
                    db.session.add(medico)
                    medicos_creados += 1
            
            # Crear pacientes de ejemplo
            pacientes_data = [
                {
                    'dni': '11111111',
                    'nombre': 'Ana',
                    'apellido': 'López',
                    'fecha_nacimiento': datetime.strptime('1985-03-15', '%Y-%m-%d').date(),
                    'genero': 'Femenino',
                    'telefono': '+58 212 111-1111',
                    'email': 'ana.lopez@email.com',
                    'direccion': 'Av. Principal 1234, Caracas'
                },
                {
                    'dni': '22222222',
                    'nombre': 'Roberto',
                    'apellido': 'Martínez',
                    'fecha_nacimiento': datetime.strptime('1978-07-22', '%Y-%m-%d').date(),
                    'genero': 'Masculino',
                    'telefono': '+58 212 222-2222',
                    'email': 'roberto.martinez@email.com',
                    'direccion': 'Calle Bolívar 567, Caracas'
                }
            ]
            
            pacientes_creados = 0
            for paciente_data in pacientes_data:
                paciente = Paciente.query.filter_by(dni=paciente_data['dni']).first()
                if not paciente:
                    paciente = Paciente(**paciente_data)
                    db.session.add(paciente)
                    pacientes_creados += 1
            
            # Crear insumos de ejemplo
            insumos_data = [
                {
                    'codigo': 'INS001',
                    'nombre': 'Jeringas 10ml',
                    'descripcion': 'Jeringas desechables de 10ml',
                    'stock': 100,
                    'stock_minimo': 20,
                    'precio_unitario': 2.50
                },
                {
                    'codigo': 'INS002',
                    'nombre': 'Guantes Látex M',
                    'descripcion': 'Guantes de látex talla M',
                    'stock': 200,
                    'stock_minimo': 50,
                    'precio_unitario': 1.80
                },
                {
                    'codigo': 'INS003',
                    'nombre': 'Algodón Estéril',
                    'descripcion': 'Algodón estéril 100g',
                    'stock': 50,
                    'stock_minimo': 10,
                    'precio_unitario': 5.00
                }
            ]
            
            insumos_creados = 0
            for insumo_data in insumos_data:
                insumo = Insumo.query.filter_by(codigo=insumo_data['codigo']).first()
                if not insumo:
                    insumo = Insumo(**insumo_data)
                    db.session.add(insumo)
                    insumos_creados += 1
            
            # Crear medicamentos de ejemplo
            medicamentos_data = [
                {
                    'codigo': 'MED001',
                    'nombre': 'Paracetamol 500mg',
                    'descripcion': 'Analgésico y antipirético',
                    'principio_activo': 'Paracetamol',
                    'presentacion': 'Comprimidos',
                    'stock': 150,
                    'stock_minimo': 30,
                    'precio_unitario': 0.50,
                    'fecha_vencimiento': datetime.strptime('2025-12-31', '%Y-%m-%d').date()
                },
                {
                    'codigo': 'MED002',
                    'nombre': 'Ibuprofeno 400mg',
                    'descripcion': 'Antiinflamatorio no esteroideo',
                    'principio_activo': 'Ibuprofeno',
                    'presentacion': 'Comprimidos',
                    'stock': 120,
                    'stock_minimo': 25,
                    'precio_unitario': 0.75,
                    'fecha_vencimiento': datetime.strptime('2025-10-31', '%Y-%m-%d').date()
                }
            ]
            
            medicamentos_creados = 0
            for medicamento_data in medicamentos_data:
                medicamento = Medicamento.query.filter_by(codigo=medicamento_data['codigo']).first()
                if not medicamento:
                    medicamento = Medicamento(**medicamento_data)
                    db.session.add(medicamento)
                    medicamentos_creados += 1
            
            # Crear servicios clínicos de ejemplo
            servicios_data = [
                {
                    'codigo': 'SER001',
                    'nombre': 'Consulta General',
                    'descripcion': 'Consulta médica general',
                    'precio': 50.00,
                    'categoria': 'Consultas'
                },
                {
                    'codigo': 'SER002',
                    'nombre': 'Electrocardiograma',
                    'descripcion': 'Estudio cardíaco',
                    'precio': 120.00,
                    'categoria': 'Estudios'
                },
                {
                    'codigo': 'SER003',
                    'nombre': 'Análisis de Sangre',
                    'descripcion': 'Análisis bioquímico completo',
                    'precio': 80.00,
                    'categoria': 'Laboratorio'
                }
            ]
            
            servicios_creados = 0
            for servicio_data in servicios_data:
                servicio = ServicioClinico.query.filter_by(codigo=servicio_data['codigo']).first()
                if not servicio:
                    servicio = ServicioClinico(**servicio_data)
                    db.session.add(servicio)
                    servicios_creados += 1
            
            db.session.commit()
            print("✅ Datos de ejemplo creados exitosamente")
            print(f"   - {medicos_creados} médicos")
            print(f"   - {pacientes_creados} pacientes")
            print(f"   - {insumos_creados} insumos")
            print(f"   - {medicamentos_creados} medicamentos")
            print(f"   - {servicios_creados} servicios clínicos")
            return True
    except Exception as e:
        print(f"❌ Error al crear datos de ejemplo: {e}")
        import traceback
        traceback.print_exc()
        return False

def verify_database():
    """Verificar que la base de datos esté correctamente configurada"""
    print("\n🔍 Verificando base de datos...")
    try:
        with app.app_context():
            # Verificar conexión
            db.engine.connect().close()
            print("✅ Conexión a la base de datos verificada")
            
            # Verificar usuario admin
            admin = Usuario.query.filter_by(username='admin').first()
            if admin:
                print("✅ Usuario administrador encontrado")
            else:
                print("⚠️  Usuario administrador no encontrado")
            
            # Contar tablas
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"✅ {len(tables)} tablas encontradas en la base de datos")
            
            return True
    except Exception as e:
        print(f"❌ Error al verificar base de datos: {e}")
        return False

def main():
    """Función principal"""
    print_banner()
    
    # Verificar conexión a PostgreSQL
    if not check_postgresql_connection():
        sys.exit(1)
    
    # Crear base de datos
    if not create_database():
        sys.exit(1)
    
    # Crear tablas
    if not create_tables():
        sys.exit(1)
    
    # Crear usuario administrador
    if not create_admin_user():
        sys.exit(1)
    
    # Crear datos de ejemplo (opcional)
    create_sample_data()
    
    # Verificar
    verify_database()
    
    # Resumen final
    print("\n" + "=" * 60)
    print("✅ BASE DE DATOS POSTGRESQL CREADA EXITOSAMENTE")
    print("=" * 60)
    print("\n📋 Información de conexión:")
    print(f"   Host: {db_manager.host}")
    print(f"   Puerto: {db_manager.port}")
    print(f"   Base de datos: {db_manager.database}")
    print(f"   Usuario: {db_manager.user}")
    print("\n🔐 Credenciales de acceso a la aplicación:")
    print("   Usuario: admin")
    print("   Contraseña: admin123")
    print("   ⚠️  IMPORTANTE: Cambia la contraseña después del primer acceso")
    print("\n🚀 Próximos pasos:")
    print("   1. Ejecuta: python app.py")
    print("   2. Accede a: http://localhost:5000")
    print("   3. Inicia sesión con las credenciales de arriba")
    print("=" * 60)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Proceso cancelado por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

