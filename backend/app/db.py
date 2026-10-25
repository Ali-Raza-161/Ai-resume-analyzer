"""PostgreSQL via DATABASE_URL when set, else SQLite fallback (same ORM models).
Production: Neon/Supabase Postgres. Local demo: SQLite file resumes.db."""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
URL = os.environ.get("DATABASE_URL", "sqlite:///./resumes.db")
connect_args = {"check_same_thread": False} if URL.startswith("sqlite") else {}
engine = create_engine(URL, connect_args=connect_args)
Session = sessionmaker(bind=engine)
def get_db():
    db = Session()
    try: yield db
    finally: db.close()
