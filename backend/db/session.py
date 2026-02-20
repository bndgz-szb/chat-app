import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

DB_URL = os.getenv("DB_URL")

if DB_URL == None:
	raise Exception("Don't forget to create .env file with DB_URL")

engine = create_engine(DB_URL, echo=True)

SessionLocal = sessionmaker(autoflush=False, bind=engine)
