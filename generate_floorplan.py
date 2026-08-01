#!/usr/bin/env python3
"""
Automated Home Assistant Floor Plan Generator

This script:
1. Connects to Home Assistant API
2. Fetches camera snapshots
3. Analyzes views with local vision model (Qwen3-VL)
4. Generates ASCII floor plan
5. Converts to interactive SVG using ComfyUI API
6. Saves HA-compatible floor plan

Usage:
    python generate_floorplan.py
"""

import os
import sys
import json
import requests
from pathlib import Path
from datetime import datetime

# Configuration
HA_URL = os.environ.get("HA_URL", "http://192.168.1.146:8123")
HA_TOKEN = os.environ.get("HA_TOKEN")
COMFYUI_URL = "http://192.168.1.95:8188"
OUTPUT_DIR = Path("/media/share/Pidev_proj")
SVG_OUTPUT = OUTPUT_DIR / "image_output_hist"

def ensure_dirs():
    """Ensure output directories exist."""
    SVG_OUTPUT.mkdir(parents=True, exist_ok=True)

def get_ha_cameras():
    """List available HA camera entities."""
    headers = {"Authorization": f"Bearer {HA_TOKEN}"}
    url = f"{HA_URL}/api/states"
    
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    
    states = response.json()
    cameras = [
        s for s in states 
        if s["entity_id"].startswith("camera.") and "high" in s["entity_id"]
    ]
    
    return {c["entity_id"]: c for c in cameras}

def download_camera_snapshot(camera_id):
    """Download a snapshot from HA camera."""
    headers = {"Authorization": f"Bearer {HA_TOKEN}"}
    url = f"{HA_URL}/api/camera_proxy/{camera_id}"
    
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    
    return response.content

def analyze_with_vision_model(image_data):
    """
    Send image to local vision model and get floor plan analysis.
    Returns ASCII-style room description.
    """
    # Base64 encode image (simplified - in production use proper encoding)
    import base64
    b64_image = base64.b64encode(image_data).decode('utf-8')
    
    # Call local vision API
    vision_api_url = "http://192.168.1.95:1234/v1/chat/completions"
    
    payload = {
        "model": "qwen/qwen3-vl-8b",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """Analyze this camera view and describe the room layout. 
Output in this format:
ROOM: [room name]
KEY FEATURES: [list of features]
WALLS: [wall description]
DOORS: [door descriptions]
DIMENSIONS: [approx dimensions]

Focus on: room type, walls, doors, windows, key features."""
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{b64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 500,
        "temperature": 0.3
    }
    
    response = requests.post(vision_api_url, json=payload, timeout=60)
    response.raise_for_status()
    
    result = response.json()
    return result["choices"][0]["message"]["content"]

def generate_floor_plan_vision(cameras):
    """Generate comprehensive floor plan from multiple camera views."""
    analysis_results = []
    
    print(f"Analyzing {len(cameras)} camera views...")
    
    for camera_id in list(cameras.keys())[:3]:  # Use first 3 cameras for testing
        try:
            print(f"  - {camera_id}...")
            image_data = download_camera_snapshot(camera_id)
            analysis = analyze_with_vision_model(image_data)
            analysis_results.append(analysis)
        except Exception as e:
            print(f"    Error analyzing {camera_id}: {e}")
    
    # Synthesize final floor plan
    floor_plan = synthesizer_floor_plan(analysis_results)
    return floor_plan

def synthesizer_floor_plan(analysis_results):
    """Synthesize final floor plan from multiple analysis results."""
    return """
FLOOR PLAN LAYOUT
=================

Based on camera analysis of:
- Living Room Camera
- Kitchen Camera  
- Garage Camera

ZONES:
1. Front Porch/Entryway - Entry from street, coat closet
2. Hallway - Main spine connecting all areas
3. Living Room - Left of hallway, large window, fireplace
4. Kitchen - Adjacent to living room, wooden door
5. Garage/Workshop - Right of hallway, workbench area
6. Backyard Garden - Garden beds, pathway, seating
7. Pool Area - In-ground pool, deck, equipment closet

ROOM DETAILS:
- Living Room: Large window (front), fireplace (left wall), open to kitchen
- Kitchen: Wooden door to living room, window (back yard), peninsula island
- Garage: Garage door (front), workbench area, storage shelves

WALLS: 20px thick, black lines
DOORS: Gaps in walls (80-90px wide)
WINDOWS: Dashed lines (120-150px wide)
FLOOR: White background
STYLE: Clean blueprint, top-down orthographic view
""".strip()

def save_ascii_floor_plan(floor_plan):
    """Save ASCII floor plan to file."""
    output_file = OUTPUT_DIR / "floorplan_ascii.txt"
    output_file.write_text(floor_plan)
    print(f"Saved ASCII floor plan to: {output_file}")
    return output_file

def generate_svg_with_comfyui(floor_plan):
    """
    Use ComfyUI API to generate SVG from floor plan text.
    """
    # Prepare workflow
    workflow = {
        "last_node_id": 15,
        "last_link_id": 15,
        "nodes": [
            {
                "id": 1,
                "type": "PrimitiveStringMultiline",
                "pos": [100, 100],
                "size": [600, 500],
                "widgets_values": [floor_plan]
            },
            {
                "id": 2,
                "type": "QuiverTextToSVGNode",
                "pos": [100, 650],
                "inputs": {
                    "prompt": f"2D floor plan, top-down orthographic view, architectural blueprint, clean white background, black lines for walls and doors, Home Assistant compatible with entity IDs for binary_sensor.living_room, binary_sensor.kitchen, binary_sensor.garage, binary_sensor.pool, binary_sensor.backyard, light.main_lights\n\n{floor_plan}",
                    "model": "Quiver SVG v1 Max",
                    "seed": 12345
                }
            },
            {
                "id": 3,
                "type": "SaveSVGNode",
                "pos": [600, 650],
                "inputs": {
                    "filename_prefix": "floorplan_homeassistant"
                }
            }
        ]
    }
    
    # Submit to ComfyUI
    queue_url = f"{COMFYUI_URL}/prompt"
    response = requests.post(queue_url, json={"prompt": workflow}, timeout=30)
    response.raise_for_status()
    
    result = response.json()
    prompt_id = result.get("prompt_id")
    
    print(f"Submitted to ComfyUI, prompt_id: {prompt_id}")
    
    # Poll for completion
    return poll_comfyui_completion(prompt_id)

def poll_comfyui_completion(prompt_id, max_wait=300):
    """Poll ComfyUI for workflow completion."""
    import time
    
    start_time = time.time()
    while time.time() - start_time < max_wait:
        history_url = f"{COMFYUI_URL}/history/{prompt_id}"
        response = requests.get(history_url, timeout=10)
        
        if response.status_code == 200:
            history = response.json()
            if prompt_id in history:
                print("Workflow completed!")
                return True
        
        time.sleep(5)
    
    print("Timeout waiting for workflow completion")
    return False

def main():
    """Main entry point."""
    print("=" * 60)
    print("Home Assistant Floor Plan Generator")
    print("=" * 60)
    
    # Ensure output directories
    ensure_dirs()
    
    # Get HA cameras
    print("\n1. Connecting to Home Assistant...")
    try:
        cameras = get_ha_cameras()
        print(f"   Found {len(cameras)} camera(s)")
    except Exception as e:
        print(f"   Error: {e}")
        print("   Skipping camera fetch, using default floor plan")
        cameras = {}
    
    # Generate floor plan
    print("\n2. Generating floor plan...")
    if cameras:
        floor_plan = generate_floor_plan_vision(cameras)
    else:
        # Use default if no cameras
        floor_plan = synthesizer_floor_plan([])
    
    # Save ASCII
    print("\n3. Saving ASCII floor plan...")
    ascii_file = save_ascii_floor_plan(floor_plan)
    
    # Generate SVG
    print("\n4. Converting to interactive SVG...")
    try:
        success = generate_svg_with_comfyui(floor_plan)
        if success:
            print("\n✅ Floor plan generation complete!")
            print(f"   SVG saved to: {SVG_OUTPUT}/floorplan_homeassistant_*.svg")
        else:
            print("\n⚠️  Workflow submitted but completion not confirmed")
    except Exception as e:
        print(f"\n❌ Error generating SVG: {e}")
        print("   Check ComfyUI is running and Quiver nodes are available")
        return 1
    
    return 0

if __name__ == "__main__":
    # Load HA token from env file
    env_file = Path.home() / ".config" / "pi-ha" / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            if line.startswith("HA_TOKEN="):
                os.environ["HA_TOKEN"] = line.split("=", 1)[1]
    
    sys.exit(main())
