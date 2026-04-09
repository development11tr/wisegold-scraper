import requests
import json
import re

def scrape_wisegold():
    url = "https://www.linkedin.com/company/wisegoldcapital"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    
    response = requests.get(url, headers=headers)
    html = response.text
    
    match = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
    
    if not match:
        print("JSON-LD not found")
        return
    
    data = json.loads(match.group(1))
    graph = data.get("@graph", [])
    
    posts = [item for item in graph if item.get("@type") == "DiscussionForumPosting"]
    
    results = []
    for post in posts:
        results.append({
            "title": post.get("headline", ""),
            "text": post.get("text", ""),
            "date": post.get("datePublished", ""),
            "url": post.get("url", "")
        })
    
    with open("WiseGoldLinkedInPosts.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"{len(results)} posts found")

scrape_wisegold()
