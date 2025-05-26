from fastapi import FastAPI
from app.api.login import router as login_router
from api.register import router as register_router
from api.users import router as users_router
from api.records import router as records_router
from api.photos import router as photos_router
from api.attendance import router as attendance_router
from database import Base, engine
from models import user


app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(login_router, prefix="/login")
app.include_router(register_router, prefix="/register")
app.include_router(users_router, prefix="/users")
app.include_router(records_router, prefix="/records")
app.include_router(photos_router, prefix="/photos")
app.include_router(attendance_router, prefix="/attendance")