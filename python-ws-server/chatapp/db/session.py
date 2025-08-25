import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_URL = os.getenv("DB_URL")

engine = create_engine(DB_URL, echo=True)

SessionLocal = sessionmaker(autoflush=False, bind=engine)
