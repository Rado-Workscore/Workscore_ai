from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.models.base import Base

class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)
    camera_id = Column(Integer, ForeignKey("cameras.id"), nullable=False)

    uploaded_at = Column(DateTime, default=datetime.utcnow)
    is_processed = Column(Boolean, default=False)

    warehouse = relationship("Warehouse", back_populates="videos")
    camera = relationship("Camera", back_populates="videos")
