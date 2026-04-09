from playwright.sync_api import sync_playwright
import json
from datetime import datetime

def scrape_wisegold():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        page.goto("https://www.linkedin.com/company/wisegoldcapital/posts/?feedView=all")
        page.wait_for_timeout(5000)
        
        posts = page.query_selector_all(".feed-shared-update-v2")
        
        results = []
        for post in posts:
            try:
                text = post.query_selector(".feed-shared-text")
                results.append({
                    "texto": text.inner_text() if text else "",
                    "fecha": datetime.now().isoformat()
                })
            except:
                pass
        
        browser.close()
        
        with open("resultados.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"{len(results)} posts encontrados")

scrape_wisegold()
