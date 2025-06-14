import tempfile

from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkfrs.v2.region.frs_region import FrsRegion
from huaweicloudsdkfrs.v2 import *
from huaweicloudsdkcore.http.formdata import FormFile
from dotenv import load_dotenv
from fastapi import UploadFile
from app.exceptions import NotRealFaceError, AddFaceError
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.face import Face

import os

load_dotenv()
def GetCredential(ak, sk):
    return BasicCredentials(ak, sk)

ak = os.getenv("HUAWEICLOUD_SDK_AK")
sk = os.getenv("HUAWEICLOUD_SDK_SK")
credentials = GetCredential(ak, sk)

def GetClient():
    client =  FrsClient.new_builder(FrsClient) \
         .with_credentials(credentials) \
         .with_region(FrsRegion.value_of("cn-north-4")) \
         .build()
    return client

client = GetClient()

async def searchFaceByFile(file: UploadFile, face_set_name: str = "test"):
    tmp_path = None
    form_file = None
    try:
        # 读取文件内容并验证非空
        file_bytes = await file.read()
        if not file_bytes:
            raise NotRealFaceError("上传的文件为空，请重新上传")
        file.file.seek(0)  # 重置读取指针，确保后续还能读取

        # 创建临时文件并写入内容
        suffix = '.' + file.content_type.split('/')[-1] if '/' in file.content_type else ''
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix, mode='wb') as tmp:
            tmp.write(file_bytes)
            tmp_path = tmp.name

        # 构造请求
        form_file = FormFile(tmp_path, file.content_type or "application/octet-stream")
        request = SearchFaceByFileRequest()
        request.face_set_name = face_set_name
        request.body = SearchFaceByFileRequestBody(
            top_n=10,
            image_file=form_file
        )

        # 调用接口
        response: SearchFaceByFileResponse = client.search_face_by_file(request)
        if not response.faces:
            raise NotRealFaceError("人脸库中未找到匹配的人脸，请先添加人脸2")

        face = response.faces[0]
        if not face:
            raise NotRealFaceError("人脸库中未找到匹配的人脸，请先添加人脸3")

        return {
            "message": "success" if face.similarity > 0.7 else "failed",
            "data": {
                "similarity": face.similarity,
                "face_id": face.face_id,
            }
        }

    except exceptions.ClientRequestException as e:
        print(e.status_code, e.request_id, e.error_code, e.error_msg)

    finally:
        if form_file:
            form_file.close()
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception as cleanup_err:
                print(f"清理临时文件失败: {cleanup_err}")


async def createFaceSet(face_set_name: str):
    try:
        request = CreateFaceSetRequest()
        request.body = CreateFaceSetReq(
            face_set_name=face_set_name,
            external_fields={"timestamp": {"type": "long"}}
        )
        response: CreateFaceSetResponse = client.create_face_set(request)
        print(response)
        return {
            "message": "successfully created face set",
            "data": response.face_set_info
        }
    except exceptions.ClientRequestException as e:
        print(e.status_code)
        print(e.request_id)
        print(e.error_code)
        print(e.error_msg)


async def showFaceSet(face_set_name: str):
    try:
        request = ShowFaceSetRequest()
        request.face_set_name = face_set_name
        response = client.show_face_set(request)
        print(response)
    except exceptions.ClientRequestException as e:
        print(e.status_code)
        print(e.request_id)
        print(e.error_code)
        print(e.error_msg)


async def showAllFaceSet():
    try:
        request = ShowAllFaceSetsRequest()
        response = client.show_all_face_sets(request)
        print(response)
    except exceptions.ClientRequestException as e:
        print(e.status_code)
        print(e.request_id)
        print(e.error_code)
        print(e.error_msg)


async def deleteFaceSet(face_set_name: str):
    try:
        request = DeleteFaceSetRequest()
        request.face_set_name = face_set_name
        response = client.delete_face_set(request)
        print(response)
    except exceptions.ClientRequestException as e:
        print(e.status_code)
        print(e.request_id)
        print(e.error_code)
        print(e.error_msg)


async def addFacesByFile(file: UploadFile, db: Session, current_user: User, face_set_name: str = "test"):
    tmp_path = None
    form_file = None
    try:
        file_bytes = await file.read()
        if not file_bytes:
            raise ValueError("上传文件为空，请重新上传")

        with tempfile.NamedTemporaryFile(delete=False,suffix='.'+file.content_type.split('/')[1], mode='wb') as tmp:
            tmp.write(file_bytes)
            tmp_path = tmp.name

        form_file = FormFile(tmp_path, file.content_type)

        request = AddFacesByFileRequest()
        request.face_set_name = face_set_name
        request.body = AddFacesByFileRequestBody(

            image_file=form_file
        )

        response: AddFacesByFileResponse = client.add_faces_by_file(request)
        print(response)

        face = response.faces[0] if response.faces else None
        if not face:
            raise AddFaceError("No face detected in the image.")

        new_face = Face(
            face_id=face.face_id,
            face_set_id=response.face_set_id,
            face_set_name=response.face_set_name,
            user_id=current_user.id,
        )
        db.add(new_face)
        db.commit()
        db.refresh(new_face)

        return {
            "message": "successfully added face",
            "data": response
        }

    except exceptions.ClientRequestException as e:
        print(e.status_code, e.request_id, e.error_code, e.error_msg)
        raise AddFaceError("Failed to add face: " + e.error_msg)

    finally:
        if form_file:
            form_file.close()
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception as cleanup_err:
                print(f"清理临时文件失败: {cleanup_err}")




async def deleteFace(user_id:str, db: Session, face_set_name: str = "test"):
    # Delete Face By FaceId
    try:

        face = db.query(Face).filter(Face.student_id == user_id).first()
        request = DeleteFaceByFaceIdRequest()
        request.face_set_name = face_set_name
        request.face_id = face.face_id if face else None
        response = client.delete_face_by_face_id(request)
        db.query(Face).filter(Face.face_id == face.face_id, Face.student_id == user_id).delete()
        db.query(User).filter(User.id == user_id).delete()
        db.commit()
        print(response)
        return {
            "message": "successfully deleted face",
            "data": response
        }
    except exceptions.ClientRequestException as e:
        print(e.status_code)
        print(e.request_id)
        print(e.error_code)
        print(e.error_msg)

    # Delete Face By ExternalImageId
    # try:
    #     request = DeleteFaceByExternalImageIdRequest()
    #     request.face_set_name = "face_set_name"
    #     request.external_image_id = "external_image_id"
    #     response = client.delete_face_by_external_image_id(request)
    #     print(response)
    # except exceptions.ClientRequestException as e:
    #     print(e.status_code)
    #     print(e.request_id)
    #     print(e.error_code)
    #     print(e.error_msg)


async def batchDeleteFaces():
    try:
        request = BatchDeleteFacesRequest()
        request.face_set_name = "face_set_name"
        request.body = DeleteFacesBatchReq(
            filter="age:[20 TO 30]"
        )
        response = client.batch_delete_faces(request)
        print(response)
    except exceptions.ClientRequestException as e:
        print(e.status_code)
        print(e.request_id)
        print(e.error_code)
        print(e.error_msg)


async def updateFace(current_user: User, db: Session, face_set_name: str):
    try:
        face = db.query(Face).filter(Face.student_id == current_user.student_id).first()
        request = UpdateFaceRequest()
        request.face_set_name = face_set_name
        request.body = UpdateFaceReq(face_id= face.face_id)
        response = client.update_face(request)
        print(response)
    except exceptions.ClientRequestException as e:
        print(e.status_code)
        print(e.request_id)
        print(e.error_code)
        print(e.error_msg)


async def showFaces():
    # Show Faces By FaceId
    try:
        request = ShowFacesByFaceIdRequest()
        request.face_set_name = "face_set_name"
        request.face_id = "LkPJblq6"
        response = client.show_faces_by_face_id(request)
        print(response)
    except exceptions.ClientRequestException as e:
        print(e.status_code)
        print(e.request_id)
        print(e.error_code)
        print(e.error_msg)

    # Show Faces By Limit
    try:
        request = ShowFacesByLimitRequest()
        request.face_set_name = "face_set_name"
        request.offset = 0
        request.limit = 10
        response = client.show_faces_by_limit(request)
        print(response)
    except exceptions.ClientRequestException as e:
        print(e.status_code)
        print(e.request_id)
        print(e.error_code)
        print(e.error_msg)


# detect live face by file
import tempfile

async def detectLiveFaceByFile(file: UploadFile):
    tmp_path = None
    form_file = None

    try:
        # 读取文件内容并验证非空
        file_bytes = await file.read()
        if not file_bytes:
            raise NotRealFaceError("上传的文件为空，请重新上传")
        file.file.seek(0)  # 重置读取指针，确保后续还能读取

        # 创建临时文件并写入内容
        suffix = '.' + file.content_type.split('/')[-1] if '/' in file.content_type else ''
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix, mode='wb') as tmp:
            tmp.write(file_bytes)
            tmp_path = tmp.name

        form_file = FormFile(tmp_path, file.content_type or "application/octet-stream")

        request = DetectLiveFaceByFileRequest()
        request.body = DetectLiveFaceByFileRequestBody(image_file=form_file)
        response: DetectLiveFaceByFileResponse = client.detect_live_face_by_file(request)
        result: LiveDetectFaceRespResult = response.result
        return result.alive

    except exceptions.ClientRequestException as e:
        print(e.status_code, e.request_id, e.error_code, e.error_msg)
        return False

    finally:
        if form_file:
            form_file.close()
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception as cleanup_err:
                print(f"清理临时文件失败: {cleanup_err}")
