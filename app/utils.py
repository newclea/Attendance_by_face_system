from typing import Any
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from app.exceptions import InvalidPasswordError, UserNotFoundError, UserAlreadyExistsError, MissingParameterError, NotRealFaceError

def Build_Sucess_Message(service_func, *args, **kwargs):
    try:
        result = service_func(*args, **kwargs)
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "data": result
            }
        )
    
    except InvalidPasswordError as pe:
        raise HTTPException(status_code=400, detail={
            "status": "failed",
            "message": pe.message
        })
    except UserNotFoundError as ue:
        raise HTTPException(status_code=404, detail={
            "status": "failed",
            "message": ue.message
        })
    except UserAlreadyExistsError as ue:
        raise HTTPException(status_code=409, detail={
            "status": "failed",
            "message": ue.message
        })
    except MissingParameterError as me:
        raise HTTPException(status_code=422, detail={
            "status": "failed",
            "message": me.message
        })
    except NotRealFaceError as ne:
        raise HTTPException(status_code=400, detail={
            "status": "failed",
            "message": ne.message
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail="服务内部错误：" + str(e))