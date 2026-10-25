import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from app.services.scoring import analyze, keyword_match
from app.services.parser import extract_text
SAMPLE = """Ali Raza
ali@example.com | +92 300 1234567 | linkedin.com/in/ali | github.com/ali
Summary: AI Web Developer with React and Python experience.
Education: BS AI, UMT Lahore, 2024.
Experience: Developed a chatbot, improved load time by 40%, led a team of 3.
Skills: Python, React, JavaScript, SQL, Docker
Projects: ChatDesk, SupportPilot."""
def test_score_range():
    a = analyze(SAMPLE, "We need Python, React, SQL and Docker experience.")
    assert 0 <= a["overall_score"] <= 100
    assert sum(a["category_scores"].values()) == a["overall_score"]
    assert "Python" in a["skills_found"] and "React" in a["skills_found"]
def test_keyword_match():
    km = keyword_match(SAMPLE, "Python React SQL Docker")
    assert km["similarity"] > 0
    assert "Python" in km["matched"]
def test_parser_rejects_bad_type():
    try:
        extract_text("cv.txt", b"hello"); assert False
    except ValueError: pass
def test_tips_present():
    a = analyze("John Doe\nNo sections here.")
    assert a["tips"]
