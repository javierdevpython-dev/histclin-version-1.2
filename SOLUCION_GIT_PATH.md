# 🔧 Solución: Git no está en el PATH

## Problema
Git está instalado pero no se reconoce en la terminal porque no está en el PATH del sistema.

## ✅ Solución Rápida (Manual)

### Paso 1: Abrir Variables de Entorno

1. Presiona `Win + R`
2. Escribe: `sysdm.cpl` y presiona Enter
3. Ve a la pestaña **"Opciones avanzadas"**
4. Haz clic en **"Variables de entorno"**

### Paso 2: Agregar Git al PATH

1. En la sección **"Variables del sistema"**, busca **"Path"**
2. Selecciónalo y haz clic en **"Editar"**
3. Haz clic en **"Nuevo"**
4. Agrega esta ruta:
   ```
   C:\Program Files\Git\bin
   ```
5. Haz clic en **"Aceptar"** en todas las ventanas

### Paso 3: Reiniciar Terminal

1. **Cierra completamente** PowerShell/CMD
2. **Abre una nueva terminal**
3. Prueba: `git --version`

## ✅ Solución con PowerShell (Como Administrador)

1. **Abre PowerShell como Administrador:**
   - Click derecho en PowerShell
   - "Ejecutar como administrador"

2. **Ejecuta este comando:**
   ```powershell
   [Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Program Files\Git\bin", "Machine")
   ```

3. **Reinicia tu terminal**

## ✅ Solución Temporal (Solo para esta sesión)

Si necesitas usar Git ahora mismo sin reiniciar:

```powershell
$env:Path += ";C:\Program Files\Git\bin"
```

Luego puedes usar `git` normalmente en esa terminal.

## 🧪 Verificar que Funcionó

Después de agregar Git al PATH y reiniciar la terminal:

```bash
git --version
```

Deberías ver algo como: `git version 2.x.x`

## 📤 Subir a GitHub (Después de arreglar PATH)

Una vez que Git funcione:

```bash
git add .
git commit -m "Preparar proyecto para Render"
git push origin main
```

Si te pide autenticación, sigue las instrucciones en el navegador.

