# Home Assistant Floor Plan Workflow

## Overview

This workflow generates floor plans for **Home Assistant**, not just static images.

## What You Need

Home Assistant floor plans require **SVG files** with specific structure:
- Each entity (sensor, light, switch) needs an SVG element with matching `id`
- Vector elements (`path`, `rect`, `circle`) define zones
- CSS styles control appearance based on entity state

## The Workflow

The workflow creates a **static floor plan image** first. From there, you have two options:

### Option 1: Manual SVG Conversion (Recommended)

1. **Generate floor plan image** using the workflow
2. **Open in vector editor**: Inkscape, Illustrator, or online SVG editor
3. **Trace each room zone** and assign HA entity IDs:
   ```svg
   <rect id="binary_sensor.living_room" x="100" y="100" width="300" height="200" fill="#7cb1f9"/>
   <path id="light.kitchen" d="M400,400 L500,400 L500,500 L400,500 Z" fill="white"/>
   ```
4. **Create HA entity IDs** matching your sensors:
   - `binary_sensor.living_room`
   - `binary_sensor.kitchen`
   - `binary_sensor.garage`
   - `light.main_lights`
   - `switch.fan`
5. **Add CSS styling** for state changes (see below)
6. **Save as `.svg`** and place in `www/floorplan/` directory

### Option 2: Automated SVG Generation (Advanced)

For full automation, you'd need to:
1. Parse the ASCII floor plan text
2. Convert room descriptions to SVG coordinates
3. Add entity IDs based on your HA sensors
4. Generate the complete SVG

This requires additional scripting (Python/Node.js) to parse the floor plan and output SVG.

## HA Entity Naming Convention

Your HA entity IDs should match the SVG element IDs exactly:

| HA Entity | SVG ID | Description |
|-----------|--------|-------------|
| `binary_sensor.living_room` | `<rect id="binary_sensor.living_room">` | Room occupancy sensor |
| `binary_sensor.kitchen` | `<rect id="binary_sensor.kitchen">` | Kitchen sensor |
| `light.main_lights` | `<circle id="light.main_lights">` | Main light switch |
| `switch.fan` | `<path id="switch.fan">` | Fan switch |

## Basic SVG Structure

```svg
<svg width="1024" height="1024" xmlns="http://www.w3.org/2000/svg">
  <!-- Living Room Zone -->
  <rect id="binary_sensor.living_room" 
        x="100" y="100" width="300" height="200" 
        fill="#7cb1f9"/>
  
  <!-- Kitchen Zone -->
  <path id="binary_sensor.kitchen" 
        d="M400,100 L700,100 L700,300 L400,300 Z" 
        fill="#7cb1f9"/>
  
  <!-- Hallway -->
  <rect id="binary_sensor.hallway" 
        x="350" y="350" width="100" height="400" 
        fill="#7cb1f9"/>
</svg>
```

## CSS Styling for State Changes

Create a `floorplan.css` file:

```css
/* Default state (off) */
.binary-sensor-off {
  fill: #7cb1f9 !important;
  transition: fill 5s ease;
}

/* Active state (on) */
.binary-sensor-on {
  fill: #f9d27c !important;
}

/* Lights - grayscale when off */
.light-off * {
  -webkit-filter: grayscale(100%);
  filter: grayscale(100%);
  filter: gray;
}

/* Lights - full color when on */
.light-on * {
  /* No filtering - full color */
}
```

## Minimal HA Configuration

In your `floorplan.yaml`:

```yaml
title: Home
config:
  image: /local/floorplan/home.svg
  stylesheet: /local/floorplan/home.css
  log_level: info

  defaults:
    hover_action: hover-info
    tap_action: more-info

  rules:
    - entity: binary_sensor.living_room
      element: binary_sensor.living_room
      state_action:
        - action: call-service
          service: floorplan.class_set
          service_data: binary-sensor-${entity.state}
      tap_action: more-info

    - entity: binary_sensor.kitchen
      element: binary_sensor.kitchen
      state_action:
        - action: call-service
          service: floorplan.class_set
          service_data: binary-sensor-${entity.state}
      tap_action: more-info

    # Add more rules for other entities...
```

## Tools

| Tool | Purpose |
|------|---------|
| **Inkscape** | Free vector editor (https://inkscape.org) |
| **SVG Editor** | Online SVG editor (https://svg-editor.fosscommunity.org) |
| **VS Code** | Text editor with SVG extensions |
| **Home Assistant** | The target platform |

## Quick Start

1. Run the floor plan workflow to generate an image
2. Open the image in Inkscape
3. Trace each room with vector paths
4. Assign `id` attributes matching your HA entities
5. Create CSS for state-based colors
6. Deploy to HA `www/floorplan/` directory

## Example Output

The workflow generates a clean 2D floor plan at:
```
/media/share/Pidev_proj/image_output_hist/floorplan_example_*.png
```

You can use this as a reference for tracing in your vector editor.

## Need Help?

- HA Floorplan Docs: https://experiencelovelace.github.io/ha-floorplan/
- Inkscape Tutorial: https://inkscape.org/learn/
- SVG Reference: https://www.w3schools.com/svg/

## Notes

- The workflow generates a **static image** for reference
- You'll need to manually create the **interactive SVG** with HA entity IDs
- Consider starting with a simple floor plan and adding complexity gradually
- Test in HA with `floorplan.show` service to preview changes
