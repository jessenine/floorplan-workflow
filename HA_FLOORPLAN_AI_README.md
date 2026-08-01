# Home Assistant Floor Plan Workflow - AI-Powered

## Overview

This workflow generates **interactive, AI-powered Home Assistant floor plans** with **zero manual steps**.

## How It Works

1. **Camera Analysis**: Vision model analyzes HA camera snapshots
2. **ASCII Floor Plan**: Extracts room layout, walls, doors
3. **AI SVG Generation**: `QuiverTextToSVGNode` converts ASCII to interactive SVG
4. **HA-Ready Output**: SVG with proper structure for Home Assistant

## Quick Start (Fully Automated)

The easiest way is to use the automated script:

```bash
# Set up environment
export HA_URL="http://192.168.1.146:8123"
export HA_TOKEN="your_long_lived_token"

# Run the generator
python3 generate_floorplan.py
```

This will:
1. Connect to HA and fetch camera snapshots
2. Analyze each view with the local vision model
3. Generate ASCII floor plan
4. Submit to ComfyUI to create interactive SVG
5. Save to `/media/share/Pidev_proj/image_output_hist/`

## Manual Workflow (ComfyUI)

### Input: Camera Snapshots → ASCII Description

Your vision model outputs a detailed ASCII floor plan like:

```
FLOOR PLAN LAYOUT
=================

FRONT ENTRANCE
┌─────────────────────────────────────────────────────────────────────────────────────┐
│  Front Porch/Entryway                                                               │
│  ┌──────────────┐                                                                   │
│  │  Doorway     │                                                                   │
│  │  (Front)     │                                                                   │
│  └──────┬───────┘                                                                   │
│         │                                                                           │
│         ▼                                                                           │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                        Hallway                                              │   │
│  │  ┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐                      │   │
│  │  │Living │  │Kitchen│  │Garage │  │Storage│  │Pool   │                      │   │
│  │  │Room   │  │      │  │Work-  │  │Closet │  │Area   │                      │   │
│  │  │(Left) │  │      │  │shop   │  │       │  │       │                      │   │
│  │  └───────┘  └───────┘  └───────┘  └───────┘  └───────┘                      │   │
│  └─────────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

### Process: AI Converts to Interactive SVG

The `QuiverTextToSVGNode` takes this ASCII text and generates:
- **Vector paths** for walls, rooms, doors
- **SVG elements** that can be styled
- **Interactive zones** for HA entities

### Output: Home Assistant Compatible SVG

The `SaveSVGNode` saves the SVG to:
```
/media/share/Pidev_proj/image_output_hist/floorplan_homeassistant_*.svg
```

## Quick Start

### Step 1: Run the Automated Script

```bash
cd /media/share/Pidev_proj/floorplan_workflow
python3 generate_floorplan.py
```

Or use the ComfyUI workflow directly:

### Step 1: Run the Automated Script

```bash
cd /media/share/Pidev_proj/floorplan_workflow
python3 generate_floorplan.py
```

This will:
1. Connect to HA and fetch camera snapshots
2. Analyze each view with the local vision model
3. Generate ASCII floor plan
4. Submit to ComfyUI to create interactive SVG
5. Save to `/media/share/Pidev_proj/image_output_hist/`

### Step 2: Deploy to Home Assistant

Copy the SVG to HA:

```bash
# From your Linux machine, copy to HA
scp /media/share/Pidev_proj/image_output_hist/floorplan_homeassistant_*.svg \
    homeassistant:/config/www/floorplan/
```

Or manually copy from Windows if ComfyUI runs there.

## What You Get

### Before (Manual Method):
1. Manually draw floor plan in Inkscape
2. Trace each room
3. Assign entity IDs
4. Write CSS
5. Configure HA YAML

**Time**: 1-2 hours
**Skill required**: Vector graphics, HA configuration

### After (AI Method):
1. Run camera analysis → get ASCII
2. Load workflow → click "Queue Prompt"
3. Deploy SVG to HA

**Time**: 5 minutes
**Skill required**: Basic ComfyUI usage

## HA Entity Integration

The workflow includes entity IDs in the prompt. You can customize:

```
Quiver SVG v1 Max
Prompt: "...Home Assistant compatible with entity IDs for:
  - binary_sensor.living_room
  - binary_sensor.kitchen
  - binary_sensor.garage
  - binary_sensor.pool
  - binary_sensor.backyard
  - light.main_lights"
```

Or add specific entity IDs to the ASCII text:

```
ROOMS WITH HA ENTITY IDS:
1. Living Room → binary_sensor.living_room (window_sensor)
2. Kitchen → binary_sensor.kitchen (motion_sensor)
3. Garage → binary_sensor.garage (door_sensor)
4. Pool → binary_sensor.pool (leak_sensor)
5. Backyard → binary_sensor.backyard (fence_sensor)
```

## SVG Customization

The AI-generated SVG can be further refined in Inkscape if needed:

1. **Add more detail** to room boundaries
2. **Adjust colors** for HA state styling
3. **Add icons** for lights, switches, etc.

## HA Configuration

Minimal HA floorplan configuration:

```yaml
# configuration.yaml
floorplan:
  title: Home
  config:
    image: /local/floorplan/floorplan_homeassistant.svg
    stylesheet: /local/floorplan/floorplan.css
    log_level: info
```

## Comparison: Manual vs AI

| Feature | Manual | AI-Powered |
|---------|--------|------------|
| SVG Creation | Inkscape (1-2 hrs) | AI (5 min) |
| Entity IDs | Manual assignment | AI prompt |
| Layout Accuracy | Precision | AI interpretation |
| Revision Time | Redraw (hrs) | Regenerate (min) |
| Technical Skill | Vector graphics | Basic AI tools |

## Tools

| Tool | Purpose |
|------|---------|
| **ComfyUI** | AI workflow orchestration |
| **QuiverTextToSVGNode** | Text → SVG conversion |
| **SaveSVGNode** | Save SVG to disk |
| **Home Assistant** | Display floor plan |
| **Vision Model** | Camera analysis → ASCII |

## Troubleshooting

### "QuiverTextToSVGNode not found"
- Update ComfyUI to latest version (Quiver nodes are new)
- Check built-in nodes are enabled

### "SVG not interactive in HA"
- Ensure entity IDs match HA sensor names exactly
- Check CSS file is loaded correctly
- Verify SVG path in HA config

### "Room boundaries inaccurate"
- Add more detail to ASCII description
- Use reference images with Quiver node
- Manually refine in Inkscape after generation

## Advanced: Add Reference Images

For more accurate floor plans, you can include reference images:

```python
# Add to workflow (advanced)
# Reference: camera snapshot
# This helps Quiver understand actual room layout
```

## Next Steps

1. **Test the workflow** with your camera analysis output
2. **Verify SVG in HA** - check entity bindings
3. **Customize CSS** for your color scheme
4. **Add more sensors** - lights, switches, cameras

## Example Output

Generated SVG includes:
- Room zones with paths
- Wall outlines
- Door openings
- Entity-ready structure
- HA-compatible naming

## Summary

This workflow removes all manual steps for creating Home Assistant floor plans:

**Input**: Camera analysis → ASCII description  
**Process**: AI generates SVG from text  
**Output**: Interactive HA floor plan

**Total time**: ~5 minutes  
**Manual work**: Zero (after initial setup)
