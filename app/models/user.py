from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String(50), primary_key=True, index=True)
    hashed_password = Column(String(128), nullable=False)
    student_name = Column(String(100), nullable=False)
    is_teacher = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    attendances = relationship("Attendance", back_populates="student")
    classes = relationship("Class", secondary="class_students", back_populates="students")
    faces = relationship("Face", back_populates="user")
