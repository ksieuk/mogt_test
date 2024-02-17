import io
import os
import urllib.parse
import zipfile

import lib.app.errors as _app_errors
import lib.app.split_settings as _app_split_settings
import lib.clients as _clients
import lib.models.file as _file_models


class FileService:
    def __init__(
        self,
        settings: _app_split_settings.FileSettings,
        http_client: _clients.AsyncHttpClient,
    ) -> None:
        self.settings = settings
        self.http_client = http_client

    async def get_file(self, request: _file_models.FileGetRequest):
        params = {"keys": str(request.file_id)}
        response = await self.http_client.get(self.settings.api_url, params=params)

        headers = response.headers
        filename_raw = headers.get("filename")
        if filename_raw is None:
            raise _app_errors.FilenameNotFound("Filename not found")

        filename_encoded = urllib.parse.unquote(filename_raw)
        file_path = self.settings.files_dir_path / filename_encoded
        with open(file_path, "wb") as file:
            file.write(response.content)

        return response

    async def create_zip_in_memory(self) -> io.BytesIO:
        bytes_io = io.BytesIO()

        with zipfile.ZipFile(bytes_io, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(self.settings.files_dir_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, self.settings.files_dir_path))

        bytes_io.seek(0)

        return bytes_io
