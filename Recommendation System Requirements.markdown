# Recommendation System Requirements


## System Overview
- **Purpose**: Identify the most mentioned cybersecurity topics in feeds and recommend corresponding Drill-Phish courses via personalized emails, highlighting “Most Concerning Problems” (e.g., “We recommend [Course Title] to address [Topic]”).
- **Scope**: Process streaming feed data, query the Drill-Phish API for course data, and generate tailored email recommendations using the Drill-Phish announcement module.
- **Goals**:
  - Deliver relevant, role-based course recommendations to enhance matching .
  - Support Drill-Phish’s gamified, localized content delivery.
  - Track user engagement via the Drill-Phish admin dashboard.

## Inputs
- **Feed Data**:
  - Source:  (RSS format).
  - Fields: `source`, `title`, `author`, `published`, `link`, `tags`, `summary`.
  - Sample Entry Analysis:
    - Title: “Detecting ADCS Privilege Escalation”
    - Tags: Active Directory, ADCS, Blue Team, etc.
    - Summary: Mentions Active Directory Certificate Services (ADCS) vulnerabilities.
    - Topics Detected: Active Directory (explicit in tags); potential implicit topics (e.g., privilege escalation) in summary.
    - Challenges: “ADCS” not in the 40 provided topics; may map to “Active Directory” or “Security Controls.” Unstructured summary text requires NLP for implicit topic detection.
- **Drill-Phish API Data**:
  - Format: JSON with fields `{title, scope(description), level, language, topic}`.
  - Sample Course:
    - Title: “Best Practices for Telecom”
    - Scope: “Explore advanced techniques and strategies to mitigate risks related to Telecom.”
    - Level: Intermediate
    - Language: English 
    - Topic: Telecom
  - Analysis: Direct mapping for “Telecom”; no course for “Active Directory” in sample data—may map to “Security Controls” or “Security Essentials.” Additional API data needed for full 40-topic coverage.


## Outputs
- **Personalized Emails**:
  - **Structure**:
    - Greeting: Address user by name (e.g., “Dear {user_name}”).
    - Most Concerning Problems: List top 3–5 topics (e.g., “Active Directory vulnerabilities”) with brief descriptions from feed summaries.
    - Course Recommendations: Suggest courses (e.g., “Best Practices for Telecom” for Telecom) with titles, scopes, and links.
    - Call-to-Action: Encourage course enrollment (e.g., “Start this course now”).
    - Compliance: Include acknowledgment option for policy management.
  - **Example**:
    ```
    Dear {user_name},
    Based on recent cybersecurity trends, here are the Most Concerning Problems:
    - Active Directory: Vulnerabilities in ADCS can lead to privilege escalation.
    We recommend "Security Controls" to address this issue.
    Start this course now: {course_link}
    ```
  - **Delivery**: Via Drill-Phish announcement module with AI-driven content customization.
  


## Feed Analysis
- **Format**: RSS with fields `source`, `title`, `tags`, `summary`, etc.
- **Topic Detection**:
  - Explicit: Topics like “Active Directory” in `tags`.
  - Implicit: Terms like “privilege escalation” in `summary` may map to “Insider Threat” or “Security Controls.”
- **Challenges**:
  - Unstructured `summary` text.
  - Variations (e.g., “ADCS” not in 40 topics) need mapping to existing topics.

- **Plan**:
  - Parse `title`, `tags`, `summary`.
  - Analyze 10–20 feed entries to confirm topic patterns.
  - Use keyword matching for explicit topics; explore NLP for implicit ones.

## Course Data Analysis
- **Structure**: JSON with `{title, scope, level, language, topic}`.
- **Mapping**:
  - Direct: “Telecom” → “Best Practices for Telecom.”
  - Gaps: No course for “Active Directory”; propose mapping to “Security Controls” or “Security Essentials.”
- **Categorization**:
  - Levels: Beginner, Intermediate (e.g., Telecom course), Advanced.
  - Languages: English (from sample); others to be confirmed.

- **Plan**:
  - Group similar topics (e.g., “Smishing,” “Vishing” under “Phishing”).
  - Store mappings in a spreadsheet or database (e.g., `{topic: "Telecom", course_title: "Best Practices for Telecom", level: "Intermediate", language: "English"}`).



## Future Features
- **Streaming Feeds**: Process updates in real-time or near-real-time (e.g., hourly or daily batches).
- **Compliance**: Adhere to Drill-Phish’s policy management for email acknowledgment; comply with regulations 
-**User Metadata and Segmentation**:
  - Source: Drill-Phish LMS.
  - Expected Fields: Job title (e.g., executive, technical user, general employee), department, location, language preference, completed courses, badges.

  - Note: Exact fields to be confirmed with Drill-Phish team.

  - **Criteria**:
    - **Role**: Executives (e.g., beginner-level courses), technical users (e.g., intermediate/advanced), general employees (e.g., beginner).
    - **Progress**: Prioritize incomplete courses or align with badges/certifications from Drill-Phish LMS.
  - **Example**:
    - Technical user, English preference: Recommend “Best Practices for Telecom” (Intermediate) for Telecom topic.

- **Integration**: Use Drill-Phish API for course data and announcement module for email delivery.

    - **Tracking**: Exact activities to be confirmed with Drill-Phish team 

    ## Preprocessing Pipeline
    - **Feed Parsing**:
      - Tool: Feedparser to extract `title`, `tags`, `summary`.
      - Output: Raw text for topic detection.
    - **Topic Identification**:
      - Keyword Matching: For explicit topics (e.g., “Active Directory” in `tags`).
      - NLP: spaCy or NLTK for implicit topics (e.g., “privilege escalation” in `summary`).
      - Research: Compare spaCy (fast, good for NER), NLTK (simple for keywords), BERT (accurate but resource-intensive).

# PipeLine 
  ## Preprocessing :

  ## Explicit extraction 
  1. keyword dictionary for the 40 topics, including synonyms and variations

  ## Implicit Extraction  (e.g., “privilege escalation” in summary → Insider Threat)
  1. Use an LLm to label the summary and title even if the the words aren't there 
  2. create embeddings for each feed entry using models like `sentence-transformer`
  3. then use `cos-sim` between feed and embeddings from LLM  


 ### Plan NLP techniques:

1. Keyword Matching: For tags (e.g., “Active Directory”).
2. TF-IDF: Rank keywords in summary (e.g., “vulnerabilities” prominence).
3. spaCy NER: Detect entities like “privilege escalation” in summary.
4. LDA (Topic Modeling): Extract latent topics from summary if multiple topics present.

### Topic Ranking Mechanism  (Rank topics by frequency in the feed over a 7-day window to select the top 3–5 for emails)

1. Calculate frequency (e.g., count “Active Directory” in tags, summary).
2. Normalize frequencies (e.g., divide by total entries).
3. Plan severity weighting (e.g., Malware > Clean Office Policy).

`score = frequency × weight.`
count freq 
normalize by entries 
weight severity

`{topic, count, timestamp}`


| Field     | Technique                           | Purpose                                     |
| --------- | ----------------------------------- | ------------------------------------------- |
| `tags`    | Keyword Match                       | High-precision detection via dictionary     |
| `title`   | Fuzzy Matching + TF-IDF             | Rank important topic-relevant terms         |
| `summary` | spaCy NER, Phrase Matching, Regex   | Detect implicit concepts and attacks        |
| `summary` | LLM-Based Classification (optional) | Handle abstraction, metaphor, indirect cues |

flowchart TD
    A[Input Feed (CSV)] --> B[Preprocessing (Lowercase, Clean)]
    B --> C[Keyword Matching (tags, title)]
    C --> [ summary ] 
    ↓
   4[ NER/Phrase Matching ]
    → if match: ✅ return topics
    → else: 
        ↓
    [ Basic LLM Classification ]
        → return LLM-detected topics
    F --> G[Multi-label Topic Assignment]
    G --> H[Output: Topics per Feed Entry]



