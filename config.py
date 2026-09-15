import os
from dotenv import load_dotenv

load_dotenv()

# Webhook & API Credentials
PORT = int(os.getenv("PORT", "5000"))
META_VERIFY_TOKEN = os.getenv("META_VERIFY_TOKEN", "geophoenix_secret_token_2026")
META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN", "")
META_PHONE_NUMBER_ID = os.getenv("META_PHONE_NUMBER_ID", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", os.getenv("GOOGLE_API_KEY", ""))

# GeoPhoenix Business Info
COMPANY_NAME = "GeoPhoenix GIS, AI & Remote Sensing Solutions"
COMPANY_WEBSITE = "https://geophoenixgis.com"
CONTACT_EMAIL = "contact@geophoenixgis.com"

# Quick GIS & Mapping Tiers (Fiverr / Individual Services)
QUICK_GIS_TIERS = {
    "basic": {
        "name": "Basic GIS & Mapping",
        "price": 5,
        "turnaround": "1-day delivery",
        "scope": "Simple georeferencing, file conversion (KML/SHP/GeoJSON), or plotting up to 50 points.",
        "includes": ["Up to 3 maps", "Presentation slides"]
    },
    "standard": {
        "name": "Standard Spatial Analysis",
        "price": 50,
        "turnaround": "2-day delivery",
        "scope": "Complex spatial analysis, heatmaps, buffer analysis, or remote sensing (NDVI, land cover).",
        "includes": ["3 high-res maps", "Presentation slides", "Full data deliverables"]
    },
    "premium": {
        "name": "Premium Custom GIS & Automation",
        "price": 150,
        "turnaround": "3-day delivery",
        "scope": "Full custom projects with advanced Python/R scripting for automation, 3D models, and Web Maps.",
        "includes": ["4 high-res maps", "Source scripts (Python/R)", "3D/Web Map package", "Presentation"]
    }
}

# AI Chatbot & Automation Solutions for Businesses
BOT_BUILD_SERVICES = {
    "whatsapp_ai": {
        "name": "Custom WhatsApp AI Chatbot for Business",
        "min_price": 250,
        "max_price": 600,
        "turnaround": "3 - 5 business days",
        "scope": "Tailored WhatsApp Business AI agent with automated quote estimation, lead capture, product/service RAG knowledge base, and CRM/Email handoff.",
        "deliverables": ["Full Python/Node Webhook Server", "AI Knowledge Base Integration", "Meta WhatsApp Cloud Setup", "Deployment Guide"]
    },
    "custom_rag": {
        "name": "Enterprise AI Knowledge Base & RAG Bot",
        "min_price": 500,
        "max_price": 1200,
        "turnaround": "5 - 7 business days",
        "scope": "Custom AI agent trained on your business documents (PDFs, Excel, Databases) with multi-channel support (Web widget + WhatsApp + Telegram).",
        "deliverables": ["Document RAG Vector DB", "Multi-platform integration", "Admin analytics dashboard", "Hosting setup"]
    }
}

# GeoPhoenix Enterprise Consulting Packages
SERVICE_PACKAGES = {
    "1": {
        "id": "basic_gis",
        "name": "Basic GIS & Mapping (Quick Task)",
        "min_price": 5,
        "max_price": 5,
        "turnaround": "1-day delivery",
        "deliverables": [
            "Simple georeferencing & file conversion (KML/SHP/GeoJSON)",
            "Plotting up to 50 coordinate points",
            "Presentation maps"
        ],
        "ideal_for": "Students, quick task requests, file conversion, basic point mapping."
    },
    "2": {
        "id": "standard_gis",
        "name": "Standard Spatial Analysis & Remote Sensing",
        "min_price": 50,
        "max_price": 50,
        "turnaround": "2-day delivery",
        "deliverables": [
            "Complex spatial analysis, heatmaps, buffer analysis",
            "Remote sensing (NDVI time-series, land cover mapping)",
            "3 high-resolution maps & presentation slides"
        ],
        "ideal_for": "Small business analysis, environmental checks, spatial buffers, heatmaps."
    },
    "3": {
        "id": "premium_gis",
        "name": "Premium GIS Project & Automation (Python/R & 3D Web Maps)",
        "min_price": 150,
        "max_price": 150,
        "turnaround": "3-day delivery",
        "deliverables": [
            "Full custom GIS projects with Python/R automation scripts",
            "Interactive Web Maps & 3D Terrain visualization",
            "4 high-resolution maps + complete source code & slides"
        ],
        "ideal_for": "Advanced GIS research, automated spatial pipelines, web interactive maps."
    },
    "4": {
        "id": "coastal",
        "name": "Coastal Shoreline Change Analysis (Enterprise)",
        "min_price": 400,
        "max_price": 900,
        "turnaround": "6 - 8 business days",
        "deliverables": [
            "Georeferenced shoreline vectors across multi-decade epochs",
            "Transect-based erosion and accretion rate table (DSAS analysis)",
            "Hotspot erosion map & comprehensive report"
        ],
        "ideal_for": "Coastal planning bodies, marine NGOs, land-use planning stakeholders."
    },
    "5": {
        "id": "ais_fishing",
        "name": "Fishing Effort & AIS Vessel Activity Assessment (Enterprise)",
        "min_price": 450,
        "max_price": 1000,
        "turnaround": "6 - 9 business days",
        "deliverables": [
            "Basin-wide fishing effort heatmaps (annual & seasonal)",
            "Hidden Markov Model vessel state classification (fishing, transiting, loitering)",
            "Effort trend analysis PDF report & GIS spatial layers"
        ],
        "ideal_for": "Fisheries management bodies, marine conservation NGOs, academic research teams."
    },
    "6": {
        "id": "site_selection",
        "name": "Multi-Criteria Spatial Site Suitability (MCDA)",
        "min_price": 400,
        "max_price": 900,
        "turnaround": "5 - 7 business days",
        "deliverables": [
            "Custom weighted spatial overlay (zoning, slope, accessibility, hazards)",
            "Ranked site shortlist map & suitability score matrix",
            "Scoring methodology report"
        ],
        "ideal_for": "Land investors, agricultural planners, solar/energy developers."
    },
    "7": {
        "id": "ai_chatbot_dev",
        "name": "Custom Business AI Chatbot Development (WhatsApp / RAG)",
        "min_price": 250,
        "max_price": 600,
        "turnaround": "3 - 5 business days",
        "deliverables": [
            "Full WhatsApp Business AI Assistant setup",
            "Interactive pricing estimator & document RAG knowledge base",
            "Webhook server code, deployment script & Meta API setup"
        ],
        "ideal_for": "Businesses looking to automate client intake, sales, support & quote generation on WhatsApp."
    }
}

ADD_ONS = {
    "rush": {"name": "Rush Delivery (50% faster turnaround)", "pct": 0.30},
    "ml_classification": {"name": "Machine Learning Layer (Random Forest/XGBoost/CNN)", "fixed": 250},
    "presentation_deck": {"name": "Presentation-Ready Client Deck", "fixed": 150},
    "extra_revision": {"name": "Additional Revision Round", "fixed": 50}
}
