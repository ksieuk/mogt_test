import typing

import pydantic
import pydantic_settings
import yaml

import lib.app.split_settings.utils as app_split_settings_utils


class ApiSettings(pydantic_settings.BaseSettings):
    model_config = pydantic_settings.SettingsConfigDict(
        env_file=app_split_settings_utils.ENV_PATH,
        env_prefix="TEST_API_",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    protocol: str = "http"
    host: str = "0.0.0.0"
    port: int = 8000
    headers: dict[str, str] = {"Content-Type": "application/json"}
    use_config: bool = True

    @pydantic.computed_field
    @property
    def get_api_url(self) -> str:
        return f"{self.protocol}://{self.host}:{self.port}/api/v1"

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
        return values
