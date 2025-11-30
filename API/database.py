from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

BASE_DIR = Path(__file__).resolve().parent
DATABASE_URL = f"sqlite:///{BASE_DIR / 'movies.db'}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
