#!/usr/bin/env python3
"""
Generate Home Assistant Floor Plan SVG from ASCII floor plan description.

This script generates an interactive SVG with entity-ready structure for Home Assistant.
Uses only Python standard library - no external dependencies.
"""

import sys
import re
import xml.etree.ElementTree as ET
from pathlib import Path


def parse_ascii_floorplan(ascii_text):
    """
    Parse ASCII floor plan and extract room zones.
    
    Returns dict with:
    - rooms: list of room dicts with id, name, x, y, width, height
    - title: floor plan title
    """
    rooms = []
    
    # Look for numbered room definitions
    room_pattern = re.compile(r'^(\d+)\.\s+([A-Z][a-zA-Z\s]+)', re.MULTILINE)
    for match in room_pattern.finditer(ascii_text):
        room_num = int(match.group(1))
        room_name = match.group(2).strip()
        
        # Generate entity ID from room name
        entity_id = f'binary_sensor.{room_name.lower().replace(" ", "_").replace("(", "").replace(")", "")}'
        
        rooms.append({
            'id': entity_id,
            'name': room_name,
            'x': 50 + (room_num - 1) % 3 * 220,
            'y': 80 + (room_num - 1) // 3 * 180,
            'width': 200,
            'height': 150
        })
    
    # Extract title from first line
    title = 'Home Floor Plan'
    first_line = ascii_text.split('\n')[0].strip()
    if first_line and not first_line.startswith('1.'):
        title = first_line
    
    return {
        'rooms': rooms,
        'title': title
    }


def create_svg_element(name, attributes=None, children=None):
    """Create an XML element with namespace."""
    if attributes is None:
        attributes = {}
    if children is None:
        children = []
    
    elem = ET.Element(name, attributes)
    for child in children:
        elem.append(child)
    return elem


def generate_floorplan_svg(parsed_plan, output_path):
    """Generate SVG floor plan with HA-compatible structure."""
    
    # SVG namespace
    ET.register_namespace('', 'http://www.w3.org/2000/svg')
    ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')
    
    # Create root SVG element
    svg_attrs = {
        'width': '800',
        'height': '600',
        'viewBox': '0 0 800 600',
        'xmlns': 'http://www.w3.org/2000/svg',
        'xmlns:xlink': 'http://www.w3.org/1999/xlink'
    }
    svg = create_svg_element('svg', svg_attrs)
    
    # Add style
    style_text = """.room { fill: #f0f0f0; stroke: #333; stroke-width: 2; cursor: pointer; }
.room:hover { fill: #e0e0e0; }
.room.on { fill: #4CAF50; }
.room.off { fill: #9E9E9E; }
.wall { stroke: #333; stroke-width: 4; }
.wall-door { stroke: #333; stroke-width: 2; stroke-dasharray: 5,5; }
.label { font-family: Arial, sans-serif; font-size: 14px; fill: #333; }
.entity-id { font-family: Arial, sans-serif; font-size: 10px; fill: #666; }"""
    
    style_elem = create_svg_element('style', {'type': 'text/css'})
    style_elem.text = style_text
    svg.append(style_elem)
    
    # Add title
    title_text = create_svg_element('text', {
        'x': '20',
        'y': '30',
        'font-size': '20px',
        'font-weight': 'bold',
        'class': 'label'
    })
    title_text.text = parsed_plan['title']
    svg.append(title_text)
    
    # Add rooms with entity IDs
    for room in parsed_plan['rooms']:
        # Room rectangle
        room_rect = create_svg_element('rect', {
            'x': str(room['x']),
            'y': str(room['y']),
            'width': str(room['width']),
            'height': str(room['height']),
            'class': 'room',
            'id': room['id']
        })
        svg.append(room_rect)
        
        # Room label
        label = create_svg_element('text', {
            'x': str(room['x'] + 10),
            'y': str(room['y'] + 20),
            'class': 'label'
        })
        label.text = room['name']
        svg.append(label)
        
        # Entity ID label
        entity_label = create_svg_element('text', {
            'x': str(room['x'] + 10),
            'y': str(room['y'] + 40),
            'class': 'entity-id'
        })
        entity_label.text = room['id']
        svg.append(entity_label)
        
        # Simple wall lines around room
        x, y, w, h = room['x'], room['y'], room['width'], room['height']
        for line in [
            ('line', {'x1': str(x), 'y1': str(y), 'x2': str(x + w), 'y2': str(y), 'class': 'wall'}),
            ('line', {'x1': str(x + w), 'y1': str(y), 'x2': str(x + w), 'y2': str(y + h), 'class': 'wall'}),
            ('line', {'x1': str(x + w), 'y1': str(y + h), 'x2': str(x), 'y2': str(y + h), 'class': 'wall'}),
            ('line', {'x1': str(x), 'y1': str(y + h), 'x2': str(x), 'y2': str(y), 'class': 'wall'}),
        ]:
            svg.append(create_svg_element(line[0], line[1]))
    
    # Add door openings
    # (simple representation - doors as dashed lines)
    for i, room in enumerate(parsed_plan['rooms']):
        if i > 0:
            # Add door to previous room
            prev_room = parsed_plan['rooms'][i - 1]
            door_x = prev_room['x'] + prev_room['width'] + 10
            door_y = prev_room['y'] + 75
            door = create_svg_element('line', {
                'x1': str(door_x),
                'y1': str(door_y - 10),
                'x2': str(door_x),
                'y2': str(door_y + 10),
                'class': 'wall-door'
            })
            svg.append(door)
    
    # Write to file
    tree = ET.ElementTree(svg)
    ET.indent(tree, space='  ')
    tree.write(output_path, encoding='utf-8', xml_declaration=True)


def create_sample_ascii_floorplan():
    """Create a sample ASCII floor plan for testing."""
    return """
FLOOR PLAN LAYOUT
=================

1. Front Porch/Entryway - Entry from street, coat closet
2. Hallway - Main spine connecting all areas  
3. Living Room - Left of hallway, large window, fireplace
4. Kitchen - Adjacent to living room, wooden door
5. Garage/Workshop - Right of hallway, workbench area
6. Backyard Garden - Garden beds, pathway, seating
7. Pool Area - In-ground pool, deck, equipment closet

WALLS: 20px thick, black lines
DOORS: Gaps in walls (80-90px wide)
STYLE: Clean blueprint, top-down orthographic view
"""


def main():
    if len(sys.argv) > 1:
        input_file = Path(sys.argv[1])
        if not input_file.exists():
            print(f"Error: File not found: {input_file}")
            sys.exit(1)
        ascii_text = input_file.read_text()
    else:
        print("No input file provided, using sample ASCII floor plan...")
        ascii_text = create_sample_ascii_floorplan()
    
    print("Parsing ASCII floor plan...")
    parsed_plan = parse_ascii_floorplan(ascii_text)
    
    output_path = Path("/media/share/Pidev_proj/image_output_hist/floorplan_homeassistant.svg")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"Generating SVG floor plan: {output_path}")
    generate_floorplan_svg(parsed_plan, str(output_path))
    
    print(f"✅ SVG generated successfully!")
    print(f"   Output: {output_path}")
    print(f"   Rooms found: {len(parsed_plan['rooms'])}")
    for room in parsed_plan['rooms']:
        print(f"     - {room['name']} (id: {room['id']})")


if __name__ == "__main__":
    main()
