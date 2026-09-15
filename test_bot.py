import sys
import os
import json

# Ensure UTF-8 output on Windows console
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from server import process_user_message
from services.pricing_engine import calculate_quote
from services.gis_parser import parse_coordinates_from_text, analyze_site_location

def run_tests():
    print("=" * 60)
    print("  GEOPHENIX WHATSAPP BOT AUTOMATED VERIFICATION SUITE")
    print("=" * 60)

    # 1. Main Menu Test
    print("\n--- Test 1: Main Menu Invocation ---")
    menu_resp = process_user_message("MENU")
    assert "GeoPhoenix GIS, AI & Remote Sensing" in menu_resp
    print("✅ Main menu response verified!")

    # 2. Package Listing Test
    print("\n--- Test 2: Service Packages Listing ---")
    pkg_resp = process_user_message("1")
    assert "Basic ($5 USD)" in pkg_resp
    assert "Standard ($50 USD)" in pkg_resp
    assert "Premium ($150 USD)" in pkg_resp
    print("Package List Output Sample:")
    print(pkg_resp)
    print("✅ Package list verified!")

    # 3. Interactive Pricing Estimator Test ($5 Basic vs Enterprise vs AI Chatbot)
    print("\n--- Test 3: Interactive Quote Calculator ---")
    quote_resp_basic = calculate_quote("1", rush=True)
    assert "Basic GIS & Mapping" in quote_resp_basic
    assert "$10 USD" in quote_resp_basic  # $5 base + $5 min rush = $10

    quote_resp_bot = calculate_quote("7", rush=False)
    assert "Custom Business AI Chatbot Development" in quote_resp_bot
    assert "$250 - $600 USD" in quote_resp_bot

    print("Quote Output Sample ($5 Basic + Rush):")
    print(quote_resp_basic)
    print("\nQuote Output Sample (Business AI Chatbot Build):")
    print(quote_resp_bot)
    print("✅ Pricing estimator engine verified for all tiers!")

    # 4. GIS Coordinates Parser Test
    print("\n--- Test 4: GIS Coordinate Parsing & Site Assessment ---")
    coords = parse_coordinates_from_text("6.9271, 79.8612")
    assert coords == (6.9271, 79.8612)
    site_analysis = analyze_site_location(coords[0], coords[1])
    assert "6.9271, 79.8612" in site_analysis
    assert "Sentinel-2 / Landsat-8" in site_analysis
    print("✅ Coordinate parsing and spatial site assessment verified!")

    # 5. Technical Query Fallback / AI Test
    print("\n--- Test 5: Technical GIS Consultation Response ---")
    ai_resp = process_user_message("How do you analyze coastal shoreline erosion over 30 years?")
    assert "GeoPhoenix Coastal Shoreline" in ai_resp or "DSAS" in ai_resp
    print("✅ Technical consultation response verified!")

    print("\n" + "=" * 60)
    print(" 🎉 ALL AUTOMATED TESTS PASSED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
