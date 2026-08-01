# Floor Plan Workflow - Windows Setup Guide

## Files Available (in this folder)

| File | Purpose |
|------|---------|
| **floorplan_workflow_2025.json** | ComfyUI workflow to import |
| **install_floorplan.bat** | Easy installer (double-click to run) |
| **install_floorplan_workflow.ps1** | PowerShell installation script |
| **SETUP_COMPLETE.txt** | Detailed installation instructions |

## Quick Start (Recommended)

### Option 1: Easy Install (Double-click)
1. Double-click `install_floorplan.bat`
2. Wait for installation to complete
3. Restart ComfyUI
4. Load `floorplan_workflow_2025.json`

### Option 2: Manual Install
1. Open PowerShell as Administrator in `C:\Users\shade\Downloads\Data\Packages\ComfyUI`
2. Run: `.\install_floorplan_workflow.ps1`
3. Restart ComfyUI
4. Load `floorplan_workflow_2025.json`

## What Gets Installed

### Custom Nodes (~210 MB)
1. **ComfyUI ControlNet Aux** - Provides MLSD, Lineart, Canny preprocessors
2. **ComfyUI Manager** - Optional, makes node management easier

### Models (~2.5 GB)
1. **ControlNet Union Pro Max** - All-in-one ControlNet model

## Default Workflow Settings

- **Resolution**: 1024x1024
- **Steps**: 30
- **Strength**: 0.65
- **Preprocessor**: MLSD

## Troubleshooting

- **"git not found"**: Install Git for Windows from https://git-scm.com/download/win
- **"PowerShell not found"**: Already included in Windows 10/11
- **"Access denied"**: Run PowerShell as Administrator

## Next Steps

After installation:
1. Restart ComfyUI (Ctrl+C then `python main.py`)
2. Open http://localhost:8188
3. Load `floorplan_workflow_2025.json`
4. Upload a floor plan sketch (black lines on white)
5. Click "Queue Prompt"

## Need Help?

Check **SETUP_COMPLETE.txt** for detailed instructions.

---

**Files copied from**: `/media/share/Pidev_proj/`
