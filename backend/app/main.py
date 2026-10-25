import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import engine
from .models.models import Base, Skill
from .routers import auth, resumes, admin
import json
Base.metadata.create_all(bind=engine)
# Seed skills dictionary once
from sqlalchemy.orm import Session
from .db import Session as Sess
with Sess() as db:
    if db.query(Skill).count() == 0:
        data = json.load(open(os.path.join(os.path.dirname(__file__), "data", "skills.json")))
        for s in data["skills"]: db.add(Skill(name=s["name"], category=s["category"]))
        db.commit()
app = FastAPI(title="AI Resume Analyzer")
app.add_middleware(CORSMiddleware, allow_origins=[os.environ.get("FRONTEND_ORIGIN", "http://localhost:5173")],
                   allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(auth.router); app.include_router(resumes.router); app.include_router(admin.router)
@app.get("/api/health")
def health(): return {"ok": True, "service": "ai-resume-analyzer"}
