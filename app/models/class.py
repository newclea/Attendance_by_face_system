from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey,JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base


class Class(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)

    records = relationship("Record", back_populates="clazz", cascade="all, delete-orphan")
    students = relationship("User", secondary="class_students", back_populates="classes")