# ⚡ Solución Rápida: Crear Tablas en Render

## 🚨 Problema

Error al iniciar sesión: `relation "usuario" does not exist`

## ✅ Solución en 3 Pasos

### Paso 1: Abre el Shell de Render

1. Ve a tu servicio web en Render
2. Haz clic en **"Shell"** (menú lateral)

### Paso 2: Ejecuta el Script

Copia y pega este comando:

```bash
python crear_tablas_render.py
```

### Paso 3: Verifica

Deberías ver:
```
✅ Tablas creadas exitosamente
✅ Usuario administrador creado
```

## 🎯 Iniciar Sesión

Ahora puedes iniciar sesión:
- **Usuario**: `admin`
- **Contraseña**: `admin123`

## 🔄 Si el Script No Funciona

Ejecuta esto directamente en el Shell:

```python
python -c "
from app import app, db
from werkzeug.security import generate_password_hash
from app import Usuario

with app.app_context():
    db.create_all()
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
    print('✅ Listo!')
"
```

## 📝 Nota

He actualizado `app.py` para que cree las tablas automáticamente en el próximo despliegue. Pero por ahora, ejecuta el script manualmente.

