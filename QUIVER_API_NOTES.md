# Home Assistant Floor Plan Workflow - Quiver API Notes

## Quiver Text-to-SVG Node API Format

The Quiver nodes are API nodes that require specific input formatting.

### Correct Workflow Structure

```json
{
  "prompt": {
    "5": {
      "inputs": {
        "prompt": "Text description of desired SVG",
        "model": "arrow-1.1-max",
        "seed": 12345
      },
      "class_type": "QuiverTextToSVGNode"
    },
    "6": {
      "inputs": {
        "filename_prefix": "floorplan_homeassistant",
        "svg": ["5", 0]
      },
      "class_type": "SaveSVGNode"
    }
  },
  "client_id": "unique-client-id"
}
```

### Known Issue

The `QuiverTextToSVGNode` appears to have an API compatibility issue where the dynamic combo model input isn't being passed correctly to the execute function.

### Workarounds

1. **Use ComfyUI UI directly**:
   - Open http://192.168.1.95:8188
   - Add `QuiverTextToSVGNode` node
   - Enter your prompt text
   - Select model (arrow-1.1, arrow-1.1-max, or arrow-preview)
   - Click "Queue Prompt"

2. **Use QuiverImageToSVGNode with a simple image**:
   - Create a simple PNG floor plan sketch (even just text labels)
   - Use `QuiverImageToSVGNode` to convert to SVG

3. **Manual workflow**:
   - Use the generated workflow JSON file in ComfyUI
   - Edit the prompt in the UI
   - Click "Queue Prompt"

### Workflow Files

- `floorplan_workflow_ha_svg.json` - Complete workflow for HA SVG generation
- `generate_floorplan.py` - Python script to automate camera analysis and SVG generation

### HA Floor Plan Requirements

SVG must include:
- Entity IDs matching HA sensors (e.g., `binary_sensor.living_room`)
- Proper vector elements (`<path>`, `<rect>`, `<circle>`)
- CSS styling for on/off states

## Quiver Pricing

- `arrow-1.1`: ~$0.29 USD per generation
- `arrow-1.1-max`: ~$0.36 USD per generation  
- `arrow-preview`: ~$0.43 USD per generation
