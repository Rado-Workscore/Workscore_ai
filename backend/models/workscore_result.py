from sqlalchemy import Column, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base

class WorkScoreResult(Base):
    __tablename__ = "workscore_results"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)

    date = Column(Date, nullable=False)
    score = Column(Integer, nullable=False)

    wms_usage = Column(Float, default=0.0)
    time_in_zone = Column(Float, default=0.0)
    task_accuracy = Column(Float, default=0.0)
    trajectory_deviation = Column(Float, default=0.0)

    employee = relationship("Employee", back_populates="workscore_results")
    warehouse = relationship("Warehouse", back_populates="workscore_results")
