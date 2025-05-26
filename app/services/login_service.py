from app.auth.jwt import create_access_token
from exceptions import InvalidPasswordError, UserNotFoundError, MissingParameterError
from fastapi import Depends
from sqlalchemy.orm import Session
from deps import get_db
from models.user import User
from passlib.context import CryptContext
from datetime import timedelta
from app.auth.dependencies import get_current_user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def login(student_id: str, password: str, db: Session):
    """
    Login service function.
    """

    if not student_id or not password:
        raise MissingParameterError("Missing required parameters")

    # 查询用户
    user = db.query(User).filter(User.student_id == student_id).first()
    if not user:
        raise UserNotFoundError("The student does not register yet")

    # 校验密码
    if not pwd_context.verify(password, user.hashed_password):
        raise InvalidPasswordError("Invalid or wrong password")

    # 创建 JWT Token
    access_token = create_access_token(data={"sub": user.student_id}, expires_delta=timedelta(minutes=10))
    user.is_active = True
    db.commit()
    
    return {
        "status": "success",
        "message": "Login successful",
        "user": {
            "id": user.id,
            "student_id": user.student_id,
            "student_name": user.student_name
        },
        "access_token": access_token,
        "token_type": "bearer"
    }


async def logout(current_user: User, db: Session):
    current_user.is_active = False
    db.commit()
    return {"status": "success",
            "message": "Logout successful"}