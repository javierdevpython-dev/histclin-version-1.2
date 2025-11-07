@echo off
echo ========================================
echo   LIMPIAR CREDENCIALES DE GIT
echo ========================================
echo.

echo Eliminando credenciales guardadas de GitHub...
cmdkey /list | findstr "git" >nul
if %errorlevel% equ 0 (
    for /f "tokens=3" %%a in ('cmdkey /list ^| findstr "git"') do (
        echo Eliminando: %%a
        cmdkey /delete:%%a
    )
) else (
    echo No se encontraron credenciales guardadas
)

echo.
echo ========================================
echo   Credenciales limpiadas
echo ========================================
echo.
echo Ahora intenta hacer push de nuevo.
echo Git te pedirá autenticarte con tu cuenta correcta.
echo.
pause

