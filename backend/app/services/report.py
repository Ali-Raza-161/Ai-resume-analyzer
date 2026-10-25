"""PDF report via ReportLab."""
def build_report(analysis: dict, title: str = "AI Resume Analyzer Report") -> bytes:
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    import io
    buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=A4); y = 800
    c.setFont("Helvetica-Bold", 16); c.drawString(40, y, title); y -= 30
    c.setFont("Helvetica", 12); c.drawString(40, y, f"Overall score: {analysis['overall_score']} / 100"); y -= 25
    for k, v in analysis["category_scores"].items():
        c.drawString(40, y, f"{k}: {v}"); y -= 18
    y -= 10; c.setFont("Helvetica-Bold", 12); c.drawString(40, y, "Tips:"); y -= 20
    c.setFont("Helvetica", 11)
    for t in analysis["tips"]:
        c.drawString(40, y, f"- [{t['priority']}] {t['text']}"[:110]); y -= 16
    c.save(); return buf.getvalue()
