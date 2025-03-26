from sqlalchemy import Column, Integer, String
from backend.database import Base  # սա պետք է իմանա քո SQLAlchemy setup-ը
from sqlalchemy.orm import relationship

class Warehouse(Base):
    __tablename__ = "warehouses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    location = Column(String, nullable=True)  # կամ optionally ավելացնենք պահեստի տեղադրությունը

    cameras = relationship("Camera", back_populates="warehouse", cascade="all, delete")
    employees = relationship("Employee", back_populates="warehouse")
    workscore_results = relationship("WorkScoreResult", back_populates="warehouse")
    videos = relationship("Video", back_populates="warehouse")




