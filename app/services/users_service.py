from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.models.user import User


async def reset_password_service(new_password:str, current_user: User, db: Session):
    return 



async def reset_photo_service(new_photo: UploadFile, current_user: User, db: Session):
    """
    Reset the user's photo.
    """
    if not new_photo.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="请上传图片格式的文件")
    
    # Assuming you have a method to update the user's photo in the database
    current_user.photo = new_photo.file.read()  # This is just an example; adjust as needed
    db.add(current_user)
    db.commit()
    
    return {"message": "Photo updated successfully"}