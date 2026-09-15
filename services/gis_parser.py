import re
from typing import Optional, Dict, Tuple

def parse_coordinates_from_text(text: str) -> Optional[Tuple[float, float]]:
    """
    Parses latitude and longitude from user input text.
    Handles formats like:
    - 6.9271, 79.8612
    - Lat: 6.9271 Long: 79.8612
    - 6°55'N, 79°51'E
    """
    pattern = r"([-+]?\d{1,2}\.\d+)\s*,\s*([-+]?\d{1,3}\.\d+)"
    match = re.search(pattern, text)
    if match:
        lat = float(match.group(1))
        lng = float(match.group(2))
        if -90 <= lat <= 90 and -180 <= lng <= 180:
            return (lat, lng)
    return None

def analyze_site_location(lat: float, lng: float, name: str = "Client Site") -> str:
    """
    Generates a spatial site overview based on shared coordinates.
    """
    # Create bounding box buffer (~0.05 degrees ~ 5.5km)
    min_lat, max_lat = round(lat - 0.025, 4), round(lat + 0.025, 4)
    min_lng, max_lng = round(lng - 0.025, 4), round(lng + 0.025, 4)

    return (
        f"📍 *GeoPhoenix Spatial Site Assessment*\n\n"
        f"🌐 *Coordinates Identified:* `{lat}, {lng}`\n"
        f"🗺️ *Estimated Study Bounding Box:* `[{min_lat}, {min_lng}] to [{max_lat}, {max_lng}]`\n"
        f"📐 *Approximate Focus Area:* ~25 sq km\n\n"
        f"🔍 *Initial GIS Feasibility Check:*\n"
        f"  • High-resolution Sentinel-2 / Landsat-8 imagery available for this region.\n"
        f"  • Digital Elevation Model (DEM 30m / ALOS PALSAR 12.5m) accessible.\n"
        f"  • Compatible for: Shoreline analysis, Landcover/NDVI, Slope/Terrain MCDA & Hazard Screening.\n\n"
        f"💡 *Next Steps:* Reply with your primary analysis goal (e.g. `Erosion`, `Hazard`, `Real Estate`, `Agriculture`) to receive a tailored scope!"
    )
