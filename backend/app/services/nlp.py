"""Section + skill detection. Regex/tokenizer based.
spaCy is NOT run here: the en_core_web_sm model was not downloaded in this
environment, so this module uses a documented regex fallback with the same
outputs (sections, skills, contact). Swap in spaCy phrase matching later
without changing the scoring API."""
import json, os, re
SECTIONS = ["summary", "education", "experience", "skills", "projects"]
with open(os.path.join(os.path.dirname(__file__), "..", "data", "skills.json")) as f:
    SKILL_LIST = [s["name"] for s in json.load(f)["skills"]]

def detect_sections(text: str):
    low = text.lower()
    return {s: (s in low) for s in SECTIONS}

def extract_skills(text: str):
    low = text.lower()
    return sorted({s for s in SKILL_LIST if s.lower() in low})

def extract_contact(text: str):
    email = bool(re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", text))
    phone = bool(re.search(r"(\+?\d[\d\s-]{7,}\d)", text))
    link = ("linkedin.com" in text.lower()) or ("github.com" in text.lower())
    return {"email": email, "phone": phone, "link": link}
