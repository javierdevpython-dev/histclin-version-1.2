# 📤 Cómo Subir Archivos a GitHub - SOLUCIÓN DEFINITIVA

## ⚠️ Problema Actual

Tienes credenciales guardadas de otro usuario (`javierdevpython-dev`) que no tiene permisos para tu repositorio.

## ✅ SOLUCIÓN PASO A PASO

### Paso 1: Limpiar Credenciales Guardadas

1. **Abre el Administrador de Credenciales de Windows:**
   - Presiona `Win + R`
   - Escribe: `control /name Microsoft.CredentialManager`
   - Presiona Enter

2. **Elimina credenciales de GitHub:**
   - Ve a la pestaña **"Credenciales de Windows"**
   - Busca entradas que contengan **"GitHub"** o **"git"**
   - Haz clic en cada una y selecciona **"Eliminar"**
   - Elimina TODAS las relacionadas con GitHub

### Paso 2: Crear Personal Access Token

1. **Ve a GitHub.com** e inicia sesión con tu cuenta (`jmora19921002`)

2. **Ve a Settings:**
   - Foto de perfil (arriba derecha) → **Settings**

3. **Developer settings:**
   - Menú lateral → Baja hasta el final → **Developer settings**

4. **Personal access tokens:**
   - **Personal access tokens** → **Tokens (classic)**
   - **Generate new token** → **Generate new token (classic)**

5. **Configura el token:**
   - **Note**: "Para histclin proyecto"
   - **Expiration**: Elige fecha o "No expiration"
   - **Scopes**: ✅ Marca **`repo`** (acceso completo a repositorios)
   - **Generate token** (abajo)

6. **COPIA EL TOKEN** (solo se muestra una vez)

### Paso 3: Subir Archivos

Abre PowerShell en tu carpeta del proyecto:

```powershell
# Agregar Git al PATH
$env:Path += ";C:\Program Files\Git\bin"

# Agregar archivos
git add .

# Hacer commit (si hay cambios)
git commit -m "Preparar proyecto para Render"

# Subir a GitHub
git push origin main
```

**Cuando te pida credenciales:**
- **Usuario**: `jmora19921002`
- **Contraseña**: Pega el **Personal Access Token** (NO tu contraseña normal)

### Paso 4: Verificar

1. Ve a: https://github.com/jmora19921002/histclin-version-1.2
2. Deberías ver todos tus archivos actualizados

## 🚀 Script Automático

Si prefieres usar un script, ejecuta:

```powershell
.\subir_github_final.ps1
```

## ⚡ Comandos Rápidos

Copia y pega esto en PowerShell:

```powershell
$env:Path += ";C:\Program Files\Git\bin"
git add .
git commit -m "Actualizar proyecto"
git push origin main
```

Cuando pida credenciales:
- Usuario: `jmora19921002`
- Contraseña: Tu Personal Access Token

## ✅ Estado Actual

- ✅ Archivos commiteados localmente
- ✅ Repositorio conectado a GitHub
- ⏳ Falta: Subir (necesitas autenticarte con token)

## 🎯 Siguiente Paso

Una vez que los archivos estén en GitHub:
1. Ve a Render.com
2. Conecta tu repositorio
3. Despliega tu aplicación

