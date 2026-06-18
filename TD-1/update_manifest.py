import json, sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path

manifest_path = Path(r"D:\Kapil\Books\TD-1\Book1\manifest_clean.json")
with open(manifest_path, "r", encoding="utf-8") as f:
    manifest = json.load(f)

SPOTLIGHTS = [
    {"id": "SS-01", "type": "scene_spotlight", "chapter": 1, "file": "Spotlights/spotlight_maya_desk.png", "quote": "Every project was a tiny universe of possibility."},
    {"id": "SS-02", "type": "scene_spotlight", "chapter": 2, "file": "Spotlights/spotlight_crate_discovery.png", "quote": "Whatever you are, you're coming with me."},
    {"id": "SS-03", "type": "scene_spotlight", "chapter": 3, "file": "Spotlights/spotlight_cube_awakens.png", "quote": "The cube heard it. And began to boot."},
    {"id": "SS-04", "type": "scene_spotlight", "chapter": 4, "file": "Spotlights/spotlight_blip_first_words.png", "quote": "He was ALIVE. Really, truly, impossibly ALIVE."},
    {"id": "SS-05", "type": "scene_spotlight", "chapter": 5, "file": "Spotlights/spotlight_glitch_wave.png", "quote": "A pulse of CYAN light shot out of Blip like a ripple in water."},
    {"id": "SS-06", "type": "scene_spotlight", "chapter": 7, "file": "Spotlights/spotlight_gridlord_appears.png", "quote": "Someone woke up the little cube. How... INTERESTING."},
    {"id": "SS-07", "type": "scene_spotlight", "chapter": 8, "file": "Spotlights/spotlight_team_builds.png", "quote": "Her goggles were foggy. Her fingers were scorched. Her grin was VICTORIOUS."},
    {"id": "SS-08", "type": "scene_spotlight", "chapter": 9, "file": "Spotlights/spotlight_puzzle_celebration.png", "quote": "Despite EVERYTHING - they all LAUGHED."},
    {"id": "SS-09", "type": "scene_spotlight", "chapter": 11, "file": "Spotlights/spotlight_daadi_parathas.png", "quote": "Reckless love is still love, Maya-beta."},
    {"id": "SS-10", "type": "scene_spotlight", "chapter": 13, "file": "Spotlights/spotlight_sam_traffic.png", "quote": "Like a platformer, except the consequences were REAL."},
    {"id": "SS-11", "type": "scene_spotlight", "chapter": 14, "file": "Spotlights/spotlight_blip_mainframe.png", "quote": "Version 2.0. And still himself. Still Blip."},
    {"id": "SS-12", "type": "scene_spotlight", "chapter": 17, "file": "Spotlights/spotlight_rooftop_sunset.png", "quote": "The sky is NEVER the same color twice."},
    {"id": "SS-13", "type": "scene_spotlight", "chapter": 18, "file": "Spotlights/spotlight_gridlord_truth.png", "quote": "The Gridlord wasn't the villain. They were the ALARM."},
    {"id": "SS-14", "type": "scene_spotlight", "chapter": 19, "file": "Spotlights/spotlight_maya_final_stand.png", "quote": "Glitch Squad - we have a rescue mission."},
]

LOCATIONS = [
    {"id": "LOC-01", "type": "location", "chapter": 1, "file": "Locations/location_maple_street.png"},
    {"id": "LOC-02", "type": "location", "chapter": 1, "file": "Locations/location_maya_room.png"},
    {"id": "LOC-03", "type": "location", "chapter": 9, "file": "Locations/location_nexcorp_basement.png"},
    {"id": "LOC-04", "type": "location", "chapter": 12, "file": "Locations/location_utility_tunnels.png"},
    {"id": "LOC-05", "type": "location", "chapter": 17, "file": "Locations/location_hq_lab.png"},
]

DIAGRAMS = [
    {"id": "DIA-01", "type": "diagram", "chapter": 5, "file": "Diagrams/diagram_signal_path.png"},
    {"id": "DIA-02", "type": "diagram", "chapter": 7, "file": "Diagrams/diagram_gridlord_network.png"},
    {"id": "DIA-03", "type": "diagram", "chapter": 10, "file": "Diagrams/diagram_anatomy_glitch.png"},
    {"id": "DIA-04", "type": "diagram", "chapter": 8, "file": "Diagrams/diagram_connector_key.png"},
    {"id": "DIA-05", "type": "diagram", "chapter": 16, "file": "Diagrams/diagram_project_kira.png"},
]

old_strips_count = len(manifest.get("strips", []))
del manifest["strips"]
manifest["scene_spotlights"] = SPOTLIGHTS
manifest["locations"] = LOCATIONS
manifest["diagrams"] = DIAGRAMS

with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

print(f"Removed {old_strips_count} strips, added {len(SPOTLIGHTS)} spotlights + {len(LOCATIONS)} locations + {len(DIAGRAMS)} diagrams")
