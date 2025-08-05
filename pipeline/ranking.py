from collections import Counter
from datetime import datetime, timedelta
import pandas as pd 
severity_weights = {
   #  extract topic and weights
}
from collections import Counter
from datetime import timedelta
import pandas as pd

# Load topic severity weights from the CSV
def load_topic_severity(path: str) -> dict:
    topic_df = pd.read_csv(path)
    return {row["Topic"]: row["rank"] for _, row in topic_df.iterrows()}

# Count topics in the last X days
def compute_topic_frequencies(df: pd.DataFrame, days=7) -> Counter:
    cutoff = pd.Timestamp.utcnow() - timedelta(days=days)
    recent_df = df[df['published'] >= cutoff]
    all_topics = [topic for sublist in recent_df["matched_topics"] for topic in sublist]
    return Counter(all_topics)

# Normalize frequencies (0–1)
def normalize_frequencies(freq_dict: dict, total_entries: int) -> dict:
    return {topic: count / total_entries for topic, count in freq_dict.items()}

# Apply severity rank to each topic
def apply_weighting(normalized_freq: dict, severity_weights: dict) -> dict:
    return {
        topic: score * severity_weights.get(topic, 1.0)
        for topic, score in normalized_freq.items()
    }

# Full pipeline
def get_top_topics(df: pd.DataFrame, topic_severity_map: dict, days=7, top_n=5) -> list:
    freq = compute_topic_frequencies(df, days)
    recent_entries = df[df['published'] >= pd.Timestamp.utcnow() - timedelta(days=days)]
    normalized = normalize_frequencies(freq, total_entries=len(recent_entries))
    weighted = apply_weighting(normalized, topic_severity_map)
    sorted_topics = sorted(weighted.items(), key=lambda x: x[1], reverse=True)
    return sorted_topics[:top_n]
# Load data
df = pd.read_csv("feed_data/data/combined_with_topics.csv")
df["matched_topics"] = df["matched_topics"].apply(eval)  # convert string to list
df["published"] = pd.to_datetime(df["published"], utc=True)

# Load severity map from topic CSV
severity_map = load_topic_severity("feed_data/data/Topic_Keywords.csv")

# Get top 5 trending topics this week
top_topics = get_top_topics(df, severity_map, days=3000, top_n=5)
print("Top Topics This month:")
for topic, score in top_topics:
    print(f" - {topic}: {score:.3f}")
