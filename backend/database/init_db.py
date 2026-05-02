from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

db_url = os.getenv("DB_URL")

if not db_url:
    raise ValueError("database url not set")

engine = create_engine(db_url)

with engine.connect() as conn:
    with open("backend/database/schema.sql") as f:
        conn.execute(text(f.read()))
