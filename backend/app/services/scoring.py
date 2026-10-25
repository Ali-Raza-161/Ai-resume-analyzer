"""Scoring, exact weights from the spec (total 100):
Contact 10, Structure 20, Skills 25, Experience 20, Formatting 15, Language 10.
Keyword matching: TF-IDF + cosine similarity (scikit-learn) with a
plain token-overlap fallback if scikit-learn is unavailable."""
import re
from .nlp import detect_sections, extract_skills, extract_contact

ACTION_VERBS = ["built", "developed", "improved", "led", "designed", "created", "increased", "reduced", "delivered", "managed", "implemented", "optimized"]
STOP = set("the a an and or of to in for on with by at from as is are was were be been it this that".split())

def _tokens(t):
    return [w for w in re.findall(r"[a-z0-9+#.]+", t.lower()) if w not in STOP]

def keyword_match(cv_text, jd_text):
    if not jd_text or not jd_text.strip():
        return {"similarity": 0.0, "matched": [], "missing": []}
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        v = TfidfVectorizer().fit_transform([cv_text, jd_text])
        sim = float(cosine_similarity(v[0], v[1])[0][0])
    except Exception:
        a, b = set(_tokens(cv_text)), set(_tokens(jd_text))
        sim = len(a & b) / max(len(b), 1)
    cv_skills, jd_skills = set(extract_skills(cv_text)), set(extract_skills(jd_text))
    return {"similarity": round(sim, 3), "matched": sorted(cv_skills & jd_skills), "missing": sorted(jd_skills - cv_skills)}

def analyze(cv_text, jd_text=""):
    sections = detect_sections(cv_text)
    skills = extract_skills(cv_text)
    contact = extract_contact(cv_text)
    low = cv_text.lower()
    contact_score = 10 if (contact["email"] and contact["phone"]) else (6 if (contact["email"] or contact["phone"]) else 0)
    if contact["link"]:
        contact_score = min(10, contact_score + 2)
    structure_score = round(20 * sum(sections.values()) / len(sections))
    skills_score = min(25, len(skills) * 3)
    verbs = sum(1 for v in ACTION_VERBS if v in low)
    numbers = len(re.findall(r"\d+\s?%", cv_text)) + len(re.findall(r"\b\d+\b", cv_text))
    exp_score = min(20, verbs * 3 + min(8, numbers))
    words = len(cv_text.split())
    fmt_score = 15 if 200 <= words <= 1200 else (10 if words > 50 else 3)
    sentences = [s for s in re.split(r"[.!?]", cv_text) if s.strip()]
    avg_len = (words / max(len(sentences), 1)) if sentences else 0
    lang_score = 10 if 8 <= avg_len <= 25 else 6
    cats = {"Contact information": contact_score, "Structure and sections": structure_score,
            "Skills and keywords": skills_score, "Experience quality": exp_score,
            "Formatting and ATS readability": fmt_score, "Language and grammar": lang_score}
    km = keyword_match(cv_text, jd_text)
    if jd_text.strip():
        cats["Skills and keywords"] = round(0.6 * skills_score + 0.4 * 25 * km["similarity"])
    overall = int(sum(cats.values()))
    tips = []
    if not sections.get("summary"): tips.append({"priority": "High", "text": "Add a 3 to 4 line professional summary."})
    if not any(re.search(r"\d+\s?%", cv_text) for _ in [1]): tips.append({"priority": "High", "text": "Add measurable results, e.g. 'improved load time by 40%'."})
    if km["missing"]: tips.append({"priority": "High", "text": f"Missing job-description skills: {', '.join(km['missing'][:5])} — add them if you have the experience."})
    if not contact["email"]: tips.append({"priority": "High", "text": "Add a valid email address to the contact section."})
    if words > 1200: tips.append({"priority": "Medium", "text": "CV is longer than about two pages — shorten it to the most relevant content."})
    if verbs < 2: tips.append({"priority": "Medium", "text": "Use action verbs like built, developed, improved in experience bullets."})
    if not sections.get("projects"): tips.append({"priority": "Low", "text": "Add a Projects section to show applied work."})
    return {"overall_score": overall, "category_scores": cats, "sections": sections,
            "matched_skills": km["matched"], "missing_skills": km["missing"],
            "match_percentage": round(km["similarity"] * 100, 1), "tips": tips,
            "skills_found": skills, "word_count": words}
