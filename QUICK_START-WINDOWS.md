# Quick Start: ComfyUI Floor Plan Workflow

## 30-Second Setup

### Windows Users
```powershell
cd "C:\Users\shade\Downloads\Data\Packages\ComfyUI"
.\install_floorplan_workflow.ps1
```

### Linux/Mac Users
```bash
cd ~/ComfyUI
./install_floorplan_workflow.sh
```

## What Gets Installed

| Component | Size | Purpose |
|-----------|------|---------|
| **ComfyUI ControlNet Aux** | ~200 MB | MLSD, Lineart, Canny preprocessor nodes |
| **ComfyUI Manager** | <10 MB | Node/model manager (optional) |
| **ControlNet Union Pro Max** | 2.5 GB | All-in-one ControlNet model |

## 5-Step Usage

1. **Restart ComfyUI**
   ```bash
   python main.py --listen 0.0.0.0
   ```

2. **Open http://localhost:8188**

3. **Load workflow**
   - Menu → Load Workflow → Select `floorplan_workflow_2025.json`
   - OR drag the JSON file onto the canvas

4. **Upload floor plan**
   - Click Load Image node
   - Select your floor plan sketch
   - Black lines on white background works best

5. **Run**
   - Click "Queue Prompt" (bottom right)
   - Wait ~30 seconds
   - View result in SaveImage node

## Default Settings (Ready to Use)

- **Resolution**: 1024x1024
- **Steps**: 30
- **CFG**: 6.0
- **Sampler**: dpmpp_2m_sde_gpu
- **ControlNet Strength**: 0.65
- **Preprocessor**: mlsd

## Need Adjustments?

| Problem | Fix |
|---------|-----|
| Walls drifting | Increase strength: `0.65 → 0.75` |
| Over-processed | Decrease strength: `0.65 → 0.5` |
| Too slow | Reduce steps: `30 → 20`, resolution: `1024 → 768` |

## Preprocessor Options

| Name | Use For | Best For |
|------|---------|----------|
| `mlsd` | Orthogonal walls | Architectural plans with right angles |
| `lineart` | Clean sketches | Hand-drawn or scanned plans |
| `canny` | Detailed edges | High-contrast line work |

## Prompt Templates

**Positive:**
```
2D floor plan, top-down view, architectural line drawing, 
clean white background, black lines, walls, rooms, doors, 
furniture layout, blueprint style, simple lines, no shading, 
minimal details, orthographic, plan view
```

**Negative:**
```
3D perspective, isometric, shaded, colored, textured, 
photorealistic, realistic, clutter, text, dimensions, 
people, furniture details, 3d view, depth, shadows
```

## Expected Results

| Seed | Strength | Result |
|------|----------|--------|
| `12345` | `0.65` | Balanced, clean lines |
| `67890` | `0.75` | Detailed, slightly over-processed |
| `11111` | `0.65` | Presentation-ready |
| `99999` | `0.55` | Creative, more variation |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Model not found | Check `models/controlnet/controlnet_union_sdxl_promax.pth` exists |
| Red nodes | Restart ComfyUI (loads new custom nodes) |
| Manager not visible | Ensure `--enable-manager` flag in startup command |
| Slow generation | Reduce steps to 20, resolution to 768x768 |

## Where Files Go

| File Type | Path |
|-----------|------|
| Checkpoints | `ComfyUI/models/checkpoints/` |
| ControlNets | `ComfyUI/models/controlnet/` |
| LoRAs | `ComfyUI/models/loras/` |
| Custom Nodes | `ComfyUI/custom_nodes/` |

## What's Next?

After getting the basic workflow working:

1. **Try different preprocessor** (mlsd vs lineart)
2. **Adjust strength** for tighter/looser control
3. **Add LoRA** for style variation (LineDrawing03 or caiping)
4. **Export workflow** to share with others

## Need More Help?

- **Full documentation**: `README.md`
- **Setup summary**: `FLOOR_PLAN_WORKFLOW_SUMMARY.md`
- **ComfyUI Manager**: Press `M` in ComfyUI or Settings → Manager
- **Custom Nodes Manager**: Settings → Custom Nodes

## Success Criteria

You'll know it's working when you see:
- ✅ ControlNet nodes show black/green (no red)
- ✅ "Queue Prompt" button is clickable
- ✅ Generation completes in ~30 seconds
- ✅ Output looks like a clean floor plan (not 3D, not distorted)

## Common Mistakes

❌ Forgetting to restart ComfyUI after installing custom nodes  
❌ Using colored input images (should be black/white)  
❌ Setting ControlNet strength too high (>0.9)  
❌ Using Canny for floor plans (use MLSD or Lineart)  
❌ Expecting 3D output from 2D plan (ControlNet needs depth map for 3D)

## Pro Tips

- **Fast testing**: Use 768x768, 20 steps, CFG=5.0
- **Better quality**: Use 1024x1024, 40 steps, CFG=6.5
- **Cleaner lines**: Use MLSD preprocessor with strength 0.7
- **More creative**: Use caiping LoRA at 0.4 strength
- **Faster**: Use euler_a sampler instead of dpmpp

---

**Ready to start?** Run `.\install_floorplan_workflow.ps1` (Windows) or `./install_floorplan_workflow.sh` (Linux/Mac)
