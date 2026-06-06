from sqlalchemy import Column, Integer, String, Text

from app.database.database import Base


class Finding(Base):

    __tablename__ = "findings"

    id = Column(Integer, primary_key=True)

    scan_id = Column(Integer)

    severity = Column(String)

    path = Column(String)

    check_id = Column(String)

    message = Column(Text)

    ai_analysis = Column(Text)