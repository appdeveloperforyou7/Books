# One-click setup for local Bonsai Image generation on Windows.
# Clones the demo repo, installs dependencies, downloads model.
#
# Usage:
#   Set-ExecutionPolicy -Scope CurrentUser RemoteSigned   # one-time
#   .\setup_bonsai_local.ps1

$ErrorActionPreference = 'Stop'
$ScriptDir = $PSScriptRoot
Set-Location $ScriptDir

Write-Host ""
Write-Host "========================================="
Write-Host "  Bonsai Image — Local Setup (Windows)"
Write-Host "========================================="
Write-Host ""

# Step 1: Clone Bonsai-Image-Demo
$demoDir = Join-Path $ScriptDir "Bonsai-Image-Demo"
if (Test-Path (Join-Path $demoDir ".git")) {
    Write-Host "  [OK] Bonsai-Image-Demo already cloned" -ForegroundColor Green
} else {
    Write-Host "  [1/3] Cloning Bonsai-Image-Demo..." -ForegroundColor Cyan
    git clone https://github.com/PrismML-Eng/Bonsai-Image-Demo.git $demoDir
    if ($LASTEXITCODE -ne 0) { Write-Host "  git clone failed" -ForegroundColor Red; exit 1 }
}

# Step 2: Run official setup
$venvPy = Join-Path $demoDir ".venv\Scripts\python.exe"
if (Test-Path $venvPy) {
    Write-Host "  [OK] venv already exists" -ForegroundColor Green
} else {
    Write-Host "  [2/3] Running official setup.ps1 (installs torch, gemlite, etc.)..." -ForegroundColor Cyan
    Write-Host "        This takes 5-10 minutes on first run." -ForegroundColor DarkGray
    Push-Location $demoDir
    try {
        powershell -ExecutionPolicy Bypass -File .\setup.ps1
    } finally {
        Pop-Location
    }
}

# Step 3: Verify
Write-Host ""
Write-Host "  [3/3] Verifying installation..." -ForegroundColor Cyan

if (-not (Test-Path $venvPy)) {
    Write-Host "  ERROR: venv not found at $venvPy" -ForegroundColor Red
    Write-Host "  Try running manually: cd Bonsai-Image-Demo && .\setup.ps1" -ForegroundColor Yellow
    exit 1
}

$check = & $venvPy -c @"
import torch
print(f'torch {torch.__version__}, CUDA: {torch.cuda.is_available()}')
if torch.cuda.is_available():
    print(f'GPU: {torch.cuda.get_device_name(0)}')
    print(f'VRAM: {torch.cuda.get_device_properties(0).total_mem / 1024**2:.0f} MB')
"@ 2>&1

Write-Host "  $check" -ForegroundColor White

$modelDir = Join-Path $demoDir "models"
if (Test-Path $modelDir) {
    $models = Get-ChildItem $modelDir -Directory
    if ($models) {
        Write-Host "  Models downloaded:" -ForegroundColor Green
        $models | ForEach-Object { Write-Host "    - $($_.Name)" -ForegroundColor Green }
    } else {
        Write-Host "  No models downloaded yet. Run: cd Bonsai-Image-Demo && .\scripts\download_model.ps1" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  Setup complete!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  To generate images locally:" -ForegroundColor White
Write-Host "    cd Bonsai-Image-Demo" -ForegroundColor Yellow
Write-Host "    .\.venv\Scripts\activate" -ForegroundColor Yellow
Write-Host '    python ..\bonsai_local_generate.py "your prompt here"' -ForegroundColor Yellow
Write-Host ""
Write-Host "  Or use the cloud version (no GPU needed):" -ForegroundColor White
Write-Host '    python bonsai_generate.py "your prompt here"' -ForegroundColor Yellow
Write-Host ""