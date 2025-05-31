from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import  relationship
from datetime import datetime, timezone
from database import Base

class Attendance(Base):
    __tablename__ = "attendances"

    id = Column(Integer, primary_key=True)
    record_id = Column(Integer, ForeignKey("records.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.student_id"), nullable=False)
    status = Column(String(20), default="present")

    record = relationship("Record", back_populates="attendances")
    student = relationship("User", back_populates="attendances")
