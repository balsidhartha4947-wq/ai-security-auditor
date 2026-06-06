from sqlalchemy import text
from app.database.database import engine

with engine.connect() as conn:
    conn.execute(text("ALTER TABLE repositories ADD COLUMN IF NOT EXISTS last_commit_hash VARCHAR"))
    conn.commit()
    print("✅ Migration complete")