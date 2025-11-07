@echo off
echo ========================================
echo   SUBIR PROYECTO A GITHUB
echo ========================================
echo.

REM Verificar si Git está instalado
git --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Git no está instalado o no está en el PATH
    echo.
    echo Por favor:
    echo 1. Instala Git desde: https://git-scm.com/download/win
    echo 2. Reinicia esta terminal después de instalar
    echo.
    pause
    exit /b 1
)

echo [OK] Git está instalado
echo.

REM Verificar si ya es un repositorio Git
if exist .git (
    echo [INFO] Ya es un repositorio Git
) else (
    echo [INFO] Inicializando repositorio Git...
    git init
    if errorlevel 1 (
        echo [ERROR] No se pudo inicializar Git
        pause
        exit /b 1
    )
    echo [OK] Repositorio inicializado
    echo.
)

REM Agregar todos los archivos
echo [INFO] Agregando archivos...
git add .
if errorlevel 1 (
    echo [ERROR] No se pudieron agregar los archivos
    pause
    exit /b 1
)
echo [OK] Archivos agregados
echo.

REM Verificar si hay cambios para commit
git diff --cached --quiet
if errorlevel 1 (
    echo [INFO] Haciendo commit...
    git commit -m "Preparar proyecto para despliegue en Render"
    if errorlevel 1 (
        echo [ERROR] No se pudo hacer commit
        pause
        exit /b 1
    )
    echo [OK] Commit realizado
) else (
    echo [INFO] No hay cambios para commitear
)
echo.

REM Verificar si hay un remoto configurado
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo ========================================
    echo   CONFIGURAR REPOSITORIO REMOTO
    echo ========================================
    echo.
    echo Necesitas crear un repositorio en GitHub primero:
    echo 1. Ve a https://github.com
    echo 2. Crea un nuevo repositorio
    echo 3. NO inicialices con README
    echo.
    set /p GITHUB_URL="Pega la URL de tu repositorio (ej: https://github.com/usuario/repo.git): "
    if "!GITHUB_URL!"=="" (
        echo [ERROR] URL vacía
        pause
        exit /b 1
    )
    git remote add origin !GITHUB_URL!
    if errorlevel 1 (
        echo [ERROR] No se pudo agregar el remoto
        pause
        exit /b 1
    )
    echo [OK] Repositorio remoto configurado
    echo.
)

REM Intentar hacer push
echo [INFO] Subiendo cambios a GitHub...
echo.
git branch -M main
git push -u origin main
if errorlevel 1 (
    echo.
    echo [ERROR] No se pudo subir a GitHub
    echo.
    echo Posibles causas:
    echo - No tienes permisos en el repositorio
    echo - Necesitas autenticarte (usa Personal Access Token)
    echo - El repositorio remoto no existe
    echo.
    echo Para autenticarte:
    echo 1. Ve a GitHub.com -^> Settings -^> Developer settings
    echo 2. Personal access tokens -^> Generate new token
    echo 3. Usa el token como contraseña
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   ¡ÉXITO! Proyecto subido a GitHub
echo ========================================
echo.
pause

