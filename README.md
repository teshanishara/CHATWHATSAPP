# 🌍 GeoPhoenix Advanced WhatsApp AI Chatbot

A production-ready WhatsApp AI Chatbot built specifically for **GeoPhoenix GIS & Remote Sensing Consulting**.

## Features

1. 📊 **Interactive Service Menu**: Showcases GeoPhoenix's 7 core consulting packages.
2. 🧮 **Instant Cost & Turnaround Estimator**: Calculates customized package quotes and add-on pricing (Rush delivery +30%, ML classification +$250, Presentation deck +$150).
3. 📍 **GIS Location & Coordinates Parser**: Extracts Lat/Lng coordinates from text or WhatsApp location pins and generates a preliminary spatial assessment & bounding box scope.
4. 🧠 **AI GIS Technical Advisor (Gemini AI)**: Answers complex GIS/Remote Sensing queries (DSAS shoreline transects, HMM AIS vessel state classification, STL decomposition, BFAST disturbance detection, GEE workflows).
5. 📚 **Case Studies Viewer**: Highlights GeoPhoenix flagship projects (Ireland Coastal Erosion, Indian Ocean AIS Fishing Effort, Mountain Vegetation Trends).
6. 🔌 **Dual Webhook Gateway**: Supports **Meta WhatsApp Cloud API** & **Twilio WhatsApp API**.

---

## Folder Structure

```
geophoenix_whatsapp_bot/
├── config.py                  # Service matrix, prices, and environment configuration
├── server.py                  # HTTP Webhook Server (Meta Cloud API + Twilio)
├── test_bot.py                # Verification & local testing suite
├── services/
│   ├── pricing_engine.py      # Quote calculator & menu text formatters
│   ├── gis_parser.py          # Coordinates & WhatsApp location pin processor
│   ├── ai_agent.py            # Gemini AI + expert technical consultation RAG engine
│   └── case_studies.py        # Case studies showcase module
└── .env.example               # Template for API keys
```

---

## Setup Instructions

### 1. Environment Configuration

Create a `.env` file inside `geophoenix_whatsapp_bot/`:

```env
PORT=5000
META_VERIFY_TOKEN=geophoenix_secret_token_2026
META_ACCESS_TOKEN=YOUR_META_PERMANENT_ACCESS_TOKEN
META_PHONE_NUMBER_ID=YOUR_META_PHONE_NUMBER_ID
GEMINI_API_KEY=YOUR_GEMINI_OR_GOOGLE_API_KEY
```

### 2. Run Local Server

Start the webhook server:

```bash
python server.py
```

### 3. Expose Server to Internet with ngrok

In a separate terminal, start ngrok to create a secure HTTPS tunnel:

```bash
ngrok http 5000
```

Copy the generated HTTPS forwarding URL (e.g. `https://xxxx.ngrok-free.app`).

### 4. Configure Meta WhatsApp Cloud API

1. Go to [Meta Developers Portal](https://developers.facebook.com/).
2. Select your App -> **WhatsApp** -> **Configuration**.
3. Under **Callback URL**, paste: `https://xxxx.ngrok-free.app/webhook`
4. Under **Verify Token**, enter: `geophoenix_secret_token_2026`
5. Click **Verify and Save**.
6. Subscribe to the `messages` webhook field.

---

## Testing locally without WhatsApp

Run the automated verification suite:

```bash
python test_bot.py
```
