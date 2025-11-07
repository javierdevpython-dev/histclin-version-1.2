# 🗄️ Crear Base de Datos PostgreSQL en Render

## 📋 Paso 1: Crear la Base de Datos

1. **En el Dashboard de Render**, haz clic en **"New +"** (arriba a la derecha)

2. **Selecciona "PostgreSQL"**

3. **Configura la base de datos:**
   - **Name**: `medisoft-db` (o el nombre que prefieras)
   - **Database**: `medisoft_db` (nombre de la base de datos)
   - **User**: `medisoft_user` (o déjalo por defecto)
   - **Region**: Selecciona la **misma región** que tu servicio web
   - **PostgreSQL Version**: Deja la versión más reciente (15 o 16)
   - **Plan**: Selecciona **Free** (o el plan que prefieras)

4. **Haz clic en "Create Database"**

5. **Espera 2-3 minutos** mientras Render crea la base de datos

## 🔗 Paso 2: Conectar la Base de Datos con tu Aplicación

### Opción A: Usando Variables de Entorno (Recomendado)

1. **Ve a tu servicio web** en Render (el que ya desplegaste)

2. **Ve a "Settings"** → **"Environment"**

3. **Busca la variable `DATABASE_URL`**:
   - Si ya existe, verifica que esté correcta
   - Si no existe, agrégalas:

4. **Agrega o actualiza estas variables:**
   - **Key**: `DATABASE_URL`
   - **Value**: Copia la **"Internal Database URL"** de tu base de datos PostgreSQL
     - Ve a tu base de datos en Render
     - En la sección "Connections", copia la **"Internal Database URL"**
     - Debería verse así: `postgresql://medisoft_user:password@dpg-xxxxx-a.oregon-postgres.render.com/medisoft_db`

5. **Opcional - Variables individuales** (si prefieres):
   - `POSTGRES_HOST` = El host de la Internal Database URL
   - `POSTGRES_PORT` = `5432`
   - `POSTGRES_USER` = El usuario de la Internal Database URL
   - `POSTGRES_PASSWORD` = La contraseña de la Internal Database URL
   - `POSTGRES_DB` = `medisoft_db`

6. **Guarda los cambios**

### Opción B: Usando Blueprint (render.yaml)

Si usaste el archivo `render.yaml`, la conexión debería ser automática. Solo necesitas:

1. **Verificar que el nombre de la base de datos coincida:**
   - En `render.yaml`: `name: medisoft-db`
   - En Render: El nombre que le diste a la base de datos

2. **Si no coincide**, actualiza `render.yaml` o renombra la base de datos en Render

## 🚀 Paso 3: Reiniciar la Aplicación

1. **Ve a tu servicio web** en Render

2. **Haz clic en "Manual Deploy"** → **"Deploy latest commit"**

   O simplemente espera a que Render detecte los cambios automáticamente

3. **Observa los logs** para verificar que:
   - Se conecta a la base de datos correctamente
   - Se crean las tablas (si ejecutaste `init_db.py` en el build command)

## ✅ Paso 4: Verificar que Funcionó

1. **Revisa los logs** de tu aplicación en Render
   - Deberías ver mensajes de conexión a PostgreSQL
   - No deberían aparecer errores de conexión

2. **Accede a tu aplicación:**
   - URL: `https://tu-app.onrender.com`
   - Intenta iniciar sesión con: `admin` / `admin123`

3. **Si hay errores**, revisa:
   - Que la variable `DATABASE_URL` esté correcta
   - Que la base de datos esté en la misma región que tu servicio
   - Que la base de datos esté "Available" (no pausada)

## 🔧 Paso 5: Inicializar las Tablas (Si es Necesario)

Si las tablas no se crearon automáticamente durante el build:

1. **Verifica el Build Command** en tu servicio:
   - Debería incluir: `python init_db.py`
   - Si no está, agrégalo: `pip install -r requirements.txt && python init_db.py`

2. **O ejecuta manualmente:**
   - Ve a "Shell" en tu servicio web
   - Ejecuta: `python init_db.py`

## 🐛 Solución de Problemas

### Error: "could not connect to server"

**Solución:**
- Verifica que uses la **"Internal Database URL"** (no la External)
- Verifica que la base de datos esté en la misma región
- Verifica que la base de datos esté "Available"

### Error: "database does not exist"

**Solución:**
- Verifica que el nombre de la base de datos en `DATABASE_URL` sea correcto
- Por defecto debería ser `medisoft_db`

### Error: "password authentication failed"

**Solución:**
- Usa la URL completa de la Internal Database URL
- No intentes construir la URL manualmente

### La base de datos está pausada

**Solución:**
- En el plan Free, la base de datos se pausa después de 90 días de inactividad
- Haz clic en "Resume" para reactivarla
- Puede tardar 1-2 minutos en reactivarse

## 📝 Notas Importantes

1. **Internal vs External URL:**
   - **Internal Database URL**: Para usar desde tu aplicación en Render (más rápido, mismo datacenter)
   - **External Database URL**: Para usar desde fuera de Render (más lento)

2. **Región:**
   - La base de datos y el servicio web deben estar en la misma región para mejor rendimiento

3. **Plan Free:**
   - La base de datos se pausa después de 90 días de inactividad
   - Se reactiva automáticamente cuando la usas (puede tardar 1-2 minutos)

4. **Backups:**
   - En el plan Free no hay backups automáticos
   - Considera hacer backups manuales si es importante

## ✅ Checklist

- [ ] Base de datos PostgreSQL creada en Render
- [ ] Base de datos en la misma región que el servicio web
- [ ] Variable `DATABASE_URL` configurada en el servicio web
- [ ] Build command incluye `python init_db.py`
- [ ] Aplicación reiniciada/redesplegada
- [ ] Logs muestran conexión exitosa a la base de datos
- [ ] Aplicación funciona correctamente

## 🎉 ¡Listo!

Tu aplicación debería estar conectada a la base de datos PostgreSQL en Render.

