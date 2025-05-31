from fastapi import APIRouter, Depends, UploadFile, File
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from utils import Build_Sucess_Message
from app.services.users_service import reset_password_service, reset_photo_service
from app.auth.dependencies import get_current_user
from sqlalchemy.orm import Session
from app.deps import get_db
from models.user import User



router = APIRouter()

@router.post("/pw_reset")
async def reset_password(
      new_password: str,
      current_user: User = Depends(get_current_user),
      db: Session = Depends(get_db)
    ):
    """
    Reset password for the current user.
    """
    try:
        return Build_Sucess_Message(
            reset_password_service,
            new_password=new_password,
            current_user=current_user,
            db=db
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("photo_reset")
async def reset_photo(
      file: UploadFile = File(...),
      current_user: User = Depends(get_current_user),
      db: Session = Depends(get_db)
    ):
    """
    Reset photo for the current user.
    """
    try:
        return Build_Sucess_Message(
            reset_photo_service,
            new_photo=file,
            current_user=current_user,
            db=db
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/Alluser")
async def get_all_users(db: Session = Depends(get_db)):
    """
    Get all users.
    """
    try:
        users = db.query(User).all()
        return JSONResponse(content={"users": [user.to_dict() for user in users]})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))