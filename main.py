from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.responses import JSONResponse

from thee_me.routes import user
from thee_me.routes import skills
from thee_me.routes import experiance

# from thee_me.middlewares.auth_middleware import JWTMiddleware


def create_app() -> FastAPI:
    app = FastAPI()
    origins = [
        "*"
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    app.include_router(
        user.router,
        prefix="/api",
    )

    app.include_router(
        skills.router,
        prefix="/api",
    )

    app.include_router(
        experiance.router,
        prefix="/api",
    )

    return app


app = create_app()
# app.add_middleware(JWTMiddleware)


class Settings(BaseModel):
    authjwt_secret_key: str = "2131ouidjskbnfiu134kb..12m"
    authjwt_token_type: str = "Bearer"


# callback to get your configuration
@AuthJWT.load_config
def get_config():
    return Settings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )
