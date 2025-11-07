# 🔧 Solución: Tablas No Existen en Render

## ❌ Error

```
psycopg2.errors.UndefinedTable: relation "usuario" does not exist
```

## 🔍 Causa

Las tablas no se crearon durante el build. Esto puede pasar porque:
- La base de datos no estaba conectada durante el build
- El script `init_db.py` falló silenciosamente
- La variable `DATABASE_URL` no estaba disponible durante el build

## ✅ Solución: Crear Tablas Manualmente

### Opción 1: Usar el Shell de Render (Recomendado)

1. **Ve a tu servicio web en Render**

2. **Haz clic en "Shell"** (en el menú lateral)

3. **Ejecuta este comando:**
   ```bash
   python crear_tablas_render.py
   ```

4. **Espera a que termine** - deberías ver:
   - ✅ Tablas creadas exitosamente
   - ✅ Usuario administrador creado

5. **Intenta iniciar sesión de nuevo:**
   - Usuario: `admin`
   - Contraseña: `admin123`

### Opción 2: Usar init_db.py desde el Shell

Si el script anterior no funciona, ejecuta:

```bash
python init_db.py
```

### Opción 3: Crear Tablas con Python Interactivo

1. **Abre el Shell de Render**

2. **Ejecuta Python:**
   ```bash
   python
   ```

3. **Ejecuta estos comandos:**
   ```python
   from app import app, db
   from werkzeug.security import generate_password_hash
   from app import Usuario
   
   with app.app_context():
       # Crear tablas
       db.create_all()
       print("Tablas creadas")
       
       # Crear usuario admin
       admin = Usuario.query.filter_by(username='admin').first()
       if not admin:
           admin = Usuario(
               username='admin',
               email='admin@medisoft.com',
               password_hash=generate_password_hash('admin123'),
               rol='administrador',
               nombre_completo='Administrador',
               activo=True
           )
           db.session.add(admin)
           db.session.commit()
           print("Usuario admin creado")
       else:
           print("Usuario admin ya existe")
   ```

4. **Sal de Python:**
   ```python
   exit()
   ```

## 🔄 Solución Permanente: Mejorar el Build Command

Para evitar este problema en el futuro, actualiza el Build Command en Render:

1. **Ve a tu servicio web** → **Settings** → **Build & Deploy**

2. **Actualiza el Build Command a:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Crea un script de inicio que cree las tablas si no existen**

O mejor aún, modifica `app.py` para crear las tablas automáticamente al iniciar (solo en producción):

```python
# Al final de app.py, antes de if __name__ == '__main__':
with app.app_context():
    try:
        # Verificar si las tablas existen
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        if not tables:
            print("Creando tablas...")
            db.create_all()
            
            # Crear usuario admin si no existe
            from app import Usuario
            if not Usuario.query.filter_by(username='admin').first():
                admin = Usuario(
                    username='admin',
                    email='admin@medisoft.com',
                    password_hash=generate_password_hash('admin123'),
                    rol='administrador',
                    nombre_completo='Administrador',
                    activo=True
                )
                db.session.add(admin)
                db.session.commit()
                print("Usuario admin creado")
    except Exception as e:
        print(f"Error al inicializar BD: {e}")
```

## ✅ Verificar que Funcionó

1. **Ejecuta en el Shell:**
   ```bash
   python -c "from app import app, db; from sqlalchemy import inspect; inspector = inspect(db.engine); print('Tablas:', inspector.get_table_names())"
   ```

2. **Deberías ver una lista de tablas**, incluyendo `usuario`

3. **Intenta iniciar sesión** en tu aplicación

## 📝 Notas

- El script `crear_tablas_render.py` está diseñado para ejecutarse desde el Shell de Render
- Crea todas las tablas y el usuario administrador
- Es seguro ejecutarlo múltiples veces (no duplica datos)

## 🎯 Próximos Pasos

Una vez que las tablas estén creadas:
1. Inicia sesión con `admin` / `admin123`
2. Cambia la contraseña del administrador
3. Configura tu aplicación

