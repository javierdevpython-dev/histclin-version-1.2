# Script para subir archivos a GitHub
# Este script limpia credenciales y hace push

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  SUBIR ARCHIVOS A GITHUB" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Agregar Git al PATH
$env:Path += ";C:\Program Files\Git\bin"

# Verificar Git
try {
    $gitVersion = git --version
    Write-Host "[OK] Git encontrado: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Git no está disponible" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "1. Agregando archivos nuevos..." -ForegroundColor Yellow
git add .
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Archivos agregados" -ForegroundColor Green
} else {
    Write-Host "[ERROR] No se pudieron agregar archivos" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "2. Verificando cambios..." -ForegroundColor Yellow
$status = git status --short
if ($status) {
    Write-Host "Cambios detectados:" -ForegroundColor Cyan
    Write-Host $status
    Write-Host ""
    Write-Host "3. Haciendo commit..." -ForegroundColor Yellow
    git commit -m "Actualizar proyecto para PostgreSQL y Render"
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Commit realizado" -ForegroundColor Green
    } else {
        Write-Host "[INFO] No hay cambios para commitear" -ForegroundColor Yellow
    }
} else {
    Write-Host "[INFO] No hay cambios nuevos" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "4. Subiendo a GitHub..." -ForegroundColor Yellow
Write-Host "   (Si te pide credenciales, usa tu usuario de GitHub)" -ForegroundColor Cyan
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
    Write-Host "  ERROR AL SUBIR" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Posibles soluciones:" -ForegroundColor Yellow
    Write-Host "1. Verifica que tengas permisos en el repositorio" -ForegroundColor White
    Write-Host "2. Usa un Personal Access Token como contraseña" -ForegroundColor White
    Write-Host "3. Ve a: GitHub.com -> Settings -> Developer settings -> Personal access tokens" -ForegroundColor White
    Write-Host ""
}

Write-Host ""
pause

