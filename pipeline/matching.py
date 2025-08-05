import pandas as pd
from rapidfuzz import fuzz
from rapidfuzz import process
from preprocessing import fetch_data, pre_processing

from tqdm import tqdm

from groq import Groq
import os

import requests
from bs4 import BeautifulSoup

from dotenv import load_dotenv
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))



# Load topic dictionary
def load_topic_dictionary(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["Keywords"] = df["Keywords"].apply(lambda x: [kw.strip().lower() for kw in x.split(",")])
    df["Synonyms"] = df["Synonyms"].apply(lambda x: [syn.strip().lower() for syn in x.split(",")])
    return df

# Match using keyword/synonym in summary
def match_summary_to_topics(summary: str, topic_df: pd.DataFrame) -> list:
    if not isinstance(summary, str):
        return []

    summary = summary.lower()
    matched_topics = []

    for _, row in topic_df.iterrows():
        topic = row.get("Topic", "")
        keywords = row.get("Keywords", [])
        synonyms = row.get("Synonyms", [])

        if not isinstance(keywords, list):
            keywords = []
        if not isinstance(synonyms, list):
            synonyms = []

        terms = keywords + synonyms

        if any(term in summary for term in terms):
            matched_topics.append(topic)

    return matched_topics

# Match using fuzzy score from title + tags
def match_title_tags_fuzzy(row: pd.Series, topic_df: pd.DataFrame, threshold: int = 85) -> list:
    text = f"{row['title']} {row['tags']}".lower()
    matched_topics = set()

    for _, topic_row in topic_df.iterrows():
        terms = topic_row["Keywords"] + topic_row["Synonyms"]
        for term in terms:
            score = fuzz.partial_ratio(term, text)
            if score >= threshold:
                matched_topics.add(topic_row["Topic"])
                break

    return list(matched_topics)
def fetch_article_text(url: str) -> str:
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Remove scripts/styles and extract visible text
        for tag in soup(["script", "style"]): tag.decompose()
        return ' '.join(soup.stripped_strings)
    except Exception as e:
        print(f"[WARN] Failed to fetch article text from {url}: {e}")
        return ""
    
def truncate_text(text, max_tokens=2000):
    # Roughly 4 characters per token
    max_chars = max_tokens * 2
    return text[:max_chars]

def llm_classify_summary(summary, topic_list, url=None, model="llama-3.1-8b-instant"):
    article_text = fetch_article_text(url) if url else ""
    context = article_text if article_text else summary

    context = truncate_text(context, max_tokens=2000)  # limit to 2000 tokens

    prompt = f"""You are a cybersecurity topic classifier.

Given the content below, identify all relevant topics from the list.

Topics: {topic_list}

Content: {context}

Return only a valid Python list of matched topics.
"""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        output = response.choices[0].message.content.strip()
        return eval(output) if output.startswith("[") else []
    except Exception as e:
        print(f"[Groq ERROR]: {e}")
        return []



# Apply matching pipeline to dataframe
def apply_topic_matching(df: pd.DataFrame, topic_csv_path: str, use_llm=False) -> pd.DataFrame:
    topic_df = load_topic_dictionary(topic_csv_path)

    matched_topics = []
    unmatched_indices = []
    unmatched_summaries = []

    print("[INFO] Processing feed entries...")
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Matching topics"):
        summary_matches = match_summary_to_topics(row['summary'], topic_df)
        fuzzy_matches = match_title_tags_fuzzy(row, topic_df)
        all_matches = list(set(summary_matches + fuzzy_matches))

        if not all_matches and use_llm:
            unmatched_indices.append(idx)
            unmatched_summaries.append(row['summary'])
            matched_topics.append([])  # placeholder
        else:
            matched_topics.append(all_matches)

    # Only call Groq for unmatched
    if use_llm and unmatched_summaries:
        print(f"[INFO] Classifying {len(unmatched_summaries)} unmatched summaries with LLaMA 3...")
        topic_list = topic_df["Topic"].tolist()
        llama_results = []

        for summary in tqdm(unmatched_summaries, desc="LLaMA 3 Groq Classifier"):
            result = llm_classify_summary(summary, topic_list, url=row['link'])

            llama_results.append(result)

            # Log live
            print(f"[LLM] Topics matched: {result}")

        for idx, topics in zip(unmatched_indices, llama_results):
            matched_topics[idx] = topics

    df["matched_topics"] = matched_topics
    return df

# Run pipeline
df = pd.read_csv("feed_data/data/combined_df.csv")
df = apply_topic_matching(df, "feed_data/data/Topic_Keywords.csv", use_llm=True)
df.to_csv("feed_data/data/combined_with_topics.csv", index=False)
