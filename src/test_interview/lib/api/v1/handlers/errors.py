import logging

import fastapi
import fastapi.responses as fastapi_responses
import pydantic

logger = logging.getLogger(__name__)


async def value_error_exception_handler(request: fastapi.Request, exc: pydantic.ValidationError):
    logger.debug("Request Validation error: request=%s", request, exc_info=True)
    return fastapi_responses.JSONResponse(
        status_code=fastapi.status.HTTP_400_BAD_REQUEST,
        content={"message": str(exc)},
    )
