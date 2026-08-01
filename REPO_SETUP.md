# GitHub Repository Setup for floorplan-workflow

## Repository: pidev9/floorplan-workflow

## Files to include:
- floorplan_workflow_2025.json - Main ComfyUI workflow
- install_floorplan_workflow.ps1 - Windows installation script
- install_floorplan_workflow.sh - Linux/Mac installation script
- download_model.ps1 - Model download helper
- download_model.bat - Model download helper (Windows)
- QUICK_WINDOWS_INSTALL.txt - Quick setup guide
- MANUAL_WINDOWS_INSTALL.txt - Detailed installation guide
- README.md - Project overview

## To create the repository:

1. Go to https://github.com/new
2. Enter repository name: `floorplan-workflow`
3. Make it public or private as desired
4. Click "Create repository"
5. Run these commands in your local directory:

```bash
cd /tmp/floorplan-workflow
git remote add origin https://github.com/pidev9/floorplan-workflow.git
git branch -m main
git push -u origin main
```

Or if you already created the repo:

```bash
git remote add origin https://github.com/pidev9/floorplan-workflow.git
git push -u origin main
```

## .gitignore (optional but recommended):

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so

# Virtual environments
venv/
.env
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Large files (models)
*.pth
*.safetensors
models/

# Log files
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Environment variables
.env
.env.local
.env.*.local
```

## After pushing:

The repository will be live at:
https://github.com/pidev9/floorplan-workflow

You can then share this URL with others, and they can clone it with:
```bash
git clone https://github.com/pidev9/floorplan-workflow.git
```
