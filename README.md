DrillPhish Recommendation System
A recommendation system that analyzes cybersecurity topic mentions in feed CSV files (simulating https://thedfirreport.com/feed/) and recommends Drill-Phish courses via personalized emails, integrating with the Drill-Phish API and announcement module.
Project Overview

Purpose: Identify the top 3–5 cybersecurity topics (e.g., Active Directory, Malware, Telecom) from feed data and recommend relevant Drill-Phish courses based on user roles (executive, technical, general) and language preferences (e.g., English, Arabic).
Scope: Process streaming feed CSV data, map topics to courses, generate emails via the Drill-Phish announcement module, and track engagement.
Goals:
Enhance cybersecurity awareness with role-based recommendations.
Support Drill-Phish’s gamified, localized learning management system (LMS).
Track email open rates and course enrollment.



Repository Structure
DrillPhish-Recommendation-System/
├── data/
│   ├── feed_data_1.csv              # Feed entries (CSV 1)
│   ├── feed_data_2.csv              # Feed entries (CSV 2)
│   └── Course_Mappings.csv          # Course data (simulating API)
├── docs/
│   ├── Recommendation System Requirements v2.md  # Phase 1 requirements
│   ├── Topic_Extraction_Plan.md                 # Phase 2 topic extraction
│   └── Recommendation_Plan.md                   # Phase 3 recommendation and email
