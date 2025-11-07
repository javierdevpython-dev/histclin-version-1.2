# Script para instalar y configurar la base de datos PostgreSQL
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  INSTALAR BASE DE DATOS POSTGRESQL" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar si PostgreSQL está instalado
Write-Host "1. Verificando PostgreSQL..." -ForegroundColor Yellow
$postgresService = Get-Service -Name postgresql* -ErrorAction SilentlyContinue

if ($postgresService) {
    Write-Host "[OK] PostgreSQL está instalado" -ForegroundColor Green
    $status = $postgresService | Select-Object -First 1 | Select-Object -ExpandProperty Status
    if ($status -eq "Running") {
        Write-Host "[OK] PostgreSQL está corriendo" -ForegroundColor Green
    } else {
        Write-Host "[ADVERTENCIA] PostgreSQL no está corriendo" -ForegroundColor Yellow
        Write-Host "   Intentando iniciar..." -ForegroundColor Yellow
        try {
            Start-Service -Name $postgresService[0].Name
            Write-Host "[OK] PostgreSQL iniciado" -ForegroundColor Green
        } catch {
            Write-Host "[ERROR] No se pudo iniciar PostgreSQL" -ForegroundColor Red
            Write-Host "   Inícialo manualmente desde Servicios de Windows" -ForegroundColor Yellow
        }
    }
} else {
    Write-Host "[ERROR] PostgreSQL no está instalado" -ForegroundColor Red
    Write-Host ""
    Write-Host "Para instalar PostgreSQL:" -ForegroundColor Yellow
    Write-Host "1. Descarga desde: https://www.postgresql.org/download/windows/" -ForegroundColor White
    Write-Host "2. O usa: winget install PostgreSQL.PostgreSQL" -ForegroundColor White
    Write-Host ""
    Write-Host "Después de instalar, ejecuta este script de nuevo." -ForegroundColor Yellow
    pause
    exit
}

Write-Host ""
Write-Host "2. Verificando archivo .env..." -ForegroundColor Yellow

if (Test-Path ".env") {
    Write-Host "[OK] Archivo .env existe" -ForegroundColor Green
    Write-Host ""
    Write-Host "Verifica que tenga estas variables configuradas:" -ForegroundColor Cyan
    Write-Host "  - POSTGRES_HOST=localhost" -ForegroundColor White
    Write-Host "  - POSTGRES_PORT=5432" -ForegroundColor White
    Write-Host "  - POSTGRES_USER=postgres" -ForegroundColor White
    Write-Host "  - POSTGRES_PASSWORD=tu_contraseña" -ForegroundColor White
    Write-Host "  - POSTGRES_DB=medisoft_db" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host "[ADVERTENCIA] Archivo .env no existe" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Creando archivo .env desde env_example.txt..." -ForegroundColor Yellow
    
    if (Test-Path "env_example.txt") {
        Copy-Item "env_example.txt" ".env"
        Write-Host "[OK] Archivo .env creado" -ForegroundColor Green
        Write-Host ""
        Write-Host "⚠️  IMPORTANTE: Edita el archivo .env y configura:" -ForegroundColor Red
        Write-Host "   - POSTGRES_PASSWORD: Tu contraseña de PostgreSQL" -ForegroundColor White
        Write-Host "   - SECRET_KEY: Una clave secreta aleatoria" -ForegroundColor White
        Write-Host ""
        Write-Host "Presiona Enter cuando hayas editado el archivo .env..." -ForegroundColor Yellow
        pause
    } else {
        Write-Host "[ERROR] No se encontró env_example.txt" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "3. Verificando dependencias de Python..." -ForegroundColor Yellow

try {
    $python = Get-Command python -ErrorAction Stop
    Write-Host "[OK] Python encontrado: $($python.Version)" -ForegroundColor Green
    
    Write-Host "   Verificando psycopg2..." -ForegroundColor Cyan
    $psycopg2 = python -c "import psycopg2; print('OK')" 2>$null
    if ($psycopg2 -eq "OK") {
        Write-Host "[OK] psycopg2 está instalado" -ForegroundColor Green
    } else {
        Write-Host "[ADVERTENCIA] psycopg2 no está instalado" -ForegroundColor Yellow
        Write-Host "   Instalando..." -ForegroundColor Yellow
        python -m pip install psycopg2-binary
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[OK] psycopg2 instalado" -ForegroundColor Green
        } else {
            Write-Host "[ERROR] No se pudo instalar psycopg2" -ForegroundColor Red
        }
    }
} catch {
    Write-Host "[ERROR] Python no está disponible" -ForegroundColor Red
    Write-Host "   Instala Python desde: https://www.python.org/downloads/" -ForegroundColor Yellow
    pause
    exit
}

Write-Host ""
Write-Host "4. Creando base de datos..." -ForegroundColor Yellow
Write-Host "   Ejecutando: python create_postgres_db.py" -ForegroundColor Cyan
Write-Host ""

python create_postgres_db.py

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  ¡BASE DE DATOS INSTALADA!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Próximos pasos:" -ForegroundColor Cyan
    Write-Host "1. Verifica la instalación: python check_db.py" -ForegroundColor White
    Write-Host "2. Inicia la aplicación: python app.py" -ForegroundColor White
    Write-Host "3. Accede a: http://localhost:5000" -ForegroundColor White
    Write-Host ""
    Write-Host "Credenciales:" -ForegroundColor Cyan
    Write-Host "  Usuario: admin" -ForegroundColor White
    Write-Host "  Contraseña: admin123" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "  ERROR AL CREAR BASE DE DATOS" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Revisa:" -ForegroundColor Yellow
    Write-Host "1. Que PostgreSQL esté corriendo" -ForegroundColor White
    Write-Host "2. Que las credenciales en .env sean correctas" -ForegroundColor White
    Write-Host "3. Que el usuario 'postgres' tenga permisos" -ForegroundColor White
}

Write-Host ""
pause

