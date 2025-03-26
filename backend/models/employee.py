from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    position = Column(String, nullable=True)

    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)
    warehouse = relationship("Warehouse", back_populates="employees")

    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Integer, default=1)  # 1=ակտիվ, 0=պասիվ
    workscore_results = relationship("WorkScoreResult", back_populates="employee")

    


