import requests
import json
import re
from datetime import datetime

def scrape_wisegold():
    url = "https://www.linkedin.com/company/wisegoldcapital"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "es-ES,es;q=0.9",
    }
    
    response = requests.get(url, headers=headers)
    html = response.text
    
    # Extraer el JSON-LD
    match = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
    
    if not match:
        print("No se encontró JSON-LD")
        return
    
    data = json.loads(match.group(1))
    graph = data.get("@graph", [])
    
    posts = [item for item in graph if item.get("@type") == "DiscussionForumPosting"]
    
    results = []
    for post in posts:
        results.append({
            "titulo": post.get("headline", ""),
            "texto": post.get("text", ""),
            "fecha": post.get("datePublished", ""),
            "url": post.get("url", "")
        })
    
    with open("resultados.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"{len(results)} posts encontrados")

scrape_wisegold()
