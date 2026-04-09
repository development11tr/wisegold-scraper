import requests
import json
import re

def get_article_image(url, headers):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        match = re.search(r'<meta property="og:image" content="([^"]+)"', response.text)
        if match:
            return match.group(1)
    except:
        pass
    return ""

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
        article_url = post.get("mainEntityOfPage", post.get("url", ""))
        print(f"Fetching image for: {article_url}")
        image = get_article_image(article_url, headers)
        
        results.append({
            "title": post.get("headline", ""),
            "text": post.get("text", ""),
            "date": post.get("datePublished", ""),
            "url": post.get("url", ""),
            "image": image
        })
    
    with open("WiseGoldLinkedInPosts.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"{len(results)} posts found")

scrape_wisegold()
