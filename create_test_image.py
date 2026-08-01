#!/usr/bin/env python3
"""
Create a simple test floor plan sketch for testing the workflow.
"""

from PIL import Image, ImageDraw

# Create a simple floor plan sketch (2048x2048, white background with black lines)
img = Image.new('RGB', (2048, 2048), color='white')
draw = ImageDraw.Draw(img)

# Draw some room-like structures (black lines on white background)
# Outer walls
draw.rectangle([200, 200, 1800, 1800], outline='black', width=20)

# Interior walls
draw.line([600, 200, 600, 1000], fill='black', width=15)
draw.line([1000, 200, 1000, 1000], fill='black', width=15)
draw.line([200, 800, 1800, 800], fill='black', width=15)
draw.line([1400, 1000, 1400, 1800], fill='black', width=15)

# Doors (dashed lines)
for i in range(600, 650, 20):
    draw.line([(600+i%20, 200), (600+i%20, 250)], fill='black', width=5)
for i in range(1400, 1450, 20):
    draw.line([(1400+i%20, 1800), (1400+i%20, 1750)], fill='black', width=5)

# Save
img.save('/tmp/test_floorplan.png')
print("Test floor plan created at: /tmp/test_floorplan.png")
