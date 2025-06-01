from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String(50), primary_key=True, index=True)
    hashed_password = Column(String(128), nullable=False)
    student_name = Column(String(100), nullable=False)
    is_teacher = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    faces = relationship("Face", back_populates="user")

    def to_dict(self):
        return {
            "id": self.id,
            "student_name": self.student_name,
            "is_teacher": self.is_teacher,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
