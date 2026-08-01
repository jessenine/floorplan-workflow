# Floor Plan Workflow

ComfyUI workflow for generating 2D floor plans using ControlNet Union Pro Max and MLSD preprocessor.

## 📦 What's Included

- **floorplan_workflow_2025.json** - Complete ComfyUI workflow ready to import
- **Installation scripts** - Automated setup for Windows, Linux, and Mac
- **Model download helpers** - Scripts to download ControlNet Union Pro Max
- **Documentation** - Multiple guides for different installation methods

## 🚀 Quick Start

1. Copy all files to your ComfyUI folder
2. Run `install_floorplan_workflow.ps1` (Windows) or `./install_floorplan_workflow.sh` (Linux/Mac)
3. Download ControlNet Union Pro Max (2.5 GB) using `download_model.ps1`
4. Restart ComfyUI
5. Load `floorplan_workflow_2025.json`

## 📖 Documentation

- **QUICK_WINDOWS_INSTALL.txt** - 5-minute setup for Windows
- **MANUAL_WINDOWS_INSTALL.txt** - Detailed installation guide
- **download_model.ps1** - PowerShell script to download the model
- **download_model.bat** - Batch file to download the model

## 🔧 Requirements

- ComfyUI installed and running
- Git (for installation scripts)
- ControlNet Union Pro Max model (~2.5 GB)
- Python 3.8+ with PyTorch

## 🎯 Workflow Settings

- **Resolution**: 1024x1024
- **Steps**: 30
- **CFG Scale**: 6.0
- **Sampler**: dpmpp_2m_sde_gpu
- **Strength**: 0.65
- **Preprocessor**: MLSD

## 📄 License

This project is provided as-is for educational and personal use.

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## 📧 Support

For issues or questions, please open an issue on GitHub.

---

**Happy Floor Planning!** 🏠
