import uuid

import pydantic


class FileGetRequest(pydantic.BaseModel):
    file_id: uuid.UUID
