import sys
import os
import json
import urllib.parse
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler

# Ensure UTF-8 console output on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Add root directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import PORT, META_VERIFY_TOKEN, META_ACCESS_TOKEN, META_PHONE_NUMBER_ID
from services.pricing_engine import (
    get_main_menu_text,
    get_service_list_text,
    get_package_detail_text,
    calculate_quote
)
from services.gis_parser import parse_coordinates_from_text, analyze_site_location
from services.ai_agent import generate_ai_response
from services.case_studies import get_case_studies_summary

def send_meta_whatsapp_message(to_phone: str, text_message: str):
    """Sends an outgoing message back to the user via Meta WhatsApp Cloud API."""
    if not META_ACCESS_TOKEN or not META_PHONE_NUMBER_ID:
        print("[Warning] META_ACCESS_TOKEN or META_PHONE_NUMBER_ID is missing in .env! Cannot send API reply.")
        return

    url = f"https://graph.facebook.com/v18.0/{META_PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {META_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to_phone,
        "type": "text",
        "text": {"body": text_message}
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        print(f"[Meta API Outgoing Reply Status {response.status_code}]: {response.text}")
    except Exception as e:
        print(f"[Error sending Meta WhatsApp message]: {e}")


def process_user_message(user_text: str, sender_id: str = "") -> str:
    """Core message processing routing state machine."""
    text_strip = user_text.strip()
    text_lower = text_strip.lower()

    # 1. Coordinates check
    coords = parse_coordinates_from_text(text_strip)
    if coords:
        return analyze_site_location(coords[0], coords[1])

    # 2. Main Menu Keywords
    if text_lower in ["hi", "hello", "hey", "menu", "start", "0"]:
        return get_main_menu_text()

    if text_lower in ["1", "packages", "services", "pricing"]:
        return get_service_list_text()

    if text_lower in ["2", "estimator", "calculator", "quote"]:
        return (
            "🧮 *GeoPhoenix Instant Quote Estimator*\n\n"
            "Reply with: `QUOTE <Package Number> [rush] [ml] [deck]`\n\n"
            "Quick Package Numbers:\n"
            "  • `QUOTE 1` ($5 Basic GIS / Georeferencing / File Conversion)\n"
            "  • `QUOTE 2` ($50 Standard Spatial Analysis & Heatmaps)\n"
            "  • `QUOTE 3` ($150 Premium GIS Automation & 3D/Web Maps)\n"
            "  • `QUOTE 4` (Coastal Shoreline Change Analysis)\n"
            "  • `QUOTE 5` (Fishing Effort & AIS Vessel Assessment)\n"
            "  • `QUOTE 6` (Spatial Site Suitability MCDA)\n"
            "  • `QUOTE 7` ($250-$600 Custom Business AI Chatbot Build)"
        )

    if text_lower in ["3", "chatbot", "bot", "ai bot"]:
        from services.pricing_engine import get_chatbot_service_info
        return get_chatbot_service_info()

    if text_lower in ["4", "case studies", "samples", "portfolio"]:
        return get_case_studies_summary()

    if text_lower in ["5", "location", "coords", "coordinates"]:
        return (
            "📍 *Submit Location or Coordinates*\n\n"
            "Please send us:\n"
            "  • A WhatsApp Location Pin 📌\n"
            "  • Or type raw coordinates e.g., `6.9271, 79.8612`\n\n"
            "Our GIS engine will instantly generate a bounding box assessment!"
        )

    if text_lower in ["6", "ai", "ask"]:
        return (
            "🧠 *Ask GeoPhoenix AI Technical Consultant*\n\n"
            "Type any question about GIS mapping, QGIS/ArcGIS, GEE processing, remote sensing, or Custom AI Chatbot integration!"
        )

    if text_lower in ["7", "talk", "human", "specialist", "contact"]:
        return (
            "👨‍💻 *Connecting with Teshan Ishara / GeoPhoenix Lead*\n\n"
            "Our Lead Specialist has been notified of your request!\n"
            "📧 Email: `contact@geophoenixgis.com`\n"
            "🌐 Web: `https://geophoenixgis.com`\n\n"
            "We usually respond within 1-2 business hours."
        )

    # 3. QUOTE parsing
    if text_lower.startswith("quote"):
        parts = text_strip.split()
        if len(parts) >= 2 and parts[1].isdigit():
            pkg_num = parts[1]
            rush = "rush" in text_lower
            ml = "ml" in text_lower
            deck = "deck" in text_lower
            return calculate_quote(pkg_num, rush=rush, ml_layer=ml, deck=deck)

    # 4. ESTIMATE parsing
    if text_lower.startswith("estimate"):
        parts = text_strip.split()
        if len(parts) >= 2 and parts[1].isdigit():
            return get_package_detail_text(parts[1])

    # 5. Package number direct response (1-7)
    if text_strip.isdigit() and 1 <= int(text_strip) <= 7:
        return get_package_detail_text(text_strip)

    # 6. Fallback to Gemini AI Technical Consultant
    return generate_ai_response(text_strip)


class GeoPhoenixWebhookHandler(BaseHTTPRequestHandler):

    def send_response_data(self, content_type: str, body: bytes, status: int = 200):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        """Handles Meta WhatsApp Webhook Verification and Render Health Checks."""
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)

        # Health check for root path /
        if parsed.path == "/" or parsed.path == "":
            self.send_response_data("text/html", b"<h1>GeoPhoenix WhatsApp AI Chatbot is Online and Healthy!</h1>", status=200)
            return

        mode = params.get("hub.mode", [""])[0]
        token = params.get("hub.verify_token", [""])[0]
        challenge = params.get("hub.challenge", [""])[0]

        if mode == "subscribe" and token == META_VERIFY_TOKEN:
            print(f"[Meta Webhook Verified Successfully! Challenge: {challenge}]")
            self.send_response_data("text/plain", challenge.encode("utf-8"))
        else:
            print(f"[Webhook Verification Failed. Received Token: {token}]")
            self.send_response_data("text/plain", b"Verification failed", status=403)

    def do_POST(self):
        """Handles incoming messages from Meta WhatsApp API, Twilio, or local JSON test payload."""
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")

        response_text = ""

        # A. Meta WhatsApp Cloud API JSON
        if "application/json" in self.headers.get("Content-Type", ""):
            try:
                data = json.loads(body)
                print(f"[Received Meta/JSON Webhook Payload]: {json.dumps(data, indent=2)}")

                # Check if it's a Meta Cloud API format
                if "entry" in data:
                    for entry in data["entry"]:
                        for change in entry.get("changes", []):
                            value = change.get("value", {})
                            messages = value.get("messages", [])
                            for msg in messages:
                                sender = msg.get("from", "")
                                msg_type = msg.get("type", "")

                                if msg_type == "text":
                                    user_text = msg.get("text", {}).get("body", "")
                                    response_text = process_user_message(user_text, sender)
                                elif msg_type == "location":
                                    loc = msg.get("location", {})
                                    lat, lng = loc.get("latitude"), loc.get("longitude")
                                    response_text = analyze_site_location(lat, lng)

                                # Send outgoing reply via Meta Cloud API back to sender's WhatsApp
                                if sender and response_text:
                                    send_meta_whatsapp_message(sender, response_text)

                # Local direct test payload
                elif "message" in data:
                    user_text = data["message"]
                    response_text = process_user_message(user_text)

                resp_payload = json.dumps({"status": "success", "reply": response_text}).encode("utf-8")
                self.send_response_data("application/json", resp_payload)

            except Exception as e:
                print(f"[Error processing JSON POST]: {e}")
                self.send_response_data("application/json", json.dumps({"error": str(e)}).encode("utf-8"), 500)

        # B. Twilio Form URL Encoded
        else:
            parsed_body = urllib.parse.parse_qs(body)
            user_text = parsed_body.get("Body", [""])[0]
            sender = parsed_body.get("From", [""])[0]
            print(f"[Received Twilio Webhook from {sender}]: {user_text}")

            response_text = process_user_message(user_text, sender)
            twiml_xml = f"<?xml version=\"1.0\" encoding=\"UTF-8\"?><Response><Message>{response_text}</Message></Response>"
            self.send_response_data("application/xml", twiml_xml.encode("utf-8"))


def run_server(port=PORT):
    server_address = ("", port)
    httpd = HTTPServer(server_address, GeoPhoenixWebhookHandler)
    print(f"🚀 GeoPhoenix WhatsApp AI Chatbot Webhook Server active on port {port}")
    print(f"🔗 Verification URL: http://localhost:{port}/webhook")
    print(f"🔑 Hub Verify Token: '{META_VERIFY_TOKEN}'")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping GeoPhoenix Webhook Server.")

if __name__ == "__main__":
    run_server()
