from fastapi import APIRouter, HTTPException, Depends, Form, UploadFile, File
from fastapi.responses import JSONResponse
from app.utils import Build_Sucess_Message
from app.services.register_service import register as register_service
from app.schemas.user import UserCreate
from sqlalchemy.orm import Session
from app.deps import get_db

router = APIRouter()

@router.post("/register")
async def register(
    student_id: str = Form(...),
    password: str = Form(...),
    name: str = Form(...),
    photo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Register endpoint.
    """

    return await Build_Sucess_Message(
        service_func=register_service, 
        student_id=student_id,
        password=password,
        name=name,
        photo=photo,
        db=db
    )