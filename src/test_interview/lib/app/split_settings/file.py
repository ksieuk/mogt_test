import pathlib
import typing

import pydantic
import pydantic_settings
import yaml

import lib.app.split_settings.utils as app_split_settings_utils


class FileSettings(pydantic_settings.BaseSettings):
    model_config = pydantic_settings.SettingsConfigDict(
        env_file=app_split_settings_utils.ENV_PATH,
        env_prefix="FILE_",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    api_url: str = pydantic.Field(default=...)
    files_dir_path: pathlib.Path = app_split_settings_utils.BASE_PATH / "data"
    use_config: bool = False

    @pydantic.model_validator(mode="after")
    def check_directory_exist(self) -> typing.Self:
        if not self.files_dir_path.exists():
            self.files_dir_path.mkdir()
        return self

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
        if "files_info" in data:
            values.update(data["files_info"])
            if "temp_dir" in values:
                values["files_dir_path"] = app_split_settings_utils.BASE_PATH / values["temp_dir"]
        return values
