from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
Base = declarative_base()
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True); name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False); password_hash = Column(String, nullable=False)
    role = Column(String, default="user"); created_at = Column(DateTime, default=datetime.utcnow)
    resumes = relationship("Resume", back_populates="user")
class Resume(Base):
    __tablename__ = "resumes"
    id = Column(Integer, primary_key=True); user_id = Column(Integer, ForeignKey("users.id"))
    file_name = Column(String); file_type = Column(String); extracted_text = Column(Text)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="resumes")
    analyses = relationship("Analysis", back_populates="resume")
class Analysis(Base):
    __tablename__ = "analyses"
    id = Column(Integer, primary_key=True); resume_id = Column(Integer, ForeignKey("resumes.id"))
    job_description = Column(Text, default=""); overall_score = Column(Integer)
    category_scores = Column(JSON); matched_skills = Column(JSON); missing_skills = Column(JSON); tips = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    resume = relationship("Resume", back_populates="analyses")
class Skill(Base):
    __tablename__ = "skills"
    id = Column(Integer, primary_key=True); name = Column(String, unique=True); category = Column(String)
