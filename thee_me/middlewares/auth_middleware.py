import json

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi_jwt_auth import AuthJWT
from starlette.middleware.base import BaseHTTPMiddleware


async def get_current_user(auth_jwt=Depends(AuthJWT)):
    try:
        auth_jwt.jwt_required()
        current_user = json.loads(auth_jwt.get_jwt_subject())
        return current_user
    except HTTPException as e:
        raise e
    except Exception as ee:
        raise ee
        # raise HTTPException(status_code=401, detail="Invalid token")
