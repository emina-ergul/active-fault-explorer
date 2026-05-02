from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

engine = create_engine(os.getenv("DB_URL"))

with engine.connect() as conn:
    with open("backend/database/schema.sql") as f:
        conn.execute(text(f.read()))
