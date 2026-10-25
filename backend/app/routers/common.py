from fastapi import Depends, HTTPException, Request
from ..auth import decode_token
def current_user(request: Request):
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "): raise HTTPException(401, "Login required")
    try: return decode_token(auth[7:])
    except Exception: raise HTTPException(401, "Invalid or expired token")
