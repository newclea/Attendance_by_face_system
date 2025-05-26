from pydantic import BaseModel

class UserCreate(BaseModel):
    student_id: str
    password: str
    name: str

class UserLogin(BaseModel):
    student_id: str
    password: str

class UserOut(BaseModel):
    id: int
    student_id: str
    is_active: bool

    class Config:
        orm_mode = True
