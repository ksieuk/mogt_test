import pydantic


class HealthResponse(pydantic.BaseModel):
    status: str = pydantic.Field(default=..., examples=["healthy"], description="Схема доступности сервиса")
