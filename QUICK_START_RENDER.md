# 🚀 Inicio Rápido - Despliegue en Render

## Pasos Rápidos (5 minutos)

### 1. Prepara tu código
```bash
git add .
git commit -m "Preparar para Render"
git push origin main
```

### 2. Crea cuenta en Render
- Ve a [render.com](https://render.com)
- Regístrate (gratis)
- Conecta tu repositorio (GitHub/GitLab/Bitbucket)

### 3. Despliega usando Blueprint (Más fácil)

1. En Render, haz clic en **"New +"** → **"Blueprint"**
2. Conecta tu repositorio
3. Render detectará automáticamente `render.yaml`
4. Revisa la configuración y haz clic en **"Apply"**
5. Espera 5-10 minutos mientras se despliega

### 4. O Despliega Manualmente

#### Crear Base de Datos:
1. **New +** → **PostgreSQL**
2. Name: `medisoft-db`
3. Plan: **Free**
4. Crea la base de datos

#### Crear Servicio Web:
1. **New +** → **Web Service**
2. Conecta tu repositorio
3. Configuración:
   - **Build Command**: `pip install -r requirements.txt && python init_db.py`
   - **Start Command**: `gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:$PORT app:app`
   - **Plan**: Free
4. **Environment Variables**:
   ```
   SECRET_KEY=<genera una clave aleatoria>
   FLASK_ENV=production
   DEBUG=false
   DATABASE_URL=<Internal Database URL de tu BD>
   ```
5. Guarda y despliega

### 5. Accede a tu aplicación

- URL: `https://tu-app.onrender.com`
- Usuario: `admin`
- Contraseña: `admin123`

⚠️ **Cambia la contraseña inmediatamente**

## 📝 Variables de Entorno Necesarias

```
SECRET_KEY=tu_clave_secreta_muy_larga
FLASK_ENV=production
DEBUG=false
DATABASE_URL=<proporcionado por Render>
```

## ⚠️ Importante

- **Primera vez**: Puede tardar 10-15 minutos
- **Plan Free**: La app se "duerme" después de 15 min sin uso
- **Base de datos**: Se pausa después de 90 días de inactividad

## 📚 Documentación Completa

Lee `DESPLIEGUE_RENDER.md` para más detalles.

