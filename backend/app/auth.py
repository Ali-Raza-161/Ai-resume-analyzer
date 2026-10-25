"""JWT + bcrypt helpers. SECRET_KEY from env, dev default only for local demo."""
import os, bcrypt, jwt
from datetime import datetime, timedelta
SECRET = os.environ.get("SECRET_KEY", "ai-resume-dev-secret-change-me")
ALGO = "HS256"
def hash_pw(pw: str) -> str: return bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()
def check_pw(pw: str, h: str) -> bool:
    try: return bcrypt.checkpw(pw.encode(), h.encode())
    except Exception: return False
def make_token(user_id: int, role: str = "user") -> str:
    return jwt.encode({"sub": str(user_id), "role": role, "exp": datetime.utcnow() + timedelta(hours=24)}, SECRET, algorithm=ALGO)
def decode_token(token: str):
    return jwt.decode(token, SECRET, algorithms=[ALGO])
