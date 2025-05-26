from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from utils import Build_Sucess_Message


router = APIRouter()

@router.post("/add_photo")
async def add_photo( photo: str):
    """
    Add a photo for a student.
    """
    if not student_id or not photo:
        raise HTTPException(status_code=400, detail="Missing required parameters")

    return Build_Sucess_Message(
        service_func=add_photo_service, 
        student_id=student_id, 
        photo=photo
    )