#!/bin/bash
# Simple test floor plan SVG that can be used to test the workflow

cat > /tmp/test_floorplan.svg << 'SVGEOF'
<?xml version="1.0" encoding="UTF-8"?>
<svg width="1024" height="1024" xmlns="http://www.w3.org/2000/svg">
  <!-- White background -->
  <rect width="100%" height="100%" fill="white"/>
  
  <!-- Outer walls (black, 20px thick) -->
  <rect x="50" y="50" width="924" height="924" fill="none" stroke="black" stroke-width="20"/>
  
  <!-- Interior walls -->
  <line x1="350" y1="50" x2="350" y2="450" stroke="black" stroke-width="15"/>
  <line x1="674" y1="50" x2="674" y2="450" stroke="black" stroke-width="15"/>
  <line x1="50" y1="500" x2="974" y2="500" stroke="black" stroke-width="15"/>
  <line x1="800" y1="450" x2="800" y2="974" stroke="black" stroke-width="15"/>
  
  <!-- Doors (gaps in walls) -->
  <!-- Door 1: hallway to living room -->
  <line x1="350" y1="250" x2="350" y2="300" stroke="white" stroke-width="15"/>
  <!-- Door 2: hallway to kitchen -->
  <line x1="674" y1="250" x2="674" y2="300" stroke="white" stroke-width="15"/>
  <!-- Door 3: main entrance -->
  <line x1="500" y1="50" x2="500" y2="100" stroke="white" stroke-width="15"/>
  <!-- Door 4: back area -->
  <line x1="800" y1="700" x2="800" y2="750" stroke="white" stroke-width="15"/>
  
  <!-- Labels (optional, small text) -->
  <text x="500" y="25" font-family="Arial" font-size="20" fill="black" text-anchor="middle">ENTRY</text>
  <text x="200" y="250" font-family="Arial" font-size="16" fill="black" text-anchor="middle">LIVING</text>
  <text x="500" y="250" font-family="Arial" font-size="16" fill="black" text-anchor="middle">HALLWAY</text>
  <text x="800" y="250" font-family="Arial" font-size="16" fill="black" text-anchor="middle">KITCHEN</text>
  <text x="800" y="750" font-family="Arial" font-size="16" fill="black" text-anchor="middle">BEDROOM</text>
  <text x="500" y="750" font-family="Arial" font-size="16" fill="black" text-anchor="middle">BATH</text>
</svg>
SVGEOF

echo "Test floor plan SVG created at: /tmp/test_floorplan.svg"
echo "To convert to PNG for ComfyUI:"
echo "  convert /tmp/test_floorplan.svg /tmp/test_floorplan.png"