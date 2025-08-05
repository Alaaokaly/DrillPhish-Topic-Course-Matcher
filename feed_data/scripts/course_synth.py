import csv
import random

# List of course topics provided by the user
COURSE_TOPICS = [
    "ATM Security", "Bring Your Own Device (BYOD)", "Continuity",
    "Business Email Compromise", "Clean Office Policy", "Cloud Security",
    "Customer Care", "Data Encryption", "Data Security",
    "Email Phishing Intro", "Email Phishing (Tactics)", "Financial Security",
    "Health Care Data Privacy", "Information Leakage", "Insider Threat",
    "Malware", "Mobile Security", "Laundering", "Operation Technology",
    "OWASP TOP 10", "Password Security", "PCI", "Physical Security", "PII",
    "QR Phishing", "Ransomware", "Real attacks", "Regulations", "Reporting",
    "Security Controls", "Security Essentials", "Security Procedures",
    "Smishing", "Social engineering", "Telecom", "Telework", "Threat Actors",
    "USB Attacks", "Acceptance Policy", "Using AI Safely", "Vishing",
    "Web Attacks"
]

# Possible course levels
COURSE_LEVELS = ["Beginner", "Intermediate", "Advanced", "Expert"]

# Possible course languages
COURSE_LANGUAGES = ["English","Arabic"]

def generate_course_data(num_entries=2000):
    """
    Generates a list of dictionaries, each representing a course API call.
    """
    courses = []
    for i in range(num_entries):
        topic = random.choice(COURSE_TOPICS)
        level = random.choice(COURSE_LEVELS)
        language = random.choice(COURSE_LANGUAGES)

        # Generate a title based on the topic
        title_templates = [
            f"Understanding {topic}",
            f"Essentials of {topic}",
            f"Mastering {topic} for Professionals",
            f"Advanced Strategies in {topic}",
            f"Introduction to {topic}",
            f"Securing Your Assets with {topic}",
            f"The Complete Guide to {topic}",
            f"Best Practices for {topic}",
            f"Navigating the World of {topic}"
        ]
        title = random.choice(title_templates)

        # Generate a description (scope) based on the topic
        description_templates = [
            f"This course provides an in-depth look at {topic}, covering key concepts and practical applications.",
            f"Learn the fundamental principles of {topic} and how to apply them in real-world scenarios.",
            f"Explore advanced techniques and strategies to mitigate risks related to {topic}.",
            f"A comprehensive overview of {topic}, designed for both beginners and experienced professionals.",
            f"Understand the latest trends and challenges in {topic} and how to effectively address them.",
            f"This module focuses on the practical implementation of {topic} security measures.",
            f"Gain critical insights into {topic} and its impact on modern cybersecurity.",
            f"Develop robust policies and procedures to enhance your organization's {topic} posture."
        ]
        scope = random.choice(description_templates)

        courses.append({
            "title": title,
            "scope": scope,
            "level": level,
            "language": language,
            "topic":topic
        })
    return courses

def write_to_csv(data, filename="feed_data/courses.csv"):
    """
    Writes the generated course data to a CSV file.
    """
    if not data:
        print("No data to write to CSV.")
        return

    # Define the fieldnames (CSV headers)
    fieldnames = ["title", "scope", "level", "language","topic"]

    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()  # Write the header row
            for row in data:
                writer.writerow(row)
        print(f"Successfully generated {len(data)} API call entries and saved to '{filename}'.")
    except IOError as e:
        print(f"Error writing to CSV file: {e}")

if __name__ == "__main__":
    print("Generating course data...")
    course_data = generate_course_data(num_entries=2000)
    write_to_csv(course_data)
    print("Script finished.")
