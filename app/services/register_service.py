from fastapi import Depends, UploadFile
from passlib.context import CryptContext
from app.exceptions import UserAlreadyExistsError, MissingParameterError, NotRealFaceError
from app.deps import get_db
from app.models.user import User
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.services.photos_service import detectLiveFaceByFile, addFacesByFile


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def register(student_id: str, password: str, name: str, photo: UploadFile, db: Session):
    """
    Register service function.
    """
    if not student_id or not password:
        raise MissingParameterError("Missing required parameters")

    # 检查用户是否已存在
    existing_user = db.query(User).filter(User.student_id == student_id).first()
    if existing_user:
        raise UserAlreadyExistsError("This student ID is already registered")
    
    # 检查照片是否为图片格式
    if not photo.content_type.startswith("image/"):
        raise ValueError("Please upload a valid image file")
    
    is_live_face = await detectLiveFaceByFile(photo)
    if not is_live_face:
        raise NotRealFaceError("The uploaded photo does not contain a live face")

    # 创建新用户
    hashed_password = pwd_context.hash(password)
    new_user = User(student_id=student_id, hashed_password=hashed_password, student_name=name)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    addFacesByFile(file=photo, current_user= new_user, db=db)

    

    return {
        "status": "success",
        "message": "Registration successful",
        "user": {
            "id": new_user.id,
            "student_id": new_user.student_id,
            "student_name": new_user.student_name
        }
    }