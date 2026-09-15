from config import SERVICE_PACKAGES, ADD_ONS, QUICK_GIS_TIERS, BOT_BUILD_SERVICES

def get_main_menu_text() -> str:
    """Generates the GeoPhoenix WhatsApp Welcome & Main Menu text."""
    return (
        "🌍 *Welcome to GeoPhoenix GIS, AI & Remote Sensing Solutions!*\n"
        "We deliver GIS mapping, satellite spatial analysis, custom Python/3D web maps, and **Custom Business AI Chatbots**.\n\n"
        "Please select an option by replying with a number:\n\n"
        "1️⃣ *Explore All Services & Pricing ($5 - $1,000)*\n"
        "2️⃣ *Instant Project Cost Estimator*\n"
        "3️⃣ *Custom Business AI Chatbot Development*\n"
        "4️⃣ *View Case Studies & Deliverable Samples*\n"
        "5️⃣ *Submit Coordinates / Location Pin*\n"
        "6️⃣ *Ask GeoPhoenix AI (Technical Q&A)*\n"
        "7️⃣ *Talk to a Lead Consultant (Human Handoff)*\n\n"
        "💬 Or simply describe your project directly!"
    )

def get_service_list_text() -> str:
    """Returns the list of GeoPhoenix service packages including Quick GIS & AI Chatbot tiers."""
    text = "📊 *GeoPhoenix Service Packages & Pricing Matrix*\n\n"
    text += "🔹 *Quick GIS & Mapping Tiers (Fast Turnaround):*\n"
    text += "  • *Basic ($5 USD):* Simple georeferencing, KML/SHP file conversion, up to 50 points (1-day delivery).\n"
    text += "  • *Standard ($50 USD):* Complex spatial analysis, heatmaps, buffer analysis, NDVI/land cover (2-day delivery).\n"
    text += "  • *Premium ($150 USD):* Full custom projects, Python/R automation, 3D models & Interactive Web Maps (3-day delivery).\n\n"

    text += "🔹 *Enterprise GIS & Remote Sensing Solutions:*\n"
    for key in ["4", "5", "6"]:
        pkg = SERVICE_PACKAGES[key]
        text += f"  • *{key}. {pkg['name']}:* ${pkg['min_price']} - ${pkg['max_price']} USD ({pkg['turnaround']})\n"

    text += "\n🔹 *Business AI Chatbot Solutions:*\n"
    pkg7 = SERVICE_PACKAGES["7"]
    text += f"  • *7. {pkg7['name']}:* ${pkg7['min_price']} - ${pkg7['max_price']} USD ({pkg7['turnaround']})\n\n"

    text += "Reply `ESTIMATE <Number>` (e.g., `ESTIMATE 1` for $5 Basic or `ESTIMATE 7` for AI Chatbot) for full package details!"
    return text

def get_chatbot_service_info() -> str:
    """Returns details on Business AI Chatbot Preparation Services."""
    return (
        "🤖 *Custom Business AI Chatbot Preparation & Development*\n\n"
        "We design and build advanced AI Chatbots for businesses looking to automate WhatsApp lead intake, sales, support, and pricing estimation!\n\n"
        "📌 *What We Build For Your Business:*\n"
        "  • *WhatsApp Business AI Bot:* Interactive menus, quote estimation, CRM integration.\n"
        "  • *Document RAG AI Agent:* AI answers client questions trained directly on your business PDFs, prices, and catalogs.\n"
        "  • *Location & File Processing:* Parses customer pins, coordinates, and uploaded files.\n"
        "  • *Human Escalation:* Seamless handoff to your team via WhatsApp or Email.\n\n"
        "💰 *Investment:* $250 - $600 USD (Turnaround: 3-5 days)\n"
        "📩 Reply `QUOTE 7` to get an instant tailored quote for your business chatbot!"
    )

def get_package_detail_text(pkg_num: str) -> str:
    """Returns detailed information about a specific service package."""
    pkg = SERVICE_PACKAGES.get(str(pkg_num))
    if not pkg:
        return "❌ Package not found. Please specify a valid package number (1-7)."
    
    deliverables_formatted = "\n".join([f"  • {d}" for d in pkg["deliverables"]])
    
    price_display = f"${pkg['min_price']} USD" if pkg['min_price'] == pkg['max_price'] else f"${pkg['min_price']} - ${pkg['max_price']} USD"

    return (
        f"📋 *{pkg['name']}*\n\n"
        f"💰 *Investment:* {price_display}\n"
        f"⏱️ *Turnaround Time:* {pkg['turnaround']}\n"
        f"🎯 *Target Audience:* {pkg['ideal_for']}\n\n"
        f"📦 *Included Scope & Deliverables:*\n{deliverables_formatted}\n\n"
        f"⚡ Reply `QUOTE {pkg_num}` to calculate exact estimate with optional add-ons!"
    )

def calculate_quote(pkg_num: str, rush: bool = False, ml_layer: bool = False, deck: bool = False) -> str:
    """Calculates an itemized project estimate with add-ons."""
    pkg = SERVICE_PACKAGES.get(str(pkg_num))
    if not pkg:
        return "❌ Invalid package selected for quote calculation."

    base_min = pkg["min_price"]
    base_max = pkg["max_price"]

    add_on_summary = []
    min_total = float(base_min)
    max_total = float(base_max)

    if rush:
        rush_min = max(base_min * ADD_ONS["rush"]["pct"], 5)
        rush_max = max(base_max * ADD_ONS["rush"]["pct"], 5)
        min_total += rush_min
        max_total += rush_max
        add_on_summary.append(f"  • Rush Delivery (50% faster): +${int(rush_min)}" if rush_min == rush_max else f"  • Rush Delivery (50% faster): +${int(rush_min)} - ${int(rush_max)}")

    if ml_layer:
        ml_cost = ADD_ONS["ml_classification"]["fixed"]
        min_total += ml_cost
        max_total += ml_cost
        add_on_summary.append(f"  • ML Classification Layer: +${ml_cost}")

    if deck:
        deck_cost = ADD_ONS["presentation_deck"]["fixed"]
        min_total += deck_cost
        max_total += deck_cost
        add_on_summary.append(f"  • Presentation Deck: +${deck_cost}")

    add_on_text = "\n".join(add_on_summary) if add_on_summary else "  • Standard Package Scope (No add-ons selected)"

    price_str = f"${int(min_total)} USD" if min_total == max_total else f"${int(min_total)} - ${int(max_total)} USD"

    return (
        f"📝 *GeoPhoenix Custom Project Quote*\n\n"
        f"📌 *Package:* {pkg['name']}\n"
        f"⏱️ *Base Turnaround:* {pkg['turnaround']}\n\n"
        f"⚙️ *Selected Scope & Options:*\n{add_on_text}\n\n"
        f"🏷️ *ESTIMATED TOTAL:* *{price_str}*\n\n"
        f"📩 Ready to proceed? Reply `CONFIRM` to lock in this estimate and get started!"
    )
