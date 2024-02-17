import typing

import pydantic
import pydantic_settings
import yaml

import lib.app.split_settings.utils as app_split_settings_utils


class ApiSettings(pydantic_settings.BaseSettings):
    model_config = pydantic_settings.SettingsConfigDict(
        env_file=app_split_settings_utils.ENV_PATH,
        env_prefix="API_",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    host: str = "0.0.0.0"
    port: int = 8000
    auth_basic_username: str = pydantic.Field(default=...)
    auth_basic_password: pydantic.SecretStr = pydantic.Field(default=...)
    auth_cookie_password: pydantic.SecretStr = pydantic.Field(default=...)
    use_config: bool = True

    @pydantic.model_validator(mode="before")
    @classmethod
    def load_from_config(cls, values: dict[str, typing.Any]) -> dict[str, typing.Any]:
        config_path = app_split_settings_utils.BASE_PATH / "config.yaml"
        if not values.get("use_config", True):
            return values
        if not config_path.exists():
            return values

        with open(config_path, encoding="utf-8") as file:
            data = yaml.safe_load(file)
        if "api_info" in data:
            values.update(data["api_info"])
        if "auth_info" in data and "basic" in data["auth_info"]:
            auth_basic_info = data["auth_info"]["basic"]
            values["auth_basic_username"] = auth_basic_info["username"]
            values["auth_basic_password"] = auth_basic_info["password"]
        return values
