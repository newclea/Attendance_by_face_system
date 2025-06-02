from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.utils import Build_Sucess_Message
from app.services.login_service import login as login_service
from app.services.login_service import logout as logout_service
from app.schemas.user import UserLogin
from app.auth.dependencies import get_current_user
from app.deps import get_db
from app.models.user import User

router = APIRouter()


@router.post("/login")
async def login(form: UserLogin, db: Session = Depends(get_db)):
    """
    Sign in endpoint.
    """
    return await Build_Sucess_Message(
        service_func=login_service, 
        student_id=form.student_id, 
        password=form.password,
        db=db
    )


@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Sign out endpoint.
    """
    return await Build_Sucess_Message(
        service_func=logout_service,
        current_user=current_user,
        db=db
    )
        

