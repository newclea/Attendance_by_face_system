from fastapi import FastAPI
from app.api.login import router as login_router
from app.api.register import router as register_router
from app.api.users import router as users_router
from app.api.records import router as records_router
from app.api.photos import router as photos_router
from app.api.attendance import router as attendance_router
from app.database import Base, engine
import uvicorn
import argparse
from app.services.photos_service import createFaceSet,showFaceSet,deleteFaceSet
from huaweicloudsdkfrs.v2 import ShowFaceSetResponse, FaceSetInfo

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(login_router, prefix="/login")
app.include_router(register_router, prefix="/register")
app.include_router(users_router, prefix="/users")
app.include_router(records_router, prefix="/records")
app.include_router(photos_router, prefix="/photos")
app.include_router(attendance_router, prefix="/attendance")

def main():
    parser = argparse.ArgumentParser(description="启动 FastAPI 项目")
    parser.add_argument("-r", "--init-face-lib", action="store_true", help="初始化人脸库")
    args = parser.parse_args()

    if args.init_face_lib:
        print("🔧 正在执行人脸库初始化...")
        # TODO
        response:ShowFaceSetResponse  = showFaceSet("test")
        if response is not None:
            face_set_info: FaceSetInfo = response.face_set_info
            if face_set_info is not None:
                if face_set_info.face_set_name == "test":
                    print("人脸库已存在，删除并重新创建")
                    deleteFaceSet("test")
                    createFaceSet("test")

        else:
            print("人脸库不存在，创建中...")
            createFaceSet("test")
        print("✅ 初始化完成")
    else:
        print("🚀 启动 FastAPI 服务")

    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()