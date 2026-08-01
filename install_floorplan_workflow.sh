#!/bin/bash

# ComfyUI Floor Plan Workflow Installation Script
# This script installs all necessary models and custom nodes for 2D floor plan generation

set -e

echo "========================================"
echo "ComfyUI Floor Plan Workflow Installer"
echo "========================================"
echo ""

# ComfyUI path - adjust this to your actual ComfyUI installation
COMFYUI_PATH="${COMFYUI_PATH:-/home/shade/ComfyUI}"
CUSTOM_NODES_PATH="$COMFYUI_PATH/custom_nodes"

echo "ComfyUI Path: $COMFYUI_PATH"
echo "Custom Nodes Path: $CUSTOM_NODES_PATH"
echo ""

# Create directories if they don't exist
mkdir -p "$CUSTOM_NODES_PATH"
mkdir -p "$COMFYUI_PATH/models/checkpoints"
mkdir -p "$COMFYUI_PATH/models/controlnet"
mkdir -p "$COMFYUI_PATH/models/loras"

echo "Step 1: Installing ComfyUI ControlNet Aux (preprocessors)"
echo "----------------------------------------"

if [ ! -d "$CUSTOM_NODES_PATH/ComfyUI-ControlNet-Aux" ]; then
    echo "Installing ComfyUI-ControlNet-Aux..."
    git clone https://github.com/Fannovel16/ComfyUI-ControlNet-Aux.git "$CUSTOM_NODES_PATH/ComfyUI-ControlNet-Aux"
    echo "✓ ComfyUI-ControlNet-Aux installed"
else
    echo "✓ ComfyUI-ControlNet-Aux already installed"
    cd "$CUSTOM_NODES_PATH/ComfyUI-ControlNet-Aux"
    git pull
    echo "✓ ComfyUI-ControlNet-Aux updated"
fi

echo ""
echo "Step 2: Installing ComfyUI Manager (if not present)"
echo "----------------------------------------"

if [ ! -d "$CUSTOM_NODES_PATH/ComfyUI-Manager" ]; then
    echo "Installing ComfyUI-Manager..."
    git clone https://github.com/ltdrdata/ComfyUI-Manager.git "$CUSTOM_NODES_PATH/ComfyUI-Manager"
    echo "✓ ComfyUI-Manager installed"
else
    echo "✓ ComfyUI-Manager already installed"
    cd "$CUSTOM_NODES_PATH/ComfyUI-Manager"
    git pull
    echo "✓ ComfyUI-Manager updated"
fi

echo ""
echo "Step 3: Downloading ControlNet Union Pro Max (All-in-One)"
echo "----------------------------------------"

CONTROLNET_PATH="$COMFYUI_PATH/models/controlnet/controlnet_union_sdxl_promax.pth"

if [ ! -f "$CONTROLNET_PATH" ]; then
    echo "Downloading ControlNet Union Pro Max..."
    # Using wget with retry
    wget -c --retry-connrefused --timeout=30 \
        "https://huggingface.co/xinsir/controlnet-union-sdxl-1.0/resolve/main/checkpoint.pth" \
        -O "$CONTROLNET_PATH"
    echo "✓ ControlNet Union Pro Max downloaded"
else
    echo "✓ ControlNet Union Pro Max already exists"
fi

echo ""
echo "Step 4: Downloading LineDrawing03 LoRA (if not present)"
echo "----------------------------------------"

LORA_PATH="$COMFYUI_PATH/models/loras/LineDrawing03_CE_ZIMG_AIT4k.safetensors"

if [ ! -f "$LORA_PATH" ]; then
    echo "Downloading LineDrawing03 LoRA..."
    echo "Note: You need to download this from CivitAI manually"
    echo "URL: https://civitai.com/models/91033/lineart-controlnet"
    echo ""
    echo "Or use the caiping LoRA if you have it:"
    CAIPING_PATH="$COMFYUI_PATH/models/loras/caiping.safetensors"
    if [ ! -f "$CAIPING_PATH" ]; then
        echo "caiping.safetensors not found at $CAIPING_PATH"
        echo "Please download it and place it in $COMFYUI_PATH/models/loras/"
    else
        echo "✓ caiping LoRA found"
    fi
else
    echo "✓ LineDrawing03 LoRA already exists"
fi

echo ""
echo "Step 5: Verifying Checkpoint Model"
echo "----------------------------------------"

CHECKPOINT_PATH="$COMFYUI_PATH/models/checkpoints/epicrealism_naturalSinRC1VAE.safetensors"

if [ ! -f "$CHECKPOINT_PATH" ]; then
    echo "⚠️  epicrealism_naturalSinRC1VAE.safetensors not found"
    echo "Please download it from CivitAI and place it in:"
    echo "$CHECKPOINT_PATH"
else
    echo "✓ epicrealism_naturalSinRC1VAE.safetensors found"
fi

echo ""
echo "Step 6: Downloading Workflow JSON"
echo "----------------------------------------"

WORKFLOW_PATH="/home/shade/Pidev_proj/workflow_hist/floorplan_workflow_2025.json"

if [ -f "$WORKFLOW_PATH" ]; then
    echo "✓ Workflow JSON already exists at $WORKFLOW_PATH"
else
    echo "Workflow JSON not found. Please download from:"
    echo "https://github.com/yourusername/floorplan-workflow/raw/main/floorplan_workflow_2025.json"
fi

echo ""
echo "========================================"
echo "Installation Complete!"
echo "========================================"
echo ""
echo "Next Steps:"
echo "1. Restart ComfyUI (Ctrl+C and run main.py again)"
echo "2. Open ComfyUI in browser: http://localhost:8188"
echo "3. Upload a floor plan sketch to test"
echo "4. Adjust ControlNet strength if needed (0.5-0.8)"
echo ""
echo "Preprocessor Options:"
echo "  - MLSD (best for straight lines, orthogonal geometry)"
echo "  - Lineart (best for clean sketch lines)"
echo "  - Canny (good for detailed edges, but picks up clutter)"
echo ""
echo "Common Issues:"
echo "  - If Manager doesn't appear, ensure ComfyUI was started with --enable-manager"
echo "  - If nodes show red, restart ComfyUI to load new custom nodes"
echo "  - If ControlNet errors, check the model file is in the correct folder"
echo ""
echo "For questions, see: /home/shade/Pidev_proj/workflow_hist/README.md"
