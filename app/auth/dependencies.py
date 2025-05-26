from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from .jwt import decode_access_token
from models.user import User
from deps import get_db
from sqlalchemy.orm import Session
from exceptions import UserNotFoundError, UserAlreadyDeactiveError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_access_token(token)
        student_id: str = payload.get("sub")
        if student_id is None:
            raise HTTPException(status_code=401, detail="Token无效")
        user = db.query(User).filter(User.student_id == student_id).first()
        if not user:
            raise UserNotFoundError("This student does not register yet")
        if not user.is_active:
            raise UserAlreadyDeactiveError("This user has been deactivated")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Token解析失败")
