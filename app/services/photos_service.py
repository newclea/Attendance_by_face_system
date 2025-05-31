from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkfrs.v2.region.frs_region import FrsRegion
from huaweicloudsdkfrs.v2 import *
from huaweicloudsdkcore.http.formdata import FormFile
from dotenv import load_dotenv
from fastapi import UploadFile
from exceptions import NotRealFaceError, AddFaceError
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
    try:
        file_bytes = await file.read()

        # 将其封装为 FormFile，注意要传入 filename 和 content_type
        form_file = FormFile(
            file_content=file_bytes,
            file_name=file.filename,
            content_type=file.content_type or "application/octet-stream"
        )

        request = SearchFaceByFileRequest()
        request.face_set_name = face_set_name

        request.body = SearchFaceByFileRequestBody(
            return_fields="[\"timestamp\"]",
            filter="timestamp:10",
            top_n=10,
            image_file=FormFile(form_file)
        )
        response: SearchFaceByFileResponse = client.search_face_by_file(request)
        if not response.faces:
            raise NotRealFaceError("检测到非真实人脸，请重新上传")
        face = response.faces[0]
        if not face:
            raise NotRealFaceError("检测到非真实人脸，请重新上传")
        if face.similarity > 0.9:
            return {
                "message": "success",
                "data": face,
            }
        else:
            return {
                "message": "failed",
                "data": face,
            }

        print(response)

    except exceptions.ClientRequestException as e:
        print(e.status_code)
        print(e.request_id)
        print(e.error_code)
        print(e.error_msg)


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
    try:
        request = AddFacesByFileRequest()
        request.face_set_name = face_set_name

        file_bytes = await file.read()
        form_file = FormFile(
            file_content=file_bytes,
            file_name=file.filename,
            content_type=file.content_type or "application/octet-stream"
        )

        request.body = AddFacesByFileRequestBody(
            external_fields="{\"timestamp\":12}",
            image_file=FormFile(form_file)
        )
        
        response:AddFacesByFileResponse = client.add_faces_by_file(request)
        print(response)
        face = response.faces[0]
        if not face:
            raise AddFaceError("No face detected in the image.")
        else:
            new_face = Face(
                face_id = response.faces[0],
                face_set_id = response.face_set_id,
                face_set_name = response.face_set_name,
                user_id = current_user.id,
            )
            db.add(new_face)
            db.commit()
            db.refresh(new_face)
        return {
            "message": "successfully added face",
            "data": response
        }
            
    except exceptions.ClientRequestException as e:
        print(e.status_code)
        print(e.request_id)
        print(e.error_code)
        print(e.error_msg)
        raise AddFaceError("Failed to add face: " + e.error_msg)


async def deleteFace(current_user: User, db: Session, face_set_name: str, face_id: str):
    # Delete Face By FaceId
    try:
        request = DeleteFaceByFaceIdRequest()
        request.face_set_name = face_set_name
        request.face_id = face_id
        response = client.delete_face_by_face_id(request)
        db.query(Face).filter(Face.face_id == face_id, Face.student_id == current_user.student_id).delete()
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
async def detectLiveFaceByFile(file: UploadFile):
    try:
        file_bytes = await file.read()

        # 将其封装为 FormFile，注意要传入 filename 和 content_type
        form_file = FormFile(
            file_content=file_bytes,
            file_name=file.filename,
            content_type=file.content_type or "application/octet-stream"
        )

        request = DetectLiveFaceByFileRequest()

        request.body = DetectLiveFaceByFileRequestBody(
            image_file=FormFile(form_file)
        )
        response:DetectLiveFaceByFileResponse = client.detect_live_face_by_file(request)
        result:LiveDetectFaceRespResult = response.result
        print(response)
        if result.alive:
            return True
        else:
            return False

    except exceptions.ClientRequestException as e:
        print(e.status_code)
        print(e.request_id)
        print(e.error_code)
        print(e.error_msg)
