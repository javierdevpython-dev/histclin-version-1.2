# Instrucciones para Crear la Base de Datos PostgreSQL

## Pasos Rápidos

### 1. Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```env
# Configuración de la aplicación
SECRET_KEY=tu_clave_secreta_muy_segura_cambiar_en_produccion
FLASK_ENV=development

# Configuración de PostgreSQL
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=tu_password_aqui
POSTGRES_DB=medisoft_db

# URL de la base de datos
DATABASE_URL=postgresql://postgres:tu_password_aqui@localhost:5432/medisoft_db
```

**⚠️ IMPORTANTE:** Reemplaza `tu_password_aqui` con tu contraseña real de PostgreSQL.

### 2. Asegurar que PostgreSQL esté corriendo

- **Windows:** Verifica en "Servicios de Windows" que PostgreSQL esté ejecutándose
- **Linux/macOS:** `sudo systemctl status postgresql` o `brew services list`

### 3. Ejecutar el Script de Creación

```bash
python create_postgres_db.py
```

Este script:
- ✅ Verifica la conexión a PostgreSQL
- ✅ Crea la base de datos `medisoft_db` si no existe
- ✅ Crea todas las tablas necesarias
- ✅ Crea el usuario administrador (admin/admin123)
- ✅ Opcionalmente crea datos de ejemplo

### 4. Verificar la Instalación

```bash
python check_db.py
```

### 5. Iniciar la Aplicación

```bash
python app.py
```

Luego accede a: http://localhost:5000

**Credenciales de acceso:**
- Usuario: `admin`
- Contraseña: `admin123`

⚠️ **IMPORTANTE:** Cambia la contraseña después del primer acceso.

## Solución de Problemas

### Error: "No se pudo conectar a PostgreSQL"

1. Verifica que PostgreSQL esté instalado y corriendo
2. Verifica las credenciales en el archivo `.env`
3. Verifica que el usuario tenga permisos para crear bases de datos

### Error: "psycopg2 no está instalado"

```bash
pip install psycopg2-binary
```

### Error: "La base de datos ya existe"

No es un error. El script detecta si la base de datos ya existe y continúa normalmente.

## Notas

- El script es seguro: no elimina datos existentes
- Si la base de datos ya existe, solo crea las tablas que faltan
- Si el usuario admin ya existe, no lo sobrescribe

