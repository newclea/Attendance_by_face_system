from pydantic import BaseModel
from fastapi import UploadFile, File

class UserCreate(BaseModel):
    student_id: str
    password: str
    name: str
    photo: UploadFile = File(...)

class UserLogin(BaseModel):
    student_id: str
    password: str

class UserOut(BaseModel):
    id: int
    student_id: str
    is_active: bool

    class Config:
        from_attributes = True
