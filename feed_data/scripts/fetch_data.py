import feedparser
import csv

# Define your RSS feeds
feeds = {
    "bhis": "https://www.blackhillsinfosec.com/blog/feed/",
    "dfir": "https://thedfirreport.com/feed/",
    "elastic": "https://www.elastic.co/security-labs/rss/feed.xml"
}

# Unified list for all parsed entries
combined_entries = []

for source, url in feeds.items():
    feed = feedparser.parse(url)

    for entry in feed.entries:
        title = entry.get("title", "").strip()
        author = entry.get("author", "").strip()
        published = entry.get("published", "").strip()
        link = entry.get("link", "").strip()
        tags = ", ".join(tag["term"] for tag in entry.get("tags", [])) if entry.get("tags") else ""
        summary = entry.get("summary", "").strip()

        combined_entries.append({
            "source": source,
            "title": title,
            "author": author,
            "published": published,
            "link": link,
            "tags": tags,
            "summary": summary
        })

# Write to CSV
with open("combined_threat_feeds.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "source", "title", "author", "published", "link", "tags", "summary"
    ])
    writer.writeheader()
    writer.writerows(combined_entries)

print("✅ Saved to combined_threat_feeds.csv")
