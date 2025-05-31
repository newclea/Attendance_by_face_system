from fastapi import APIRouter, Depends, UploadFile
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from utils import Build_Sucess_Message
from app.services.attendance_service import attendance_service
from app.auth.dependencies import get_current_user
from sqlalchemy.orm import Session
from app.deps import get_db
from app.services.attendance_service import attendance_service


router = APIRouter()


@router.post("/attendance")
async def mark_attendance(class_id: int,file: UploadFile, db: Session = Depends(get_db)):
    """
    Mark attendance for a student in a class.
    """
    return Build_Sucess_Message(
        attendance_service,
        class_id=class_id,
        file=file,
        db=db
    )
        

