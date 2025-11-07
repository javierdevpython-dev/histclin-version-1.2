# 📤 Instrucciones para Subir Archivos a GitHub

## ⚠️ Problema Actual

Hay credenciales guardadas de otro usuario (`javierdevpython-dev`) que no tiene permisos para tu repositorio.

## ✅ Solución: Usar Personal Access Token

GitHub ya no acepta contraseñas normales. Necesitas crear un **Personal Access Token**.

### Paso 1: Crear Personal Access Token

1. **Ve a GitHub.com** e inicia sesión con tu cuenta (`jmora19921002`)

2. **Ve a Settings:**
   - Haz clic en tu foto de perfil (arriba derecha)
   - Selecciona **"Settings"**

3. **Ve a Developer settings:**
   - En el menú lateral, baja hasta el final
   - Haz clic en **"Developer settings"**

4. **Crea un token:**
   - Haz clic en **"Personal access tokens"**
   - Selecciona **"Tokens (classic)"**
   - Haz clic en **"Generate new token"** → **"Generate new token (classic)"**

5. **Configura el token:**
   - **Note**: "Para mi proyecto histclin"
   - **Expiration**: Elige una fecha (o "No expiration")
   - **Scopes**: Marca **`repo`** (esto da acceso completo a repositorios)
   - Haz clic en **"Generate token"** (abajo)

6. **¡COPIA EL TOKEN INMEDIATAMENTE!** 
   - Se muestra solo una vez
   - Guárdalo en un lugar seguro

### Paso 2: Subir Archivos

Abre PowerShell en tu carpeta del proyecto y ejecuta:

```powershell
# Agregar Git al PATH
$env:Path += ";C:\Program Files\Git\bin"

# Agregar archivos
git add .

# Hacer commit
git commit -m "Preparar proyecto para Render"

# Subir (usarás el token como contraseña)
git push origin main
```

**Cuando te pida credenciales:**
- **Usuario**: `jmora19921002` (tu usuario de GitHub)
- **Contraseña**: Pega el **Personal Access Token** (no tu contraseña normal)

### Paso 3: Alternativa - Usar el Script

Ejecuta el script que creé:

```powershell
.\subir_github_final.ps1
```

Este script:
- Agrega todos los archivos
- Hace commit
- Intenta hacer push
- Te guiará si hay errores

## 🔧 Si Sigue Fallando

### Opción A: Limpiar Credenciales de Windows

1. Presiona `Win + R`
2. Escribe: `control /name Microsoft.CredentialManager`
3. Ve a **"Credenciales de Windows"**
4. Busca entradas relacionadas con **"GitHub"** o **"git"**
5. Elimínalas
6. Intenta hacer push de nuevo

### Opción B: Usar SSH (Más Seguro)

1. **Genera una clave SSH:**
   ```powershell
   $env:Path += ";C:\Program Files\Git\bin"
   ssh-keygen -t ed25519 -C "tu-email@ejemplo.com"
   ```

2. **Copia la clave pública:**
   ```powershell
   cat ~/.ssh/id_ed25519.pub
   ```

3. **Agrega la clave a GitHub:**
   - GitHub.com → Settings → SSH and GPG keys
   - New SSH key
   - Pega la clave pública

4. **Cambia la URL del remoto a SSH:**
   ```powershell
   git remote set-url origin git@github.com:jmora19921002/histclin-version-1.2.git
   ```

5. **Haz push:**
   ```powershell
   git push origin main
   ```

## ✅ Verificar que Funcionó

1. Ve a tu repositorio en GitHub:
   https://github.com/jmora19921002/histclin-version-1.2

2. Deberías ver todos tus archivos actualizados

3. Ahora puedes usar este repositorio para desplegar en Render

## 🚀 Siguiente Paso: Desplegar en Render

Una vez que los archivos estén en GitHub:
1. Ve a Render.com
2. Conecta tu repositorio de GitHub
3. Sigue la guía en `DESPLIEGUE_RENDER.md`

