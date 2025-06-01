from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base


class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    student_id = Column(String(50), ForeignKey("users.id"), nullable=False, index=True)
    student_name = Column(String(10), nullable=False)

    clazz = relationship("Class", back_populates="records")
