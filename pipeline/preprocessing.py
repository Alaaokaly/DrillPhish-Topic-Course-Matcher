import feedparser
import csv
import pandas as pd 
from pandas import DataFrame
from bs4 import BeautifulSoup
import re
# takes feed input and do some nlp preprocessing 
feeds = {
    "bhis": "https://www.blackhillsinfosec.com/blog/feed/",
    "dfir": "https://thedfirreport.com/feed/",
    "elastic": "https://www.elastic.co/security-labs/rss/feed.xml"
}
def fetch_data(feed_links:dict):
    combined_entries = []

    for source, url in feed_links.items():
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

    
    return pd.DataFrame(combined_entries, columns=[ "source", "title", "author", "published", "link", "tags", "summary"])
        

def pre_processing(data: DataFrame, save_path: str):
    data['title'] = data['title'].str.lower().str.strip()
    data['published'] = pd.to_datetime(data['published'], utc=True, errors='coerce', format='mixed')
    data['year'] = data['published'].dt.year
    data['month'] = data['published'].dt.month

    # Clean tags (lowercase list → then convert back to string)
    data['tags'] = data['tags'].apply(lambda x: [tag.strip().lower() for tag in x.split(',')])
    data['tags'] = data['tags'].apply(lambda tags: ", ".join(tags) if isinstance(tags, list) else "")

    # Clean summary HTML
    data['summary'] = data['summary'].apply(lambda x: BeautifulSoup(x, "html.parser").get_text())
    data['summary'] = data['summary'].str.replace(r'http\S+', '', regex=True)
    data['summary'] = data['summary'].str.replace(r'The post .* appeared first on .*', '', regex=True)
    data['summary'] = data['summary'].str.replace(r'\n', '', regex=True)
    data['summary'] = data['summary'].str.strip().str.lower()

    # Write to CSV
    with open(save_path + ".csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "source", "title", "author", "published",  'year', 'month',"link", "tags", "summary"
        ])
        writer.writeheader()
        writer.writerows(data.to_dict(orient='records'))

    print(f"[INFO] Saved cleaned data to {save_path}.csv")
    return data




data = fetch_data(feed_links=feeds)
data = pre_processing(data,save_path='feed_data/data/combined_df')