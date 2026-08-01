Write-Host "========================================" -ForegroundColor Cyan
Write-Host "ComfyUI Floor Plan - Download Model" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$TargetPath = "C:\Users\shade\ComfyUI\models\controlnet\controlnet_union_sdxl_promax.pth"
$TempPath = "$env:TEMP\checkpoint.pth"
$Url = "https://huggingface.co/xinsir/controlnet-union-sdxl-1.0/resolve/main/checkpoint.pth"

# Check if already installed
if (Test-Path $TargetPath) {
    Write-Host "Model already installed at: $TargetPath" -ForegroundColor Green
    Write-Host "Skipping download." -ForegroundColor Yellow
    return
}

# Create directory if needed
$Dir = Split-Path $TargetPath -Parent
if (-not (Test-Path $Dir)) {
    Write-Host "Creating directory: $Dir" -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $Dir | Out-Null
}

# Download
Write-Host "Downloading ControlNet Union Pro Max..." -ForegroundColor Yellow
Write-Host "URL: $Url" -ForegroundColor Gray
Write-Host "Size: ~2.5 GB" -ForegroundColor Gray
Write-Host "Destination: $TargetPath" -ForegroundColor Gray
Write-Host ""

try {
    Invoke-WebRequest -Uri $Url -OutFile $TempPath -ProgressAction SilentlyContinue
    
    # Move to final location
    Move-Item -Path $TempPath -Destination $TargetPath -Force
    
    Write-Host ""
    Write-Host "SUCCESS! Model downloaded to:" -ForegroundColor Green
    Write-Host "  $TargetPath" -ForegroundColor White
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. Restart ComfyUI (Ctrl+C, then 'python main.py')" -ForegroundColor White
    Write-Host "  2. Load floorplan_workflow_2025.json" -ForegroundColor White
    Write-Host "  3. Upload floor plan sketch and click 'Queue Prompt'" -ForegroundColor White
} catch {
    Write-Host ""
    Write-Host "FAILED to download." -ForegroundColor Red
    Write-Host ""
    Write-Host "Manual download instructions:" -ForegroundColor Yellow
    Write-Host "  1. Open browser: https://huggingface.co/xinsir/controlnet-union-sdxl-1.0" -ForegroundColor White
    Write-Host "  2. Click: checkpoint.pth" -ForegroundColor White
    Write-Host "  3. Click: 'Download' button" -ForegroundColor White
    Write-Host "  4. Move to: C:\Users\shade\ComfyUI\models\controlnet\" -ForegroundColor White
    Write-Host "  5. Rename to: controlnet_union_sdxl_promax.pth" -ForegroundColor White
    Write-Host ""
    Write-Host "Error details:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
}
