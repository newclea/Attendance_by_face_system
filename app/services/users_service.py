from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.face import Face
from app.services.photos_service import deleteFace, addFacesByFile
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def reset_password_service(new_password:str, current_user: User, db: Session):
    """
    Reset the user's password.
    """
    if not new_password:
        raise HTTPException(status_code=400, detail="新密码不能为空")
    
    # Assuming you have a method to hash the password
    hashed_password = pwd_context.hash(new_password)
    current_user.hashed_password = hashed_password
    
    db.add(current_user)
    db.commit()
    
    return {"message": "Password updated successfully"}



async def reset_photo_service(new_photo: UploadFile, current_user: User, db: Session):
    """
    Reset the user's photo (face data).
    """
    if not new_photo.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="请上传图片格式的文件")

    # 查询当前用户所有人脸
    faces = db.query(Face).filter(Face.user_id == current_user.id).all()
    for face in faces:
        await deleteFace(current_user=current_user, db=db, face_set_name=face.face_set_name, face_id=face.face_id)
        face.delete(db=db)  # 删除数据库中的人脸记录
    # 添加新的人脸
    await addFacesByFile(file=new_photo, db=db, current_user=current_user)

    return {"message": "Photo updated successfully"}