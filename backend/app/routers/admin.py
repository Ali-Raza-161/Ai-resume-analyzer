from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import json, os
from ..db import get_db
from ..models.models import User, Analysis, Skill
from ..schemas.schemas import SkillIn
from .common import current_user
router = APIRouter(prefix="/api/admin", tags=["admin"])
@router.get("/stats")
def stats(user=Depends(current_user), db: Session = Depends(get_db)):
    return {"total_users": db.query(User).count(), "total_analyses": db.query(Analysis).count(),
            "total_skills": db.query(Skill).count()}
@router.post("/skills")
def add_skill(body: SkillIn, user=Depends(current_user), db: Session = Depends(get_db)):
    s = Skill(name=body.name, category=body.category); db.add(s)
    try: db.commit()
    except Exception: db.rollback(); return {"error": "Skill already exists"}
    return {"id": s.id, "name": s.name, "category": s.category}
