# Script para limpiar credenciales y subir a GitHub
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  LIMPIAR CREDENCIALES Y SUBIR A GITHUB" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Agregar Git al PATH
$env:Path += ";C:\Program Files\Git\bin"

Write-Host "1. Limpiando credenciales guardadas..." -ForegroundColor Yellow

# Limpiar credenciales de Git
git config --global --unset credential.helper
git config --global credential.helper ""

# Limpiar credenciales de Windows relacionadas con GitHub
$creds = cmdkey /list 2>$null | Select-String -Pattern "github|git" -CaseSensitive:$false
if ($creds) {
    Write-Host "   Encontradas credenciales de GitHub" -ForegroundColor Yellow
    Write-Host "   Necesitas eliminarlas manualmente:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "   Pasos:" -ForegroundColor Cyan
    Write-Host "   1. Presiona Win + R" -ForegroundColor White
    Write-Host "   2. Escribe: control /name Microsoft.CredentialManager" -ForegroundColor White
    Write-Host "   3. Ve a 'Credenciales de Windows'" -ForegroundColor White
    Write-Host "   4. Busca y elimina entradas de 'GitHub' o 'git'" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host "   No se encontraron credenciales guardadas" -ForegroundColor Green
}

Write-Host ""
Write-Host "2. Agregando archivos..." -ForegroundColor Yellow
git add .
Write-Host "[OK] Archivos agregados" -ForegroundColor Green

Write-Host ""
Write-Host "3. Verificando commits..." -ForegroundColor Yellow
$commitsAhead = git rev-list --count origin/main..HEAD 2>$null
if ($commitsAhead -gt 0) {
    Write-Host "   Hay $commitsAhead commit(s) para subir" -ForegroundColor Cyan
} else {
    Write-Host "   No hay commits nuevos" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "4. Intentando subir a GitHub..." -ForegroundColor Yellow
Write-Host ""
Write-Host "   IMPORTANTE:" -ForegroundColor Red
Write-Host "   - Si te pide usuario: usa 'jmora19921002'" -ForegroundColor White
Write-Host "   - Si te pide contraseña: usa un Personal Access Token" -ForegroundColor White
Write-Host "   - NO uses tu contraseña normal de GitHub" -ForegroundColor White
Write-Host ""
Write-Host "   Para crear un token:" -ForegroundColor Cyan
Write-Host "   GitHub.com -> Settings -> Developer settings -> Personal access tokens" -ForegroundColor White
Write-Host ""

# Intentar push
git push origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  ¡ÉXITO! Archivos subidos a GitHub" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Repositorio: https://github.com/jmora19921002/histclin-version-1.2" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "  ERROR: No se pudo subir" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "SOLUCIÓN:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "1. Abre el Administrador de Credenciales de Windows:" -ForegroundColor White
    Write-Host "   Win + R -> control /name Microsoft.CredentialManager" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "2. Elimina todas las credenciales de 'GitHub' o 'git'" -ForegroundColor White
    Write-Host ""
    Write-Host "3. Crea un Personal Access Token en GitHub:" -ForegroundColor White
    Write-Host "   - GitHub.com -> Settings -> Developer settings" -ForegroundColor Cyan
    Write-Host "   - Personal access tokens -> Tokens (classic)" -ForegroundColor Cyan
    Write-Host "   - Generate new token -> Marca 'repo'" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "4. Ejecuta este script de nuevo" -ForegroundColor White
    Write-Host "   Cuando pida contrasena, usa el TOKEN (no tu contrasena)" -ForegroundColor White
}

Write-Host ""
pause

