import requests
import json
from datetime import datetime

def fetch_metals():
    url = "https://sys.wisegold.app/proxies/proxy_metals.php"
    try:
        response = requests.get(url, timeout=10)
        return response.json()
    except Exception as e:
        print(f"Connection failed: {e}")
        return None

def save_entry(data, json_path):
    metals = data.get("metals", {})
    date_today = datetime.utcnow().strftime("%Y-%m-%d")

    entry = {
        "date": date_today,
        "GOLD": {
            "closing": metals["GOLD"]["ClosingValue"],
            "closing_timestamp": metals["GOLD"]["ClosingTimestamp"],
            "change": metals["GOLD"]["Change"],
            "change_percent": metals["GOLD"]["ChangePercent"]
        },
        "SILVER": {
            "closing": metals["SILVER"]["ClosingValue"],
            "closing_timestamp": metals["SILVER"]["ClosingTimestamp"],
            "change": metals["SILVER"]["Change"],
            "change_percent": metals["SILVER"]["ChangePercent"]
        },
        "PLATINUM": {
            "closing": metals["PLATINUM"]["ClosingValue"],
            "closing_timestamp": metals["PLATINUM"]["ClosingTimestamp"],
            "change": metals["PLATINUM"]["Change"],
            "change_percent": metals["PLATINUM"]["ChangePercent"]
        },
        "PALLADIUM": {
            "closing": metals["PALLADIUM"]["ClosingValue"],
            "closing_timestamp": metals["PALLADIUM"]["ClosingTimestamp"],
            "change": metals["PALLADIUM"]["Change"],
            "change_percent": metals["PALLADIUM"]["ChangePercent"]
        },
    }

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            history = json.load(f)
    except:
        history = []

    history = [h for h in history if h.get("date") != date_today]
    history.insert(0, entry)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

    print(f"Metals saved for {date_today}")

def scrape_closing():
    json_path = "WiseGoldMetalPrices.json"
    data = fetch_metals()
    if not data or not data.get("success"):
        print("Failed to fetch metals data")
        return
    save_entry(data, json_path)

def verify_today():
    json_path = "WiseGoldMetalPrices.json"
    date_today = datetime.utcnow().strftime("%Y-%m-%d")

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            history = json.load(f)
    except:
        history = []

    exists = any(h.get("date") == date_today for h in history)

    if exists:
        print(f"Entry for {date_today} already exists. No action needed.")
    else:
        print(f"Entry for {date_today} missing. Fetching...")
        data = fetch_metals()
        if not data or not data.get("success"):
            print("Failed to fetch metals data")
            return
        save_entry(data, json_path)

import sys
if len(sys.argv) > 1 and sys.argv[1] == "verify":
    verify_today()
else:
    scrape_closing()
