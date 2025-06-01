from sqlalchemy.orm import Session
from fastapi import HTTPException, UploadFile
from app.services.photos_service import detectLiveFaceByFile, searchFaceByFile
from exceptions import NotRealFaceError, AddFaceError
from app.services.records_service import add_record
from app.models.face import Face
from app.models.user import User
from app.models.record import Record


async def attendance_service(
     db: Session, file: UploadFile
):
    """
    Mark attendance for a student in a class.
    """
    if not detectLiveFaceByFile(file):
        raise NotRealFaceError("检测到非真实人脸，请重新上传")
    
    response = await searchFaceByFile(file)
    if response is None:
        raise AddFaceError("人脸库中未找到匹配的人脸，请先添加人脸")
    else:
        if response.get("message") == "success":
            face_id = response.get("data").get("face_id")
            face = db.query(Face).filter(Face.face_id == face_id).first()
            record = Record(
                student_id=face.user.id,
                student_name=face.user.student_name,
            )
            return {
                "message": "人脸识别成功",
                "data": response.get("data"),
            }
        else:
            raise HTTPException(status_code=400, detail="人脸识别失败，请重新上传")

