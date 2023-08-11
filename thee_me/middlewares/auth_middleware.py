from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi_jwt_auth import AuthJWT
import json


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
