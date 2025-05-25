from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from backend.db.database import Base

class GeoFileUpload(Base):
    __tablename__ = "geo_file_uploads"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    feature_count = Column(Integer)
    geometry_type = Column(String)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
