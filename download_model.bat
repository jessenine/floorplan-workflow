@echo off
echo ========================================
echo ComfyUI Floor Plan Workflow - Download Helper
echo ========================================
echo.
echo This will download ControlNet Union Pro Max (2.5 GB)
echo.

cd /d "%~dp0"

if exist "controlnet_union_sdxl_promax.pth" (
    echo ControlNet Union Pro Max already exists!
    goto :done
)

echo Downloading ControlNet Union Pro Max...
echo File: checkpoint.pth
echo Size: ~2.5 GB
echo Destination: %~dp0controlnet_union_sdxl_promax.pth
echo.
echo Please wait... this may take several minutes depending on your connection.
echo.

powershell -Command "Invoke-WebRequest -Uri 'https://huggingface.co/xinsir/controlnet-union-sdxl-1.0/resolve/main/checkpoint.pth' -OutFile 'controlnet_union_sdxl_promax.pth'"

if exist "controlnet_union_sdxl_promax.pth" (
    echo.
    echo Download complete!
    echo.
    echo Next steps:
    echo 1. Move controlnet_union_sdxl_promax.pth to:
    echo    C:\Users\shade\ComfyUI\models\controlnet\
    echo 2. Restart ComfyUI
) else (
    echo.
    echo Download failed. Please try manual download:
    echo 1. Open browser: https://huggingface.co/xinsir/controlnet-union-sdxl-1.0
    echo 2. Download: checkpoint.pth
    echo 3. Rename to: controlnet_union_sdxl_promax.pth
    echo 4. Move to: C:\Users\shade\ComfyUI\models\controlnet\
)

:done
pause
