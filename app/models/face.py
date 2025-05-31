from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base


class Face(Base):
    __tablename__ = "faces"

    face_id = Column(String(50), primary_key=True, nullable=False, index=True)
    face_set_id = Column(String(50), nullable=False)
    face_set_name = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    user_id = Column(String(50), ForeignKey("users.id"),nullable=False)

    user = relationship("User", back_populates="faces")