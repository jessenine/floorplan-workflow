#!/usr/bin/env python3
"""
Test the ASCII-to-SVG workflow by converting example floor plan.

This script:
1. Reads the example floor plan
2. Creates a simplified ASCII description
3. Converts to SVG
4. Shows accuracy comparison
"""

import sys
import re
from pathlib import Path


def extract_rooms_from_ascii(ascii_text):
    """Extract room information from ASCII floor plan."""
    rooms = []
    
    # Find numbered room definitions
    # Pattern: 1. ROOM NAME (optional description)
    room_pattern = re.compile(r'^(\d+)\.\s+(.+?)(?:\s*\(.+\))?(?:\s*-|$)', re.MULTILINE)
    for match in room_pattern.finditer(ascii_text):
        room_num = int(match.group(1))
        room_name = match.group(2).strip()
        
        # Clean up room name - remove slashes and parentheticals
        room_name = re.sub(r'\s*\([^)]+\)', '', room_name)  # Remove (description)
        room_name = room_name.replace('/', ' ').strip()
        
        # Generate entity ID
        entity_id = f'binary_sensor.{room_name.lower().replace(" ", "_")}'
        
        rooms.append({
            'id': entity_id,
            'name': room_name,
            'order': room_num
        })
    
    return rooms


def create_simplified_ascii(rooms):
    """Create a simplified ASCII representation for the parser."""
    lines = [
        "FLOOR PLAN LAYOUT",
        "=================",
        ""
    ]
    
    for room in rooms:
        lines.append(f"{room['order']}. {room['name']}")
    
    lines.extend([
        "",
        "WALLS: 20px thick, black lines",
        "DOORS: Gaps in walls (80-90px wide)",
        "STYLE: Clean blueprint, top-down orthographic view"
    ])
    
    return "\n".join(lines)


def test_workflow(example_file, output_dir):
    """Run the full workflow test."""
    
    # Read example floor plan
    print(f"Reading example floor plan: {example_file}")
    ascii_text = Path(example_file).read_text()
    
    # Extract rooms from detailed ASCII
    print("\n1. Extracting rooms from example...")
    original_rooms = extract_rooms_from_ascii(ascii_text)
    print(f"   Found {len(original_rooms)} rooms:")
    for room in original_rooms:
        print(f"     - {room['name']} (order: {room['order']}, id: {room['id']})")
    
    # Create simplified ASCII for parser
    print("\n2. Creating simplified ASCII...")
    simplified_ascii = create_simplified_ascii(original_rooms)
    print(simplified_ascii)
    
    # Write simplified ASCII to temp file
    temp_file = Path("/tmp/example_floorplan_ascii.txt")
    temp_file.write_text(simplified_ascii)
    print(f"\n   Saved to: {temp_file}")
    
    # Run the parser
    print("\n3. Running ASCII-to-SVG parser...")
    sys.argv = ['ascii_to_svg.py', str(temp_file)]
    
    # Import and run the parser
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "ascii_to_svg", 
        "/media/share/Pidev_proj/floorplan_workflow/ascii_to_svg.py"
    )
    parser_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(parser_module)
    
    # Override main to not call if __name__ == "__main__"
    parser_module.main()
    
    # Read generated SVG
    svg_file = Path("/media/share/Pidev_proj/image_output_hist/floorplan_homeassistant.svg")
    if svg_file.exists():
        print(f"\n4. SVG generated: {svg_file}")
        svg_content = svg_file.read_text()
        
        # Count elements
        room_count = len(re.findall(r'class="room" id="', svg_content))
        wall_count = len(re.findall(r'class="wall"', svg_content))
        door_count = len(re.findall(r'class="wall-door"', svg_content))
        
        print(f"\n   SVG Statistics:")
        print(f"     - Rooms: {room_count}")
        print(f"     - Walls: {wall_count}")
        print(f"     - Doors: {door_count}")
        
        # Check entity IDs
        entity_ids = re.findall(r'id="(binary_sensor\.[^"]+)"', svg_content)
        print(f"\n   Entity IDs in SVG:")
        for eid in entity_ids:
            print(f"     - {eid}")
        
        # Accuracy check
        print(f"\n5. Accuracy Check:")
        original_ids = {r['id'] for r in original_rooms}
        svg_ids = set(entity_ids)
        
        missing = original_ids - svg_ids
        extra = svg_ids - original_ids
        matched = original_ids & svg_ids
        
        print(f"     - Matched: {len(matched)}/{len(original_ids)} rooms")
        if missing:
            print(f"     - Missing: {missing}")
        if extra:
            print(f"     - Extra (unexpected): {extra}")
        
        return True
    else:
        print("   ✗ SVG file not generated!")
        return False


def main():
    print("=" * 60)
    print("ASCII-to-SVG Workflow Test")
    print("=" * 60)
    
    example_file = "/media/share/Pidev_proj/floorplan_workflow/example_floorplan.txt"
    
    if not Path(example_file).exists():
        print(f"Error: Example file not found: {example_file}")
        sys.exit(1)
    
    success = test_workflow(example_file, Path("/media/share/Pidev_proj"))
    
    print("\n" + "=" * 60)
    if success:
        print("✅ Test completed successfully!")
    else:
        print("⚠️  Test had issues")
    print("=" * 60)


if __name__ == "__main__":
    main()
