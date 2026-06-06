from app.database.database import engine, Base

from app.models.repository import Repository
from app.models.scan import Scan
from app.models.finding import Finding

Base.metadata.create_all(bind=engine)

print("Tables created successfully")