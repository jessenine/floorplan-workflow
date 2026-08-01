# Home Assistant Floor Plan Workflow - Complete Guide

## Overview

This workflow generates **interactive Home Assistant floor plans** from ASCII floor plan descriptions. **No manual drawing required!**

## How It Works

1. **ASCII Floor Plan** → Simple text-based layout
2. **Parser Script** (`ascii_to_svg.py`) → Converts to SVG
3. **HA-Ready Output** → SVG with entity IDs for Home Assistant

## Quick Start

### Method 1: Automated (Camera Analysis → ASCII → SVG)

```bash
# 1. Run camera analysis to generate ASCII
python3 /media/share/Pidev_proj/floorplan_workflow/generate_floorplan.py

# 2. The script automatically generates SVG from the ASCII output
```

### Method 2: Manual (ASCII → SVG)

```bash
# 1. Create your ASCII floor plan (see example below)
# 2. Generate SVG
python3 /media/share/Pidev_proj/floorplan_workflow/ascii_to_svg.py

# 3. Or with specific ASCII file
python3 /media/share/Pidev_proj/floorplan_workflow/ascii_to_svg.py /path/to/floorplan.txt
```

## ASCII Floor Plan Format

Create a simple text file with numbered rooms:

```
FLOOR PLAN LAYOUT
=================

1. Front Porch/Entryway - Entry from street, coat closet
2. Hallway - Main spine connecting all areas  
3. Living Room - Left of hallway, large window
4. Kitchen - Adjacent to living room
5. Garage/Workshop - Right of hallway
6. Backyard Garden - Garden beds, pathway
7. Pool Area - In-ground pool, deck

WALLS: 20px thick, black lines
DOORS: Gaps in walls (80-90px wide)
```

### Room Naming Rules

- Room names are automatically converted to entity IDs
- Spaces become underscores: "Living Room" → `binary_sensor.living_room`
- Special characters removed: "G6 Pool-Pond" → `binary_sensor.g6_pool_pond`

## Generated SVG

The script generates an SVG with:

- **Room zones** as rectangles with entity IDs
- **Wall outlines** as solid lines
- **Door openings** as dashed lines
- **Room labels** (name)
- **Entity labels** (HA sensor ID)
- **CSS styling** for hover/on/off states

### SVG Structure Example

```xml
<svg width="800" height="600" viewBox="0 0 800 600">
  <style type="text/css">
    .room { fill: #f0f0f0; stroke: #333; }
    .room:hover { fill: #e0e0e0; }
    .room.on { fill: #4CAF50; }
    .room.off { fill: #9E9E9E; }
    .wall { stroke: #333; stroke-width: 4; }
    .label { font-family: Arial; font-size: 14px; }
  </style>
  
  <!-- Room with entity ID -->
  <rect 
    id="binary_sensor.living_room" 
    class="room" 
    x="50" y="80" width="200" height="150" 
  />
  <text x="60" y="100" class="label">Living Room</text>
  <text x="60" y="120" class="entity-id">binary_sensor.living_room</text>
</svg>
```

## Deploy to Home Assistant

### Step 1: Copy SVG to HA

```bash
# From your Linux machine
scp /media/share/Pidev_proj/image_output_hist/floorplan_homeassistant.svg \
    homeassistant:/config/www/floorplan/
```

### Step 2: Configure HA Floorplan

Create or update `floorplan.yaml` in your HA config directory:

```yaml
floorplan:
  title: Home
  config:
    image: /local/floorplan/floorplan_homeassistant.svg
    stylesheet: /local/floorplan/floorplan.css
    log_level: info
```

### Step 3: Create CSS (Optional)

```css
/* floorplan.css */
/* Turn on lights when sensor is on */
#binary_sensor.living_room.on { fill: #FFD700; }
#binary_sensor.kitchen.on { fill: #FFD700; }
#binary_sensor.garage.on { fill: #FFD700; }

/* Show doorbell when triggered */
#binary_sensor.doorbell.on { fill: #FF4500; }
```

## Files in This Workflow

| File | Purpose |
|------|---------|
| `ascii_to_svg.py` | **Main script** - Converts ASCII to HA SVG |
| `generate_floorplan.py` | Camera analysis + ASCII generation |
| `floorplan_workflow_ha_svg.json` | ComfyUI workflow (Quiver API - has issues) |
| `HA_FLOORPLAN_README.md` | Original HA documentation |
| `HA_FLOORPLAN_AI_README.md` | AI-powered workflow guide |
| `QUIVER_API_NOTES.md` | Quiver API troubleshooting |

## Comparison

| Method | Time | Skill Required | Output |
|--------|------|----------------|--------|
| **Manual (Inkscape)** | 1-2 hours | Vector graphics | Static SVG |
| **Quiver API** | 5 min | AI tools | AI-generated SVG |
| **ascii_to_svg.py** | 2 min | Text editing | Structured SVG |

## Troubleshooting

### "No module named 'svgwrite'"
The script uses only Python standard library - no external dependencies needed!

### "Permission denied" when writing to HA
Use SSH key authentication or run from within HA:

```bash
# Copy from within HA container
docker cp floorplan_homeassistant.svg homeassistant:/config/www/floorplan/
```

### SVG not showing in HA
- Check file path in `floorplan.yaml` matches actual location
- Verify SVG loads in browser (open `/local/floorplan/floorplan_homeassistant.svg`)
- Clear HA cache: Developer Tools → Clear Cache

## Advanced: Custom Entity IDs

Modify `ascii_to_svg.py` to use custom naming:

```python
# Change from:
entity_id = f'binary_sensor.{room_name.lower().replace(" ", "_")}'

# To custom pattern:
entity_id = f'binary_sensor.{room_num}_{room_name.lower().replace(" ", "_")}'
```

## Example Output

Generated SVG includes:
- 7+ room zones
- Entity IDs: `binary_sensor.living_room`, `binary_sensor.kitchen`, etc.
- CSS for hover/on/off states
- Wall/door visualization

## Next Steps

1. Test the generated SVG in your browser
2. Copy to HA and configure `floorplan.yaml`
3. Add CSS for sensor-based styling
4. Link actual HA sensors to SVG elements

## Summary

**AI-free, dependency-free floor plan generation:**
- ASCII text → Parser → HA-compatible SVG
- All entity IDs properly formatted
- CSS styling for on/off states
- Zero manual vector work
