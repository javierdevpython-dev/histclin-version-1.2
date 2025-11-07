# 🗄️ Guía Completa: Instalar Base de Datos PostgreSQL

## 📋 Paso 1: Instalar PostgreSQL

### Opción A: Descargar e Instalar (Recomendado)

1. **Descarga PostgreSQL:**
   - Ve a: https://www.postgresql.org/download/windows/
   - O directamente: https://www.enterprisedb.com/downloads/postgres-postgresql-downloads
   - Descarga la versión más reciente (ej: PostgreSQL 15 o 16)

2. **Instala PostgreSQL:**
   - Ejecuta el instalador descargado
   - Durante la instalación:
     - ✅ Marca "PostgreSQL Server"
     - ✅ Marca "Command Line Tools"
     - ✅ Marca "pgAdmin 4" (interfaz gráfica, opcional pero útil)
   - **IMPORTANTE:** Anota la contraseña que configures para el usuario `postgres`
   - Puerto: Deja el predeterminado (5432)
   - Locale: Deja el predeterminado

3. **Verifica la instalación:**
   - Abre "Servicios de Windows" (Win + R → `services.msc`)
   - Busca "postgresql" - debería estar "En ejecución"

### Opción B: Instalar con Chocolatey (si lo tienes)

```powershell
choco install postgresql
```

### Opción C: Instalar con Winget (Windows 10/11)

```powershell
winget install PostgreSQL.PostgreSQL
```

## 📝 Paso 2: Configurar Variables de Entorno

1. **Crea el archivo `.env`** en la raíz del proyecto:

```env
# Configuración de la aplicación
SECRET_KEY=tu_clave_secreta_muy_segura_cambiar_en_produccion
FLASK_ENV=development

# Configuración de PostgreSQL
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=TU_CONTRASEÑA_DE_POSTGRES
POSTGRES_DB=medisoft_db

# URL de la base de datos
DATABASE_URL=postgresql://postgres:TU_CONTRASEÑA_DE_POSTGRES@localhost:5432/medisoft_db
```

**⚠️ IMPORTANTE:** 
- Reemplaza `TU_CONTRASEÑA_DE_POSTGRES` con la contraseña que configuraste durante la instalación
- Para generar una SECRET_KEY segura, ejecuta: `python -c "import secrets; print(secrets.token_hex(32))"`

## 🔧 Paso 3: Instalar Dependencias de Python

Abre PowerShell en tu carpeta del proyecto y ejecuta:

```powershell
pip install -r requirements.txt
```

Esto instalará todas las dependencias, incluyendo `psycopg2-binary` para PostgreSQL.

## 🚀 Paso 4: Crear la Base de Datos

Ejecuta el script de creación:

```powershell
python create_postgres_db.py
```

Este script:
- ✅ Verifica la conexión a PostgreSQL
- ✅ Crea la base de datos `medisoft_db` si no existe
- ✅ Crea todas las tablas necesarias
- ✅ Crea el usuario administrador (admin/admin123)
- ✅ Te pregunta si quieres crear datos de ejemplo

## ✅ Paso 5: Verificar la Instalación

Ejecuta:

```powershell
python check_db.py
```

Deberías ver:
- Total de usuarios en la BD
- Lista de usuarios (incluyendo el admin)
- Estructura de la tabla Usuario

## 🎯 Paso 6: Iniciar la Aplicación

```powershell
python app.py
```

Luego accede a: **http://localhost:5000**

**Credenciales de acceso:**
- Usuario: `admin`
- Contraseña: `admin123`

⚠️ **IMPORTANTE:** Cambia la contraseña después del primer acceso.

## 🐛 Solución de Problemas

### Error: "No se pudo conectar a PostgreSQL"

**Solución:**
1. Verifica que PostgreSQL esté corriendo:
   - Abre "Servicios de Windows" (Win + R → `services.msc`)
   - Busca "postgresql" y verifica que esté "En ejecución"
   - Si no está, haz clic derecho → "Iniciar"

2. Verifica las credenciales en `.env`:
   - Asegúrate de que `POSTGRES_PASSWORD` sea correcta
   - Asegúrate de que `POSTGRES_USER` sea `postgres` (o el usuario que configuraste)

3. Verifica el puerto:
   - Por defecto es `5432`
   - Si cambiaste el puerto durante la instalación, actualiza `POSTGRES_PORT` en `.env`

### Error: "psycopg2 no está instalado"

**Solución:**
```powershell
pip install psycopg2-binary
```

### Error: "La base de datos ya existe"

**No es un error.** El script detecta si la base de datos ya existe y continúa normalmente.

### Error: "password authentication failed"

**Solución:**
1. Verifica la contraseña en `.env`
2. Si olvidaste la contraseña, puedes cambiarla:
   - Abre pgAdmin 4
   - O ejecuta: `psql -U postgres` (te pedirá la contraseña)
   - Luego: `ALTER USER postgres WITH PASSWORD 'nueva_contraseña';`

### Error: "permission denied to create database"

**Solución:**
El usuario `postgres` debería tener permisos. Si no:
1. Abre pgAdmin 4
2. Conéctate al servidor
3. Click derecho en "Login/Group Roles" → "postgres" → "Properties"
4. Ve a "Privileges" y marca "Can login?" y "Superuser"

## 📊 Usar pgAdmin 4 (Opcional)

pgAdmin 4 es una interfaz gráfica para PostgreSQL:

1. **Abre pgAdmin 4** (debería estar en el menú de inicio)

2. **Conéctate al servidor:**
   - Click derecho en "Servers" → "Create" → "Server"
   - Name: `Local PostgreSQL`
   - Host: `localhost`
   - Port: `5432`
   - Username: `postgres`
   - Password: Tu contraseña de PostgreSQL

3. **Explora tu base de datos:**
   - Expande "Databases" → `medisoft_db`
   - Verás todas las tablas creadas

## 🎉 ¡Listo!

Tu base de datos PostgreSQL está instalada y configurada. Ahora puedes:
- Usar la aplicación localmente
- Desplegar en Render (usará la base de datos de Render automáticamente)

## 📚 Comandos Útiles

```powershell
# Verificar que PostgreSQL esté corriendo
Get-Service -Name postgresql*

# Reiniciar PostgreSQL
Restart-Service postgresql-x64-15  # (ajusta el nombre según tu versión)

# Conectar a PostgreSQL desde línea de comandos
psql -U postgres -d medisoft_db

# Listar bases de datos (desde psql)
\l

# Salir de psql
\q
```

