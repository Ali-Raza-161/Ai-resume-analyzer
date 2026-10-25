from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..models.models import User
from ..schemas.schemas import Register, Login
from ..auth import hash_pw, check_pw, make_token
router = APIRouter(prefix="/api/auth", tags=["auth"])
@router.post("/register")
def register(body: Register, db: Session = Depends(get_db)):
    if db.query(User).filter_by(email=body.email).first():
        raise HTTPException(400, "Email already registered")
    u = User(name=body.name, email=body.email, password_hash=hash_pw(body.password))
    db.add(u); db.commit(); db.refresh(u)
    return {"id": u.id, "name": u.name, "email": u.email, "token": make_token(u.id, u.role)}
@router.post("/login")
def login(body: Login, db: Session = Depends(get_db)):
    u = db.query(User).filter_by(email=body.email).first()
    if not u or not check_pw(body.password, u.password_hash):
        raise HTTPException(401, "Invalid email or password")
    return {"id": u.id, "name": u.name, "email": u.email, "role": u.role, "token": make_token(u.id, u.role)}
