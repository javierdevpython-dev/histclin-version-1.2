# ⚡ Pasos Rápidos: Instalar Base de Datos

## 🎯 Resumen en 4 Pasos

### 1️⃣ Instalar PostgreSQL

**Opción A - Descargar:**
- Ve a: https://www.postgresql.org/download/windows/
- Descarga e instala (anota la contraseña del usuario `postgres`)

**Opción B - Winget:**
```powershell
winget install PostgreSQL.PostgreSQL
```

### 2️⃣ Crear archivo `.env`

Crea un archivo `.env` en la raíz del proyecto:

```env
SECRET_KEY=clave_secreta_aleatoria_muy_larga
FLASK_ENV=development
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=TU_CONTRASEÑA_DE_POSTGRES
POSTGRES_DB=medisoft_db
DATABASE_URL=postgresql://postgres:TU_CONTRASEÑA_DE_POSTGRES@localhost:5432/medisoft_db
```

**⚠️ Reemplaza:**
- `TU_CONTRASEÑA_DE_POSTGRES` → La contraseña que configuraste al instalar PostgreSQL
- `clave_secreta_aleatoria_muy_larga` → Puedes usar cualquier texto largo y aleatorio

### 3️⃣ Instalar dependencias

```powershell
pip install -r requirements.txt
```

### 4️⃣ Crear base de datos

**Opción A - Script automático:**
```powershell
.\instalar_bd.ps1
```

**Opción B - Manual:**
```powershell
python create_postgres_db.py
```

## ✅ Verificar

```powershell
python check_db.py
```

## 🚀 Iniciar aplicación

```powershell
python app.py
```

Accede a: **http://localhost:5000**

**Login:**
- Usuario: `admin`
- Contraseña: `admin123`

## 🐛 Problemas Comunes

### PostgreSQL no está corriendo
1. Abre "Servicios de Windows" (Win + R → `services.msc`)
2. Busca "postgresql"
3. Si no está corriendo, haz clic derecho → "Iniciar"

### Error de conexión
- Verifica que la contraseña en `.env` sea correcta
- Verifica que PostgreSQL esté corriendo

### psycopg2 no instalado
```powershell
pip install psycopg2-binary
```

## 📚 Documentación Completa

Lee `INSTALAR_BASE_DATOS.md` para más detalles.

