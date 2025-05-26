from typing import Any
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from exceptions import InvalidPasswordError, UserNotFoundError, UsernameAlreadyExistsError, MissingParameterError

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
    except Exception as e:
        raise HTTPException(status_code=500, detail="服务内部错误：" + str(e))