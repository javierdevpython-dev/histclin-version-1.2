# Script para agregar Git al PATH permanentemente
# Ejecutar como Administrador

$gitPath = "C:\Program Files\Git\bin"
$currentPath = [Environment]::GetEnvironmentVariable("Path", "Machine")

if ($currentPath -notlike "*$gitPath*") {
    [Environment]::SetEnvironmentVariable("Path", "$currentPath;$gitPath", "Machine")
    Write-Host "✅ Git agregado al PATH del sistema" -ForegroundColor Green
    Write-Host "Reinicia tu terminal para que los cambios surtan efecto" -ForegroundColor Yellow
} else {
    Write-Host "✅ Git ya está en el PATH" -ForegroundColor Green
}

Write-Host "`nPara verificar, reinicia PowerShell y ejecuta: git --version" -ForegroundColor Cyan

