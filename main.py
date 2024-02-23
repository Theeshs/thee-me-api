from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel

from thee_me.education.service import education_router
from thee_me.experience.service import experience_router
from thee_me.projects.service import project_router
from thee_me.skills.service import skills_router

# from thee_me.middlewares.auth_middleware import JWTMiddleware
from thee_me.user.service import user_router
from thee_me.user_services.service import service_router


def create_app() -> FastAPI:
    app = FastAPI()
    origins = ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(
        user_router,
        prefix="/api",
    )

    app.include_router(
        skills_router,
        prefix="/api",
    )

    app.include_router(
        experience_router,
        prefix="/api",
    )

    app.include_router(
        education_router,
        prefix="/api",
    )

    app.include_router(service_router, prefix="/api")

    app.include_router(project_router, prefix="/api")

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
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})
