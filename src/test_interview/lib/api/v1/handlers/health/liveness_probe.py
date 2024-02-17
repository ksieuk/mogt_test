import fastapi

import lib.api.v1.schemas as api_schemas

router = fastapi.APIRouter()


@router.get(
    "/",
    response_model=api_schemas.HealthResponse,
    summary="Статус работоспособности",
    description="Проверяет доступность сервиса FastAPI.",
)
async def health():
    return api_schemas.HealthResponse(status="healthy")
