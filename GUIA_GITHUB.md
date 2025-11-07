# 📤 Guía para Subir tu Proyecto a GitHub

## 🔧 Paso 1: Instalar Git

### Opción A: Descargar Git para Windows

1. **Descarga Git:**
   - Ve a: https://git-scm.com/download/win
   - Descarga el instalador (se descargará automáticamente)

2. **Instala Git:**
   - Ejecuta el instalador descargado
   - Sigue el asistente (usa las opciones por defecto)
   - Asegúrate de marcar "Add Git to PATH" durante la instalación

3. **Verifica la instalación:**
   - Abre una nueva terminal (PowerShell o CMD)
   - Ejecuta: `git --version`
   - Deberías ver algo como: `git version 2.x.x`

### Opción B: Instalar con Chocolatey (si lo tienes)

```powershell
choco install git
```

### Opción C: Instalar con Winget (Windows 10/11)

```powershell
winget install --id Git.Git -e --source winget
```

## 📝 Paso 2: Configurar Git (Primera vez)

Después de instalar Git, configura tu nombre y email:

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu-email@ejemplo.com"
```

## 🚀 Paso 3: Subir tu Proyecto a GitHub

### Opción A: Usando la Terminal (Recomendado)

1. **Abre PowerShell o CMD** en la carpeta de tu proyecto:
   ```
   C:\Users\CAJA2\Desktop\histclin-version-1.2
   ```

2. **Inicializa el repositorio Git** (si no está inicializado):
   ```bash
   git init
   ```

3. **Agrega todos los archivos:**
   ```bash
   git add .
   ```

4. **Haz tu primer commit:**
   ```bash
   git commit -m "Primer commit - Proyecto Medisoft"
   ```

5. **Crea un repositorio en GitHub:**
   - Ve a https://github.com
   - Inicia sesión o crea una cuenta
   - Haz clic en "New" (botón verde) o el icono "+"
   - Nombre: `histclin-version-1.2` (o el que prefieras)
   - Elige "Public" o "Private"
   - **NO marques** "Initialize with README"
   - Haz clic en "Create repository"

6. **Conecta tu repositorio local con GitHub:**
   ```bash
   git remote add origin https://github.com/TU-USUARIO/histclin-version-1.2.git
   ```
   (Reemplaza `TU-USUARIO` con tu nombre de usuario de GitHub)

7. **Sube tu código:**
   ```bash
   git branch -M main
   git push -u origin main
   ```

8. **Si te pide credenciales:**
   - Usuario: Tu nombre de usuario de GitHub
   - Contraseña: Usa un **Personal Access Token** (no tu contraseña normal)
   - Para crear un token: GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token

### Opción B: Usando GitHub Desktop (Más Fácil)

1. **Descarga GitHub Desktop:**
   - Ve a: https://desktop.github.com
   - Descarga e instala

2. **Inicia sesión en GitHub Desktop** con tu cuenta de GitHub

3. **Abre tu proyecto:**
   - File → Add Local Repository
   - Selecciona la carpeta: `C:\Users\CAJA2\Desktop\histclin-version-1.2`

4. **Haz commit:**
   - Escribe un mensaje: "Primer commit - Proyecto Medisoft"
   - Haz clic en "Commit to main"

5. **Publica en GitHub:**
   - Haz clic en "Publish repository"
   - Elige el nombre y si será público o privado
   - Haz clic en "Publish repository"

### Opción C: Usando Visual Studio Code

1. **Abre VS Code** en tu carpeta del proyecto

2. **Abre la terminal integrada:**
   - View → Terminal
   - O presiona `` Ctrl + ` ``

3. **Sigue los pasos de la Opción A** desde el paso 2

## 🔐 Paso 4: Autenticación con GitHub

GitHub ya no acepta contraseñas normales. Necesitas un **Personal Access Token**:

### Crear un Personal Access Token:

1. Ve a GitHub.com → Tu perfil → **Settings**
2. En el menú lateral, ve a **Developer settings**
3. Haz clic en **Personal access tokens** → **Tokens (classic)**
4. Haz clic en **Generate new token (classic)**
5. Configura:
   - **Note**: "Para mi proyecto Medisoft"
   - **Expiration**: Elige una fecha (o "No expiration")
   - **Scopes**: Marca `repo` (esto da acceso completo a repositorios)
6. Haz clic en **Generate token**
7. **¡COPIA EL TOKEN INMEDIATAMENTE!** (solo se muestra una vez)

### Usar el Token:

Cuando Git te pida credenciales:
- **Usuario**: Tu nombre de usuario de GitHub
- **Contraseña**: Pega el Personal Access Token (no tu contraseña)

## 📋 Comandos Rápidos de Referencia

```bash
# Ver estado de los archivos
git status

# Agregar todos los archivos
git add .

# Hacer commit
git commit -m "Descripción de los cambios"

# Ver commits
git log

# Subir cambios a GitHub
git push

# Ver repositorios remotos
git remote -v

# Agregar repositorio remoto
git remote add origin https://github.com/USUARIO/REPOSITORIO.git

# Cambiar URL del remoto
git remote set-url origin https://github.com/USUARIO/REPOSITORIO.git
```

## ⚠️ Problemas Comunes

### Error: "git no se reconoce"

**Solución**: Git no está instalado o no está en el PATH
- Instala Git desde https://git-scm.com/download/win
- Reinicia la terminal después de instalar

### Error: "fatal: not a git repository"

**Solución**: No has inicializado Git en esta carpeta
```bash
git init
```

### Error: "fatal: remote origin already exists"

**Solución**: Ya existe un remoto. Cambia la URL:
```bash
git remote set-url origin https://github.com/USUARIO/REPOSITORIO.git
```

### Error: "authentication failed"

**Solución**: Usa un Personal Access Token en lugar de tu contraseña

### Error: "failed to push some refs"

**Solución**: Primero haz pull:
```bash
git pull origin main --allow-unrelated-histories
git push -u origin main
```

## ✅ Verificar que Funcionó

1. Ve a tu repositorio en GitHub: `https://github.com/TU-USUARIO/histclin-version-1.2`
2. Deberías ver todos tus archivos allí
3. Ahora puedes usar este repositorio para desplegar en Render

## 🎯 Siguiente Paso: Desplegar en Render

Una vez que tu código esté en GitHub:
1. Ve a Render.com
2. Conecta tu repositorio de GitHub
3. Sigue la guía en `DESPLIEGUE_RENDER.md`

