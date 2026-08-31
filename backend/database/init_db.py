from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

db_password = os.getenv("POSTGRES_PASSWORD")
db_url = f"postgresql://postgres:{db_password}@localhost:5432/seismic"

if not db_url:
    raise ValueError("database url not set")

engine = create_engine(db_url)

with engine.connect() as conn:
    with open("backend/database/schema.sql") as f:
        conn.execute(text(f.read()))
