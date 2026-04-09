# WiseGold Scraper

Automated data pipeline that collects and publishes two types of data from WiseGold Capital:

1. **LinkedIn Posts** — Weekly Pulse articles published on the WiseGold Capital LinkedIn page.
2. **Metal Closing Prices** — Daily closing prices for Gold, Silver, Platinum, and Palladium.

All data is stored as public JSON files and updated automatically via GitHub Actions.

---

## Public JSON Endpoints

These files are updated automatically and can be consumed from any website or application:

| File | URL |
|------|-----|
| LinkedIn Posts | `https://raw.githubusercontent.com/development11tr/wisegold-scraper/main/WiseGoldLinkedInPosts.json` |
| Metal Prices | `https://raw.githubusercontent.com/development11tr/wisegold-scraper/main/WiseGoldMetalPrices.json` |

---

## Repository Structure

```
wisegold-scraper/
├── .github/
│   └── workflows/
│       ├── scraper_posts.yml       # Workflow for LinkedIn posts
│       └── scraper_closing.yml     # Workflow for metal closing prices
├── scraper_posts.py                # Script that scrapes LinkedIn posts
├── scraper_closing.py              # Script that scrapes metal closing prices
├── scraper_posts.html              # HTML viewer for LinkedIn posts
├── scraper_closing.html            # HTML viewer for metal closing prices
├── WiseGoldLinkedInPosts.json      # Auto-generated: LinkedIn posts data
├── WiseGoldMetalPrices.json        # Auto-generated: Metal closing prices data
└── README.md
```

---

## How It Works

### 1. LinkedIn Posts (`scraper_posts`)

- Fetches the public HTML of the [WiseGold Capital LinkedIn page](https://www.linkedin.com/company/wisegoldcapital)
- Extracts structured post data from the `JSON-LD` block embedded in the page
- For each post, fetches the article URL to extract the cover image via `og:image`
- Saves all posts to `WiseGoldLinkedInPosts.json`

**Schedule:** Runs every day at **8:00 AM UTC** and **8:00 PM UTC**

**Data collected per post:**
```json
{
  "title": "Post headline",
  "text": "Full post text",
  "date": "2026-04-04T04:02:13.935Z",
  "url": "https://www.linkedin.com/posts/...",
  "image": "https://media.licdn.com/..."
}
```

---

### 2. Metal Closing Prices (`scraper_closing`)

- Fetches real-time metal data from the WiseGold proxy API
- Extracts the closing price, closing timestamp, and daily change for each metal
- Appends a new entry to `WiseGoldMetalPrices.json` each day (no duplicates)

**Schedule:** Runs every day at **9:00 PM UTC (5:00 PM EDT)**

**Data collected per day:**
```json
{
  "date": "2026-04-09",
  "GOLD": {
    "closing": "4794.1600",
    "closing_timestamp": "2026-04-09T13:30:03-04:00",
    "change": "39.4400",
    "change_percent": "0.83"
  },
  "SILVER": { ... },
  "PLATINUM": { ... },
  "PALLADIUM": { ... }
}
```

---

## Consuming the Data

You can use the JSON endpoints in any HTML page with a simple `fetch`:

```html
<!-- LinkedIn Posts -->
<script>
  fetch('https://raw.githubusercontent.com/development11tr/wisegold-scraper/main/WiseGoldLinkedInPosts.json')
    .then(r => r.json())
    .then(posts => {
      posts.forEach(post => {
        console.log(post.title, post.date, post.url);
      });
    });
</script>

<!-- Metal Prices -->
<script>
  fetch('https://raw.githubusercontent.com/development11tr/wisegold-scraper/main/WiseGoldMetalPrices.json')
    .then(r => r.json())
    .then(history => {
      history.forEach(entry => {
        console.log(entry.date, entry.GOLD.closing);
      });
    });
</script>
```

This works from any server — GoDaddy, WordPress, Webflow, or any platform that supports JavaScript.

---

## HTML Viewers

Two ready-to-use HTML files are included:

- **`scraper_posts.html`** — Displays LinkedIn posts with image, title, date, text, and link.
- **`scraper_closing.html`** — Displays a historical table of daily metal closing prices.

Both files fetch data directly from the public JSON URLs above and can be hosted on any web server.

---

## Data Sources

- **LinkedIn Posts:** [WiseGold Capital on LinkedIn](https://www.linkedin.com/company/wisegoldcapital) — public page, no authentication required.
- **Metal Prices:** WiseGold Capital internal proxy API serving real-time precious metals data.

---

## Notes

- The JSON files in this repository are auto-generated and committed by GitHub Actions on every run.
- No credentials, API keys, or sensitive data are stored in this repository.
- LinkedIn data is extracted from publicly accessible pages only.
