"""CV text extraction: PDF via pdfplumber, DOCX via python-docx. Max 5 MB, PDF/DOCX only."""
import io
MAX_SIZE = 5 * 1024 * 1024

def extract_text(filename: str, content: bytes) -> str:
    if len(content) > MAX_SIZE:
        raise ValueError("File exceeds 5 MB limit")
    low = filename.lower()
    if low.endswith(".pdf"):
        import pdfplumber
        texts = []
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            for page in pdf.pages:
                texts.append(page.extract_text() or "")
        return "\n".join(texts).strip()
    if low.endswith(".docx"):
        from docx import Document
        doc = Document(io.BytesIO(content))
        return "\n".join(p.text for p in doc.paragraphs).strip()
    raise ValueError("Only PDF and DOCX files are allowed")
