from fastapi import Depends
from passlib.context import CryptContext
from exceptions import UserAlreadyExistsError, MissingParameterError
from deps import get_db
from models.user import User
from passlib.context import CryptContext
from sqlalchemy.orm import Session


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def register(student_id: str, password: str, name: str, db: Session):
    """
    Register service function.
    """
    if not student_id or not password:
        raise MissingParameterError("Missing required parameters")

    # 检查用户是否已存在
    existing_user = db.query(User).filter(User.student_id == student_id).first()
    if existing_user:
        raise UserAlreadyExistsError("This student ID is already registered")

    # 创建新用户
    hashed_password = pwd_context.hash(password)
    new_user = User(student_id=student_id, hashed_password=hashed_password, student_name=name)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "status": "success",
        "message": "Registration successful",
        "user": {
            "id": new_user.id,
            "student_id": new_user.student_id,
            "student_name": new_user.student_name
        }
    }