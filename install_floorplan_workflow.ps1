# ComfyUI Floor Plan Workflow Installation Script (Windows PowerShell)
# Run this script in PowerShell as Administrator from your ComfyUI folder

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "ComfyUI Floor Plan Workflow Installer" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# ComfyUI path - adjust this to your actual ComfyUI installation
$ComfyUIPath = "${env:USERPROFILE}\Downloads\Data\Packages\ComfyUI"
$CustomNodesPath = Join-Path $ComfyUIPath "custom_nodes"

Write-Host "ComfyUI Path: $ComfyUIPath" -ForegroundColor Yellow
Write-Host "Custom Nodes Path: $CustomNodesPath" -ForegroundColor Yellow
Write-Host ""

# Create directories if they don't exist
New-Item -ItemType Directory -Force -Path $CustomNodesPath | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $ComfyUIPath "models\checkpoints") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $ComfyUIPath "models\controlnet") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $ComfyUIPath "models\loras") | Out-Null

# Step 1: Install ComfyUI ControlNet Aux
Write-Host "Step 1: Installing ComfyUI ControlNet Aux (preprocessors)" -ForegroundColor Cyan
Write-Host "----------------------------------------" -ForegroundColor Cyan

$ControlNetAuxPath = Join-Path $CustomNodesPath "ComfyUI-ControlNet-Aux"
if (-not (Test-Path $ControlNetAuxPath)) {
    Write-Host "Installing ComfyUI-ControlNet-Aux..." -ForegroundColor Green
    git clone https://github.com/Fannovel16/ComfyUI-ControlNet-Aux.git $ControlNetAuxPath
    Write-Host "✓ ComfyUI-ControlNet-Aux installed" -ForegroundColor Green
} else {
    Write-Host "✓ ComfyUI-ControlNet-Aux already installed" -ForegroundColor Green
    Set-Location $ControlNetAuxPath
    git pull
    Write-Host "✓ ComfyUI-ControlNet-Aux updated" -ForegroundColor Green
}

# Step 2: Install ComfyUI Manager
Write-Host ""
Write-Host "Step 2: Installing ComfyUI Manager (if not present)" -ForegroundColor Cyan
Write-Host "----------------------------------------" -ForegroundColor Cyan

$ManagerPath = Join-Path $CustomNodesPath "ComfyUI-Manager"
if (-not (Test-Path $ManagerPath)) {
    Write-Host "Installing ComfyUI-Manager..." -ForegroundColor Green
    git clone https://github.com/ltdrdata/ComfyUI-Manager.git $ManagerPath
    Write-Host "✓ ComfyUI-Manager installed" -ForegroundColor Green
} else {
    Write-Host "✓ ComfyUI-Manager already installed" -ForegroundColor Green
    Set-Location $ManagerPath
    git pull
    Write-Host "✓ ComfyUI-Manager updated" -ForegroundColor Green
}

# Step 3: Download ControlNet Union Pro Max
Write-Host ""
Write-Host "Step 3: Downloading ControlNet Union Pro Max (All-in-One)" -ForegroundColor Cyan
Write-Host "----------------------------------------" -ForegroundColor Cyan

$ControlNetPath = Join-Path $ComfyUIPath "models\controlnet\controlnet_union_sdxl_promax.pth"

if (-not (Test-Path $ControlNetPath)) {
    Write-Host "Downloading ControlNet Union Pro Max..." -ForegroundColor Green
    $url = "https://huggingface.co/xinsir/controlnet-union-sdxl-1.0/resolve/main/checkpoint.pth"
    $progressPreference = 'silentlyContinue'
    Invoke-WebRequest -Uri $url -OutFile $ControlNetPath
    Rename-Item $ControlNetPath "controlnet_union_sdxl_promax.pth"
    Write-Host "✓ ControlNet Union Pro Max downloaded" -ForegroundColor Green
} else {
    Write-Host "✓ ControlNet Union Pro Max already exists" -ForegroundColor Green
}

# Step 4: Check for LoRAs
Write-Host ""
Write-Host "Step 4: Checking for LoRAs" -ForegroundColor Cyan
Write-Host "----------------------------------------" -ForegroundColor Cyan

$LoraPath = Join-Path $ComfyUIPath "models\loras\LineDrawing03_CE_ZIMG_AIT4k.safetensors"
$CaipingPath = Join-Path $ComfyUIPath "models\loras\caiping.safetensors"

if (-not (Test-Path $LoraPath)) {
    Write-Host "⚠️  LineDrawing03 LoRA not found" -ForegroundColor Yellow
    Write-Host "Download from: https://civitai.com/models/91033/lineart-controlnet" -ForegroundColor Yellow
    Write-Host "Place in: $LoraPath" -ForegroundColor Yellow
} else {
    Write-Host "✓ LineDrawing03 LoRA found" -ForegroundColor Green
}

if (-not (Test-Path $CaipingPath)) {
    Write-Host "⚠️  caiping LoRA not found" -ForegroundColor Yellow
    Write-Host "Please download and place in: $CaipingPath" -ForegroundColor Yellow
} else {
    Write-Host "✓ caiping LoRA found" -ForegroundColor Green
}

# Step 5: Verify Checkpoint
Write-Host ""
Write-Host "Step 5: Verifying Checkpoint Model" -ForegroundColor Cyan
Write-Host "----------------------------------------" -ForegroundColor Cyan

$CheckpointPath = Join-Path $ComfyUIPath "models\checkpoints\epicrealism_naturalSinRC1VAE.safetensors"

if (-not (Test-Path $CheckpointPath)) {
    Write-Host "⚠️  epicrealism_naturalSinRC1VAE.safetensors not found" -ForegroundColor Yellow
    Write-Host "Download from CivitAI and place in: $CheckpointPath" -ForegroundColor Yellow
} else {
    Write-Host "✓ epicrealism_naturalSinRC1VAE.safetensors found" -ForegroundColor Green
}

# Step 6: Copy Workflow
Write-Host ""
Write-Host "Step 6: Setting up workflow" -ForegroundColor Cyan
Write-Host "----------------------------------------" -ForegroundColor Cyan

$WorkflowSource = "C:\path\to\floorplan_workflow_2025.json"
$WorkflowDest = Join-Path $ComfyUIPath "floorplan_workflow_2025.json"

if (Test-Path $WorkflowSource) {
    Copy-Item $WorkflowSource $WorkflowDest
    Write-Host "✓ Workflow copied to ComfyUI folder" -ForegroundColor Green
} else {
    Write-Host "⚠️  Workflow JSON not found at $WorkflowSource" -ForegroundColor Yellow
    Write-Host "Download from: https://github.com/yourusername/floorplan-workflow" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Installation Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Restart ComfyUI (Ctrl+C and run main.py again)" -ForegroundColor White
Write-Host "2. Open ComfyUI in browser: http://localhost:8188" -ForegroundColor White
Write-Host "3. Upload a floor plan sketch to test" -ForegroundColor White
Write-Host "4. Adjust ControlNet strength if needed (0.5-0.8)" -ForegroundColor White
Write-Host ""
Write-Host "Preprocessor Options:" -ForegroundColor Yellow
Write-Host "  - MLSD (best for straight lines, orthogonal geometry)" -ForegroundColor White
Write-Host "  - Lineart (best for clean sketch lines)" -ForegroundColor White
Write-Host "  - Canny (good for detailed edges, but picks up clutter)" -ForegroundColor White
Write-Host ""
Write-Host "Common Issues:" -ForegroundColor Yellow
Write-Host "  - If Manager doesn't appear, ensure ComfyUI was started with --enable-manager" -ForegroundColor White
Write-Host "  - If nodes show red, restart ComfyUI to load new custom nodes" -ForegroundColor White
Write-Host "  - If ControlNet errors, check the model file is in the correct folder" -ForegroundColor White
Write-Host ""
