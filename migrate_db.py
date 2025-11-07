"""
Script para migrar la base de datos con los nuevos cambios
"""
from app import app, db
from sqlalchemy import text

print("=== Migrando Base de Datos ===\n")

with app.app_context():
    try:
        # Obtener conexión a la base de datos
        connection = db.engine.connect()
        trans = connection.begin()
        
        try:
            print("Actualizando tabla Enfermera...")
            # Cambiar DNI por RIF en Enfermera
            try:
                connection.execute(text("ALTER TABLE enfermera RENAME COLUMN dni TO rif"))
                print("✓ Columna 'dni' renombrada a 'rif' en enfermera")
            except Exception as e:
                print(f"  Nota: {e}")
            
            # Agregar horario a Enfermera
            try:
                connection.execute(text("ALTER TABLE enfermera ADD COLUMN horario VARCHAR(200)"))
                print("✓ Columna 'horario' agregada a enfermera")
            except Exception as e:
                print(f"  Nota: {e}")
            
            print("\nActualizando tabla Bioanalista...")
            # Actualizar Bioanalista - cambiar nombre a rif si existe dni
            try:
                connection.execute(text("ALTER TABLE bioanalista ADD COLUMN rif VARCHAR(20) UNIQUE"))
                print("✓ Columna 'rif' agregada a bioanalista")
            except Exception as e:
                print(f"  Nota: {e}")
            
            # Agregar tipo y dirección a Bioanalista
            try:
                connection.execute(text("ALTER TABLE bioanalista ADD COLUMN tipo VARCHAR(50)"))
                print("✓ Columna 'tipo' agregada a bioanalista")
            except Exception as e:
                print(f"  Nota: {e}")
                
            try:
                connection.execute(text("ALTER TABLE bioanalista ADD COLUMN direccion TEXT"))
                print("✓ Columna 'direccion' agregada a bioanalista")
            except Exception as e:
                print(f"  Nota: {e}")
            
            print("\nActualizando tabla Emergencia...")
            # Agregar campos de vinculación a Emergencia
            try:
                connection.execute(text("ALTER TABLE emergencia ADD COLUMN tratamiento_id INTEGER"))
                print("✓ Columna 'tratamiento_id' agregada a emergencia")
            except Exception as e:
                print(f"  Nota: {e}")
                
            try:
                connection.execute(text("ALTER TABLE emergencia ADD COLUMN cirugia_id INTEGER"))
                print("✓ Columna 'cirugia_id' agregada a emergencia")
            except Exception as e:
                print(f"  Nota: {e}")
                
            try:
                connection.execute(text("ALTER TABLE emergencia ADD COLUMN hospitalizacion_id INTEGER"))
                print("✓ Columna 'hospitalizacion_id' agregada a emergencia")
            except Exception as e:
                print(f"  Nota: {e}")
            
            print("\nCreando tabla AnalisisBioanalista...")
            # Crear tabla AnalisisBioanalista
            try:
                connection.execute(text("""
                    CREATE TABLE IF NOT EXISTS analisis_bioanalista (
                        id SERIAL PRIMARY KEY,
                        bioanalista_id INTEGER NOT NULL,
                        examen_id INTEGER NOT NULL,
                        fecha_analisis TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        resultados TEXT,
                        observaciones TEXT,
                        FOREIGN KEY (bioanalista_id) REFERENCES bioanalista(id),
                        FOREIGN KEY (examen_id) REFERENCES examen(id)
                    )
                """))
                print("✓ Tabla 'analisis_bioanalista' creada")
            except Exception as e:
                print(f"  Nota: {e}")
            
            trans.commit()
        except Exception as e:
            trans.rollback()
            raise e
        finally:
            connection.close()
        
        print("\n✅ Migración completada exitosamente")
        print("\nIMPORTANTE: Si ya tienes datos en la base de datos:")
        print("- Los bioanalistas necesitarán tener un RIF asignado")
        print("- Las enfermeras ahora usan RIF en lugar de DNI")
        
    except Exception as e:
        print(f"\n❌ Error durante la migración: {e}")
        import traceback
        traceback.print_exc()
