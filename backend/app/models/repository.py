# backend/app/models/repository.py
from sqlalchemy import Column, Integer, String
from app.database.database import Base


class Repository(Base):
    __tablename__ = "repositories"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    url = Column(String, unique=True, index=True)
    last_commit_hash = Column(String, nullable=True)