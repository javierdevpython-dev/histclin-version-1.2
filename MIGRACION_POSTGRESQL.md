# Guía de Migración de SQLite a PostgreSQL

Esta guía te ayudará a migrar tu proyecto de SQLite a PostgreSQL.

## Prerrequisitos

1. **PostgreSQL instalado y corriendo**
   - Windows: Descarga desde [postgresql.org](https://www.postgresql.org/download/windows/)
   - Linux: `sudo apt-get install postgresql postgresql-contrib`
   - macOS: `brew install postgresql`

2. **Python 3.8 o superior**

3. **Dependencias de Python instaladas**
   ```bash
   pip install -r requirements.txt
   ```

## Paso 1: Configurar PostgreSQL

1. **Crear una base de datos en PostgreSQL:**
   ```sql
   CREATE DATABASE medisoft_db;
   ```

2. **Crear un usuario (opcional, puedes usar el usuario postgres por defecto):**
   ```sql
   CREATE USER medisoft_user WITH PASSWORD 'tu_password';
   GRANT ALL PRIVILEGES ON DATABASE medisoft_db TO medisoft_user;
   ```

## Paso 2: Configurar Variables de Entorno

1. **Crear archivo `.env`** (si no existe):
   ```bash
   cp env_example.txt .env
   ```

2. **Editar el archivo `.env`** con tus credenciales de PostgreSQL:
   ```env
   # Configuración de la aplicación
   SECRET_KEY=tu_clave_secreta_muy_segura_cambiar_en_produccion
   FLASK_ENV=development

   # Configuración de PostgreSQL
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=tu_password
   POSTGRES_DB=medisoft_db

   # URL de la base de datos
   DATABASE_URL=postgresql://postgres:tu_password@localhost:5432/medisoft_db
   ```

## Paso 3: Inicializar la Base de Datos PostgreSQL

Ejecuta el script de inicialización para crear las tablas:

```bash
python init_db.py
```

Este script:
- Crea todas las tablas necesarias
- Crea un usuario administrador por defecto (admin/admin123)
- Opcionalmente crea datos de ejemplo

## Paso 4: Migrar Datos de SQLite a PostgreSQL

Si tienes datos existentes en SQLite que quieres migrar:

1. **Asegúrate de que la base de datos SQLite existe:**
   - Debe estar en `instance/medisoft.db`

2. **Ejecuta el script de migración:**
   ```bash
   python migrate_sqlite_to_postgres.py
   ```

3. **El script:**
   - Lee todos los datos de SQLite
   - Los migra a PostgreSQL
   - Maneja conflictos automáticamente (no duplica datos)
   - Muestra un resumen de la migración

## Paso 5: Verificar la Migración

1. **Verificar la conexión:**
   ```bash
   python check_db.py
   ```

2. **Iniciar la aplicación:**
   ```bash
   python app.py
   ```

3. **Acceder a la aplicación:**
   - URL: http://localhost:5000
   - Usuario: admin
   - Contraseña: admin123

## Cambios Realizados

### Archivos Actualizados

1. **`config.py`**: Configurado para usar PostgreSQL exclusivamente
2. **`database_config.py`**: Gestor de conexiones PostgreSQL
3. **`migrate_db.py`**: Actualizado para usar sintaxis PostgreSQL (SERIAL en lugar de AUTOINCREMENT, TIMESTAMP en lugar de DATETIME)

### Nuevos Archivos

1. **`migrate_sqlite_to_postgres.py`**: Script para migrar datos de SQLite a PostgreSQL

## Diferencias entre SQLite y PostgreSQL

### Sintaxis SQL

| SQLite | PostgreSQL |
|--------|------------|
| `INTEGER PRIMARY KEY AUTOINCREMENT` | `SERIAL PRIMARY KEY` |
| `DATETIME` | `TIMESTAMP` |
| `TEXT` | `TEXT` (igual) |
| `INTEGER` | `INTEGER` (igual) |

### Características

- **PostgreSQL** es más robusto para producción
- **PostgreSQL** soporta transacciones más complejas
- **PostgreSQL** tiene mejor rendimiento con grandes volúmenes de datos
- **PostgreSQL** soporta usuarios y permisos más granulares

## Solución de Problemas

### Error: "No se pudo conectar a PostgreSQL"

1. Verifica que PostgreSQL esté corriendo:
   ```bash
   # Windows
   # Verifica en Servicios de Windows
   
   # Linux/macOS
   sudo systemctl status postgresql
   ```

2. Verifica las credenciales en `.env`

3. Verifica que la base de datos exista:
   ```sql
   \l  -- Listar bases de datos
   ```

### Error: "psycopg2 no está instalado"

```bash
pip install psycopg2-binary
```

### Error durante la migración de datos

- El script maneja errores por tabla, así que algunas tablas pueden migrarse aunque otras fallen
- Revisa los mensajes de error para identificar problemas específicos
- Algunos tipos de datos pueden necesitar conversión manual

## Notas Importantes

1. **Backup**: Siempre haz backup de tu base de datos SQLite antes de migrar
2. **Pruebas**: Prueba la aplicación después de la migración antes de eliminar SQLite
3. **Producción**: En producción, considera usar un usuario de base de datos dedicado con permisos limitados
4. **Seguridad**: Cambia las credenciales por defecto después de la primera configuración

## Soporte

Si encuentras problemas durante la migración:
1. Revisa los logs de error
2. Verifica que todas las dependencias estén instaladas
3. Asegúrate de que PostgreSQL esté correctamente configurado

