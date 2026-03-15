[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("start", "stop", "db-migrate", "lint", "scaffold", "test")]
    [string]$Action,

    [Parameter(Mandatory=$false)]
    [string]$Target
)

$RootDir = Get-Location
$BackendDir = "$RootDir\backend"
$FrontendDir = "$RootDir\frontend"

function Start-Dev {
    Write-Host "🚀 Starting High-Productivity Environment..." -ForegroundColor Cyan
    
    # 1. Start Infrastructure
    Write-Host "📦 Starting Infrastructure (Postgres + pgvector)..."
    docker-compose up -d
    
    # 2. Sync Backend
    Write-Host "🐍 Syncing Backend Dependencies with uv..."
    Set-Location $BackendDir
    & .\.venv312\Scripts\uv.exe pip sync requirements_uv.txt | Out-Null
    
    # 3. Start Processes
    Write-Host "📡 Launching Backend & Frontend..."
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; `$env:PYTHONPATH='.'; .\.venv312\Scripts\python.exe -m uvicorn app.main:app --reload" -WindowStyle Normal
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev -- --turbo" -WindowStyle Normal
    
    Write-Host "✅ System is up! Backend: :8000 | Frontend: :3000" -ForegroundColor Green
}

function Run-Lint {
    Write-Host "🧹 Linting Codebase..." -ForegroundColor Yellow
    Set-Location $BackendDir
    & .\.venv312\Scripts\uv.exe run ruff check . --fix
    Set-Location $FrontendDir
    npm run lint:fix
    Write-Host "✨ Clean!" -ForegroundColor Green
}

function Run-Test {
    Write-Host "🧪 Running Backend Tests..." -ForegroundColor Cyan
    Set-Location $BackendDir
    & .\.venv312\Scripts\uv.exe run pytest
    Write-Host "🏁 Tests Completed!" -ForegroundColor Green
}

switch ($Action) {
    "start" { Start-Dev }
    "lint"  { Run-Lint }
    "test"  { Run-Test }
    "stop"  { docker-compose down }
    "scaffold" { Write-Host "Scaffolding $Target... (Not implemented yet)" }
    Default { Write-Host "Unknown action" }
}
