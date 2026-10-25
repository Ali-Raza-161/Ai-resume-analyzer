from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session
from typing import Optional
import json
from ..db import get_db
from ..models.models import Resume, Analysis
from ..services.parser import extract_text
from ..services.scoring import analyze
from ..services.report import build_report
from .common import current_user
router = APIRouter(prefix="/api", tags=["resumes"])

@router.post("/resumes/analyze")
async def analyze_cv(file: UploadFile = File(...), job_description: Optional[str] = Form(""),
                     user=Depends(current_user), db: Session = Depends(get_db)):
    content = await file.read()
    try: text = extract_text(file.filename, content)
    except ValueError as e: raise HTTPException(400, str(e))
    if not text: raise HTTPException(400, "No readable text found in file (scanned image PDFs need OCR, out of scope for v1)")
    res = Resume(user_id=int(user["sub"]), file_name=file.filename, file_type=file.filename.rsplit(".", 1)[-1].lower(), extracted_text=text)
    db.add(res); db.commit(); db.refresh(res)
    a = analyze(text, job_description or "")
    an = Analysis(resume_id=res.id, job_description=job_description or "", overall_score=a["overall_score"],
                  category_scores=a["category_scores"], matched_skills=a["matched_skills"],
                  missing_skills=a["missing_skills"], tips=a["tips"])
    db.add(an); db.commit(); db.refresh(an)
    return {"analysis_id": an.id, "resume_id": res.id, **a}

@router.get("/analyses")
def list_analyses(user=Depends(current_user), db: Session = Depends(get_db)):
    rows = db.query(Analysis).join(Resume).filter(Resume.user_id == int(user["sub"])).order_by(Analysis.created_at.desc()).all()
    return [{"id": r.id, "resume_id": r.resume_id, "overall_score": r.overall_score, "created_at": str(r.created_at)} for r in rows]

@router.get("/analyses/{aid}")
def get_analysis(aid: int, user=Depends(current_user), db: Session = Depends(get_db)):
    r = db.query(Analysis).join(Resume).filter(Analysis.id == aid, Resume.user_id == int(user["sub"])).first()
    if not r: raise HTTPException(404, "Analysis not found")
    return {"id": r.id, "resume_id": r.resume_id, "overall_score": r.overall_score,
            "category_scores": r.category_scores, "matched_skills": r.matched_skills,
            "missing_skills": r.missing_skills, "tips": r.tips, "created_at": str(r.created_at)}

@router.get("/analyses/{aid}/report")
def report(aid: int, user=Depends(current_user), db: Session = Depends(get_db)):
    r = db.query(Analysis).join(Resume).filter(Analysis.id == aid, Resume.user_id == int(user["sub"])).first()
    if not r: raise HTTPException(404, "Analysis not found")
    pdf = build_report({"overall_score": r.overall_score, "category_scores": r.category_scores, "tips": r.tips})
    return Response(content=pdf, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename=resume-report-{aid}.pdf"})

@router.delete("/analyses/{aid}")
def delete_analysis(aid: int, user=Depends(current_user), db: Session = Depends(get_db)):
    r = db.query(Analysis).join(Resume).filter(Analysis.id == aid, Resume.user_id == int(user["sub"])).first()
    if not r: raise HTTPException(404, "Analysis not found")
    db.delete(r); db.commit(); return {"deleted": aid}
