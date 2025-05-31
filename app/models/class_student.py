from sqlalchemy import Column, Integer, ForeignKey
from database import Base

class ClassStudent(Base):
    __tablename__ = "class_students"

    id = Column(Integer, primary_key=True)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.student_id"), nullable=False)