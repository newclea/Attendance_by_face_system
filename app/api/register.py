from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from app.utils import Build_Sucess_Message
from app.services.register_service import register as register_service
from app.schemas.user import UserCreate
from sqlalchemy.orm import Session
from app.deps import get_db

router = APIRouter()

@router.post("/register")
async def register(form: UserCreate, db: Session = Depends(get_db)):
    """
    Register endpoint.
    """

    return Build_Sucess_Message(
        service_func=register_service, 
        student_id=form.student_id, 
        password=form.password, 
        name=form.name,
        photo=form.photo,
        db=db
    )