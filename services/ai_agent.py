import os
import warnings
from config import GEMINI_API_KEY, COMPANY_NAME, COMPANY_WEBSITE, SERVICE_PACKAGES

SYSTEM_PROMPT = f"""
You are the Lead AI GIS & Automation Consultant for {COMPANY_NAME} ({COMPANY_WEBSITE}).
Your goal is to converse naturally with any customer on WhatsApp, understand their business or technical needs, answer any questions, and recommend the best GeoPhoenix solution.

GeoPhoenix Service & Pricing Portfolio:
1. Basic GIS & Mapping ($5 USD | 1-day delivery): Simple georeferencing, KML/SHP/GeoJSON file conversion, plotting up to 50 points.
2. Standard Spatial Analysis & Heatmaps ($50 USD | 2-day delivery): Complex spatial analysis, heatmaps, buffer analysis, NDVI, land cover mapping.
3. Premium Custom GIS & Automation ($150 USD | 3-day delivery): Advanced Python/R automation, 3D models, Interactive Web Maps, source code.
4. Coastal Shoreline Change Analysis ($400 - $900 USD | 6-8 days): Multi-decade erosion/accretion DSAS analysis, GEE cloud-free imagery, vector layers.
5. Fishing Effort & AIS Vessel Activity ($450 - $1,000 USD | 6-9 days): Global Fishing Watch AIS processing, Hidden Markov Models (HMM) vessel state classification, KDE effort heatmaps.
6. Multi-Criteria Spatial Site Suitability MCDA ($400 - $900 USD | 5-7 days): Custom weighted overlay scoring for solar, ag, real estate, land development.
7. Custom Business AI Chatbot Development ($250 - $600 USD | 3-5 days): Custom WhatsApp AI Assistants, Document RAG knowledge bases, automated quote generators for any business.

Conversation Guidelines:
- Respond in a warm, professional, highly knowledgeable, and helpful tone using GitHub/WhatsApp formatting (emojis, bolding).
- If the customer asks a technical question (e.g. QGIS, ArcGIS, Google Earth Engine, Python, DSAS, NDVI, satellite data, AI chatbots), give a clear, expert answer.
- If the customer describes a project (e.g., "I need to map a farm", "I want a chatbot for my store", "Can you check flood risk?"), recommend the appropriate package tier and price range.
- Encourage them to share coordinates/location pin or reply `MENU` to see all structured options.
- Keep responses concise and easy to read on a mobile phone screen (under 200 words).
"""

def generate_ai_response(user_query: str) -> str:
    """Generates an intelligent AI response using Gemini AI or robust expert fallback."""
    if GEMINI_API_KEY:
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                try:
                    from google import genai
                    client = genai.Client(api_key=GEMINI_API_KEY)
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=f"{SYSTEM_PROMPT}\n\nCustomer Inquiry: {user_query}\n\nProvide an engaging WhatsApp reply:"
                    )
                    if response and response.text:
                        return response.text.strip()
                except Exception:
                    import google.generativeai as legacy_genai
                    legacy_genai.configure(api_key=GEMINI_API_KEY)
                    model = legacy_genai.GenerativeModel("gemini-1.5-flash-latest")
                    response = model.generate_content(
                        f"{SYSTEM_PROMPT}\n\nCustomer Inquiry: {user_query}\n\nProvide an engaging WhatsApp reply:"
                    )
                    if response and response.text:
                        return response.text.strip()
        except Exception as e:
            print(f"[AI Agent Error]: {e}")

    # Fallback Expert System when API key is pending
    query_lower = user_query.lower()

    if any(k in query_lower for k in ["coastal", "shoreline", "erosion", "sea", "beach"]):
        return (
            "🌊 *GeoPhoenix Coastal Shoreline Analysis*\n\n"
            "We conduct multi-decade shoreline change studies (1990s - Present) using satellite imagery:\n"
            "  • Cloud-free compositing in Google Earth Engine\n"
            "  • Automated NDWI/MNDWI shoreline extraction\n"
            "  • Transect-based DSAS erosion/accretion rate tables\n\n"
            "📁 *Deliverables:* Georeferenced vectors, rate tables, & hotspot maps.\n"
            "💰 *Investment:* $400 - $900 USD (6-8 days)\n\n"
            "Reply `QUOTE 4` for an instant quote, or share your study area coordinates!"
        )

    elif any(k in query_lower for k in ["chatbot", "bot", "whatsapp bot", "automation", "ai bot"]):
        return (
            "🤖 *Custom Business AI Chatbot Development*\n\n"
            "We build custom WhatsApp AI Chatbots for businesses to automate client intake, sales, support, and quote calculation!\n\n"
            "📌 *Features:* Document RAG AI, Interactive Menus, Quote Generators, Meta/Twilio Cloud setup.\n"
            "💰 *Investment:* $250 - $600 USD (3-5 days)\n\n"
            "Reply `QUOTE 7` for a custom quote, or tell us about your business!"
        )

    elif any(k in query_lower for k in ["fishing", "ais", "vessel", "ocean", "ship", "marine"]):
        return (
            "⚓ *GeoPhoenix AIS Fishing Effort Assessment*\n\n"
            "We process AIS vessel tracking data across ocean basins:\n"
            "  • Hidden Markov Model (HMM) speed/heading behavior classification\n"
            "  • Kernel Density Estimation (KDE) fishing effort heatmaps\n\n"
            "💰 *Investment:* $450 - $1,000 USD (6-9 days)\n\n"
            "Reply `QUOTE 5` or let us know your target ocean region!"
        )

    elif any(k in query_lower for k in ["map", "mapping", "qgis", "arcgis", "point", "file", "convert"]):
        return (
            "🗺️ *GeoPhoenix GIS Mapping & Spatial Analysis*\n\n"
            "Whether you need quick mapping or advanced spatial analysis, we've got you covered:\n"
            "  • *Basic ($5 USD):* Georeferencing, KML/SHP file conversion, plotting points (1 day).\n"
            "  • *Standard ($50 USD):* Complex spatial analysis, heatmaps, NDVI, buffer zones (2 days).\n"
            "  • *Premium ($150 USD):* Custom Python/R automation, 3D terrain & Interactive Web Maps (3 days).\n\n"
            "Tell us a bit more about your map project or reply `MENU`!"
        )

    else:
        return (
            f"🌍 *GeoPhoenix GIS & AI Solutions*\n\n"
            f"Thank you for reaching out regarding *\"{user_query}\"*!\n\n"
            f"We specialize in:\n"
            f"  • GIS Mapping & Spatial Analysis ($5 - $150)\n"
            f"  • Enterprise Satellite & Remote Sensing ($400 - $1,000)\n"
            f"  • Custom Business AI Chatbots ($250 - $600)\n\n"
            f"How can we best assist your project today? Reply `MENU` to view all packages, or send us your study area location pin 📌!"
        )
