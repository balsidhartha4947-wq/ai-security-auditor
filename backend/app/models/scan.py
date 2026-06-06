from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.database.database import Base


class Scan(Base):

    __tablename__ = "scans"

    id = Column(Integer, primary_key=True)

    repository_id = Column(Integer)

    status = Column(String)

    total_findings = Column(Integer)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )