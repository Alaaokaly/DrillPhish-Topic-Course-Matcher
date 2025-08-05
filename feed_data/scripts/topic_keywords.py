import pandas as pd

# Define the initial 10 topics with associated data
data = [
    {
        "Topic": "Active Directory",
        "Keywords": "Active Directory, AD, ADCS",
        "Synonyms": "directory services, domain controller",
        "Notes": "Map 'ADCS' to Active Directory or Security Controls; confirm with stakeholders."
    },
    {
        "Topic": "Telecom",
        "Keywords": "telecom, telecommunications, VoIP",
        "Synonyms": "telephony",
        "Notes": "Matches 'Best Practices for Telecom'."
    },
    {
        "Topic": "Malware",
        "Keywords": "malware, virus, trojan, ransomware",
        "Synonyms": "spyware, worm",
        "Notes": "Matches 'Essentials of Malware'; check ransomware overlap."
    },
    {
        "Topic": "Ransomware",
        "Keywords": "ransomware, crypto-locker, extortion",
        "Synonyms": "encryption malware",
        "Notes": "May overlap with Malware course."
    },
    {
        "Topic": "Phishing",
        "Keywords": "phishing, email phishing, spear-phishing",
        "Synonyms": "email scam",
        "Notes": "Awaiting course mapping."
    },
    {
        "Topic": "Social Engineering",
        "Keywords": "social engineering, deception, manipulation",
        "Synonyms": "pretexting, baiting",
        "Notes": "May relate to phishing and insider threat."
    },
    {
        "Topic": "Insider Threat",
        "Keywords": "insider threat, internal attacker, rogue employee",
        "Synonyms": "privilege abuse, insider risk",
        "Notes": "Map 'privilege escalation' in summary to this topic."
    },
    {
        "Topic": "Security Controls",
        "Keywords": "security controls, access control, policies",
        "Synonyms": "safeguards, security measures",
        "Notes": "May include 'ADCS', firewall, or endpoint configurations."
    },
    {
        "Topic": "BYOD",
        "Keywords": "BYOD, bring your own device, mobile device security",
        "Synonyms": "personal device use",
        "Notes": "Tag mentions of mobile or personal device policy."
    },
    {
        "Topic": "ATM Security",
        "Keywords": "ATM security, ATM fraud, skimming",
        "Synonyms": "cash machine security",
        "Notes": "Detect 'skimming' or 'physical compromise' in summary."
    }
]

# Create a DataFrame
df = pd.DataFrame(data)

# Save to Excel
excel_path = "/mnt/data/Topic_Keywords.xlsx"
df.to_excel(excel_path, index=False)

excel_path
