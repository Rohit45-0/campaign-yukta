# Simple Deployment Script for Windows
# Run this in PowerShell

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "YuktaMedia Deal Extractor - Deployment" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Build Frontend
Write-Host "`n[1/3] Building Frontend..." -ForegroundColor Yellow
Set-Location frontend
npm run build
Set-Location ..

# Create dist folder
Write-Host "`n[2/3] Creating distribution..." -ForegroundColor Yellow
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
New-Item -ItemType Directory -Path "dist"
New-Item -ItemType Directory -Path "dist/backend"
New-Item -ItemType Directory -Path "dist/frontend"

# Copy backend
Copy-Item "backend/*.py" "dist/backend/"
Copy-Item "backend/requirements.txt" "dist/backend/"

# Copy frontend build
Copy-Item -Recurse "frontend/build/*" "dist/frontend/"

# Create start script
$startScript = @"
@echo off
echo Starting YuktaMedia Deal Extractor...
echo.
echo Backend: http://127.0.0.1:8000
echo Frontend: Open dist/frontend/index.html in browser
echo.
cd backend
start python -m uvicorn main:app --host 127.0.0.1 --port 8000
cd ..
timeout /t 3
start "" "frontend/index.html"
"@
Set-Content -Path "dist/start.bat" -Value $startScript

Write-Host "`n[3/3] Done!" -ForegroundColor Green
Write-Host "`nDistribution created in 'dist' folder" -ForegroundColor Cyan
Write-Host "Share the 'dist' folder with your client" -ForegroundColor Cyan
Write-Host "`nTo run: Execute dist/start.bat" -ForegroundColor Yellow
