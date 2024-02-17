import logging
import typing
import uuid

import fastapi
import fastapi.responses
import fastapi.security

import lib.app.errors as _app_errors
import lib.app.split_settings as app_split_settings
import lib.file.services as _file_services
import lib.models.file as _file_models

logger = logging.getLogger(__name__)


class FilesHandler:
    security = fastapi.security.HTTPBasic()

    def __init__(
        self,
        settings: app_split_settings.ApiSettings,
        file_service: _file_services.FileService,
    ):
        self.settings = settings
        self.file_service = file_service

        self.router = fastapi.APIRouter()
        self.register()

    def register(self):
        self.router.add_api_route(
            "/get_file/{file_id}",
            endpoint=self.get_file,
            methods=["GET"],
            summary="Получение файла",
            description="Получение файла по его id (UUID4)",
            dependencies=[fastapi.Depends(self.__verify_credentials)],
        )
        self.router.add_api_route(
            "/download_zip",
            endpoint=self.download_zip,
            methods=["GET"],
            summary="Скачать все файлы в виде zip",
            description="Скачать все файлы в виде zip",
            dependencies=[fastapi.Depends(self.__verify_credentials), fastapi.Depends(self.__verify_cookie)],
        )

    async def get_file(self, file_id: uuid.UUID) -> fastapi.responses.JSONResponse:
        try:
            await self.file_service.get_file(_file_models.FileGetRequest(file_id=file_id))
        except _app_errors.FilenameNotFound as e:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND,
                detail="Filename not found",
            ) from e

        return fastapi.responses.JSONResponse(
            status_code=fastapi.status.HTTP_200_OK,
            content={"message": "File was downloaded"},
        )

    async def download_zip(self) -> fastapi.responses.StreamingResponse:
        bytes_io = await self.file_service.create_zip_in_memory()

        return fastapi.responses.StreamingResponse(
            bytes_io,
            media_type="application/x-zip-compressed",
            headers={"Content-Disposition": "attachment; filename=output.zip"},
        )

    async def __verify_credentials(
        self,
        credentials: fastapi.security.HTTPBasicCredentials = fastapi.Depends(security),
    ):
        correct_username = self.settings.auth_basic_username
        correct_password = self.settings.auth_basic_password.get_secret_value()
        if credentials.username != correct_username or credentials.password != correct_password:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Basic"},
            )

    async def __verify_cookie(self, mojo: typing.Annotated[str | None, fastapi.Cookie()] = None):
        if mojo != self.settings.auth_cookie_password.get_secret_value():
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized access, invalid cookie",
            )
