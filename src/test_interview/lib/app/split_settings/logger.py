import pydantic_settings

import lib.app.split_settings.utils as app_split_settings_utils


class LoggingSettings(pydantic_settings.BaseSettings):
    model_config = pydantic_settings.SettingsConfigDict(
        env_file=app_split_settings_utils.ENV_PATH,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_default_handlers: list[str] = [
        "console",
    ]

    log_level_handlers: str = "INFO"
    log_level_loggers: str = "INFO"
    log_level_root: str = "INFO"


def get_logging_config(
    log_format: str,
    log_default_handlers: list[str],
    log_level_handlers: str,
    log_level_loggers: str,
    log_level_root: str,
):
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {"format": log_format},
            "default": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": "%(levelprefix)s %(message)s",
                "use_colors": None,
            },
            "access": {
                "()": "uvicorn.logging.AccessFormatter",
                "fmt": "%(levelprefix)s %(client_addr)s - '%(request_line)s' %(status_code)s",
            },
        },
        "handlers": {
            "console": {
                "level": log_level_handlers,
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            },
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
            "access": {
                "formatter": "access",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "": {
                "handlers": log_default_handlers,
                "level": log_level_loggers,
            },
            "uvicorn.error": {
                "level": log_level_loggers,
            },
            "uvicorn.access": {
                "handlers": ["access"],
                "level": log_level_loggers,
                "propagate": False,
            },
        },
        "root": {
            "level": log_level_root,
            "formatter": "verbose",
            "handlers": log_default_handlers,
        },
    }
