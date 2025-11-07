# Guía de Despliegue en Render (Gratis)

Esta guía te ayudará a desplegar tu aplicación Medisoft en Render usando el plan gratuito.

## 📋 Requisitos Previos

1. **Cuenta en Render**: Regístrate en [render.com](https://render.com) (gratis)
2. **Repositorio Git**: Tu código debe estar en GitHub, GitLab o Bitbucket
3. **PostgreSQL**: Render proporciona una base de datos PostgreSQL gratuita

## 🚀 Pasos para Desplegar

### Paso 1: Preparar el Repositorio

1. **Asegúrate de tener todos los archivos necesarios:**
   - ✅ `requirements.txt`
   - ✅ `Procfile`
   - ✅ `render.yaml` (opcional pero recomendado)
   - ✅ `runtime.txt`
   - ✅ `build.sh` (opcional)

2. **Haz commit y push de los cambios:**
   ```bash
   git add .
   git commit -m "Preparar para despliegue en Render"
   git push origin main
   ```

### Paso 2: Crear Servicio Web en Render

1. **Inicia sesión en Render** y haz clic en "New +"

2. **Selecciona "Web Service"**

3. **Conecta tu repositorio:**
   - Selecciona tu proveedor (GitHub/GitLab/Bitbucket)
   - Autoriza a Render
   - Selecciona el repositorio de tu proyecto

4. **Configura el servicio:**
   - **Name**: `medisoft-app` (o el nombre que prefieras)
   - **Environment**: `Python 3`
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt && python init_db.py
     ```
   - **Start Command**: 
     ```bash
     gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:$PORT app:app
     ```
   - **Plan**: Selecciona **Free**

### Paso 3: Crear Base de Datos PostgreSQL

1. **En el dashboard de Render, haz clic en "New +"**

2. **Selecciona "PostgreSQL"**

3. **Configura la base de datos:**
   - **Name**: `medisoft-db`
   - **Database**: `medisoft_db`
   - **User**: `medisoft_user` (o déjalo por defecto)
   - **Plan**: Selecciona **Free**
   - **Region**: Selecciona la misma región que tu servicio web

4. **Copia la "Internal Database URL"** (la necesitarás después)

### Paso 4: Configurar Variables de Entorno

En la configuración de tu servicio web, ve a la sección **"Environment"** y agrega:

#### Variables Requeridas:

```
SECRET_KEY=tu_clave_secreta_muy_larga_y_aleatoria_aqui
FLASK_ENV=production
DEBUG=false
DATABASE_URL=<pega aquí la Internal Database URL de tu base de datos>
```

#### Cómo obtener una SECRET_KEY segura:

```python
import secrets
print(secrets.token_hex(32))
```

O usa un generador online: https://randomkeygen.com/

#### Ejemplo de DATABASE_URL:
```
postgresql://medisoft_user:password@dpg-xxxxx-a.oregon-postgres.render.com/medisoft_db
```

### Paso 5: Configurar el Servicio Web

1. **En la configuración del servicio web:**

   - **Auto-Deploy**: Actívalo si quieres que se despliegue automáticamente en cada push
   - **Health Check Path**: `/` (o deja vacío)
   - **Dockerfile Path**: (déjalo vacío, no usamos Docker)

2. **Guarda los cambios**

### Paso 6: Desplegar

1. **Render comenzará a construir tu aplicación automáticamente**

2. **Observa los logs** en tiempo real para ver el progreso

3. **Espera a que el build termine** (puede tomar 5-10 minutos la primera vez)

4. **Verifica que el servicio esté "Live"** (debería aparecer un check verde)

### Paso 7: Verificar el Despliegue

1. **Haz clic en la URL** que Render te proporciona (algo como `https://medisoft-app.onrender.com`)

2. **Inicia sesión con:**
   - Usuario: `admin`
   - Contraseña: `admin123`

3. **⚠️ IMPORTANTE**: Cambia la contraseña inmediatamente después del primer acceso

## 🔧 Configuración Avanzada

### Usar render.yaml (Recomendado)

Si prefieres usar el archivo `render.yaml` que ya creamos:

1. En Render, ve a "New +" → "Blueprint"
2. Conecta tu repositorio
3. Render detectará automáticamente el archivo `render.yaml`
4. Revisa la configuración y haz clic en "Apply"

Esto creará tanto el servicio web como la base de datos automáticamente.

### Variables de Entorno Adicionales

Puedes agregar más variables si las necesitas:

```
HOST=0.0.0.0
PORT=10000
PYTHON_VERSION=3.11.0
```

## 🐛 Solución de Problemas

### Error: "Build failed"

1. **Revisa los logs de build** en Render
2. **Verifica que `requirements.txt` esté correcto**
3. **Asegúrate de que todas las dependencias estén listadas**

### Error: "Database connection failed"

1. **Verifica que la variable `DATABASE_URL` esté correctamente configurada**
2. **Asegúrate de que la base de datos esté en la misma región que el servicio web**
3. **Verifica que la base de datos esté "Available" (no pausada)**

### Error: "Application crashed"

1. **Revisa los logs del servicio** en Render
2. **Verifica que `SECRET_KEY` esté configurada**
3. **Asegúrate de que el `Start Command` sea correcto**

### La aplicación se duerme después de inactividad

**Render Free tiene un límite**: Si tu aplicación no recibe tráfico por 15 minutos, se "duerme". La próxima solicitud puede tardar 30-60 segundos en despertar.

**Soluciones:**
- Usa un servicio de "ping" gratuito como [UptimeRobot](https://uptimerobot.com) para mantenerla activa
- O considera actualizar a un plan de pago si necesitas que esté siempre activa

### Error: "Port already in use"

Render maneja el puerto automáticamente. Asegúrate de usar `$PORT` en tu comando de inicio.

## 📊 Monitoreo

### Ver Logs

1. Ve a tu servicio en Render
2. Haz clic en "Logs"
3. Puedes ver logs en tiempo real o descargarlos

### Métricas

En el plan gratuito, Render proporciona métricas básicas:
- Uptime
- Response time
- Request count

## 🔒 Seguridad

1. **Cambia `SECRET_KEY`** por una clave única y segura
2. **Cambia la contraseña del admin** después del primer acceso
3. **No expongas credenciales** en el código
4. **Usa HTTPS** (Render lo proporciona automáticamente)

## 💰 Límites del Plan Gratuito

- **750 horas/mes** de tiempo de ejecución
- **512 MB RAM**
- **0.1 CPU compartida**
- **La aplicación se "duerme"** después de 15 minutos de inactividad
- **Base de datos PostgreSQL gratuita** con 1 GB de almacenamiento

## 📝 Notas Importantes

1. **Primera vez**: El despliegue inicial puede tardar 10-15 minutos
2. **Base de datos**: La base de datos gratuita se pausa después de 90 días de inactividad
3. **Backups**: Considera hacer backups regulares de tu base de datos
4. **Dominio personalizado**: Puedes agregar un dominio personalizado en la configuración

## 🎉 ¡Listo!

Tu aplicación debería estar funcionando en Render. Si tienes problemas, revisa los logs y esta guía.

## 📞 Soporte

- **Documentación de Render**: https://render.com/docs
- **Comunidad**: https://community.render.com

