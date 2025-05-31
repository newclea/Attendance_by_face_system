from fastapi import APIRouter, Depends
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from utils import Build_Sucess_Message
from app.services.records_service import get_records as get_records_service
from app.auth.dependencies import get_current_user
from app.deps import get_db
from models.user import User
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/records")
async def get_records(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Get all records.
    """
    return Build_Sucess_Message(
        get_records_service,
        current_user=current_user,
        db=db,
    )