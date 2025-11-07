#!/usr/bin/env python3
"""
Script para migrar datos de SQLite a PostgreSQL
Este script lee los datos de la base de datos SQLite y los migra a PostgreSQL

Uso:
1. Asegúrate de tener PostgreSQL instalado y corriendo
2. Configura las variables de entorno en .env para PostgreSQL
3. Ejecuta: python migrate_sqlite_to_postgres.py
"""

import os
import sys
import sqlite3
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Importar configuración de PostgreSQL
from database_config import db_manager

# Ruta a la base de datos SQLite
SQLITE_DB_PATH = os.path.join('instance', 'medisoft.db')

def get_sqlite_tables(sqlite_conn):
    """Obtener lista de todas las tablas en SQLite"""
    cursor = sqlite_conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    tables = [row[0] for row in cursor.fetchall()]
    return tables

def get_table_columns(sqlite_conn, table_name):
    """Obtener columnas de una tabla"""
    cursor = sqlite_conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    return columns

def get_table_data(sqlite_conn, table_name):
    """Obtener todos los datos de una tabla"""
    cursor = sqlite_conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    columns = [description[0] for description in cursor.description]
    rows = cursor.fetchall()
    return columns, rows

def convert_value(value, column_type):
    """Convertir valores de SQLite a PostgreSQL"""
    if value is None:
        return None
    
    # Convertir tipos de fecha/hora
    if 'TIMESTAMP' in column_type.upper() or 'DATETIME' in column_type.upper():
        if isinstance(value, str):
            try:
                # Intentar parsear diferentes formatos de fecha
                return datetime.fromisoformat(value.replace('Z', '+00:00'))
            except:
                return value
        return value
    
    # Convertir booleanos
    if isinstance(value, bool):
        return value
    if isinstance(value, int) and column_type.upper() == 'BOOLEAN':
        return bool(value)
    
    return value

def migrate_table(sqlite_conn, table_name, pg_conn, pg_cursor):
    """Migrar una tabla completa de SQLite a PostgreSQL"""
    print(f"\nMigrando tabla: {table_name}")
    
    try:
        # Obtener datos de SQLite
        columns, rows = get_table_data(sqlite_conn, table_name)
        
        if not rows:
            print(f"  ⚠ Tabla {table_name} está vacía, saltando...")
            return True
        
        print(f"  📊 Encontrados {len(rows)} registros")
        
        # Construir query de inserción
        placeholders = ', '.join(['%s'] * len(columns))
        column_names = ', '.join([f'"{col}"' for col in columns])
        insert_query = f'INSERT INTO "{table_name}" ({column_names}) VALUES ({placeholders}) ON CONFLICT DO NOTHING'
        
        # Migrar datos
        migrated = 0
        for row in rows:
            try:
                # Convertir valores si es necesario
                converted_row = [convert_value(val, 'TEXT') for val in row]
                pg_cursor.execute(insert_query, converted_row)
                migrated += 1
            except Exception as e:
                print(f"  ⚠ Error al migrar registro: {e}")
                print(f"     Datos: {row[:3]}...")  # Mostrar primeros 3 valores
                continue
        
        pg_conn.commit()
        print(f"  ✅ {migrated} registros migrados exitosamente")
        return True
        
    except Exception as e:
        print(f"  ❌ Error al migrar tabla {table_name}: {e}")
        pg_conn.rollback()
        return False

def check_postgresql_tables(pg_conn, pg_cursor):
    """Verificar que las tablas existan en PostgreSQL"""
    pg_cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
    """)
    tables = [row[0] for row in pg_cursor.fetchall()]
    return tables

def main():
    """Función principal de migración"""
    print("=" * 60)
    print("🔄 MIGRACIÓN DE SQLITE A POSTGRESQL")
    print("=" * 60)
    print()
    
    # Verificar que existe la base de datos SQLite
    if not os.path.exists(SQLITE_DB_PATH):
        print(f"❌ Error: No se encontró la base de datos SQLite en {SQLITE_DB_PATH}")
        print("   Asegúrate de que el archivo existe antes de migrar")
        sys.exit(1)
    
    print(f"✅ Base de datos SQLite encontrada: {SQLITE_DB_PATH}")
    
    # Conectar a SQLite
    try:
        sqlite_conn = sqlite3.connect(SQLITE_DB_PATH)
        print("✅ Conectado a SQLite")
    except Exception as e:
        print(f"❌ Error al conectar a SQLite: {e}")
        sys.exit(1)
    
    # Conectar a PostgreSQL
    if not db_manager.connect():
        print("❌ Error: No se pudo conectar a PostgreSQL")
        print("   Verifica las credenciales en el archivo .env")
        sqlite_conn.close()
        sys.exit(1)
    
    print("✅ Conectado a PostgreSQL")
    
    # Crear tablas en PostgreSQL si no existen
    print("\n📋 Verificando tablas en PostgreSQL...")
    try:
        from app import app, db
        with app.app_context():
            db.create_all()
            print("✅ Tablas verificadas/creadas en PostgreSQL")
    except Exception as e:
        print(f"⚠️  Advertencia al crear tablas: {e}")
        print("   Continuando con la migración...")
    
    # Obtener lista de tablas de SQLite
    sqlite_tables = get_sqlite_tables(sqlite_conn)
    print(f"\n📊 Tablas encontradas en SQLite: {len(sqlite_tables)}")
    for table in sqlite_tables:
        print(f"   - {table}")
    
    # Verificar tablas en PostgreSQL
    pg_tables = check_postgresql_tables(db_manager.connection, db_manager.cursor)
    print(f"\n📊 Tablas en PostgreSQL: {len(pg_tables)}")
    
    # Confirmar migración
    print("\n" + "=" * 60)
    print("⚠️  ADVERTENCIA:")
    print("   Este proceso migrará todos los datos de SQLite a PostgreSQL.")
    print("   Los datos existentes en PostgreSQL NO serán eliminados,")
    print("   pero pueden haber duplicados si ya existen.")
    print("=" * 60)
    print("\n¿Deseas continuar? (s/n): ", end='')
    
    respuesta = input().lower().strip()
    if respuesta != 's':
        print("Migración cancelada")
        sqlite_conn.close()
        db_manager.disconnect()
        sys.exit(0)
    
    # Migrar cada tabla
    print("\n🚀 Iniciando migración...")
    print("=" * 60)
    
    success_count = 0
    error_count = 0
    
    for table in sqlite_tables:
        if migrate_table(sqlite_conn, table, db_manager.connection, db_manager.cursor):
            success_count += 1
        else:
            error_count += 1
    
    # Cerrar conexiones
    sqlite_conn.close()
    db_manager.disconnect()
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE MIGRACIÓN")
    print("=" * 60)
    print(f"✅ Tablas migradas exitosamente: {success_count}")
    if error_count > 0:
        print(f"❌ Tablas con errores: {error_count}")
    print("\n✅ Migración completada")
    print("\n📋 Próximos pasos:")
    print("1. Verifica los datos en PostgreSQL")
    print("2. Prueba la aplicación con la nueva base de datos")
    print("3. Una vez verificado, puedes hacer backup de la base SQLite")
    print("=" * 60)

if __name__ == '__main__':
    main()

