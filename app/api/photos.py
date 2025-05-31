from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from utils import Build_Sucess_Message
from app.services.photos_service import addFacesByFile
from sqlalchemy.orm import Session
from app.deps import get_db
from app.models.user import User
from app.auth.dependencies import get_current_user

router = APIRouter()



@router.post("/add_photo")
async def add_photo(current_user: User = Depends(get_current_user), file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Add a photo for a student.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="请上传图片格式的文件")
    
    Build_Sucess_Message(
        addFacesByFile,
        file = file,
        db = db
    )